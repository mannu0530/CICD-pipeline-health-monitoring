db = db.getSiblingDB('cicd_dashboard');

// Create collections
db.createCollection('pipelines');
db.createCollection('builds');
db.createCollection('metrics');
db.createCollection('alerts');
db.createCollection('configurations');

// Create indexes
db.pipelines.createIndex({ "pipeline_id": 1 }, { unique: true });
db.pipelines.createIndex({ "tool": 1, "status": 1 });
db.pipelines.createIndex({ "started_at": -1 });

db.builds.createIndex({ "build_id": 1 }, { unique: true });
db.builds.createIndex({ "pipeline_id": 1 });
db.builds.createIndex({ "status": 1, "started_at": -1 });

db.metrics.createIndex({ "date": 1, "tool": 1 }, { unique: true });

db.alerts.createIndex({ "status": 1, "created_at": -1 });

print('MongoDB initialized successfully');
