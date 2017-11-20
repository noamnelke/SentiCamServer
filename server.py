from flask import Flask, request
import emotion_api

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/recognize', methods=['POST'])
def recognize():
    image_data = request.data
    try:
        return emotion_api.recognize(image_data)
    except emotion_api.NoFaceRecognizedError:
        return {'error': 'No face recognized'}, 400
    except emotion_api.MultipleFacesRecognizedError:
        return {'error': 'Multiple faces recognized (only one is supported)'}, 400


if __name__ == '__main__':
    app.run()
