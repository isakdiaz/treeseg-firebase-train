import os.path

import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
import cv2 as cv
import pickle


def read_dictionary(filename):
    file_to_read = open(filename, "rb")

    loaded_dictionary = pickle.load(file_to_read)
    print(f"Pickle Dictionary read with {len(loaded_dictionary.keys())} entries.")
    return(loaded_dictionary)

def create_black_img():
    # Create a black image
    return np.zeros((512, 512, 3), np.uint8)

FIREBASE_DICTIONARY = "firebase-db.pkl"
MASK_DIRECTORY = "mask"
MASK_EXTENSION = ".jpg"

MASK_DIRECTORY = "mask"
MASK_EXTENSION = ".png"

# Make output directories
mask_path = os.path.join(os.getcwd(), MASK_DIRECTORY)

# Create paths if they don't exist
if not os.path.exists(mask_path):
    os.mkdir(mask_path)


firebaseDb = read_dictionary(FIREBASE_DICTIONARY)
# print(firebaseDb)

for key in firebaseDb.keys():
    # print(key)
    x_points = np.array(firebaseDb[key][0]['x'])
    y_points = np.array(firebaseDb[key][0]['y'])

    # Original Pts from  -0.5 to 0.5, need to remap to 0 to 512
    # Note, firebaseDb points increase from bottom-left to top-right while openCV images increase from top-left to bottom-right
    # Vertical flip necessary to align
    x_points = (x_points + 0.5) * 512
    y_points = (y_points + 0.5) * 512
    zipped_pts = list(zip(x_points, y_points))

    img = create_black_img()
    pts = np.array(zipped_pts, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv.fillPoly(img, [pts], (255, 255, 255))

    # Flip vertically due to Unity and OpenCV having different coordinate systems
    img = cv.flip(img, 0)

    # Images are in JPG format and Masks are in PNG format
    filename = os.path.join(os.getcwd(), MASK_DIRECTORY, key + MASK_EXTENSION)
    print(filename)
    cv.imwrite(filename, img)

# cv.imwrite('color_img.jpg', img)
# cv.imshow('Color image', img)
# cv.waitKey(0)
# cv.destroyAllWindows()