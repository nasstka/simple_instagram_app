from django.shortcuts import render, redirect
from django.forms.models import model_to_dict

from .forms import PhotoForm
from .models import Photo, VisionFaceDetails, VisionLabelsDetails
from .utils import get_all_objects, save_photo_vision_data


def dashboard(request):
    photos = Photo.objects.all().order_by('-id')
    return render(request, 'dashboard.html', {'photos': photos})


def photo_detail(request, pk):  
    photo = Photo.objects.get(id=pk)

    faces_details = get_all_objects(VisionFaceDetails, pk)

    labels_details = get_all_objects(VisionLabelsDetails, pk)

    container = {
        'photo': photo, 
        'faces_details': faces_details,
        'lables_details': labels_details,
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
            save_photo_vision_data(post.pk, post)

            return redirect('photo_detail', pk=post.pk)
    else:
        form = PhotoForm()

    return render(request, 'photo_add.html', {'form': form})
