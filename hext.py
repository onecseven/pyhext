from cgi import test
import cv2 
import pytesseract
import numpy as np
import colorsys, os
from slope import write_sorted
from utils import text2file

def extract_text(crop, img_thresh):
    result = []
    for line in crop:
        (data_ocr) = extract_all(line, img_thresh)
        test_list = ' '.join(data_ocr).split()
        result.append(test_list)
    result.reverse()
    return result

def treat_img(input):
    img_src = cv2.imread(input)
    (img_thresh, img_gray) = threshold_image(img_src)
    (img_mask, img_hsv) = mask_image(img_src)
    
    if is_empty_mask(img_mask):
        return [], []
    
    (img_contour, img_box, crop) = draw_contour_boundings(img_src, img_mask, threshold_area=400)
    return crop, img_thresh

def show(img):
    cv2.imshow("visual print", img)
    cv2.waitKey(0)

def threshold_image(img_src):
    """Grayscale image and apply Otsu's threshold"""
    window_name = 'Image'
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    (null, img_thresh) = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img_thresh, img_gray

def is_empty_mask(img_mask):
    for array in img_mask:
        for num in array:
            if num:
                return False
            else:
                pass
    return True

def mask_image(img_src):
    # RGB to HSV color space conversion
    img_hsv = cv2.cvtColor(img_src, cv2.COLOR_BGR2HSV)
    upper = np.array([179, 255, 255])
    lower = np.array([0, 107, 0])
    
    # Color segmentation with lower and upper threshold ranges to obtain a binary image
    img_mask = cv2.inRange(img_hsv, lower, upper)

    
    img_mask_denoised = denoise_image(img_mask)
    
    return img_mask_denoised, img_hsv

def denoise_image(img_mask):
    """Denoise image with a morphological transformation."""

    # Morphological transformations to remove small noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img_denoised = cv2.morphologyEx(
        img_mask, cv2.MORPH_OPEN, kernel, iterations=1)

    return img_denoised

def extract_all(img_src, img_thresh):
    # Extract all text as one string
    string_ocr = pytesseract.image_to_string(
        img_thresh, lang='eng', config='--psm 6')
    # Extract all text and meta data as dictionary
    data_ocr = pytesseract.image_to_data(img_src, lang='eng', config='--psm 6', output_type=pytesseract.Output.DICT)

    return data_ocr["text"] 

def draw_contour_boundings(img_src, img_mask, threshold_area=400):
    """Draw contour bounding and contour bounding box"""
    # Contour detection
    contours, hierarchy, = cv2.findContours(
        img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create two copies of source image
    img_contour = img_src.copy()
    img_box = img_src.copy()
    crop = []
    for idx, c in enumerate(contours):
        # Skip small contours because its probably noise
        if  cv2.contourArea(c) < threshold_area:
            continue

        # Draw contour in red
        cv2.drawContours(img_contour, contours, idx, (0, 0, 255), 2, cv2.LINE_4, hierarchy)

        # Get bounding box position and size of contour
        x, y, w, h = cv2.boundingRect(c)
        # the 5is  for padding
        crop.append(img_src.copy()[y:y+h+5, x:x+w+5])
        # Draw bounding box in blue
        cv2.rectangle(img_box, (x, y), (x + w, y + h), (255, 0, 0), 2, cv2.LINE_AA, 0)
    return img_contour, img_box, crop

def process(png_path, input, png):
    if os.path.isfile(png_path):
        (crop, img_thresh) = treat_img(png_path)
        text = extract_text(crop, img_thresh)
        text2file(text, input, png)
    os.remove(png_path) 

