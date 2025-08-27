from pymongo import MongoClient
from pymongo.database import Database
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database connection manager for MongoDB"""
    
    def __init__(self, connection_string: str, database_name: str):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
    
    def connect(self) -> bool:
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.database_name]
            
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"Successfully connected to MongoDB database: {self.database_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            return False
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
    
    def get_database(self) -> Optional[Database]:
        """Get database instance"""
        return self.db
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        try:
            if self.client:
                self.client.admin.command('ping')
                return True
            return False
        except:
            return False
    
    def create_collections(self):
        """Create required collections if they don't exist"""
        if self.db is None:
            logger.error("Database not connected")
            return False
        
        try:
            # Create collections
            collections = ['pipelines', 'builds', 'metrics', 'alerts', 'configurations']
            
            for collection_name in collections:
                if collection_name not in self.db.list_collection_names():
                    self.db.create_collection(collection_name)
                    logger.info(f"Created collection: {collection_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to create collections: {str(e)}")
            return False
    
    def get_collection_stats(self) -> dict:
        """Get collection statistics"""
        if self.db is None:
            return {}
        
        stats = {}
        try:
            for collection_name in self.db.list_collection_names():
                collection = self.db[collection_name]
                stats[collection_name] = {
                    'count': collection.count_documents({}),
                    'size': collection.estimated_document_size()
                }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {str(e)}")
        
        return stats

# Global database instance
db_manager: Optional[DatabaseManager] = None

def init_database(connection_string: str, database_name: str) -> bool:
    """Initialize global database connection"""
    global db_manager
    
    db_manager = DatabaseManager(connection_string, database_name)
    
    if db_manager.connect():
        db_manager.create_collections()
        return True
    
    return False

def get_database() -> Optional[Database]:
    """Get database instance"""
    global db_manager
    
    if db_manager and db_manager.is_connected():
        return db_manager.get_database()
    
    return None

def close_database():
    """Close database connection"""
    global db_manager
    
    if db_manager:
        db_manager.disconnect()
        db_manager = None
