import hashlib
from gi.repository import GdkPixbuf

def hash_password(password):
    """Returns the SHA-256 hash of the password."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password, stored_hash):
    """Verifies a password against a stored hash."""
    if not stored_hash:
        return False
    return hash_password(password) == stored_hash

def fast_blur_pixbuf(pixbuf, radius=10):
    """
    Applies a fast blur by downscaling and then upscaling the GdkPixbuf.
    Radius is roughly simulated by the scale factor.
    """
    if not pixbuf:
        return None

    width = pixbuf.get_width()
    height = pixbuf.get_height()

    # Calculate scale factor based on radius (higher radius = smaller scale)
    # A divisor of 10 means 1/10th resolution
    scale_factor = max(2, radius) 
    
    small_width = max(1, width // scale_factor)
    small_height = max(1, height // scale_factor)

    # Downscale
    small_pixbuf = pixbuf.scale_simple(
        small_width, 
        small_height, 
        GdkPixbuf.InterpType.NEAREST
    )

    # Upscale (Bilinear gives a blurry look)
    blurred_pixbuf = small_pixbuf.scale_simple(
        width, 
        height, 
        GdkPixbuf.InterpType.BILINEAR
    )

    return blurred_pixbuf
