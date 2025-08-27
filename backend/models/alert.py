from datetime import datetime
from typing import Optional, List
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId

class Alert:
    """Alert model for pipeline notifications"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.alerts
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for performance"""
        self.collection.create_index([("status", ASCENDING), ("created_at", DESCENDING)])
        self.collection.create_index([("pipeline_id", ASCENDING)])
    
    def create(self, alert_data: dict) -> str:
        """Create a new alert record"""
        alert_data['created_at'] = datetime.utcnow()
        alert_data['status'] = alert_data.get('status', 'active')
        
        result = self.collection.insert_one(alert_data)
        return str(result.inserted_id)
    
    def get_by_id(self, alert_id: str) -> Optional[dict]:
        """Get alert by ID"""
        try:
            alert = self.collection.find_one({"_id": ObjectId(alert_id)})
            if alert:
                alert['_id'] = str(alert['_id'])
            return alert
        except:
            return None
    
    def list_alerts(self, status: Optional[str] = None, limit: int = 50) -> List[dict]:
        """List alerts with optional filtering"""
        filter_query = {}
        if status:
            filter_query["status"] = status
        
        alerts = list(self.collection.find(filter_query)
                     .sort("created_at", DESCENDING)
                     .limit(limit))
        
        for alert in alerts:
            alert['_id'] = str(alert['_id'])
        
        return alerts
