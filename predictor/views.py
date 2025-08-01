from django.shortcuts import render
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Import the model downloader
from .utils import download_model

# Class labels (must match your model training order)
class_names = ['wheat', 'weed', 'unknown']

# Allowed image formats
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png')

def predict_disease(request):
    if request.method == 'POST' and request.FILES.get('leaf_image'):
        img_file = request.FILES['leaf_image']

        # Validate file type
        if not img_file.name.lower().endswith(ALLOWED_EXTENSIONS):
            return render(request, 'upload.html', {
                'error': 'Unsupported file type. Please upload a .jpg, .jpeg, or .png image.'
            })

        # Save uploaded image
        media_folder = settings.MEDIA_ROOT
        if not os.path.exists(media_folder):
            os.makedirs(media_folder)

        file_path = os.path.join(media_folder, img_file.name)
        with open(file_path, 'wb+') as dest:
            for chunk in img_file.chunks():
                dest.write(chunk)

        try:
            # ⬇️ Ensure model is downloaded before loading
            download_model()

            # Load model (only when needed)
            model_path = os.path.join(settings.BASE_DIR, 'model', 'maize_disease_model.h5')
            model = load_model(model_path)

            # Preprocess image
            img = image.load_img(file_path, target_size=(150, 150))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predict using CNN
            prediction = model.predict(img_array)
            predicted_index = np.argmax(prediction)
            predicted_class = class_names[predicted_index]

            # Image URL for display
            image_url = os.path.join(settings.MEDIA_URL, img_file.name)

            # Show only class name (no confidence)
            message = predicted_class.upper()

            return render(request, 'result.html', {
                'prediction': message,
                'image_path': image_url
            })

        except Exception as e:
            return render(request, 'upload.html', {
                'error': f"Error processing image: {str(e)}"
            })

    # Handle GET or no file uploaded
    return render(request, 'upload.html')



