from PIL import ImageGrab, Image, ImageEnhance
import numpy
import pytesseract
import cv2

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """

    # Change image
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray)
    # https://stackoverflow.com/questions/43232813/convert-opencv-image-format-to-pil-image-format
    enhancer = ImageEnhance.Sharpness(Image.fromarray(image))
    enhance = enhancer.enhance(7.0)
    enhancecv2 = numpy.asarray(enhance)
    invertenhance = cv2.bitwise_not(enhancecv2)
    invertenhancegray = cv2.cvtColor(invertenhance, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Original image',image)
    cv2.imshow('Gray image', gray)  
    cv2.imshow('Invert image', invert)
    cv2.imshow('Enhance image', enhancecv2)
    cv2.imshow('Enhance invert image', invertenhance)
    cv2.imshow('Enhance invert gray', invertenhancegray)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # options: https://github.com/tesseract-ocr/tesseract/blob/master/doc/tesseract.1.asc
    colortext = pytesseract.image_to_string(image, config='--psm 8 digits')  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    graytext = pytesseract.image_to_string(gray, config='--psm 8 digits')  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    inverttext = pytesseract.image_to_string(invert, config='--psm 8 digits')
    enhancetext = pytesseract.image_to_string(enhancecv2, config='--psm 8 digits')
    invertenhancetext = pytesseract.image_to_string(invertenhance, config='--psm 8 digits')
    invertenhancegraytext = pytesseract.image_to_string(invertenhancegray, config='--psm 8 digits')

    value = dict();
    value["colortext"] = colortext
    value["graytext"] = graytext
    value["inverttext"] = inverttext
    value["enhancetext"] = enhancetext
    value["invertenhancetext"] = invertenhancetext
    value["invertenhancegraytext"] = invertenhancegraytext
    return value

value = ocr_core("images/tftstream.png")
print("color: " + value["colortext"])
print("gray: " + value["graytext"])
print("invert: " + value["inverttext"])
print("enhance: " + value["enhancetext"])
print("invert enhance: " + value["invertenhancetext"])
print("invert enhance gray: " + value["invertenhancegraytext"])