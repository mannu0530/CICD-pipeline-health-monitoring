from datetime import datetime
from typing import Optional, List
from pymongo import ASCENDING

class Configuration:
    """Configuration model for system settings"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.configurations
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for performance"""
        self.collection.create_index([("tool", ASCENDING)], unique=True)
    
    def create(self, config_data: dict) -> str:
        """Create a new configuration record"""
        config_data['created_at'] = datetime.utcnow()
        config_data['updated_at'] = datetime.utcnow()
        
        result = self.collection.insert_one(config_data)
        return str(result.inserted_id)
    
    def get_by_tool(self, tool: str) -> Optional[dict]:
        """Get configuration by tool"""
        config = self.collection.find_one({"tool": tool})
        if config:
            config['_id'] = str(config['_id'])
        return config
    
    def update(self, tool: str, update_data: dict) -> bool:
        """Update configuration for a tool"""
        update_data['updated_at'] = datetime.utcnow()
        
        result = self.collection.update_one(
            {"tool": tool},
            {"$set": update_data},
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None
    
    def list_all(self) -> List[dict]:
        """List all configurations"""
        configs = list(self.collection.find())
        
        for config in configs:
            config['_id'] = str(config['_id'])
        
        return configs
