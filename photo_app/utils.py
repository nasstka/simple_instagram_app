from django.forms.models import model_to_dict

from .models import VisionFaceDetails, VisionLabelsDetails
from .services import photo_vision_service


def get_all_objects(model, photo_id):
    results = []
    details = model.objects.filter(photo_id=photo_id)

    for detail in details:
        detail = model_to_dict(detail)
        results.append(detail)

    return results


def save_photo_vision_data(photo_pk, post):
    photo_vision_data = photo_vision_service(photo_pk)

    list_of_faces = photo_vision_data.get('faces')
    for face in list_of_faces:
        details_of_face = VisionFaceDetails.objects.create(
            photo=post, 
            **face
        )
    
    list_of_labels = photo_vision_data.get('labels')
    labels_description = [*list_of_labels]
    for description in labels_description:
        labels_in_photo = VisionLabelsDetails(
            photo=post, 
            labels=description,
            score=list_of_labels[description]
        )
        labels_in_photo.save()
