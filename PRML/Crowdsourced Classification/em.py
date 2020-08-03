'''
EM API for a crowd-sourcing problem with specifications as follows:
Assume there are d annotators, and n data points in one of two categories (binary classes)
The probability of error is parameterised for each annotator
given by a real number , i.e, P(X_ij = 1 | Z_i = 0) = P(X_ij = 0| Z_i = 1) = u_j
Assume that the true label is parameterised by P(Z_i = 1) = a. Our aim is to find the true label
distribution, and also mismatch error for each annotator.
'''
import csv 

class EMCrowdSource:

    def __init__(self, n = 1, d = 1):
        self.n = n
        self.d = d
        self.q = [0] * n
        self.u = [0] * d
        self.a = 0.5

    def readData(self, source):
        rows = []
        with open(source, 'r') as csvfile: 
            csvreader = csv.reader(csvfile) 
            for row in csvreader: 
                rows.append([int(i) for i in row]) 
        self.x = rows
        print(self.x)
        self.n = len(rows)
        self.d = len(rows[0])
        self.q = [0] * self.n
        self.u = [0] * self.d
    
    @staticmethod
    def product(seq):
        ans = 1
        for i in seq:
            ans *= i
        return ans

    def __E(self):
        for i in range(self.n):
            p1 = self.a * EMCrowdSource.product([self.u[j] * (1- self.x[i][j]) + (1 - self.u[j])*(self.x[i][j]) for j in range(self.d)])
            p0 = (1 - self.a) * EMCrowdSource.product([(1 - self.u[j]) * (1- self.x[i][j]) + (self.u[j])*(self.x[i][j]) for j in range(self.d)])
            self.q[i] = p1/(p1 + p0)
        
    def __M(self):
        self.a = sum(self.q)/self.n
        for j in range(self.d):
            self.u[j] = sum([self.q[i] * (1 - self.x[i][j]) + (1 - self.q[i]) * (self.x[i][j]) for i in range(self.n)])/self.n

    def initialise(self, a = 0.5, u = []):
        if len(u) == 0:
            self.u = [0.4] * self.d
        else:
            self.a = a
            self.u = u

    def singleStep(self, e = True, m = True):
        self.__E()
        self.__M()
        if e:
            print("E step:")
            print("The values of gamma in order")
            for i in self.q:
                print("%.3f" %i , end = " | ")
            print()
            print()
        if m:
            print("M step:")
            print("a = %.3f" %self.a)
            print("The values of u in order")
            for i in self.u:
                print("%.3f" %i , end = " | ")
            print()
            print()
    
    def runAlgorithm(self, num_iter = 10, e= True, m=True):
        for i in range(num_iter):
            print("Iteration number: ", i + 1)
            print()
            self.singleStep(e, m)
