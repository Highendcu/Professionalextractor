from flask import Blueprint, request, jsonify, Response
from app.services.extractor import start_extraction, EXTRACTION_DATA, EXTRACTION_ACTIVE, DATA_LOCK, stop_extraction
import threading

bp = Blueprint('api', __name__)

@bp.route('/extract', methods=['POST'])
def extract():
    form_data = {
        'urls': [url.strip() for url in request.form.get('urls', '').split(',') if url.strip()],
        'keywords': [kw.strip() for kw in request.form.get('keywords', '').split(',') if kw.strip()],
        'platforms': request.form.getlist('platforms[]'),
        'country': request.form.get('country'),
        'state': request.form.get('state')
    }

    thread = threading.Thread(target=start_extraction, kwargs=form_data)
    thread.daemon = True
    thread.start()

    return jsonify({"status": "extraction_started"})

@bp.route('/view-extraction')
def view_extraction():
    with DATA_LOCK:
        total = len(EXTRACTION_DATA)
        data = EXTRACTION_DATA.copy()
    return jsonify({"numbers": data, "total": total, "active": EXTRACTION_ACTIVE})

@bp.route('/stop-extraction', methods=['POST'])
def stop_extraction_route():
    stop_extraction()
    return jsonify({"status": "Extraction stopped"})

@bp.route('/export-data')
def export_data():
    format = request.args.get('format', 'csv')
    with DATA_LOCK:
        if format == 'csv':
            csv_data = "Number,Name,Address\n"
            for entry in EXTRACTION_DATA:
                csv_data += f"{entry['number']},{entry['name']},{entry['address']}\n"
            return Response(csv_data, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=extracted_data.csv"})
        return jsonify(EXTRACTION_DATA)
		
@bp.route('/verify-credentials', methods=['POST'])
def verify_credentials():
    data = request.form or request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    from app.models.user import load_users
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            if not user.get("expiry") or datetime.fromisoformat(user["expiry"]) > datetime.utcnow():
                session['license_valid'] = True
                return jsonify({"valid": True})
    return jsonify({"valid": False})

@bp.route('/bulk-send', methods=['POST'])
def bulk_send():
    message = request.form.get("message", "")
    # TODO: Integrate with your SMS or WhatsApp bulk API
    print("Sending bulk message:", message[:60])
    return jsonify({"status": "sent"})

@bp.route('/bulk-verify', methods=['POST'])
def bulk_verify():
    raw = request.form.get("numbers", "")
    numbers = [n.strip() for n in raw.split(",") if n.strip()]
    # TODO: Connect to verification API or phone lookup
    print("Verifying", len(numbers), "numbers...")
    return jsonify({"status": "verified", "count": len(numbers)})
