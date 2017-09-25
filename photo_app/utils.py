from django.forms.models import model_to_dict

from .models import VisionFaceDetails, VisionLabelsDetails
from .services import photo_vision_service


def convert_model_objects_to_dicts(model, photo_id):
    """
    Gets model and retrives all of the model objects that are filtered by
    photo_id, which is given as 2nd function argument then, converts the
    queryset into list of dicts.
    """

    results = []
    details = model.objects.filter(photo_id=photo_id)

    for detail in details:
        detail = model_to_dict(detail)
        results.append(detail)

    return results


def save_photo_vision_data(photo_pk, post):
    """
    Saves face and labels data received from Google Cloud Vision API
    to database.
    """

    photo_vision_data = photo_vision_service(photo_pk)

    list_of_faces = photo_vision_data.get('faces')
    if list_of_faces:
        for face in list_of_faces:
            VisionFaceDetails.objects.create(
                photo=post,
                **face
            )

    list_of_labels = photo_vision_data.get('labels')
    if list_of_labels:
        labels_description = [*list_of_labels]
        for description in labels_description:
            labels_in_photo = VisionLabelsDetails(
                photo=post,
                labels=description,
                score=list_of_labels[description]
            )
            labels_in_photo.save()
