import requests  # to get image from the web
import shutil  # to save it locally
import os


def download_images_update_students(studentInfo, outputImgDir):
    returnval = False
    for student in studentInfo.students:

        # check if file name already exists in outputImgDir
        image_url = student.imgUrl
        filename = image_url.split("/")[-1]
        filepath = os.path.join(outputImgDir, filename)
        if os.path.exists(filepath):
            print("Image for {} {} already exists, skipping".format(student.firstname, student.lastname))
            continue

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(filepath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Image for {} {} sucessfully Downloaded: {}'.format(student.firstname, student.lastname, filename))
            returnval=True
            student.imgPath = filepath
        else:
            print("ERROR: Image for {} {} couldn't be retrieved.".format(student.firstname, student.lastname, filename))
            returnval = False
            break
    return returnval
