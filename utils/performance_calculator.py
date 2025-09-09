"""Performance calculator for lab metrics."""

class PerformanceCalculator:
    """Calculates performance metrics for lab operations."""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_tat(self, start_time, end_time):
        """Calculate turnaround time."""
        if end_time and start_time:
            return (end_time - start_time).total_seconds() / 60
        return 0
    
    def calculate_efficiency(self, completed_tasks, total_tasks):
        """Calculate efficiency percentage."""
        if total_tasks > 0:
            return (completed_tasks / total_tasks) * 100
        return 0
    
    def calculate_performance_score(self, metrics):
        """Calculate overall performance score."""
        score = 0
        weights = {
            "efficiency": 0.3,
            "tat": 0.3,
            "quality": 0.2,
            "compliance": 0.2
        }
        
        for metric, value in metrics.items():
            if metric in weights:
                score += weights[metric] * value
        
        return min(100, max(0, score))