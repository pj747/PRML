import csv 

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
    #print(dic3[st])     
    if(dic3[st]>0.2):
        se2.add(st)
    else:
        se1.add(st)
    
fte, rte=inpcsv("test.csv") 

ans=[]
id1=[]
for row in rte:
    if(row[2] in se1):
        ans.append(0)
    else:
        ans.append(1)
    id1.append(row[0])

fra, rra=inpcsv("ratings.csv")
fso, rso=inpcsv("remarks_supp_opp.csv")

drt={}
dso={}
for row in rra:
    drt.update({(row[0], row[1]):int(row[3])-1})
#print(fso)
for row in rso:
    dso.update({(row[0], row[1]):1 if row[2]=='True' else 0})

print(ftr)
r1=[0,0,0,0]
rt=[0,0,0,0]
s1=[0,0]
st=[0,0]
for row in rtr:
    emp=row[1]
    com=row[2]
    res=row[4]
    p=(emp, com)
    if(p in drt):
        rt[drt[p]]+=1
        if(res=='1'):
            r1[drt[p]]+=1
    if(p in dso):
        st[dso[p]]+=1
        if(res=='1'):
            s1[dso[p]]+=1
        
# print(r1)
# print(s1)
# print(rt)
# print(st)


for ind in range(len(rte)):
    row=rte[ind]
    emp=row[1]
    com=row[2]
    p=(emp, com)
    if(p in drt and drt[p]==1):
        ans[ind]=1
    if(p in dso and dso[p]==0):
        ans[ind]=0


with open('out.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "left"])
    for i in range(len(ans)):
        writer.writerow([id1[i], ans[i]])        
