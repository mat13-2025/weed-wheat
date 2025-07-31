import os
import requests
from django.conf import settings

def download_model():
    model_dir = os.path.join(settings.BASE_DIR, 'model')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'maize_disease_model.h5')

    if not os.path.exists(model_path):
        print("Downloading model from Google Drive...")
        file_id = "10liAww1q4L7cwW0ESzn6QqCCkLu3KV4c"
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(url)
        with open(model_path, 'wb') as f:
            f.write(response.content)
        print("Model download complete.")
