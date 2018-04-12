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

def askfor_userinfo(student_grades):
    usertype = raw_input("are you a student or a teacher ?")
    if usertype == "teacher" or usertype == "student":
        ID = (str(raw_input("Enter your ID")))
        username = raw_input("Enter your username")
        password = raw_input("Enter your Password")
        hashlibpassword = hashlib.sha224(password).hexdigest()
        return ID, username, password, hashlibpassword, usertype
    else:
        print "invalid input please select 'student' or 'teacher"
        askfor_userinfo(student_grades)


def checkforpassword(ID, username, password, hashlibpassword, student_grades):
    for key in student_grades:
        if ID == key:
            if student_grades[ID]["User"]["Password"] == hashlib.sha224(password).hexdigest() and student_grades[ID]["User"]["Username"] == username:
                return ID, username, password, hashlibpassword
            elif student_grades[ID]["User"]["Password"] != hashlib.sha224(password).hexdigest():
                print "Wrong password"
                newpassword = raw_input("Please enter your Password again")
                checkforpassword(ID, username, newpassword, hashlibpassword, student_grades)
            elif student_grades[ID]["User"]["Username"] != username:
                print "Wrong username for " + "ID number:" + str(ID)
                newusername = raw_input("Please enter your username again")
                checkforpassword(ID, newusername, password, hashlibpassword, student_grades)
    return ID, username, password, hashlibpassword

def insertorcheck(ID, gradesbreakdown, student_grades, username, password, hashlibpassword, usertype):
        if usertype == "teacher":
            ID = str(raw_input("Enter student ID"))
            for key in student_grades:
                if ID == key:
                    x = changethegrades(ID, student_grades, username, usertype)
                    return x, ID
            username = raw_input("create a username for the student")
            password = raw_input("create a password for the student")
            hashlibpassword = hashlib.sha224(password).hexdigest()
            y = insertthegrades(gradesbreakdown, ID, username, hashlibpassword)
            return y, ID
        else:
            for key in student_grades:
                if ID == key:
                    x = changethegrades(ID, student_grades, username, usertype)
                    return x, ID
            y = insertthegrades(gradesbreakdown, ID, username, hashlibpassword)
            return y, ID
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


def insertthegrades(gradesbreakdown, ID, username, hashlibpassword):
    newID = {ID:{"User":{"Username":username, "Password":hashlibpassword},"grades":{}}}
    for key in gradesbreakdown:
        print "The percentage for " + key + "  is  " + str((gradesbreakdown[key])) + "%"
        newID[ID]["grades"][key] = checknumber(key)
    return newID

def changethegrades(ID, student_grades, username, usertype):
    if student_grades[ID]["User"]["Username"] == username or usertype == "teacher":
        print "You are authorized"
        for key in student_grades[ID]["grades"]:
            print "your grade for " + str(key) + " is " + str(student_grades[ID]["grades"][key])
            x = str(raw_input("Do you want to change your grade type y for yes, n for no"))
            if x == "y":
                student_grades[ID]["grades"][key] = checknumber(key)
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
    print "Username:"+ current_grades[ID]["User"]["Username"]
    for key in current_grades[ID]["grades"]:
        print str(key) + "'s grade for " + str(current_grades[ID]["User"]["Username"])  + " is " + str(current_grades[ID]["grades"][key])
    for x in range(len(convmatrix)):
        if int(convmatrix[x]["max"]) >= int(fingrade) and int(convmatrix[x]["min"]) <= int(fingrade):
            print "Final grade is " + str(fingrade) + " Final mark is " + str(convmatrix[x]["mark"])

def saveGrades(student_grades, current_grades, ID):
    student_grades[ID] = current_grades[ID]
    file = open("students_grades.json", "w")
    file.write(json.dumps(student_grades))
    file.close()


def main():
    student_grades = loadgradesfile()
    gradesbreakdown, convmatrix = loadgc_setup()
    ID, username, password, hashlibpassword, usertype = askfor_userinfo(student_grades)
    checkforpassword(ID, username, password, hashlibpassword, student_grades)
    current_grades, ID = insertorcheck(ID, gradesbreakdown, student_grades, username, password, hashlibpassword, usertype)
    saveGrades(student_grades, current_grades, ID)
    fingrade = finalgrade(gradesbreakdown, current_grades, ID)
    printfinalgrades(convmatrix, fingrade, current_grades, ID)

main()