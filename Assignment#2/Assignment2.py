## Importing Necessary Modules
import argparse
import os
from lib import student_info
from lib import imgs_utils


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
    validStudents = imgs_utils.download_images_update_students(studentInfos, outputImgDir)

    #4. Sort students based on last name
    validStudents.sort(key=lambda x: x.lastname)

    #5. Display images
    imgs_utils.plot_all_students(validStudents)





