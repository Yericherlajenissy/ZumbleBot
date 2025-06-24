from huggingface_hub import InferenceClient
import os
import time
import random
import string

# Define the folder to save generated images
OUTPUT_FOLDER = "static/generated"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Initialize the Hugging Face InferenceClient
client = InferenceClient(
    api_key="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"  # Replace with your actual API key
)

def generate_image(prompt):
    try:
        # Use the InferenceClient to generate an image with the model
        print("Generating image with prompt:", prompt)
        image = client.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0"
        )
        
        if image is None:
            return "Error: No image generated. Check model and API key."
        
        # Create a unique filename
        timestamp = int(time.time())
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        unique_filename = f"generated_image_{timestamp}_{random_string}.png"
        
        # Save the image
        output_path = os.path.join(OUTPUT_FOLDER, unique_filename)
        image.save(output_path)
        
        if not os.path.exists(output_path):
            return "Error: Image file not saved. Check folder permissions."
        
        print("Image generated and saved at:", output_path)
        return unique_filename
    
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return f"Error generating image: {str(e)}"
