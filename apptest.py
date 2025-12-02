from flask import Flask, request, jsonify, send_file
from keras.models import model_from_json
import numpy as np
import cv2
import base64

app = Flask(__name__)

# Load model
with open("fer.json", "r") as json_file:
    loaded_model_json = json_file.read()

model = model_from_json(loaded_model_json)
model.load_weights("fer.weights.h5")

emotion_labels = [
    'Tức giận',
    'Ghê tởm',
    'Sợ hãi',
    'Vui vẻ',
    'Buồn bã',
    'Ngạc nhiên',
    'Bình thường'
]

def preprocess_image(gray):
    img = cv2.resize(gray, (48, 48))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=-1)
    return img

@app.route("/")
def index():
    return send_file("indextest.html")

@app.route("/scripttest.js")
def js_file():
    return send_file("scripttest.js")

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("image")

    if file:
        img = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)
    else:
        data_url = request.form.get("image")
        img_bytes = base64.b64decode(data_url.split(",")[1])
        img = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)

    processed = preprocess_image(img)
    prediction = model.predict(processed)
    emotion = emotion_labels[np.argmax(prediction)]

    return jsonify({"emotion": emotion})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
