# face_auth_module.py
import cv2
import pickle
import numpy as np
import psycopg2
from psycopg2 import Error

HAAR_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
DB_PARAMS = {
    "dbname": "face_auth_db",
    "user": "postgres",
    "password": "1842",
    "host": "localhost",
    "port": "5432"
}

face_cascade = cv2.CascadeClassifier(HAAR_PATH)

def recognize_user(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)

    if len(faces) != 1:
        return None

    (x, y, w, h) = faces[0]
    face_img = img[y:y+h, x:x+w]

    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        cursor.execute("SELECT username, face_data FROM users;")
        users = cursor.fetchall()

        for username, face_data_bytes in users:
            recognizer = pickle.loads(face_data_bytes)
            label, confidence = recognizer.predict(face_img)
            if confidence < 50:
                return username
    except Error as e:
        print("DB error:", e)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

    return None