import json
import hashlib

def loadgc_setup():
    with open('gc_setup.json') as data_file:
        course = json.load(data_file)
    grade_breakdown = course["course_setup"]["grade_breakdown"]
    conv_matrix = course["course_setup"]["conv_matrix"]
    return grade_breakdown, conv_matrix

def loadgradesfile():
    try:
        with open('students_grades.json') as data_file:
            student_grade = json.load(data_file)
            return student_grade
    except:
        file = open('students_grades.json', "w")
        file.write("{}")
        file.close()
        with open('students_grades.json') as data_file:
            student_grade = json.load(data_file)
            return student_grade

def askfor_userinfo():
    ID = str(raw_input("Enter student ID"))
    name = raw_input("Enter your name")
    password = raw_input("Enter your Password")
    hashlibpassword = hashlib.sha224(password).hexdigest()
    return ID, name, password, hashlibpassword

def insertorcheck(ID, gradesbreakdown, student_grades, name, password, hashlibpassword):
    for key in student_grades:
        if ID == key:
            x = changethegrades(ID, student_grades, name, password)
            return x
    y = insertthegrades(gradesbreakdown, ID, name, hashlibpassword)
    return y

def checknumber(key):
    try:
        x = input("What is your Current Grade for " + key + " Please insert -1 if you don't have a grade yet")
        if x <= 100 and x >= -1:
            return x
        else:
            print "Invalid input"
            x = checknumber(key)
            return x
    except:
        print "Invalid input"
        x = checknumber(key)
        return x


def insertthegrades(gradesbreakdown, ID, name, hashlibpassword):
    newID = {ID:{"User":{"name":name, "password":hashlibpassword},"grades":{}}}
    for key in gradesbreakdown:
        print "The percentage for " + key + "  is  " + str((gradesbreakdown[key])) + "%"
        newID[ID]["grades"][key] = checknumber(key)
    return newID

def changethegrades(ID, student_grades, name, password):
    if student_grades[ID]["User"]["password"] == hashlib.sha224(password).hexdigest():
        print "You are authorized"
        for key in student_grades[ID]["grades"]:
            print "your grade for " + str(key) + " is " + str(student_grades[ID]["grades"][key])
            x = str(raw_input("Do you want to change your grade type y for yes, n for no"))
            if x == "y":
                student_grades[ID]["grades"][key] = checknumber(key)
    else:
        print "you are not authorized"
        newpassword = raw_input("Please enter your Password again")
        changethegrades(ID, student_grades, name, newpassword)
    return student_grades


def finalgrade(gradesbreakdown, current_grades, ID):
    finalgrade = 0
    for key in current_grades[ID]["grades"]:
        if current_grades[ID]["grades"][key] != -1:
            calc_grade = float(current_grades[ID]["grades"][key]) * gradesbreakdown[key] / 100
            finalgrade = finalgrade + calc_grade
    return finalgrade

def printfinalgrades(convmatrix, fingrade, current_grades, ID):
    print "ID:"+ ID
    print "Name:"+ current_grades[ID]["User"]["name"]
    for key in current_grades[ID]["grades"]:
        print "Your grade for " + str(key) + " is " + str(current_grades[ID]["grades"][key])
    for x in range(len(convmatrix)):
        if int(convmatrix[x]["max"]) >= int(fingrade) and int(convmatrix[x]["min"]) <= int(fingrade):
            print "your final grade is " + str(fingrade) + " your mark is " + str(convmatrix[x]["mark"])

def saveGrades(student_grades, current_grades, ID):
    student_grades[ID] = current_grades[ID]
    file = open("students_grades.json", "w")
    file.write(json.dumps(student_grades))
    file.close()


def main():
    student_grades = loadgradesfile()
    ID, name, password, hashlibpassword = askfor_userinfo()
    gradesbreakdown, convmatrix = loadgc_setup()
    current_grades = insertorcheck(ID, gradesbreakdown, student_grades, name, password, hashlibpassword)
    saveGrades(student_grades, current_grades, ID)
    fingrade = finalgrade(gradesbreakdown, current_grades, ID)
    printfinalgrades(convmatrix, fingrade, current_grades, ID)

main()