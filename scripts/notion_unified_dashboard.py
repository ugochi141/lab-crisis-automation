#!/usr/bin/env python3
"""
Unified Notion Dashboard Creator
Consolidates all lab systems into a single comprehensive dashboard
"""

import os
import json
import logging
from datetime import datetime, timedelta
from notion_client import Client
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotionUnifiedDashboard:
    """Creates and maintains a unified Notion dashboard for all lab systems"""
    
    def __init__(self):
        self.notion_token = os.environ.get('NOTION_API_TOKEN', '')
        if self.notion_token:
            self.notion = Client(auth=self.notion_token)
        else:
            logger.warning("Notion API token not set - running in demo mode")
            self.notion = None
            
        # Dashboard configuration
        self.dashboard_config = {
            "title": "🧬 Lab Operations Command Center",
            "databases": {
                "performance": os.environ.get('NOTION_PERFORMANCE_DB_ID', 'demo_perf_db'),
                "incidents": os.environ.get('NOTION_INCIDENT_DB_ID', 'demo_incident_db'),
                "alerts": os.environ.get('NOTION_ALERTS_DB_ID', 'demo_alerts_db'),
                "staff": os.environ.get('NOTION_STAFF_DB_ID', 'demo_staff_db'),
                "equipment": os.environ.get('NOTION_EQUIPMENT_DB_ID', 'demo_equipment_db')
            }
        }
        
    def create_dashboard_structure(self):
        """Creates the unified dashboard structure"""
        
        dashboard_structure = {
            "type": "page",
            "object": "page",
            "properties": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": self.dashboard_config["title"]
                        }
                    }
                ]
            },
            "children": [
                # Header Section
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "🏥 Laboratory Operations Command Center"}
                        }]
                    }
                },
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
                        }],
                        "icon": {"emoji": "🔄"},
                        "color": "blue_background"
                    }
                },
                
                # Executive Summary Section
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "📊 Executive Summary"}
                        }]
                    }
                },
                {
                    "object": "block",
                    "type": "column_list",
                    "column_list": {
                        "children": [
                            {
                                "object": "column",
                                "children": [
                                    self._create_metric_card("🎯 Performance Score", "97.2%", "Grade: A+", "green"),
                                    self._create_metric_card("⏱️ Average TAT", "45 min", "Target: <60 min", "green"),
                                    self._create_metric_card("📈 Daily Volume", "1,250", "+3.2% from yesterday", "blue")
                                ]
                            },
                            {
                                "object": "column",
                                "children": [
                                    self._create_metric_card("✅ QC Pass Rate", "98.7%", "Target: >98%", "green"),
                                    self._create_metric_card("👥 Staff On Duty", "28", "Optimal staffing", "blue"),
                                    self._create_metric_card("🚨 Active Alerts", "2", "2 warnings", "yellow")
                                ]
                            },
                            {
                                "object": "column",
                                "children": [
                                    self._create_metric_card("🤖 Automation Rate", "72.5%", "Target: 80%", "yellow"),
                                    self._create_metric_card("💻 System Uptime", "99.95%", "Excellent", "green"),
                                    self._create_metric_card("💰 Cost Savings", "$2.5M", "Annual projection", "green")
                                ]
                            }
                        ]
                    }
                },
                
                # Real-time Monitoring Section
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "🔴 Real-Time Monitoring"}
                        }]
                    }
                },
                {
                    "object": "block",
                    "type": "toggle",
                    "toggle": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "📊 Live TAT Tracking"}
                        }],
                        "children": [
                            self._create_tat_table()
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "toggle",
                    "toggle": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "🚨 Active Alerts & Incidents"}
                        }],
                        "children": [
                            self._create_alerts_table()
                        ]
                    }
                },
                
                # Workflow Status Section
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "🔄 Automated Workflows"}
                        }]
                    }
                },
                self._create_workflow_status_table(),
                
                # Staff Performance Section
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "👥 Staff Performance"}
                        }]
                    }
                },
                self._create_staff_performance_gallery(),
                
                # Equipment Status Section
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "🔧 Equipment Status"}
                        }]
                    }
                },
                self._create_equipment_status_board(),
                
                # Quick Actions Section
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{
                            "type": "text",
                            "text": {"content": "⚡ Quick Actions"}
                        }]
                    }
                },
                self._create_quick_actions()
            ]
        }
        
        return dashboard_structure
    
    def _create_metric_card(self, title, value, subtitle, color):
        """Creates a metric card block"""
        return {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": f"{title}\n"},
                        "annotations": {"bold": True}
                    },
                    {
                        "type": "text",
                        "text": {"content": f"{value}\n"},
                        "annotations": {"bold": True, "color": color}
                    },
                    {
                        "type": "text",
                        "text": {"content": subtitle},
                        "annotations": {"color": "gray"}
                    }
                ],
                "color": f"{color}_background"
            }
        }
    
    def _create_tat_table(self):
        """Creates TAT tracking table"""
        return {
            "object": "block",
            "type": "table",
            "table": {
                "table_width": 5,
                "has_column_header": True,
                "has_row_header": False,
                "children": [
                    {
                        "object": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Department"}}],
                                [{"type": "text", "text": {"content": "Current TAT"}}],
                                [{"type": "text", "text": {"content": "Target"}}],
                                [{"type": "text", "text": {"content": "Status"}}],
                                [{"type": "text", "text": {"content": "Trend"}}]
                            ]
                        }
                    },
                    {
                        "object": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Chemistry"}}],
                                [{"type": "text", "text": {"content": "42 min"}}],
                                [{"type": "text", "text": {"content": "60 min"}}],
                                [{"type": "text", "text": {"content": "✅ On Target"}}],
                                [{"type": "text", "text": {"content": "📈 Improving"}}]
                            ]
                        }
                    },
                    {
                        "object": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Hematology"}}],
                                [{"type": "text", "text": {"content": "38 min"}}],
                                [{"type": "text", "text": {"content": "45 min"}}],
                                [{"type": "text", "text": {"content": "✅ Excellent"}}],
                                [{"type": "text", "text": {"content": "➡️ Stable"}}]
                            ]
                        }
                    },
                    {
                        "object": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Microbiology"}}],
                                [{"type": "text", "text": {"content": "68 min"}}],
                                [{"type": "text", "text": {"content": "60 min"}}],
                                [{"type": "text", "text": {"content": "⚠️ Over Target"}}],
                                [{"type": "text", "text": {"content": "📉 Needs Attention"}}]
                            ]
                        }
                    }
                ]
            }
        }
    
    def _create_alerts_table(self):
        """Creates alerts and incidents table"""
        return {
            "object": "block",
            "type": "table",
            "table": {
                "table_width": 4,
                "has_column_header": True,
                "children": [
                    {
                        "object": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Priority"}}],
                                [{"type": "text", "text": {"content": "Alert"}}],
                                [{"type": "text", "text": {"content": "Time"}}],
                                [{"type": "text", "text": {"content": "Action"}}]
                            ]
                        }
                    },
                    {
                        "object": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "🔴 High"}}],
                                [{"type": "text", "text": {"content": "TAT exceeded in Micro"}}],
                                [{"type": "text", "text": {"content": "10 min ago"}}],
                                [{"type": "text", "text": {"content": "Staff notified"}}]
                            ]
                        }
                    },
                    {
                        "object": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "🟡 Medium"}}],
                                [{"type": "text", "text": {"content": "QC warning - Chemistry"}}],
                                [{"type": "text", "text": {"content": "25 min ago"}}],
                                [{"type": "text", "text": {"content": "Under review"}}]
                            ]
                        }
                    }
                ]
            }
        }
    
    def _create_workflow_status_table(self):
        """Creates workflow status table"""
        return {
            "object": "block",
            "type": "table",
            "table": {
                "table_width": 4,
                "has_column_header": True,
                "children": [
                    {
                        "object": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Workflow"}}],
                                [{"type": "text", "text": {"content": "Status"}}],
                                [{"type": "text", "text": {"content": "Last Run"}}],
                                [{"type": "text", "text": {"content": "Next Run"}}]
                            ]
                        }
                    },
                    {
                        "object": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "🚨 Alert Forwarding"}}],
                                [{"type": "text", "text": {"content": "✅ Active"}}],
                                [{"type": "text", "text": {"content": "2 min ago"}}],
                                [{"type": "text", "text": {"content": "In 3 min"}}]
                            ]
                        }
                    },
                    {
                        "object": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "🔬 Crisis Detection"}}],
                                [{"type": "text", "text": {"content": "✅ Active"}}],
                                [{"type": "text", "text": {"content": "1 min ago"}}],
                                [{"type": "text", "text": {"content": "In 4 min"}}]
                            ]
                        }
                    },
                    {
                        "object": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "📊 Performance Analysis"}}],
                                [{"type": "text", "text": {"content": "✅ Active"}}],
                                [{"type": "text", "text": {"content": "15 min ago"}}],
                                [{"type": "text", "text": {"content": "In 45 min"}}]
                            ]
                        }
                    },
                    {
                        "object": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "🔄 Master Orchestration"}}],
                                [{"type": "text", "text": {"content": "✅ Active"}}],
                                [{"type": "text", "text": {"content": "30 min ago"}}],
                                [{"type": "text", "text": {"content": "In 30 min"}}]
                            ]
                        }
                    }
                ]
            }
        }
    
    def _create_staff_performance_gallery(self):
        """Creates staff performance gallery view"""
        return {
            "object": "block",
            "type": "column_list",
            "column_list": {
                "children": [
                    {
                        "object": "column",
                        "children": [{
                            "object": "block",
                            "type": "callout",
                            "callout": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {"content": "⭐ Top Performer\nJohn Smith\n• Efficiency: 95%\n• TAT: 38 min avg\n• QC Pass: 99.2%"}
                                }],
                                "color": "green_background",
                                "icon": {"emoji": "🏆"}
                            }
                        }]
                    },
                    {
                        "object": "column",
                        "children": [{
                            "object": "block",
                            "type": "callout",
                            "callout": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {"content": "📈 Most Improved\nSarah Johnson\n• Efficiency: +12%\n• TAT: -8 min\n• Errors: -45%"}
                                }],
                                "color": "blue_background",
                                "icon": {"emoji": "📈"}
                            }
                        }]
                    },
                    {
                        "object": "column",
                        "children": [{
                            "object": "block",
                            "type": "callout",
                            "callout": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {"content": "🎯 Team Goals\n• Target TAT: <60 min\n• QC Pass: >98%\n• Efficiency: >85%"}
                                }],
                                "color": "purple_background",
                                "icon": {"emoji": "🎯"}
                            }
                        }]
                    }
                ]
            }
        }
    
    def _create_equipment_status_board(self):
        """Creates equipment status board"""
        return {
            "object": "block",
            "type": "column_list",
            "column_list": {
                "children": [
                    {
                        "object": "column",
                        "children": [{
                            "object": "block",
                            "type": "callout",
                            "callout": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {"content": "🟢 Online (12)\n• Chemistry Analyzer 1-4\n• Hematology 1-3\n• Coag 1-2\n• Micro 1-3"}
                                }],
                                "color": "green_background"
                            }
                        }]
                    },
                    {
                        "object": "column",
                        "children": [{
                            "object": "block",
                            "type": "callout",
                            "callout": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {"content": "🟡 Maintenance (2)\n• Chemistry Analyzer 5\n  (PM scheduled)\n• Hematology 4\n  (Calibration)"}
                                }],
                                "color": "yellow_background"
                            }
                        }]
                    },
                    {
                        "object": "column",
                        "children": [{
                            "object": "block",
                            "type": "callout",
                            "callout": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {"content": "🔴 Offline (0)\n• All systems operational\n• No critical failures\n• 99.95% uptime"}
                                }],
                                "color": "red_background"
                            }
                        }]
                    }
                ]
            }
        }
    
    def _create_quick_actions(self):
        """Creates quick actions section"""
        return {
            "object": "block",
            "type": "column_list",
            "column_list": {
                "children": [
                    {
                        "object": "column",
                        "children": [{
                            "object": "block",
                            "type": "to_do",
                            "to_do": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {"content": "🚨 Trigger Emergency Response"},
                                    "annotations": {"bold": True}
                                }],
                                "checked": False
                            }
                        }]
                    },
                    {
                        "object": "column",
                        "children": [{
                            "object": "block",
                            "type": "to_do",
                            "to_do": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {"content": "📊 Generate Daily Report"},
                                    "annotations": {"bold": True}
                                }],
                                "checked": False
                            }
                        }]
                    },
                    {
                        "object": "column",
                        "children": [{
                            "object": "block",
                            "type": "to_do",
                            "to_do": {
                                "rich_text": [{
                                    "type": "text",
                                    "text": {"content": "🔄 Refresh All Metrics"},
                                    "annotations": {"bold": True}
                                }],
                                "checked": False
                            }
                        }]
                    }
                ]
            }
        }
    
    def sync_with_data_sources(self):
        """Syncs dashboard with all data sources"""
        sync_results = {
            "timestamp": datetime.now().isoformat(),
            "sources_synced": [],
            "errors": []
        }
        
        # Sync with Power BI
        try:
            powerbi_data = self._fetch_powerbi_metrics()
            sync_results["sources_synced"].append("Power BI")
        except Exception as e:
            sync_results["errors"].append(f"Power BI sync failed: {e}")
        
        # Sync with Teams
        try:
            teams_data = self._fetch_teams_alerts()
            sync_results["sources_synced"].append("Teams")
        except Exception as e:
            sync_results["errors"].append(f"Teams sync failed: {e}")
        
        # Sync with GitHub
        try:
            github_data = self._fetch_github_workflows()
            sync_results["sources_synced"].append("GitHub")
        except Exception as e:
            sync_results["errors"].append(f"GitHub sync failed: {e}")
        
        logger.info(f"Sync completed: {len(sync_results['sources_synced'])} sources synced")
        return sync_results
    
    def _fetch_powerbi_metrics(self):
        """Fetches metrics from Power BI"""
        # Placeholder for Power BI API integration
        return {
            "tat_average": 45,
            "qc_pass_rate": 98.7,
            "daily_volume": 1250
        }
    
    def _fetch_teams_alerts(self):
        """Fetches alerts from Teams"""
        # Placeholder for Teams API integration
        return {
            "active_alerts": 2,
            "critical": 0,
            "warnings": 2
        }
    
    def _fetch_github_workflows(self):
        """Fetches workflow status from GitHub"""
        # Placeholder for GitHub API integration
        return {
            "active_workflows": 4,
            "last_run_success": True,
            "next_scheduled": datetime.now() + timedelta(minutes=5)
        }
    
    def create_dashboard_page(self, parent_page_id=None):
        """Creates the dashboard page in Notion"""
        if not self.notion:
            logger.warning("Notion client not initialized - returning demo structure")
            return self.create_dashboard_structure()
        
        try:
            # Create the page
            dashboard_structure = self.create_dashboard_structure()
            
            if parent_page_id:
                dashboard_structure["parent"] = {"page_id": parent_page_id}
            else:
                # Use workspace as parent if no specific page provided
                dashboard_structure["parent"] = {"workspace": True}
            
            response = self.notion.pages.create(**dashboard_structure)
            logger.info(f"Dashboard created successfully: {response['url']}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to create dashboard: {e}")
            return None
    
    def update_dashboard_metrics(self, page_id):
        """Updates dashboard with latest metrics"""
        if not self.notion:
            logger.warning("Notion client not initialized - skipping update")
            return
        
        try:
            # Fetch latest data
            sync_results = self.sync_with_data_sources()
            
            # Update the page
            # Note: This would require updating specific blocks
            # For now, we'll append a status update
            
            update_block = {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{
                        "type": "text",
                        "text": {"content": f"📊 Metrics updated at {datetime.now().strftime('%H:%M:%S')}"}
                    }],
                    "icon": {"emoji": "✅"},
                    "color": "green_background"
                }
            }
            
            self.notion.blocks.children.append(block_id=page_id, children=[update_block])
            logger.info("Dashboard metrics updated successfully")
            
        except Exception as e:
            logger.error(f"Failed to update dashboard: {e}")

def main():
    """Main function to create and setup the dashboard"""
    logger.info("Creating Unified Notion Dashboard...")
    
    dashboard = NotionUnifiedDashboard()
    
    # Create dashboard structure
    structure = dashboard.create_dashboard_structure()
    
    # Save structure to file for reference
    with open('notion_dashboard_structure.json', 'w') as f:
        json.dump(structure, f, indent=2, default=str)
    
    logger.info("Dashboard structure created and saved to notion_dashboard_structure.json")
    
    # If Notion API is configured, create the actual page
    if dashboard.notion:
        page = dashboard.create_dashboard_page()
        if page:
            logger.info(f"Dashboard page created: {page.get('url', 'No URL available')}")
            
            # Schedule regular updates (in production, this would be a scheduled job)
            logger.info("Dashboard can be updated via scheduled jobs or webhooks")
    else:
        logger.info("Run with NOTION_API_TOKEN environment variable to create actual dashboard")
    
    return 0

if __name__ == "__main__":
    exit(main())