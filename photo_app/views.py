from django.shortcuts import render, redirect

from .forms import PhotoForm
from .models import Photo, VisionFaceDetails, VisionLabelsDetails
from .utils import convert_model_objects_to_dicts, save_photo_vision_data


def dashboard(request):
    photos = Photo.objects.all().order_by('-id')

    return render(request, 'dashboard.html', {'photos': photos})


def photo_detail(request, pk):
    photo_instance = Photo.objects.get(id=pk)

    faces_details = convert_model_objects_to_dicts(VisionFaceDetails, pk)
    labels_details = convert_model_objects_to_dicts(VisionLabelsDetails, pk)

    container = {
        'photo': photo_instance,
        'faces_details': faces_details,
        'lables_details': labels_details,
    }

    return render(request, 'photo_detail.html', container)


def photo_delete(request, pk):
    photo_instance = Photo.objects.get(id=pk)
    photo_instance.delete()

    return render(request, 'photo_delete.html')


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
