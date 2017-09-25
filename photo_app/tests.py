import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from my_instagram import settings
from .forms import PhotoForm, Photo
from .services import photo_vision_service


class PhotoFormTest(TestCase):
    fixtures = ['photos']

    def prepare_form(self):
        data = {
            'title': 'test2',
            'description': 'test2',
        }

        test_file_path = os.path.join(
            settings.BASE_DIR, 'test_data', 'upload_test_image.jpg'
        )

        file_data = {
            'image': SimpleUploadedFile(
                'test_image.jpg',
                content=open(test_file_path, 'rb').read(),
                content_type='image/jpeg'
            ),
        }
        form = PhotoForm(data, file_data)
        return form

    def test_if_fixtures_are_loaded(self):
        photo = Photo.objects.all().count()
        self.assertNotEqual(photo, 0)

    def test_user_can_access_dashboard_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_photo_detail_view(self):
        response = self.client.get('/dashboard/1/')
        self.assertEqual(response.status_code, 200)

    def test_user_can_delete_photo(self):
        initial_count = Photo.objects.all().count()

        Photo.objects.all().delete()
        final_count = Photo.objects.all().count()
        self.assertNotEqual(initial_count, final_count)

    def test_user_can_upload_image(self):
        # Check if form is valid
        form = self.prepare_form()
        self.assertTrue(form.is_valid())

        # Check if form was saved correctly
        form.save()
        self.assertEqual(Photo.objects.all().count(), 2)

    def test_for_service_work_correctly(self):
        form = self.prepare_form()
        form.save()

        photo = Photo.objects.get(id=2)
        results = photo_vision_service(photo_id=photo.id)

        self.assertTrue(results)

    def test_invalid_form(self):
        invalid_data = {
            'title': 'a'*101,
            'description': ''
        }

        invalid_file = {
            'image': 'image.pdf'
        }

        form = PhotoForm(invalid_data, invalid_file)
        self.assertFalse(form.is_valid())
