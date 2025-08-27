from datetime import datetime
from typing import Optional, List
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId

class Pipeline:
    """Pipeline model for CI/CD pipeline data"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.pipelines
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for performance"""
        self.collection.create_index([("pipeline_id", ASCENDING)], unique=True)
        self.collection.create_index([("tool", ASCENDING), ("status", ASCENDING)])
        self.collection.create_index([("started_at", DESCENDING)])
        self.collection.create_index([("repository", ASCENDING), ("branch", ASCENDING)])
    
    def create(self, pipeline_data: dict) -> str:
        """Create a new pipeline record"""
        pipeline_data['created_at'] = datetime.utcnow()
        pipeline_data['updated_at'] = datetime.utcnow()
        
        result = self.collection.insert_one(pipeline_data)
        return str(result.inserted_id)
    
    def get_by_id(self, pipeline_id: str) -> Optional[dict]:
        """Get pipeline by ID"""
        pipeline = self.collection.find_one({"pipeline_id": pipeline_id})
        if pipeline:
            pipeline['_id'] = str(pipeline['_id'])
        return pipeline
    
    def get_by_mongo_id(self, mongo_id: str) -> Optional[dict]:
        """Get pipeline by MongoDB ObjectId"""
        try:
            pipeline = self.collection.find_one({"_id": ObjectId(mongo_id)})
            if pipeline:
                pipeline['_id'] = str(pipeline['_id'])
            return pipeline
        except:
            return None
    
    def update(self, pipeline_id: str, update_data: dict) -> bool:
        """Update pipeline data"""
        update_data['updated_at'] = datetime.utcnow()
        
        result = self.collection.update_one(
            {"pipeline_id": pipeline_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete(self, pipeline_id: str) -> bool:
        """Delete pipeline by ID"""
        result = self.collection.delete_one({"pipeline_id": pipeline_id})
        return result.deleted_count > 0
    
    def list_pipelines(self, 
                      tool: Optional[str] = None,
                      status: Optional[str] = None,
                      repository: Optional[str] = None,
                      limit: int = 50,
                      offset: int = 0) -> List[dict]:
        """List pipelines with optional filtering"""
        filter_query = {}
        
        if tool:
            filter_query["tool"] = tool
        if status:
            filter_query["status"] = status
        if repository:
            filter_query["repository"] = {"$regex": repository, "$options": "i"}
        
        pipelines = list(self.collection.find(filter_query)
                        .sort("started_at", DESCENDING)
                        .skip(offset)
                        .limit(limit))
        
        # Convert ObjectId to string
        for pipeline in pipelines:
            pipeline['_id'] = str(pipeline['_id'])
        
        return pipelines
    
    def get_pipeline_count(self, tool: Optional[str] = None, status: Optional[str] = None) -> int:
        """Get count of pipelines with optional filtering"""
        filter_query = {}
        
        if tool:
            filter_query["tool"] = tool
        if status:
            filter_query["status"] = status
        
        return self.collection.count_documents(filter_query)
    
    def get_recent_pipelines(self, limit: int = 10) -> List[dict]:
        """Get recent pipeline executions"""
        pipelines = list(self.collection.find()
                        .sort("started_at", DESCENDING)
                        .limit(limit))
        
        for pipeline in pipelines:
            pipeline['_id'] = str(pipeline['_id'])
        
        return pipelines
    
    def get_pipelines_by_status(self, status: str, limit: int = 50) -> List[dict]:
        """Get pipelines by status"""
        pipelines = list(self.collection.find({"status": status})
                        .sort("started_at", DESCENDING)
                        .limit(limit))
        
        for pipeline in pipelines:
            pipeline['_id'] = str(pipeline['_id'])
        
        return pipelines
    
    def get_pipeline_stats(self, tool: Optional[str] = None) -> dict:
        """Get pipeline statistics"""
        match_query = {}
        if tool:
            match_query["tool"] = tool
        
        pipeline = [
            {"$match": match_query},
            {"$group": {
                "_id": "$status",
                "count": {"$sum": 1},
                "avg_duration": {"$avg": "$duration"}
            }}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        stats = {
            "total": 0,
            "success": 0,
            "failure": 0,
            "running": 0,
            "pending": 0,
            "avg_duration": 0
        }
        
        total_duration = 0
        total_count = 0
        
        for result in results:
            status = result["_id"]
            count = result["count"]
            avg_duration = result.get("avg_duration", 0)
            
            stats[status] = count
            stats["total"] += count
            
            if avg_duration:
                total_duration += avg_duration * count
                total_count += count
        
        if total_count > 0:
            stats["avg_duration"] = total_duration / total_count
        
        return stats
