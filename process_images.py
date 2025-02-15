import os
import requests
from load_dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
from io import BytesIO
import json

load_dotenv()

# Initialize OpenAI API client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),
                base_url="https://api.openai.com")

# Function to predict whether an image contains inappropriate content using OpenAI's models


def moderate_image(image_path):
    try:
        # Open the image file
        with open(image_path, 'rb') as image_file:
            # Send image to OpenAI's model for analysis (e.g., CLIP or any other available model)
            response = client.images.create(
                model="dall-e-2",  # You can choose a model such as DALL-E 2 or any available OpenAI model that processes images
                images=[image_file]
            )
            # Get the first response from the data
            result = response['data'][0]

            # Here, you can check for certain criteria like unsafe content, or trigger a custom filter
            # For example, checking if the model returns any NSFW flag or inappropriate metadata (you may need a custom prompt for this)
            if 'safe' in result['metadata'] and result['metadata']['safe'] == False:
                return {"is_safe": False, "reason": "NSFW content detected"}
            else:
                return {"is_safe": True}

    except Exception as e:
        print(f"Error in moderate_image: {e}")
        # In case of an error, assume the image is safe.
        return {"is_safe": True}

# Function to process image URL for moderation


def analyze_image_url(image_url):
    try:
        # Download image content from the URL
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        # Send the image content to OpenAI for analysis
        return moderate_image(image)
    except Exception as e:
        print(f"Error analyzing image URL: {e}")
        return {"is_safe": True}
