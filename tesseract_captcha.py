from PIL import Image, ImageOps
import pytesseract
import requests
from io import BytesIO
import cv2
import numpy as np

# Path to the Tesseract executable (update it according to your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    # Open the image using PIL
    with Image.open(image_path) as img:
        # Convert the image to grayscale
        img_gray = ImageOps.grayscale(img)
        
        # Apply thresholding to create a binary image
        threshold_value = 100  # Adjust this threshold as needed
        img_threshold = img_gray.point(lambda p: p > threshold_value and 255)
        
        # Invert the colors (if necessary)
        img_inverted = ImageOps.invert(img_threshold)
        
        # Perform additional preprocessing steps if needed (e.g., noise removal, contrast enhancement)
        
        return img_inverted

def solve_captcha(image_path):
    try:
        # Preprocess the captcha image
        preprocessed_image = preprocess_image(image_path)
        
        # Perform OCR on the preprocessed image
        captcha_text = pytesseract.image_to_string(preprocessed_image)
        
        return captcha_text.strip()
    except Exception as e:
        print(f"Error solving captcha: {str(e)}")
        return None


# def process_image(img):
#     try:
#         # Convert the image to grayscale
#         image_data = response.content

#         # Convert the image data to a numpy array
#         nparr = np.frombuffer(image_data, np.uint8)

#         # Decode the numpy array into an OpenCV image format
#         img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#         # Perform any necessary image processing using OpenCV
#         # For example, convert the image to grayscale
#         gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
#         # Apply thresholding to create a binary image
#         _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
#         # Perform morphological operations to clean up the image (noise removal)
#         kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#         opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        
#         # Perform OCR on the preprocessed image
#         captcha_text = pytesseract.image_to_string(opening)
        
#         return captcha_text.strip()
#     except Exception as e:
#         print(f"Error processing image: {str(e)}")
#         return None

# def correct_skew(response):
#     image_data = response.content

#     # Convert the image data to a numpy array
#     nparr = np.frombuffer(image_data, np.uint8)

#     # Decode the numpy array into an OpenCV image format
#     img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # Convert image to grayscale
#     gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
#     # Apply Gaussian blur to reduce noise
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
#     # Apply edge detection
#     edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
    
#     # Perform line detection using Hough Transform
#     lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    
#     # Calculate average angle of detected lines
#     angles = []
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi
#         angles.append(angle)
#     median_angle = np.median(angles)
    
#     # Rotate the image to correct skew
#     rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    
#     return rotated  


def process_image(img):
    try:
        # Convert the image data to a numpy array
        nparr = np.frombuffer(img, np.uint8)

        # Decode the numpy array into an OpenCV image format
        img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Correct skew and deskew the image
        def correct_skew(image):
            # Convert image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply edge detection
            edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
            
            # Perform line detection using Hough Transform
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
            
            # Calculate average angle of detected lines
            if lines is not None:
    # Calculate average angle of detected lines
                angles = []
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi
                    angles.append(angle)
                median_angle = np.median(angles)
                # Rotate the image to correct skew
                rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            else:
                # Handle case when no lines are detected
                rotated = image  # Use the original image
            return rotated

        corrected_image = correct_skew(img_cv)
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(corrected_image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to create a binary image
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Perform morphological operations to clean up the image (noise removal)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Perform OCR on the preprocessed image
        captcha_text = pytesseract.image_to_string(opening)
        
        return captcha_text.strip()
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None



# Example usage
image_url  = "https://images-na.ssl-images-amazon.com/captcha/lqbiackd/Captcha_clbxeklngq.jpg"
response = requests.get(image_url)
if response.status_code == 200:
    img = Image.open(BytesIO(response.content))


# captcha_image_path = "captcha.png"  # Path to your captcha image
threshold_value = 100  # Adjust this threshold as needed
img_threshold = img.point(lambda p: p > threshold_value and 255)
img_inverted = ImageOps.invert(img_threshold)
captcha_text = captcha_text = pytesseract.image_to_string(img_inverted)
if captcha_text:
    print(f"Solved Captcha: {captcha_text}")
else:
    print("Failed to solve captcha.")

solved = process_image(response.content)
print(solved)

# rotated = correct_skew(response)