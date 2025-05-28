# app.py
from flask import Flask, request, jsonify
from PIL import Image
import tensorflow as tf
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = tf.keras.applications.mobilenet_v2.MobileNetV2(weights='imagenet')
decode = tf.keras.applications.mobilenet_v2.decode_predictions
preprocess = tf.keras.applications.mobilenet_v2.preprocess_input

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_path = data.get('imagePath')

    if not image_path:
        return jsonify({'error': 'No image path provided'}), 400

    try:
        img = Image.open(image_path).resize((224, 224))
        img_array = np.expand_dims(np.array(img), axis=0)
        img_array = preprocess(img_array)

        preds = model.predict(img_array)
        label = decode(preds, top=1)[0][0][1]  # Get top class label
        return jsonify({'food': label})

    except Exception as e:
        print(f"❌ Flask error: {e}")
        return jsonify({'error': 'Failed to classify image'}), 500

if __name__ == '__main__':
    app.run(port=5001)
