from em import EMCrowdSource
import csv
def createData():
    #test data
    #20 data points, 4 annotatorrs
    x =[[] for i in range(20)]
    x[0] = [1, 0, 1, 1]
    x[1] = [0, 0, 0, 1]
    x[2] = [0, 1, 0, 1]
    x[3] = [0, 0, 1, 1]
    x[4] = [0, 0, 1, 1]
    x[5] = [0, 0 , 1, 0]
    x[6] = list(x[1])
    x[7] = list(x[3])
    x[8] = list(x[1])
    x[9] = list(x[1])
    x[10] = [1, 1, 1, 0]
    x[11] = [1, 1, 0, 0]
    x[12] = list(x[10])
    x[13] = [1, 1, 0, 1]
    x[14] = [1, 0, 1, 0]
    x[15] = [1, 1, 1, 0]
    x[16] = [0, 1, 0, 0]
    x[17] = [1, 1, 0, 0]
    x[18] = [1, 1, 1, 0]
    x[19] = [1, 1, 0, 0]
    with open('test.csv', 'w', newline='') as csvfile:
        datawriter = csv.writer(csvfile)
        for row in x:
            datawriter.writerow(row)

createData()

a = EMCrowdSource()
a.readData("test.csv")
a.initialise(a = 0.5, u = [0.1] * 4)
a.runAlgorithm(10)


#Try runnning the above for various initial parameters
#As the data follows the probabilistic model assumed,
#it is almost entirely insensitive to initial parameter choice.
#However, it will fail at a = 0.5, u = [0.5] * 4 as it cannot
#trust the data at all