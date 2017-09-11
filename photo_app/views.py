import io
import os

from google.cloud import vision
from django.shortcuts import render, redirect
from PIL import Image, ImageDraw

from .forms import PhotoForm
from .models import Photo


LIKELIHOOD_NAME = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY',
                   'POSSIBLE', 'LIKELY', 'VERY_LIKELY')

def dashboard(request):
    photos = Photo.objects.all().order_by('-id')
    return render(request, 'dashboard.html', {'photos': photos})

def photo_detail(request, pk):  
    photo = Photo.objects.get(id=pk)

    client = vision.ImageAnnotatorClient()
    file_name = photo.photo.path

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # Label detection
    label_response = client.label_detection(image=image)
    labels = label_response.label_annotations

    # Face detection
    face_response = client.face_detection(image=image)
    faces = face_response.face_annotations

    img = Image.open(file_name)
    draw = ImageDraw.Draw(img)

    face_list = []
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=3, fill='#ff0000')

        face_detail = {
            'anger': LIKELIHOOD_NAME[face.anger_likelihood],
            'joy':  LIKELIHOOD_NAME[face.joy_likelihood],
            'surprise': LIKELIHOOD_NAME[face.surprise_likelihood],
            'sorrow': LIKELIHOOD_NAME[face.sorrow_likelihood],
        }
        face_list.append(face_detail)
        
    image_name, extension = os.path.splitext(file_name)
    new_image_name = image_name + '-Poly' + extension
    img.save(new_image_name, 'JPEG')

    new_photo = Photo() 
    new_photo.photo = new_image_name
    
    contents = {
        'photo': photo,
        'labels': labels, 
        'faces': face_list,
        'new_photo': new_photo,
    }
    
    return render(request, 'photo_detail.html', contents)
                                                                                                              
def photo_delete(request, pk):
    delete_photo = Photo.objects.get(id=pk)
    delete_photo.delete()
    return render(request, 'photo_delete.html',{'delete_photo': delete_photo})

def photo_add(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('photo_detail', pk=post.pk)
    else:
        form = PhotoForm()

    return render(request, 'photo_add.html', {'form':form})
