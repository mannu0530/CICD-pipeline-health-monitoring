from datetime import datetime
from typing import Optional, List
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId

class Build:
    """Build model for individual build records"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.builds
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for performance"""
        self.collection.create_index([("build_id", ASCENDING)], unique=True)
        self.collection.create_index([("pipeline_id", ASCENDING)])
        self.collection.create_index([("status", ASCENDING), ("started_at", DESCENDING)])
        self.collection.create_index([("job_name", ASCENDING)])
    
    def create(self, build_data: dict) -> str:
        """Create a new build record"""
        build_data['created_at'] = datetime.utcnow()
        build_data['updated_at'] = datetime.utcnow()
        
        result = self.collection.insert_one(build_data)
        return str(result.inserted_id)
    
    def get_by_id(self, build_id: str) -> Optional[dict]:
        """Get build by ID"""
        build = self.collection.find_one({"build_id": build_id})
        if build:
            build['_id'] = str(build['_id'])
        return build
    
    def get_by_mongo_id(self, mongo_id: str) -> Optional[dict]:
        """Get build by MongoDB ObjectId"""
        try:
            build = self.collection.find_one({"_id": ObjectId(mongo_id)})
            if build:
                build['_id'] = str(build['_id'])
            return build
        except:
            return None
    
    def update(self, build_id: str, update_data: dict) -> bool:
        """Update build data"""
        update_data['updated_at'] = datetime.utcnow()
        
        result = self.collection.update_one(
            {"build_id": build_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete(self, build_id: str) -> bool:
        """Delete build by ID"""
        result = self.collection.delete_one({"build_id": build_id})
        return result.deleted_count > 0
    
    def get_by_pipeline(self, pipeline_id: str, limit: int = 50, offset: int = 0) -> List[dict]:
        """Get builds for a specific pipeline"""
        builds = list(self.collection.find({"pipeline_id": pipeline_id})
                     .sort("started_at", DESCENDING)
                     .skip(offset)
                     .limit(limit))
        
        for build in builds:
            build['_id'] = str(build['_id'])
        
        return builds
    
    def list_builds(self, 
                    status: Optional[str] = None,
                    job_name: Optional[str] = None,
                    limit: int = 50,
                    offset: int = 0) -> List[dict]:
        """List builds with optional filtering"""
        filter_query = {}
        
        if status:
            filter_query["status"] = status
        if job_name:
            filter_query["job_name"] = {"$regex": job_name, "$options": "i"}
        
        builds = list(self.collection.find(filter_query)
                     .sort("started_at", DESCENDING)
                     .skip(offset)
                     .limit(limit))
        
        for build in builds:
            build['_id'] = str(build['_id'])
        
        return builds
    
    def get_build_count(self, status: Optional[str] = None, job_name: Optional[str] = None) -> int:
        """Get count of builds with optional filtering"""
        filter_query = {}
        
        if status:
            filter_query["status"] = status
        if job_name:
            filter_query["job_name"] = {"$regex": job_name, "$options": "i"}
        
        return self.collection.count_documents(filter_query)
    
    def get_recent_builds(self, limit: int = 10) -> List[dict]:
        """Get recent builds"""
        builds = list(self.collection.find()
                     .sort("started_at", DESCENDING)
                     .limit(limit))
        
        for build in builds:
            build['_id'] = str(build['_id'])
        
        return builds
    
    def get_builds_by_status(self, status: str, limit: int = 50) -> List[dict]:
        """Get builds by status"""
        builds = list(self.collection.find({"status": status})
                     .sort("started_at", DESCENDING)
                     .limit(limit))
        
        for build in builds:
            build['_id'] = str(build['_id'])
        
        return builds
    
    def get_build_stats(self, pipeline_id: Optional[str] = None) -> dict:
        """Get build statistics"""
        match_query = {}
        if pipeline_id:
            match_query["pipeline_id"] = pipeline_id
        
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
    
    def update_logs(self, build_id: str, logs: str) -> bool:
        """Update build logs"""
        result = self.collection.update_one(
            {"build_id": build_id},
            {"$set": {"logs": logs, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    def append_logs(self, build_id: str, log_line: str) -> bool:
        """Append a line to build logs"""
        result = self.collection.update_one(
            {"build_id": build_id},
            {"$push": {"logs": log_line}, "$set": {"updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0
