from waitress import serve
from app import app  # Replace 'app' with the actual name of your Flask app if it's different

serve(app, host='0.0.0.0', port=8080)

