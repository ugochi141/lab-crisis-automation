"""
Kaiser Permanente Lab Automation System
Notion Integration Client

Handles all interactions with Notion databases for performance tracking,
incident management, and operational data with HIPAA compliance.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import aiohttp
import json

from config.config_manager import NotionConfig
from utils.audit_logger import AuditLogger


class NotionClient:
    """
    Async client for Notion API integration with comprehensive
    error handling and audit logging.
    """
    
    def __init__(self, config: NotionConfig):
        """
        Initialize Notion client
        
        Args:
            config: Notion configuration settings
        """
        self.config = config
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {config.api_token}",
            "Notion-Version": config.version,
            "Content-Type": "application/json"
        }
        self.logger = logging.getLogger('notion_client')
        self.audit_logger = AuditLogger()
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure session is available"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers=self.headers,
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make authenticated request to Notion API
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            data: Request payload
            params: Query parameters
            
        Returns:
            API response data
        """
        session = await self._ensure_session()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            async with session.request(
                method=method,
                url=url,
                json=data,
                params=params
            ) as response:
                response_data = await response.json()
                
                if response.status >= 400:
                    error_msg = f"Notion API error {response.status}: {response_data.get('message', 'Unknown error')}"
                    self.logger.error(error_msg)
                    raise Exception(error_msg)
                
                # Log successful API calls for audit
                self.audit_logger.log_api_call(
                    service="notion",
                    method=method,
                    endpoint=endpoint,
                    status_code=response.status
                )
                
                return response_data
                
        except Exception as e:
            self.logger.error(f"Notion API request failed: {e}")
            raise
    
    async def get_performance_data(self, days_back: int = 1) -> List[Dict[str, Any]]:
        """
        Get performance data from Notion database
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            List of performance records
        """
        try:
            # Calculate date filter
            start_date = (datetime.now() - timedelta(days=days_back)).isoformat()
            
            # Query performance database
            query_data = {
                "filter": {
                    "property": "Date",
                    "date": {
                        "after": start_date
                    }
                },
                "sorts": [
                    {
                        "property": "Date",
                        "direction": "descending"
                    }
                ]
            }
            
            response = await self._make_request(
                "POST",
                f"databases/{self.config.performance_db_id}/query",
                data=query_data
            )
            
            # Transform response to standardized format
            performance_data = []
            for result in response.get("results", []):
                try:
                    properties = result.get("properties", {})
                    
                    # Extract data with proper type handling
                    record = {
                        "id": result.get("id"),
                        "staff_member": self._extract_title(properties.get("Staff Member")),
                        "date": self._extract_date(properties.get("Date")),
                        "shift": self._extract_select(properties.get("Shift")),
                        "samples_processed": self._extract_number(properties.get("Samples Processed")),
                        "error_count": self._extract_number(properties.get("Error Count")),
                        "break_time_minutes": self._extract_number(properties.get("Break Time (mins)")),
                        "qc_completion_percent": self._extract_number(properties.get("QC Completion %")),
                        "tat_target_met": self._extract_checkbox(properties.get("TAT Target Met")),
                        "performance_score": self._extract_formula(properties.get("Performance Score")),
                        "supervisor": self._extract_people(properties.get("Supervisor")),
                        "status": self._extract_select(properties.get("Status")),
                        "notes": self._extract_text(properties.get("Notes"))
                    }
                    performance_data.append(record)
                    
                except Exception as e:
                    self.logger.error(f"Failed to parse performance record: {e}")
                    continue
            
            self.logger.info(f"Retrieved {len(performance_data)} performance records")
            return performance_data
            
        except Exception as e:
            self.logger.error(f"Failed to get performance data: {e}")
            raise
    
    async def get_open_incidents(self) -> List[Dict[str, Any]]:
        """
        Get open incidents from Notion database
        
        Returns:
            List of open incident records
        """
        try:
            # Query for open incidents
            query_data = {
                "filter": {
                    "or": [
                        {
                            "property": "Status",
                            "select": {
                                "equals": "Open"
                            }
                        },
                        {
                            "property": "Status",
                            "select": {
                                "equals": "In Progress"
                            }
                        }
                    ]
                },
                "sorts": [
                    {
                        "property": "Date/Time",
                        "direction": "descending"
                    }
                ]
            }
            
            response = await self._make_request(
                "POST",
                f"databases/{self.config.incident_db_id}/query",
                data=query_data
            )
            
            # Transform response to standardized format
            incidents = []
            for result in response.get("results", []):
                try:
                    properties = result.get("properties", {})
                    
                    incident = {
                        "id": result.get("id"),
                        "incident_id": self._extract_title(properties.get("Incident ID")),
                        "date_time": self._extract_date(properties.get("Date/Time")),
                        "staff_member": self._extract_select(properties.get("Staff Member")),
                        "incident_type": self._extract_select(properties.get("Incident Type")),
                        "severity": self._extract_select(properties.get("Severity")),
                        "impact": self._extract_select(properties.get("Impact")),
                        "status": self._extract_select(properties.get("Status")),
                        "description": self._extract_text(properties.get("Description")),
                        "root_cause": self._extract_text(properties.get("Root Cause")),
                        "corrective_action": self._extract_text(properties.get("Corrective Action")),
                        "follow_up_date": self._extract_date(properties.get("Follow-up Date")),
                        "pattern_count": self._extract_number(properties.get("Pattern Count"))
                    }
                    incidents.append(incident)
                    
                except Exception as e:
                    self.logger.error(f"Failed to parse incident record: {e}")
                    continue
            
            self.logger.info(f"Retrieved {len(incidents)} open incidents")
            return incidents
            
        except Exception as e:
            self.logger.error(f"Failed to get incident data: {e}")
            raise
    
    async def create_incident(self, incident_data: Dict[str, Any]) -> str:
        """
        Create new incident in Notion database
        
        Args:
            incident_data: Incident information
            
        Returns:
            Created page ID
        """
        try:
            # Prepare page data
            page_data = {
                "parent": {
                    "database_id": self.config.incident_db_id
                },
                "properties": {
                    "Incident ID": {
                        "title": [
                            {
                                "text": {
                                    "content": incident_data.get("incident_id", "")
                                }
                            }
                        ]
                    },
                    "Date/Time": {
                        "date": {
                            "start": incident_data.get("timestamp", datetime.now().isoformat())
                        }
                    },
                    "Staff Member": {
                        "select": {
                            "name": incident_data.get("staff_member", "")
                        }
                    },
                    "Incident Type": {
                        "select": {
                            "name": incident_data.get("incident_type", "")
                        }
                    },
                    "Severity": {
                        "select": {
                            "name": incident_data.get("severity", "Medium")
                        }
                    },
                    "Impact": {
                        "select": {
                            "name": incident_data.get("impact", "")
                        }
                    },
                    "Description": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": incident_data.get("description", "")
                                }
                            }
                        ]
                    },
                    "Status": {
                        "select": {
                            "name": "Open"
                        }
                    }
                }
            }
            
            response = await self._make_request(
                "POST",
                "pages",
                data=page_data
            )
            
            page_id = response.get("id")
            self.logger.info(f"Created incident {incident_data.get('incident_id')} with ID {page_id}")
            
            # Log to audit trail
            self.audit_logger.log_incident_creation({
                "incident_id": incident_data.get("incident_id"),
                "page_id": page_id,
                "staff_member": incident_data.get("staff_member"),
                "severity": incident_data.get("severity")
            })
            
            return page_id
            
        except Exception as e:
            self.logger.error(f"Failed to create incident: {e}")
            raise
    
    async def update_performance_metrics(self, metrics_data: Dict[str, Any]) -> str:
        """
        Update or create performance metrics record
        
        Args:
            metrics_data: Performance metrics
            
        Returns:
            Updated/created page ID
        """
        try:
            # Check if record exists for today and staff member
            existing_record = await self._find_existing_performance_record(
                metrics_data.get("staff_member"),
                metrics_data.get("date", datetime.now().date().isoformat())
            )
            
            # Prepare properties data
            properties = {
                "Staff Member": {
                    "title": [
                        {
                            "text": {
                                "content": metrics_data.get("staff_member", "")
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": metrics_data.get("date", datetime.now().date().isoformat())
                    }
                },
                "Shift": {
                    "select": {
                        "name": metrics_data.get("shift", "")
                    }
                },
                "Samples Processed": {
                    "number": metrics_data.get("samples_processed", 0)
                },
                "Error Count": {
                    "number": metrics_data.get("error_count", 0)
                },
                "Break Time (mins)": {
                    "number": metrics_data.get("break_time_minutes", 0)
                },
                "QC Completion %": {
                    "number": metrics_data.get("qc_completion_percent", 0)
                },
                "TAT Target Met": {
                    "checkbox": metrics_data.get("tat_target_met", False)
                },
                "Status": {
                    "select": {
                        "name": metrics_data.get("status", "Good")
                    }
                }
            }
            
            # Add notes if provided
            if metrics_data.get("notes"):
                properties["Notes"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": metrics_data.get("notes")
                            }
                        }
                    ]
                }
            
            if existing_record:
                # Update existing record
                response = await self._make_request(
                    "PATCH",
                    f"pages/{existing_record['id']}",
                    data={"properties": properties}
                )
                page_id = existing_record["id"]
                action = "updated"
            else:
                # Create new record
                page_data = {
                    "parent": {
                        "database_id": self.config.performance_db_id
                    },
                    "properties": properties
                }
                
                response = await self._make_request(
                    "POST",
                    "pages",
                    data=page_data
                )
                page_id = response.get("id")
                action = "created"
            
            self.logger.info(f"Performance metrics {action} for {metrics_data.get('staff_member')}")
            
            # Log to audit trail
            self.audit_logger.log_performance_update({
                "action": action,
                "page_id": page_id,
                "staff_member": metrics_data.get("staff_member"),
                "date": metrics_data.get("date")
            })
            
            return page_id
            
        except Exception as e:
            self.logger.error(f"Failed to update performance metrics: {e}")
            raise
    
    async def _find_existing_performance_record(self, staff_member: str, date: str) -> Optional[Dict]:
        """Find existing performance record for staff member and date"""
        try:
            query_data = {
                "filter": {
                    "and": [
                        {
                            "property": "Staff Member",
                            "title": {
                                "equals": staff_member
                            }
                        },
                        {
                            "property": "Date",
                            "date": {
                                "equals": date
                            }
                        }
                    ]
                }
            }
            
            response = await self._make_request(
                "POST",
                f"databases/{self.config.performance_db_id}/query",
                data=query_data
            )
            
            results = response.get("results", [])
            return results[0] if results else None
            
        except Exception as e:
            self.logger.error(f"Failed to find existing performance record: {e}")
            return None
    
    # Helper methods for extracting data from Notion properties
    def _extract_title(self, prop: Optional[Dict]) -> str:
        """Extract title property value"""
        if not prop or prop.get("type") != "title":
            return ""
        title_list = prop.get("title", [])
        return title_list[0].get("text", {}).get("content", "") if title_list else ""
    
    def _extract_text(self, prop: Optional[Dict]) -> str:
        """Extract rich text property value"""
        if not prop or prop.get("type") != "rich_text":
            return ""
        text_list = prop.get("rich_text", [])
        return text_list[0].get("text", {}).get("content", "") if text_list else ""
    
    def _extract_number(self, prop: Optional[Dict]) -> float:
        """Extract number property value"""
        if not prop or prop.get("type") != "number":
            return 0.0
        return prop.get("number", 0.0) or 0.0
    
    def _extract_select(self, prop: Optional[Dict]) -> str:
        """Extract select property value"""
        if not prop or prop.get("type") != "select":
            return ""
        select_obj = prop.get("select")
        return select_obj.get("name", "") if select_obj else ""
    
    def _extract_checkbox(self, prop: Optional[Dict]) -> bool:
        """Extract checkbox property value"""
        if not prop or prop.get("type") != "checkbox":
            return False
        return prop.get("checkbox", False)
    
    def _extract_date(self, prop: Optional[Dict]) -> Optional[str]:
        """Extract date property value"""
        if not prop or prop.get("type") != "date":
            return None
        date_obj = prop.get("date")
        return date_obj.get("start") if date_obj else None
    
    def _extract_people(self, prop: Optional[Dict]) -> List[str]:
        """Extract people property value"""
        if not prop or prop.get("type") != "people":
            return []
        people_list = prop.get("people", [])
        return [person.get("name", "") for person in people_list]
    
    def _extract_formula(self, prop: Optional[Dict]) -> float:
        """Extract formula property value"""
        if not prop or prop.get("type") != "formula":
            return 0.0
        formula_obj = prop.get("formula", {})
        if formula_obj.get("type") == "number":
            return formula_obj.get("number", 0.0) or 0.0
        return 0.0
    
    async def query_database(self, database_id: str, filter: Optional[Dict] = None, 
                           sorts: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Query a Notion database
        
        Args:
            database_id: Database ID to query
            filter: Optional filter criteria
            sorts: Optional sort criteria
            
        Returns:
            Query results
        """
        try:
            query_data = {}
            if filter:
                query_data["filter"] = filter
            if sorts:
                query_data["sorts"] = sorts
                
            response = await self._make_request(
                "POST",
                f"databases/{database_id}/query",
                data=query_data
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to query database: {e}")
            raise
    
    async def create_page(self, database_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new page in a database
        
        Args:
            database_id: Database ID to create page in
            properties: Page properties
            
        Returns:
            Created page data
        """
        try:
            page_data = {
                "parent": {
                    "database_id": database_id
                },
                "properties": properties
            }
            
            response = await self._make_request(
                "POST",
                "pages",
                data=page_data
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to create page: {e}")
            raise
    
    async def update_page(self, page_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing page
        
        Args:
            page_id: Page ID to update
            properties: Properties to update
            
        Returns:
            Updated page data
        """
        try:
            response = await self._make_request(
                "PATCH",
                f"pages/{page_id}",
                data={"properties": properties}
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to update page: {e}")
            raise
    
    async def get_page_content(self, page_id: str) -> Dict[str, Any]:
        """
        Get page content and properties
        
        Args:
            page_id: Page ID to retrieve
            
        Returns:
            Page data
        """
        try:
            response = await self._make_request(
                "GET",
                f"pages/{page_id}"
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to get page content: {e}")
            raise
    
    async def get_database_items(self, database_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all items from a database
        
        Args:
            database_id: Database ID to query
            limit: Maximum number of items to retrieve
            
        Returns:
            List of database items
        """
        try:
            response = await self.query_database(
                database_id,
                sorts=[{"timestamp": "created_time", "direction": "descending"}]
            )
            
            items = response.get("results", [])[:limit]
            return items
            
        except Exception as e:
            self.logger.error(f"Failed to get database items: {e}")
            raise
    
    async def close(self):
        """Close the client session"""
        if self.session:
            await self.session.close()
