class Student: 

    def __init__(self, fname, lname, email, sessions):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.sessions = sessions
    
    def getFname(self):
        return self.fname
    
    def getLname(self):
        return self.lname
    
    def getEmail(self):
        return self.email
    
    def getSessions(self):
        return self.sessions