from flask import Blueprint, jsonify, current_app
from datetime import datetime, timedelta

from .. import db
from ..models import ScanResult
from ..tasks import run_scan_task

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/scan', methods=['POST'])
def scan():
    """Triggers the asynchronous news scanning task."""
    task = run_scan_task.delay()
    return jsonify({'task_id': task.id}), 202

@api_bp.route('/tasks/<task_id>')
def get_status(task_id):
    """Returns the status of a Celery task."""
    task = current_app.extensions['celery'].AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'status': task.info.get('status', '')}
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # Something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

@api_bp.route('/history')
def get_history():
    days = 7
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    results = ScanResult.query.filter(
        ScanResult.scan_time >= cutoff
    ).order_by(ScanResult.scan_time.asc()).all()
    
    history_data = {}
    for result in results:
        if result.keyword not in history_data:
            history_data[result.keyword] = []
        history_data[result.keyword].append({
            'scan_time': result.scan_time.isoformat(),
            'avg_sentiment': result.avg_sentiment,
            'article_count': result.article_count
        })
    
    return jsonify({
        'history': history_data,
        'keywords': list(history_data.keys()),
        'days': days
    })

@api_bp.route('/history/summary')
def get_history_summary():
    results = db.session.query(
        ScanResult.keyword,
        db.func.count(ScanResult.id).label('scan_count'),
        db.func.avg(ScanResult.avg_sentiment).label('overall_avg'),
        db.func.min(ScanResult.scan_time).label('first_scan'),
        db.func.max(ScanResult.scan_time).label('last_scan')
    ).group_by(ScanResult.keyword).all()
    
    summary = []
    for r in results:
        summary.append({
            'keyword': r.keyword,
            'scan_count': r.scan_count,
            'overall_avg': round(r.overall_avg, 3) if r.overall_avg else 0,
            'first_scan': r.first_scan.isoformat() if r.first_scan else None,
            'last_scan': r.last_scan.isoformat() if r.last_scan else None
        })
    
    total_scans = db.session.query(
        db.func.count(db.func.distinct(ScanResult.scan_time))
    ).scalar() or 0
    
    return jsonify({
        'summary': summary,
        'total_scans': total_scans
    })

