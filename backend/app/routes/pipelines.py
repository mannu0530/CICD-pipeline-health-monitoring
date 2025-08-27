from flask import Blueprint, request, jsonify
from datetime import datetime

bp = Blueprint('pipelines', __name__, url_prefix='/api/v1/pipelines')

@bp.route('/', methods=['GET'])
def list_pipelines():
    """List all pipelines"""
    return jsonify({
        'success': True,
        'data': [],
        'message': 'Pipelines endpoint - coming soon',
        'timestamp': datetime.utcnow().isoformat()
    })

@bp.route('/<pipeline_id>', methods=['GET'])
def get_pipeline(pipeline_id):
    """Get pipeline by ID"""
    return jsonify({
        'success': True,
        'data': {'id': pipeline_id},
        'message': 'Pipeline details - coming soon',
        'timestamp': datetime.utcnow().isoformat()
    })
