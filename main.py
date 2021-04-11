from PIL import ImageGrab, Image, ImageEnhance
import numpy
import pytesseract
import cv2
import pygetwindow as gw

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """

    # Change image
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # https://stackoverflow.com/questions/43232813/convert-opencv-image-format-to-pil-image-format
    enhancer = ImageEnhance.Sharpness(Image.fromarray(gray))
    enhance = enhancer.enhance(7.0)
    enhancecv2 = numpy.asarray(enhance)
    invertenhance = cv2.bitwise_not(enhancecv2) # might revert back to regular invert gray

    cv2.imshow('Enhance invert image', invertenhance)

    # options: https://github.com/tesseract-ocr/tesseract/blob/master/doc/tesseract.1.asc
    invertenhancetext = pytesseract.image_to_string(invertenhance, config='--psm 8 digits')

    value = dict();
    value["invertenhancetext"] = invertenhancetext
    return value

value = ocr_core("images/tft25.png")
print("invert enhance: " + value["invertenhancetext"])
window = gw.getActiveWindow() # might work better on Windows
print(window)
print(type(window))