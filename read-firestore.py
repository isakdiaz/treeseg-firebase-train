import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
import pickle
import pandas as pd


def write_dictionary(filename, dictionary):
    f = open(filename, "wb")
    # create a binary pickle file

    # write the python object (dict) to pickle file
    pickle.dump(dictionary, f)
    # close file
    f.close()

    print(f"Pickle file {filename} written from firebase database with {len(dictionary.keys())} entries.")


if __name__ == "__main__":
    # Place credentials in same folder and change variable
    FIREBASE_CREDENTIALS_PATH = "credentials/biome-app-2-firebase-adminsdk-soxoo-b3f1bf7e27.json"
    MASK_COORDINATE_FOLDER = "mask-coordinates"
    OUTPUT_PATH = "firebase-db.pkl"

    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)

    db = firestore.client()  # this connects to our Firestore database
    # collection = db.collection("mask-coordinates").document("magnolia-grandiflora").collection("2022-01-09-17-47-31-R268")  # opens 'diameter-measurements' collection
    #
    results = np.empty((0,3), float)
    # results = [[1,2,3]]

    firebaseDB = dict()

    # LIST SPECIES (species name not used in masks)
    for document in (db.collection(MASK_COORDINATE_FOLDER).list_documents()):
        # LIST SNAPSHOTS
        #print(document.id)
        for collect in document.collections():
            collectId = collect.id
            # print(type(collectId))
            # LIST SELECTIONS
            for final_doc in (collect.get()):
                firebaseDB[collectId] = firebaseDB.get(collectId, []) + [final_doc.to_dict()]
                # print(firebaseDB)

    print(f"Finished writing mask coordinate database from {MASK_COORDINATE_FOLDER} to Pickle File: {OUTPUT_PATH}")
    # print(firebaseDB)
    write_dictionary(OUTPUT_PATH, firebaseDB)


