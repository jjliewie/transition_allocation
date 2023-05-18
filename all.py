all_sessions = []
all_students = []

sess = [[], [], []]

import csv
from session import Session
from student import Student
from itertools import permutations
from random import randint
import xlsxwriter

with open('files/caps.csv', 'r') as f:
    reader = csv.reader(f)
    for _, line in enumerate(reader):
        temp = Session(line[0].strip(), line[2], int(line[1]), [], 0)
        # print(int(line[1]))
        all_sessions.append(temp)
        if int(line[2]) == 3:
            for i in range(3): sess[i].append(Session(line[0].strip(), line[2], int(line[1]), [], i+1))
        elif int(line[2]) == 2:
            tempint = randint(0, 2)
            for i in range(3):
                if i != tempint: sess[i].append(Session(line[0].strip(), line[2], int(line[1]), [], i+1))
        else: sess[randint(0, 2)].append(Session(line[0].strip(), line[2], int(line[1]), [], randint(0, 2)+1))
f.close()

with open('files/student_info.csv', 'r') as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if i == 0: continue
        given = [line[2].strip(), line[3].strip(), line[4].strip()]
        possible = list(permutations(given))
        all_students.append(Student(line[1], line[0], line[5], possible))
f.close()

# for i in all_sessions:
#     print(i.getName())

sessNames = [[], [], []]
for i in range(len(sess)):
    for j in range(len(sess[i])):
        thisname = sess[i][j].getName()
        sessNames[i].append(thisname)

def calcOptimal(x, y, z, xcap, ycap, zcap):
    # print(x, y, z, xcap, ycap, zcap)
    if x >= xcap: 
        return float('inf')
    if y >= ycap: 
        return float('inf')
    if z >= zcap: 
        return float('inf')

    # print("checkpoint")
    return (x/xcap) + (y/ycap) + (z/zcap)

cnt = 0

for student in all_students:
    stsess = student.getSessions()
    curoptimal = float('inf')
    opsessions = stsess[0]
    for i in range(len(stsess)):
        possibility = True
        for j in range(len(stsess[i])):
            if stsess[i][j] not in sessNames[j]:
                possibility = False
                break
        if not possibility: continue

        idx1 = sessNames[0].index(stsess[i][0])
        idx2 = sessNames[1].index(stsess[i][1])
        idx3 = sessNames[2].index(stsess[i][2])

        one = len(sess[0][idx1].getStudents())
        two = len(sess[1][idx2].getStudents())
        three = len(sess[2][idx3].getStudents())

        onecap = sess[0][idx1].getCap()
        twocap = sess[1][idx2].getCap()
        threecap = sess[2][idx3].getCap()

        opvalue = calcOptimal(one, two, three, onecap, twocap, threecap)

        if opvalue < curoptimal:
            opsessions = stsess[i]
            curoptimal = opvalue

    if curoptimal > 1000: 
        cnt += 1
        continue

    idx1 = sessNames[0].index(opsessions[0])
    idx2 = sessNames[1].index(opsessions[1])
    idx3 = sessNames[2].index(opsessions[2])

    sess[0][idx1].addStudent(student)
    sess[1][idx2].addStudent(student)
    sess[2][idx3].addStudent(student)

print(cnt)

workbook = xlsxwriter.Workbook('files/result.xlsx')

for i in range(len(sess)):
    worksheet = workbook.add_worksheet("Session " + str(i+1))
    labels = sessNames[i]
    label_col = 0
    for l in labels: 
        worksheet.write(0,label_col, l)
        label_col += 5
    for j in range(len(sess[i])):
        data = []
        thisstudents = sess[i][j].getStudents()
        for st in thisstudents:
            data.append([st.getFname(), st.getLname(), st.getEmail()])
            # print([st.getFname(), st.getLname(), st.getEmail()])
        row = 1
        for d in data:
            col = (j*5)
            for dd in d:
                worksheet.write(row, col, dd)
                col += 1
            row += 1
workbook.close()