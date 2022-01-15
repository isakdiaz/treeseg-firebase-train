#!/usr/bin/env bash
python read-firestore.py && python draw-coordinate-masks.py && python read-firebase-storage.py
