from datetime import datetime
from typing import Optional
from pymongo import ASCENDING, DESCENDING

class Metric:
    """Metric model for pipeline analytics data"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.metrics
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for performance"""
        self.collection.create_index([("date", ASCENDING), ("tool", ASCENDING)], unique=True)
        self.collection.create_index([("date", DESCENDING)])
    
    def create(self, metric_data: dict) -> str:
        """Create a new metric record"""
        metric_data['created_at'] = datetime.utcnow()
        
        result = self.collection.insert_one(metric_data)
        return str(result.inserted_id)
    
    def get_by_date(self, date: str, tool: Optional[str] = None) -> Optional[dict]:
        """Get metrics by date and optionally by tool"""
        query = {"date": date}
        if tool:
            query["tool"] = tool
            
        metric = self.collection.find_one(query)
        if metric:
            metric['_id'] = str(metric['_id'])
        return metric
