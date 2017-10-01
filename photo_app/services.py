import io
import os

from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Photo


LIKELIHOOD_NAME = (
    'Unkown',
    'Very Unlikely',
    'Unlikely',
    'Possible',
    'Likely',
    'Very Likely'
)

FONT_PATH = '/home/nastka/Desktop/Roboto/Roboto-Regular.ttf'
FONT = ImageFont.truetype(FONT_PATH, 25)


def photo_vision_service(photo_id):
    """
    It use the Google Cloud Vision API to detect faces and labels in an image.
    Label Detection detects broad sets of categories within an image.
    Face Detection detects multiple faces within an image along with the
    associated key facial attributes such as emotional state.
    """

    photo = Photo.objects.get(id=photo_id)

    client = vision.ImageAnnotatorClient()
    file_name = photo.image.path

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # Label detection
    label_response = client.label_detection(image=image)
    labels = label_response.label_annotations

    label_list = {}
    for label in labels:
        label_list[label.description] = label.score

    # Face detection
    face_response = client.face_detection(image=image)
    faces = face_response.face_annotations

    img = Image.open(file_name)
    draw = ImageDraw.Draw(img)

    count = 0
    face_list = []
    for face in faces:
        count += 1
        box = [
            (vertex.x, vertex.y)
            for vertex in face.fd_bounding_poly.vertices
        ]
        draw.line(box + [box[0]], width=3, fill='#00ff00')

        text_coordinate_x = box[0][0] - 5
        text_coordinate_y = box[1][1] - 35
        draw.text(
            (text_coordinate_x, text_coordinate_y),
            ''.join(['#', str(count)]),
            fill='#00ff00',
            font=FONT
        )

        for landmark in face.landmarks:
            face_landmarks = (landmark.position.x, landmark.position.y)
            second_coordinate_x = face_landmarks[0] + 3
            second_coordinate_y = face_landmarks[1] + 3
            draw.rectangle(
                (
                    face_landmarks,
                    (second_coordinate_x, second_coordinate_y)
                ),
                fill='#00ff00'
            )

        face_detail = {
            'anger': LIKELIHOOD_NAME[face.anger_likelihood],
            'joy':  LIKELIHOOD_NAME[face.joy_likelihood],
            'surprise': LIKELIHOOD_NAME[face.surprise_likelihood],
            'sorrow': LIKELIHOOD_NAME[face.sorrow_likelihood],
        }
        face_list.append(face_detail)

    image_name, extension = os.path.splitext(file_name)
    new_image_name = ''.join([image_name, '-modified', extension])
    img.save(new_image_name)

    photo.modified_image = SimpleUploadedFile(
        new_image_name,
        content=open(new_image_name, 'rb').read(),
        content_type='image/*'
    )
    photo.save()

    contents = {
        'labels': label_list,
        'faces': face_list,
    }

    return contents
