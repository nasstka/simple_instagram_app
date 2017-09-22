from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from .forms import PhotoForm
from .models import Photo, VisionFaceDetails, VisionLabelsDetails
from .services import photo_vision_service


def dashboard(request):
    photos = Photo.objects.all().order_by('-id')
    return render(request, 'dashboard.html', {'photos': photos})


def photo_detail(request, pk):  
    photo = Photo.objects.get(id=pk)

    faces_details = VisionFaceDetails.objects.filter(photo_id=pk)
    list_of_faces_details = []
    for detail in faces_details:
        detail = model_to_dict(detail)
        list_of_faces_details.append(detail)

    labels_details = VisionLabelsDetails.objects.filter(photo_id=pk)
    list_of_labels_details = []
    for label in labels_details:
        label = model_to_dict(label)
        list_of_labels_details.append(label)

    container = {
        'photo': photo, 
        'faces_details': list_of_faces_details,
        'lables_details': list_of_labels_details,
    }

    return render(request, 'photo_detail.html', container)


def photo_delete(request, pk):
    delete_photo = Photo.objects.get(id=pk)
    delete_photo.delete()
    return render(request, 'photo_delete.html', {'delete_photo': delete_photo})


def photo_add(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            photo_vision_data = photo_vision_service(post.pk)

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

            return redirect('photo_detail', pk=post.pk)
    else:
        form = PhotoForm()

    return render(request, 'photo_add.html', {'form': form})
