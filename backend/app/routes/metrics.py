from flask import Blueprint, request, jsonify
from datetime import datetime

bp = Blueprint('metrics', __name__, url_prefix='/api/v1/metrics')

@bp.route('/', methods=['GET'])
def get_metrics():
    """Get dashboard metrics"""
    return jsonify({
        'success': True,
        'data': {
            'total_pipelines': 0,
            'success_rate': 0,
            'failure_rate': 0,
            'average_build_time': 0
        },
        'message': 'Metrics endpoint - coming soon',
        'timestamp': datetime.utcnow().isoformat()
    })
