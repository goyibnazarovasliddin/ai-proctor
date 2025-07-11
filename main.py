from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from recognition_utils import recognize_face_from_path
from log_utils import log_status
import os

app = Flask(__name__)

# Foydalanuvchi rasmi va vaqtinchalik fayllar uchun papkalar
UPLOAD_FOLDER_TEMP = 'uploaded_frames'
UPLOAD_FOLDER_FACES = 'face_images'
os.makedirs(UPLOAD_FOLDER_TEMP, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_FACES, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user')
def add_user():
    return render_template("add_user.html")

@app.route('/save_user', methods=['POST'])
def save_user():
    name = request.form.get("name")
    image = request.files['image']
    filename = secure_filename(f"{name}.jpg")
    path = os.path.join(UPLOAD_FOLDER_FACES, filename)
    image.save(path)
    return jsonify({"status": "Yuz saqlandi"})

@app.route('/status', methods=['POST'])
def status():
    data = request.get_json()
    camera_on = data.get("camera_on", False)
    mic_on = data.get("mic_on", False)

    if camera_on and mic_on:
        status_text = "Kamera va mikrofon ishlamoqda"
    elif camera_on:
        status_text = "Faqat kamera ishlamoqda"
    elif mic_on:
        status_text = "Faqat mikrofon ishlamoqda"
    else:
        status_text = "Harakat aniqlanmadi"

    return jsonify({"status": status_text})

@app.route("/upload_face", methods=["POST"])
def upload_face():
    file = request.files["frame"]
    camera_on = request.form.get("camera_on") == "true"
    mic_on = request.form.get("mic_on") == "true"

    file_path = os.path.join("temp.jpg")
    file.save(file_path)

    name = recognize_face_from_path(file_path)

    if name:
        if camera_on and mic_on:
            status_text = f"Gapiryapti va ko‘rinmoqda - {name}"
        elif camera_on:
            status_text = f"Faqat ko‘rinmoqda - {name}"
        elif mic_on:
            status_text = f"Faqat gapiryapti - {name}"
        else:
            status_text = f"Inaktiv - {name}"
    else:
        # Kamera ochiq bo‘lsa, lekin yuz aniqlanmasa
        if camera_on:
            status_text = "Yuz aniqlanmadi — shaxs topilmadi"
        elif mic_on:
            status_text = "Faqat gapiryapti — shaxs topilmadi"
        else:
            status_text = "Harakat aniqlanmadi"

    log_status(status_text)
    return jsonify({"status": status_text})

if __name__ == '__main__':
    app.run(debug=True)
