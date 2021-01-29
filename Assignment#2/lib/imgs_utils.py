import requests  # to get image from the web
import shutil  # to save it locally
import os, math
import matplotlib.pyplot as plt
import cv2


def download_images_update_students(studentInfo, outputImgDir):
    #Delete all existing files in output dir
    filelist = [f for f in os.listdir(outputImgDir)]
    for f in filelist:
        os.remove(os.path.join(outputImgDir, f))

    validStudentList = []
    for i, student in enumerate(studentInfo.students):

        # check if file name already exists in outputImgDir
        image_url = student.imgUrl
        filename = image_url.split("/")[-1]
        filepath = os.path.join(outputImgDir, filename)
        if os.path.exists(filepath):
            print("Image name for {} {} already exists, renaming".format(student.firstname, student.lastname))
            filename = student.firstname + "_" + student.lastname + "_" + filename
            filepath = os.path.join(outputImgDir, filename)
            student.imgPath = filepath

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(image_url, stream=True)
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(filepath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Image for {} {} sucessfully Downloaded: {}'.format(student.firstname, student.lastname, filename))
            student.imgPath = filepath
            validStudentList.append(student)
        else:
            print("ERROR: Image for {} {} couldn't be retrieved.".format(student.firstname, student.lastname, filename))
    return validStudentList

def plot_all_students(validStudents):
    numStudents = len(validStudents)
    numRowsCols = math.ceil(math.sqrt(numStudents))

    fig = plt.figure()
    plt.cla()
    plt.clf()
    i = 1
    for student in validStudents:
        # plt.subplot(numRowsCols, numRowsCols, i)
        img = plt.imread(validStudents[i-1].imgPath)
        ax = fig.add_subplot(numRowsCols + 1, numRowsCols, i)
        ax.set_axis_off()
        ax.text(75, 170, str(student.firstname +" "+ student.lastname),
                fontsize=6, ha='center')
        ax.imshow(img)
        i += 1

    fig.show()
    fig.savefig('students.png')

def runFacialDetection(validStudents):

    faceCascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")

    for student in validStudents:
        image = cv2.imread(student.imgPath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        print("Found {0} faces!".format(len(faces)))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Faces found", image)
        cv2.waitKey(0)
