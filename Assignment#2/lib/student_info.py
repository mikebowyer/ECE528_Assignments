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
            newStudent = Student(line)
            self.students.append(newStudent)


class Student:
    def __init__(self, studentInfo):
        self.lastname = studentInfo[0]
        self.firstname = studentInfo[1]
        self.imgUrl = studentInfo[2]
        self.imgPath = ""
