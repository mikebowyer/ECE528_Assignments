## Importing Necessary Modules
import requests # to get image from the web
import shutil # to save it locally
import argparse
from lib import student_info


parser = argparse.ArgumentParser(description='Read in student list csv file, then plot all head shots with names')
parser.add_argument('--student-list', help='path to student list')
parser.add_argument('--output-image-dir', help='Where to save images')

if __name__ == '__main__':
    #1. Grab argument of location of image, and master information csv
    args = parser.parse_args()
    studentListFilePath = args.student_list
    outputImgDir = args.output_image_dir
    print("Input student information file: {}".format(studentListFilePath))
    print("Saving downloaded images to: {}".format(outputImgDir))

    #2. Read in csv file
    student_info.Students(studentListFilePath)


    #3. Download Images locally

    #4.
    ## Set up the image URL and filename
    image_url = "https://sites.google.com/a/umich.edu/mbowyer/courseartefacts/BowyerHeadshot_150x150.PNG"
    filename = image_url.split("/")[-1]

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')



