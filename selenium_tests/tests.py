import os

import requests

from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from my_instagram import settings
from photo_app.models import Photo, VisionLabelsDetails


class SeleniumTestCase(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(SeleniumTestCase, self).setUp()

    def upload_images(self, driver):
        test_image = os.path.join(
            settings.BASE_DIR, 'test_data', 'upload_test_image.jpg'
        )

        add_button = driver.find_element_by_xpath(
            '//a[@class="btn btn-primary"]'
        )
        add_button.click()

        title_input = driver.find_element_by_name('title')
        title_input.send_keys('Tests')

        desc_input = driver.find_element_by_name('description')
        desc_input.send_keys('Test image')

        image_input = driver.find_element_by_name('image')
        image_input.send_keys(test_image)

        save_button = driver.find_element_by_xpath(
            '/html/body/div[3]/div/div/form/div[4]/button'
        )
        save_button.click()

    def wait(self, driver, delay):
        WebDriverWait(driver, delay).until(EC.url_contains('/dashboard/1/'))

    def open(self):
        driver = self.driver
        driver.get(self.live_server_url)

        return driver

    def test_user_can_add_photos(self):
        driver = self.open()

        self.upload_images(driver)

        self.wait(driver, 10)
        back_button = driver.find_element_by_xpath(
            '//a[@class="navbar-brand"]'
        )
        back_button.click()

    def test_blank_dashboard_view(self):
        driver = self.open()

        assert 'VisionApp' in driver.title

        photos = Photo.objects.count()
        assert photos == 0

        assert 'No images were uploaded yet.' in driver.page_source

    def test_not_blank_dashboard_view(self):
        driver = self.open()
        self.upload_images(driver)

        self.wait(driver, 10)
        back_button = driver.find_element_by_xpath(
            '//a[@class="navbar-brand"]'
        )
        back_button.click()

        thumbnails = driver.find_elements_by_class_name('img-thumbnail')
        image_count = len(thumbnails)

        assert image_count != 0

        photos = Photo.objects.count()
        assert photos != 0

    def test_detail_view_of_photo(self):
        driver = self.open()

        self.upload_images(driver)

        image_detail_url = driver.find_element_by_css_selector(
            '.card-img-top'
        ).get_attribute('src')

        # Check image
        response = requests.get(image_detail_url)
        assert response.status_code == 200

        image_title = driver.find_element_by_class_name('card-title')
        assert 'Tests' in image_title.text

        image_desc = driver.find_element_by_class_name('card-text')
        assert 'Test image' in image_desc.text

        # Check labels detection
        label_tabel = driver.find_element_by_tag_name('tbody')
        label_rows = len(label_tabel.find_elements_by_tag_name('tr'))
        labels_count = VisionLabelsDetails.objects.count()
        assert labels_count == label_rows

        # Check face detection
        faces_tab = driver.find_element_by_link_text('Faces')
        faces_tab.click()

        face_count = len(driver.find_elements_by_xpath(
            '//table[@class="table table-striped"]'
        ))
        assert face_count != 0

    def test_user_can_delete_photo(self):
        driver = self.open()

        self.upload_images(driver)
        self.wait(driver, 10)

        delete_button = driver.find_element_by_link_text('Delete photo')
        delete_button.click()

        driver.implicitly_wait(5)
        delete_info = driver.find_element_by_class_name(
            'jumbotron-heading'
        )
        assert 'Photo Deleted Successfully!' in delete_info.text

        back_button = driver.find_element_by_link_text('Back to Dashboard')
        back_button.click()

    def tearDown(self):
        self.driver.close()
        super(SeleniumTestCase, self).tearDown()
