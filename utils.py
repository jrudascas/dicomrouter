from os.path import join
import os


def decryption(hash, key):
    return hash


def find_dicom_images(folder_path):
    dicom_files = []
    for (root, dirs, files) in os.walk(folder_path):
        for file in files:
            dicom_files.append(join(root, file))

    return dicom_files
