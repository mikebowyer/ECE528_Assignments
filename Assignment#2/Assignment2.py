## Importing Necessary Modules
import argparse
import os
from lib import student_info
from lib import download_imgs


parser = argparse.ArgumentParser(description='Read in student list csv file, then plot all head shots with names')
parser.add_argument('--student-list', help='path to student list')
parser.add_argument('--output-image-dir', help='Where to save images')

if __name__ == '__main__':
    #1. Grab argument of location of image, and master information csv
    args = parser.parse_args()
    studentListFilePath = args.student_list
    outputImgDir = args.output_image_dir
    if not os.path.exists(outputImgDir):
        os.makedirs(outputImgDir)
    print("Input student information file: {}".format(studentListFilePath))
    print("Saving downloaded images to: {}".format(outputImgDir))

    #2. Read in csv file
    studentInfos = student_info.Students(studentListFilePath)

    #3. Download Images and update students image file path
    download_imgs.download_images_update_students(studentInfos, outputImgDir)

    print("Hello world!")





