# Function for antialiasing the video
def resize_with_antialiasing(img, new_size):
    
    img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)  # Interpolate for antialiasing
    return np.clip(img, 0, 255).astype(np.uint8)  # Limit values and convert to uint8

# Function for waiting for a file to be created
def wait_for_file_creation(file_path, timeout=30, min_size=1000):
    start_time = time.time()
    while not os.path.exists(file_path) or os.path.getsize(file_path) < min_size:
        if time.time() - start_time > timeout:
            raise TimeoutError("Timeout while waiting for file creation")
        time.sleep(1)