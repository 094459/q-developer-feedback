from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import json
import qrcode
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flashing messages

# Initialize data storage
DATA_FILE = "messages.json"

def load_messages():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_messages(messages):
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f)

def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('static/feedback_qr.png')

@app.route('/')
def index():
    messages = load_messages()
    return render_template('messages.html', messages=messages)

@app.route('/messages')
def get_messages():
    messages = load_messages()
    return jsonify(messages)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            messages = load_messages()
            messages.append(message)
            save_messages(messages)
            flash('Thank you! Your message has been submitted successfully.', 'success')
            return render_template('feedback.html', success=True)
    return render_template('feedback.html')

# if __name__ == '__main__':
#     Path('static').mkdir(exist_ok=True)
#     generate_qr_code('http://localhost:5000/feedback')
#     app.run(debug=True)
if __name__ == '__main__':
    Path('static').mkdir(exist_ok=True)
    # Update QR code to use 0.0.0.0 instead of localhost
    generate_qr_code('https://dev-feedback.ricsue.dev/feedback')
    # Modified to listen on all interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)
