import requests
import settings


class NoFaceRecognizedError(Exception):
    pass


class MultipleFacesRecognizedError(Exception):
    pass


def recognize(image_data):
    response = requests.post(url=settings.API_HOST + '/emotion/v1.0/recognize',
                             data=image_data,
                             headers=_get_headers())
    face_data = _extract_face_data(response)
    top_emotion = _get_top_emotion(face_data['scores'])

    return {"feeling": top_emotion,
            "faceRectangle": face_data['faceRectangle'],
            "imageData": image_data}


def _get_headers():
    return {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': settings.API_KEY,
    }


def _get_top_emotion(scores):
    return max(scores.items(), key=lambda emotion: emotion[1])[0]


def _extract_face_data(response):
    faces = response.json()
    if len(faces) == 0:
        raise NoFaceRecognizedError()
    if len(faces) > 1:
        raise MultipleFacesRecognizedError()
    return faces[0]
