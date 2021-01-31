## Importing Necessary Modules
import argparse
import os
from lib import student_info
from lib import imgs_utils



parser = argparse.ArgumentParser(description='Read in student list csv file, then plot all head shots with names. Optionally run facial detection.')
parser.add_argument('--student-list', help='Path to student list')
parser.add_argument('--output-image-dir', help='Path to directory where to save output student matrix image')
parser.add_argument('-fd','--run-face-detection',action='store_true', help='Set when you want to run facial detection for each student image')

if __name__ == '__main__':
    #1. Grab argument of location of image, and master information csv
    print("INFO: Parsing input arguments")
    args = parser.parse_args()
    studentListFilePath = args.student_list
    outputImgDir = args.output_image_dir
    if not os.path.exists(outputImgDir):
        os.makedirs(outputImgDir)
    print("INFO: Input student information file: {}".format(studentListFilePath))
    print("INFO: Saving downloaded images to: {}".format(outputImgDir))

    #2. Read in csv file
    print("INFO: Reading in student information")
    studentInfos = student_info.Students(studentListFilePath)

    #3. Download Images and update students image file path
    print("INFO: Downloading student images locally")
    validStudents = imgs_utils.download_images_update_students(studentInfos, outputImgDir)

    #4. Sort students based on last name
    print("INFO: Sorting students by last name")
    validStudents.sort(key=lambda x: x.lastname)

    #5. Display images
    print("INFO: Generating matrix of student images")
    imgs_utils.plot_all_students(validStudents)

    if(args.run_face_detection):
        print("INFO: Running facial detection on each student image")
        imgs_utils.runFacialDetection(validStudents)





