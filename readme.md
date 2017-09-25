my_instagram app installation guide:

1. Create and activate virtualenv (with python3.6)
2. pip install -r requirements.txt
3. Google Cloud Vision API:
    1. pip install --upgrade google-cloud-vision
    2. Install the Google Cloud SDK (https://cloud.google.com/sdk/docs/)
    3. [from SDK dir] gcloud auth application-default login
4. python manage.py migrate
5. python manage.py runserver

Test app:
http://localhost:8000/