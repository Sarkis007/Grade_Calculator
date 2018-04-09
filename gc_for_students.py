import json

def loadgradesbreakdown():
    with open('gc_setup.json') as data_file:
        course = json.load(data_file)
    grade_breakdown = course["course_setup"]["grade_breakdown"]
    return grade_breakdown

def loadconvmatrix():
    with open('gc_setup.json') as data_file1:
        conv_matrix = json.load(data_file1)["course_setup"]["conv_matrix"]
    return conv_matrix

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

def askforID():
    ID = str(raw_input("Enter student ID"))
    return ID

def checkifIDexist(student_grades, ID):
    for key in student_grades:
        if ID == key:
            return 1
    return 0

def insertthegrades(gradesbreakdown, studentID):
    newID = {studentID:{}}
    for key in gradesbreakdown:
        print "The percentage for " + key + "  is  " + str((gradesbreakdown[key])) + "%"
        try:
            newID[studentID][key] = input("What is your Current Grade for " + key + " Please insert -1 if you don't have a grade yet")
        except:
            newID[studentID][key] = input("invaild input for  " + key + " Please insert a number between 0 and 100, insert -1 if you don't have a grade yet")
        while newID[studentID][key] > 100 or newID[studentID][key] < -1:
            newID[studentID][key] = input("invaild input for  " + key + " Please insert a number between 0 and 100, insert -1 if you don't have a grade yet")
    return newID

def changethegrades(studentID, student_grades):
    for key in student_grades[studentID]:
        print "your grade for " + str(key) + " is " + str(student_grades[studentID][key])
        x = str(raw_input("Do you want to change your grade type y for yes, n for no"))
        if x == "y":
            try:
                student_grades[studentID][key] = input("What is your Current Grade for: " + key)
            except:
                student_grades[studentID][key] = input("invaild input for  " + key + " Please insert a number between 0 and 100, insert -1 if you don't have a grade yet")
            while student_grades[studentID][key] > 100 or student_grades[studentID][key] < -1:
                student_grades[studentID][key] = input("invaild input for  " + key + " Please insert a number between 0 and 100, insert -1 if you don't have a grade yet")
    return student_grades

def insertorcheck(checkifIDexist, ID, gradesbreakdown, student_grades):
        if checkifIDexist == True:
            x = changethegrades(ID, student_grades)
            return x
        elif checkifIDexist == False:
            y = insertthegrades(gradesbreakdown, ID)
            return y

def saveGrades(student_grades, current_grades, ID):
    student_grades[ID] = current_grades[ID]
    print "Your grades are: " + (json.dumps(student_grades[ID]))
    file = open("students_grades.json", "w")
    file.write(json.dumps(student_grades))
    file.close()

def finalgrade(gradesbreakdown, current_grades, studentID):
    finalgrade = 0
    for key in current_grades[studentID]:
        if current_grades[studentID][key] != -1:
            calc_grade = int(current_grades[studentID][key]) * gradesbreakdown[key] / 100
            finalgrade = finalgrade + calc_grade
    return finalgrade

def printgradeasletter(convmatrix, Current_Grade):
    for x in range(len(convmatrix)):
        if int(convmatrix[x]["max"]) >= int(Current_Grade) and int(convmatrix[x]["min"]) <= int(Current_Grade):

            print "your grade is " + str(Current_Grade) + " your mark is " + str(convmatrix[x]["mark"])

def main():
    student_grades = loadgradesfile()
    ID = askforID()
    gradesbreakdown = loadgradesbreakdown()
    convmatrix = loadconvmatrix()
    checkifexist = checkifIDexist(student_grades, ID)
    current_grades = insertorcheck(checkifexist, ID, gradesbreakdown, student_grades)
    saveGrades(student_grades, current_grades, ID)
    fingrade = finalgrade(gradesbreakdown, current_grades, ID)
    printgradeasletter(convmatrix, fingrade)

main()