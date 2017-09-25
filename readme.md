my_instagram app installation guide:

1. Create and activate virtualenv (with python3.6)
2. pip install -r requirements.txt
3. Google Cloud Vision API:
    a) pip install --upgrade google-cloud-vision
    b) Install the Google Cloud SDK (https://cloud.google.com/sdk/docs/)
    c) gcloud auth application-default login
4. python manage.py migrate
5. python manage.py runserver

http://localhost:8000/