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

    Returns (file_path, metadata_dict) on success, or (None, None) on failure.
    metadata_dict includes: original_size_kb, compressed_size_kb, savings_pct,
                            original_dims, final_dims, was_resized, mode
    """
    try:
        # 1. Read original file size before processing
        uploaded_file.seek(0, 2)  # Seek to end
        original_size_bytes = uploaded_file.tell()
        uploaded_file.seek(0)  # Reset

        # 2. Open the image using Pillow
        image = Image.open(uploaded_file)
        original_mode = image.mode
        original_dims = image.size  # (width, height)

        # Convert to RGB if it is in RGBA/P mode to allow JPEG conversion and compression
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # 3. Resize maintaining aspect ratio if image width exceeds max_width
        w, h = image.size
        was_resized = False
        if w > max_width:
            aspect_ratio = h / w
            new_width = max_width
            new_height = int(max_width * aspect_ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            was_resized = True

        final_dims = image.size  # (width, height)

        # 4. Generate a unique file name
        timestamp = int(time.time() * 1000)
        file_name = f"post_{user_id}_{timestamp}.jpg"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        # 5. Save image with JPEG compression
        image.save(file_path, "JPEG", quality=quality, optimize=True)

        # 6. Measure compressed size
        compressed_size_bytes = os.path.getsize(file_path)

        # 7. Build metadata
        savings_pct = round((1 - compressed_size_bytes / original_size_bytes) * 100, 1) if original_size_bytes > 0 else 0
        metadata = {
            "original_size_kb": round(original_size_bytes / 1024, 1),
            "compressed_size_kb": round(compressed_size_bytes / 1024, 1),
            "savings_pct": savings_pct,
            "original_dims": original_dims,
            "final_dims": final_dims,
            "was_resized": was_resized,
            "mode": original_mode,
        }

        return file_path, metadata
    except Exception as e:
        print(f"Error processing image: {e}")
        return None, None


def upload_post(user_id, uploaded_file, caption):
    """
    Coordinates photo upload: processes the image, saves it, and adds a post record to the database.
    Returns (success, message) for backward compatibility.
    For the full metadata, use upload_post_with_metadata().
    """
    ok, msg, _ = upload_post_with_metadata(user_id, uploaded_file, caption)
    return ok, msg


def upload_post_with_metadata(user_id, uploaded_file, caption):
    """
    Coordinates photo upload with full compression metadata.
    Returns (success: bool, message: str, metadata: dict | None)
    """
    if not uploaded_file:
        return False, "No file uploaded.", None

    # Process & compress image
    saved_path, metadata = process_and_save_image(uploaded_file, user_id)
    if not saved_path:
        return False, "Failed to process image. Please upload a valid image file (JPG, PNG, JPEG).", None

    # Create record in DB
    post_id = database.create_post(user_id, saved_path, caption)
    if post_id:
        return True, "Post uploaded successfully!", metadata
    else:
        # Cleanup file if DB insertion failed
        try:
            if os.path.exists(saved_path):
                os.remove(saved_path)
        except Exception:
            pass
        return False, "Failed to save post to the database.", None


def delete_user_post(post_id, user_id):
    """
    Deletes a user's post from the database and deletes the physical file.
    """
    success = database.delete_post(post_id, user_id)
    if success:
        return True, "Post deleted successfully."
    return False, "Could not delete post. Ensure you are the owner."

