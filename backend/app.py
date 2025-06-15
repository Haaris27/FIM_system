from flask import Flask, jsonify
from flask_cors import CORS
from api.routes import api_bp
from monitoring.file_monitor import FileMonitor
from notifier import EmailNotifier
import psutil

app = Flask(__name__)
CORS(app)

# Initialize our monitoring systems
file_monitor = FileMonitor()
email_notifier = EmailNotifier()

# Make email_notifier available to routes
app.config['email_notifier'] = email_notifier

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

# Add a health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'running',
        'system': {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent
        }
    })

if __name__ == '__main__':
    try:
        print("🚀 FIM System Starting...")
        print("📁 Monitoring directory:", file_monitor.TEST_DIRECTORY)
        print("🔍 API available at http://localhost:5000")
        app.run(debug=True, port=5000)
    except KeyboardInterrupt:
        print("\n⚠️ Shutting down gracefully...")
        file_monitor.observer.stop()
        file_monitor.observer.join()
