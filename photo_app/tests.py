from django.test import TestCase, Client

from .models import Photo

class PhotoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        new_photo = Photo.objects.create(title='Lion',
                                        description='African big cat',
                                        photo='lion.jpeg')

    def test_title_label(self):
        new_photo = Photo.objects.get(id=1)
        field_label = new_photo._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_description_label(self):
        new_photo = Photo.objects.get(id=1)
        field_label = new_photo._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_title_max_length(self):
        new_photo = Photo.objects.get(id=1)
        max_length = new_photo._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_description_max_length(self):
        new_photo = Photo.objects.get(id=1)
        max_length = new_photo._meta.get_field('description').max_length
        self.assertEqual(max_length, 250)

    def test_user_can_add_photo(self):
        self.assertEqual(Photo.objects.count(), 1)

    def test_user_can_delete_photo(self):
        del_photo = Photo.objects.get(id=1)
        del_photo.delete()
        self.assertEqual(Photo.objects.count(), 0)
