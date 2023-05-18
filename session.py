class Session:

    def __init__(self, name, number, cap, students, time):
        self.name = name
        self.number = number
        self.cap = cap
        self.students = students
        self.time = time
    
    def getName(self): return self.name
    def getNumber(self): return self.number
    def getCap(self): return self.cap
    def getStudents(self): return self.students
    def getTime(self): return self.time

    def addStudent(self, student):
        self.students.append(student)