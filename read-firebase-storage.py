import firebase_admin
from firebase_admin import credentials, storage
import numpy as np
import pickle
import pandas as pd
import os

def download_blob(bucket, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    # storage_client = storage.Client()
    #
    # bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object from bucket {} to local file {}.".format(
            source_blob_name, destination_file_name
        )
    )


# Place credentials in same folder and change variable
FIREBASE_CREDENTIALS_PATH = "credentials/biome-app-2-firebase-adminsdk-soxoo-b3f1bf7e27.json"
FIREBASE_IMAGE_FOLDER = "vdbh-image"
FIREBASE_MASK_FOLDER = "vdbh-mask"

# Save options
IMAGE_SAVE_DIRECTORY = "image"
IMAGE_SAVE_EXTENSION = ".jpg"
MASK_SAVE_DIRECTORY = "mask"
MASK_SAVE_EXTENSION = ".png"

# Make output directories
image_path = os.path.join(os.getcwd(), IMAGE_SAVE_DIRECTORY)
mask_path = os.path.join(os.getcwd(), MASK_SAVE_DIRECTORY)

# Create paths if they don't exist
if not os.path.exists(image_path):
    os.mkdir(image_path)

if not os.path.exists(mask_path):
    os.mkdir(mask_path)


cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred, {'storageBucket': 'biome-app-2.appspot.com'})



bucket = storage.bucket()
# bucket.blob("vdbh-mask/pinus-clausa/2022-01-09-14-05-34-R883").download_to_filename("test.jpg")


mask_filenames = [blob.name for blob in list(bucket.list_blobs()) if FIREBASE_MASK_FOLDER in blob.name]
image_filenames = [blob.name for blob in list(bucket.list_blobs()) if FIREBASE_IMAGE_FOLDER in blob.name]


mask_count = 0
for filename in mask_filenames:
    destination_filename = filename.split("/")[-1]
    destination_filename = os.path.join(mask_path, destination_filename.split(".")[0] + MASK_SAVE_EXTENSION)
    download_blob(bucket, filename, destination_filename)
    mask_count += 1

image_count = 0
for filename in image_filenames:
    destination_filename = filename.split("/")[-1]
    destination_filename = os.path.join(image_path, destination_filename.split(".")[0] + IMAGE_SAVE_EXTENSION)
    download_blob(bucket, filename, destination_filename)
    image_count += 1


print(f"Finished saving {mask_count} mask captures from {FIREBASE_MASK_FOLDER} folder on Firebase Storage.")
print(f"Finished saving {image_count} image captures from {FIREBASE_IMAGE_FOLDER} folder on Firebase Storage.")


# download_blob(bucket, "vdbh-mask", "2022-01-09-14-05-34-R883")