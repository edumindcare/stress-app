from flask import Flask, request, jsonify, send_from_directory
from keras.models import model_from_json
import numpy as np
import cv2
import os

app = Flask(__name__)

# Load model
with open("fer.json", "r") as f:
    model = model_from_json(f.read())
model.load_weights("fer.weights.h5")

# Label thứ tự giống khi train
labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Load bộ phát hiện khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/')
def index():
    return send_from_directory('.', 'predict.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    filename = file.filename
    file.save(filename)

    # Đọc ảnh màu, chuyển sang gray
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) == 0:
        os.remove(filename)
        return jsonify({'emotion': 'No face detected'})

    # Lấy khuôn mặt đầu tiên
    (x, y, w, h) = faces[0]
    roi_gray = gray[y:y+h, x:x+w]
    roi_gray = cv2.resize(roi_gray, (48, 48))

    # Tiền xử lý như lúc train
    img_pixels = np.expand_dims(np.expand_dims(roi_gray, -1), 0)
    img_pixels = img_pixels.astype('float32')
    img_pixels -= np.mean(img_pixels)
    img_pixels /= np.std(img_pixels) + 1e-5  # tránh chia cho 0

    # Dự đoán
    preds = model.predict(img_pixels)
    emotion = labels[np.argmax(preds)]

    os.remove(filename)
    return jsonify({'emotion': emotion})

if __name__ == '__main__':
    app.run(debug=True)