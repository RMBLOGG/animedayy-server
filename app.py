from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)

# File untuk menyimpan data update (Vercel menggunakan /tmp untuk temporary storage)
UPDATE_DATA_FILE = '/tmp/update_info.json'

def get_default_data():
    """Get default update data"""
    return {
        'version_code': 1,
        'version_name': '1.0.0',
        'update_required': False,
        'update_title': '',
        'update_message': '',
        'download_url': '',
        'whats_new': [],
        'last_updated': datetime.now().isoformat()
    }

# Initialize data file jika belum ada atau kosong
def init_update_file():
    """Initialize update file with default data"""
    if not os.path.exists(UPDATE_DATA_FILE):
        with open(UPDATE_DATA_FILE, 'w') as f:
            json.dump(get_default_data(), f, indent=2)
    else:
        # Check if file is empty or corrupted
        try:
            with open(UPDATE_DATA_FILE, 'r') as f:
                content = f.read().strip()
                if not content:
                    raise ValueError("Empty file")
                json.loads(content)
        except (ValueError, json.JSONDecodeError):
            # File is empty or corrupted, reinitialize
            with open(UPDATE_DATA_FILE, 'w') as f:
                json.dump(get_default_data(), f, indent=2)

# Initialize file on startup
init_update_file()

def load_update_info():
    """Load update info from JSON file"""
    try:
        with open(UPDATE_DATA_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                # File is empty, return default and save it
                default_data = get_default_data()
                save_update_info(default_data)
                return default_data
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading update info: {e}")
        # Return and save default data
        default_data = get_default_data()
        save_update_info(default_data)
        return default_data

def save_update_info(data):
    """Save update info to JSON file"""
    try:
        data['last_updated'] = datetime.now().isoformat()
        with open(UPDATE_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving update info: {e}")
        return False

# ===========================================
# ADMIN PANEL ROUTES
# ===========================================

@app.route('/')
def admin_panel():
    """Admin panel untuk input informasi update"""
    update_info = load_update_info()
    return render_template('admin.html', update_info=update_info)

@app.route('/admin/update', methods=['POST'])
def update_app_info():
    """Endpoint untuk submit form update info"""
    try:
        # Ambil data dari form
        version_code = int(request.form.get('version_code', 1))
        version_name = request.form.get('version_name', '1.0.0')
        update_required = request.form.get('update_required') == 'on'
        update_title = request.form.get('update_title', '')
        update_message = request.form.get('update_message', '')
        download_url = request.form.get('download_url', '')
        
        # Whats new (multiple items)
        whats_new = []
        whats_new_items = request.form.getlist('whats_new[]')
        for item in whats_new_items:
            if item.strip():
                whats_new.append(item.strip())
        
        # Simpan data
        data = {
            'version_code': version_code,
            'version_name': version_name,
            'update_required': update_required,
            'update_title': update_title,
            'update_message': update_message,
            'download_url': download_url,
            'whats_new': whats_new
        }
        
        save_update_info(data)
        
        return redirect(url_for('admin_panel'))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===========================================
# API ENDPOINTS FOR ANDROID APP
# ===========================================

@app.route('/api/check-update', methods=['GET'])
def check_update():
    """
    Endpoint untuk aplikasi Android cek update
    Query params:
    - current_version_code: int (version code aplikasi saat ini)
    """
    try:
        current_version = int(request.args.get('current_version_code', 1))
        update_info = load_update_info()
        
        latest_version = update_info['version_code']
        has_update = latest_version > current_version
        
        response = {
            'has_update': has_update,
            'current_version': current_version,
            'latest_version': latest_version,
            'latest_version_name': update_info['version_name'],
            'update_required': update_info['update_required'] and has_update,
            'update_title': update_info['update_title'],
            'update_message': update_info['update_message'],
            'download_url': update_info['download_url'],
            'whats_new': update_info['whats_new'],
            'last_updated': update_info['last_updated']
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update-info', methods=['GET'])
def get_update_info():
    """Get full update information"""
    update_info = load_update_info()
    return jsonify(update_info)

# Vercel serverless function handler
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
