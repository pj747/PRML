import csv 

filename = "train.csv"
filename1 = "test.csv"
op="out.csv"
fields = [] 
rows = [] 
with open(filename, 'r') as csvfile: 
	csvreader = csv.reader(csvfile) 
	fields = next(csvreader) 
	for row in csvreader: 
		rows.append(row) 
alcm=set([])
for row in rows: 
    alcm.add(row[2])
dic1={}
dic2={}
dic3={}
for st in alcm:
    dic1.update({st: 0})
    dic2.update({st: 0})
    dic3.update({st: 0})

for row in rows:
    dic1[row[2]]+=1
    dic2[row[2]]+=1 if(row[4]=='1') else 0
# print(dic1, dic2)


for st in dic1:
    dic3.update({st: dic2[st]/dic1[st]})
print(dic3)
se1 =set()
se2 =set()

for st in dic3:
    if(dic3[st]>0.2):
        se2.add(st)
    else:
        se1.add(st)
    

fields1 = [] 
rows1 = [] 
with open(filename1, 'r') as csvfile: 
	csvreader = csv.reader(csvfile) 
	fields1 = next(csvreader) 
	for row in csvreader: 
		rows1.append(row)

ans=[]
id1=[]
for row in rows1:
    if(row[2] in se1 ):
        ans.append(0)
    else:
        ans.append(1)
    id1.append(row[0])

with open('out.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "left"])
    for i in range(len(ans)):
        writer.writerow([id1[i], ans[i]])
