import os
import time
from PIL import Image
import database

# Ensure the uploads directory exists
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def process_and_save_image(uploaded_file, user_id, max_width=1080, quality=75):
    """
    Validates, resizes, and compresses an uploaded image file, then saves it to the local uploads directory.
    - uploaded_file: The file object from st.file_uploader.
    - user_id: The ID of the user uploading the image.
    - max_width: Maximum width of the image (standard social media format).
    - quality: JPEG compression quality (0-100).
    
    Returns the file path on success, or None on failure.
    """
    try:
        # 1. Open the image using Pillow
        image = Image.open(uploaded_file)
        
        # Convert to RGB if it is in RGBA/P mode to allow JPEG conversion and compression
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
            
        # 2. Resize maintaining aspect ratio if image width exceeds max_width
        w, h = image.size
        if w > max_width:
            aspect_ratio = h / w
            new_width = max_width
            new_height = int(max_width * aspect_ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        # 3. Generate a unique file name
        timestamp = int(time.time() * 1000)
        file_name = f"post_{user_id}_{timestamp}.jpg"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        # 4. Save image with JPEG compression
        image.save(file_path, "JPEG", quality=quality, optimize=True)
        return file_path
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def upload_post(user_id, uploaded_file, caption):
    """
    Coordinates photo upload: processes the image, saves it, and adds a post record to the database.
    """
    if not uploaded_file:
        return False, "No file uploaded."
        
    # Process & compress image
    saved_path = process_and_save_image(uploaded_file, user_id)
    if not saved_path:
        return False, "Failed to process image. Please upload a valid image file (JPG, PNG, JPEG)."
        
    # Create record in DB
    post_id = database.create_post(user_id, saved_path, caption)
    if post_id:
        return True, "Post uploaded successfully!"
    else:
        # Cleanup file if DB insertion failed
        try:
            if os.path.exists(saved_path):
                os.remove(saved_path)
        except Exception:
            pass
        return False, "Failed to save post to the database."

def delete_user_post(post_id, user_id):
    """
    Deletes a user's post from the database and deletes the physical file.
    """
    success = database.delete_post(post_id, user_id)
    if success:
        return True, "Post deleted successfully."
    return False, "Could not delete post. Ensure you are the owner."
