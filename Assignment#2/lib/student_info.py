import csv


class Students:
    def __init__(self, studentInfoFilePath):
        self.studentInfoFilePath = studentInfoFilePath
        self.students = []
        self.read_in_student_info()

    def read_in_student_info(self):
        file = csv.reader(open(self.studentInfoFilePath), delimiter=',')
        for line in file:
            print(line)


class Student:
    def __init__(self, lastname, firstname, url):
        self.lastname = lastname
        self.firstname = firstname
        self.imgUrl = url
        self.imgPath = ""
