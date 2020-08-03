import csv 
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

def inpcsv(filename):
    fields=rows=[]
    with open(filename, 'r') as csvfile: 
        csvreader = csv.reader(csvfile) 
        fields = next(csvreader) 
        for row in csvreader: 
            rows.append(row) 
    return fields, rows


op="out.csv"
ftr, rtr=inpcsv("train.csv")

alcm=set([])
for row in rtr: 
    alcm.add(row[2])

dic1={}
dic2={}
dic3={}
for st in alcm:
    dic1.update({st: 0})
    dic2.update({st: 0})
    dic3.update({st: 0})

for row in rtr:
    dic1[row[2]]+=1
    dic2[row[2]]+=1 if(row[4]=='1') else 0


for st in dic1:
    dic3.update({st: dic2[st]/dic1[st]})

se1 =set()
se2 =set()

for st in dic3:
    if(dic3[st]>0.22):
        se2.add(st)
    else:
        se1.add(st)
    
fields1, rows1= inpcsv("test.csv")

ans=[]
id1=[]
for row in rows1:
    if(row[2] in se1 ):
        ans.append(0)
    else:
        ans.append(1)
    id1.append(row[0])


'''
What is to be done:
sort all companies by their acceptance rate and make this dimension as x1   
make rating as dimension 2 and support as dimension 3.
Run a random forest on this
'''
lst=[]
for st in dic3:
    lst.append((dic3[st], st))
lst.sort()
print(lst)

dic4={}
cnt=0
for it in lst:
    dic4.update({it[1]:cnt})
    cnt+=1
print(dic4)

fte, rte=inpcsv("test.csv") 
fra, rra=inpcsv("ratings.csv")
fso, rso=inpcsv("remarks_supp_opp.csv")



drt={}
drc={}
dso={}
dsc={}
for row in rra:
    drc.update({(row[0], row[1]):0})
    drt.update({(row[0], row[1]):0})
for row in rso:
    dsc.update({(row[0], row[1]):0})
    dso.update({(row[0], row[1]):0})

for row in rra:
    drt.update({(row[0], row[1]):drt[(row[0], row[1])]+int(row[3])})
    drc.update({(row[0], row[1]):drc[(row[0], row[1])]+1})
for row in rso:
    dso.update({(row[0], row[1]):dso[(row[0], row[1])]+(1 if row[2]=='True' else 0)})
    dsc.update({(row[0], row[1]):dsc[(row[0], row[1])]+1})


drta={}
dsoa={}
for st in drt:
    drta[st]=drt[st]/drc[st]
for st in dso:
    dsoa[st]=dso[st]/dsc[st]

drt=drta
dso=dsoa  

ind=0
for row in rte:
    if(ans[ind]==0 and (row[1], row[2]) in drt and drt[(row[1], row[2])]<2.05):
        ans[ind]=1
    elif(ans[ind]==1 and (row[1], row[2]) in dso and dso[(row[1], row[2])]<0.6):
        ans[ind]=0
    ind+=1

with open('out.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "left"])
    for i in range(len(ans)):
        writer.writerow([int(id1[i]), int(ans[i])])