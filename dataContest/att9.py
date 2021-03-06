import csv 
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.kernel_ridge import KernelRidge
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from scipy import stats as s
from sklearn.linear_model import SGDClassifier
from sklearn import preprocessing
def srtby(row):
    s=row[2]
    str=s[6:10]+s[3:5]+s[0:2]
    return str
def srtby1(row):
    s=row[4]
    str=s[6:10]+s[3:5]+s[0:2]
    return str
def rsum(dict): 
     sum = 0
     for i in dict.values(): 
           sum = sum + i 
     return sum

def inpcsv(filename):
    fields=rows=[]
    with open(filename, 'r') as csvfile: 
        csvreader = csv.reader(csvfile) 
        fields = next(csvreader) 
        for row in csvreader: 
            rows.append(row) 
    return fields, rows

ftr, rtr= inpcsv("train.csv")
fte, rte= inpcsv("test.csv")
fso, rso= inpcsv("remarks_supp_opp.csv")
fre, rre= inpcsv("remarks.csv")
frt ,rrt= inpcsv("ratings.csv")

#Here we create a mapping from each company to a score the larger the score the liklier thata person will leave
dc={}
ds={}
dav={}
y ={}
for row in rtr:
    y.update({(row[1],row[2]):row[4]})
    dc.update({row[2]: 0})
    ds.update({row[2]: 0})
    dav.update({row[2]: 0})
for row in rtr:
    dc[row[2]]+=1
    ds[row[2]]+=1 if(row[4]=='1') else 0
for st in dc:
    dav.update({st: ds[st]/dc[st]})
lst=[]
for st in dav:
    lst.append((dav[st], st))
lst.sort()

dic_com_ind={}
for ind,it in enumerate(lst):
    dic_com_ind.update({it[1]:ind})


#We make three features average rating, count of rating and most recent rating 
rrt.sort(key=srtby)
lrt={}
art={}
crt={}
mnrt={}
mxrt={}
srt={}
trt={}
mdrt={}
for row in rrt:
    lrt[row[0],row[1]]=0
    art[row[0],row[1]]=0
    crt[row[0],row[1]]=0
    mxrt[row[0],row[1]]=0
    mnrt[row[0],row[1]]=5
    mdrt[row[0],row[1]]=0
    srt[row[0],row[1]]=0
    trt[row[0],row[1]]=[]

for row in rrt:
    lrt[row[0],row[1]]=int(row[3])
    crt[row[0],row[1]]+=1
    art[row[0],row[1]]+=int(row[3])
    mnrt[row[0],row[1]]=min(int(row[3]), mnrt[row[0],row[1]])
    mxrt[row[0],row[1]]=max(int(row[3]), mxrt[row[0],row[1]])
    srt[row[0],row[1]]+=int(row[3])*int(row[3])
    trt[row[0],row[1]].append(int(row[3]))

for it in crt:
    art[it]=art[it]/crt[it]
for it in crt:
    srt[it]=(srt[it]/crt[it] - art[it]**2)
for it in crt:
    mdrt[it]=s.mode(trt[it])[0]

# remarkID = {}
# for row in rre:
#     remarkID[row[2]] = 1
# cr = 0
# cf = 0
# for row in rso:
#     cr+=1
#     if row[4] not in remarkID:
#         cf +=1
# print(cr, cf)

lre={}
are={}
cre={}
rre.sort(key=srtby1)
reid = {}
for row in rre:
    lre[row[0],row[1]]=0
    are[row[0],row[1]]=0
    cre[row[0],row[1]]=0
    reid[row[2]] = (row[0], row[1])
for row in rre:
    lre[row[0],row[1]]=len(row[3])
    cre[row[0],row[1]]+=1
    are[row[0],row[1]]+=len(row[3])
for it in cre:
    are[it]=are[it]/cre[it]


aso={}
cso={}
cof = {}
aof = {}
alof = {}
clof = {}
for row in rso:
    aso[row[0],row[1]]=0
    cso[row[0],row[1]]=0
    if row[4] in reid:
        cof[reid[row[4]]] = 0
        aof[reid[row[4]]] = 0
        alof[reid[row[4]]] = 0
        clof[reid[row[4]]] = 0
for row in rso:
    aso[row[0],row[1]]+=1 if row[2]=="True" else 0
    cso[row[0],row[1]]+=1
    if row[4] in reid:
        if (row[0], row[1]) in y: 
            if row[2] == "True":
                alof[reid[row[4]]] += int(y[row[0], row[1]])
            clof[reid[row[4]]] += int(y[row[0], row[1]])
        cof[reid[row[4]]] += 1
        aof[reid[row[4]]]+=1 if row[2]=="True" else 0
for it in cso:
    aso[it]=aso[it]/cso[it]

for it in cof:
    aof[it] = aof[it] / cof[it]

for it in clof:
    if clof[it] != 0:
        alof[it] = alof[it] / clof[it]





# [2045, 1318]
# [147, 20]
# Total number of people who stayed, number of people who left and had NO opinion about their remark
# total number of people who left, number of people who left who did not have an opinion on their remark



avg_mnrt=rsum(mnrt)/len(mnrt)
avg_mxrt=rsum(mxrt)/len(mxrt)
avg_mdrt=rsum(mdrt)/len(mdrt)
avg_lre=rsum(lre)/len(lre)
avg_are=rsum(are)/len(are)
avg_cre=rsum(cre)/len(cre)
avg_aso=rsum(aso)/len(aso)
avg_cso=rsum(cso)/len(cso)
avg_lrt=rsum(lrt)/len(lrt)
avg_art=rsum(art)/len(art)
avg_crt=rsum(crt)/len(crt)
avg_srt=rsum(srt)/len(srt)
avg_alof = rsum(aof)/len(alof)
avg_clof = rsum(cof)/len(clof)
trX=np.ndarray(shape=(len(rtr), 15))
trY=np.zeros((len(rtr),))

ind=0
for row in rtr:
    em=row[1]
    co=row[2]
    trX[ind][0]=dic_com_ind[co]
    trX[ind][1]=(int)(row[3][6:10])
    trX[ind][2]=avg_lrt
    trX[ind][3]=avg_art
    trX[ind][4]=avg_crt 
    trX[ind][5]=avg_lre
    trX[ind][6]=avg_are
    trX[ind][7]=avg_cre
    trX[ind][8]=avg_aso
    trX[ind][9]=avg_cso
    trX[ind][10]=avg_mnrt
    trX[ind][11]=avg_mxrt
    trX[ind][12]=avg_srt
    trX[ind][13] = avg_alof
    trX[ind][14] = avg_clof
    
    p=(em,co)
    if(p in lrt):
        trX[ind][2]=lrt[p]
    if(p in art):
        trX[ind][3]=art[p]
    if(p in crt):
        trX[ind][4]=crt[p]
    if(p in lre):
        trX[ind][5]=lre[p]
    if(p in are):
        trX[ind][6]=are[p]
    if(p in cre):
        trX[ind][7]=cre[p]
    if(p in aso):
        trX[ind][8]=aso[p]
    if(p in cso):
        trX[ind][9]=cso[p]
    if (p in mnrt):
        trX[ind][10]=mnrt[p]
    if (p in mxrt):
        trX[ind][11]=mxrt[p]
    if(p in srt):
        trX[ind][12]=srt[p]
    if(p in alof):
        trX[ind][13] = alof[p]
    if(p in clof):
        trX[ind][14] = clof[p]
        
    trY[ind]=row[4]
    ind+=1
scaler = preprocessing.StandardScaler().fit(trX)
m1=RandomForestClassifier(n_estimators=201)
m2=AdaBoostClassifier(n_estimators=101, learning_rate=0.5)
m3=GaussianNB()
m4=KNeighborsClassifier(n_neighbors=5)
m6=DecisionTreeClassifier(min_samples_split=3)
m7=GradientBoostingClassifier()
m8=svm.SVC(kernel='rbf', max_iter=200, probability=True)
m9=SGDClassifier(max_iter=20, loss='log')

trX=scaler.transform(trX)
m1.fit(trX, trY)
m2.fit(trX, trY)
m3.fit(trX, trY)
m4.fit(trX, trY)
m6.fit(trX, trY)
m7.fit(trX, trY)
m8.fit(trX, trY)
m9.fit(trX, trY)

id1=[]
ind=0
teX=np.ndarray(shape=(len(rte),15))
a5=np.zeros(len(rte))
for row in rte:
    id1.append(row[0])
    em=row[1]
    co=row[2]
    teX[ind][0]=dic_com_ind[co]
    teX[ind][1]=(int)(row[3][6:10])
    teX[ind][2]=avg_lrt
    teX[ind][3]=avg_art
    teX[ind][4]=avg_crt
    teX[ind][5]=avg_lre
    teX[ind][6]=avg_are
    teX[ind][7]=avg_cre
    teX[ind][8]=avg_aso
    teX[ind][9]=avg_cso
    teX[ind][10]=avg_mnrt
    teX[ind][11]=avg_mxrt
    teX[ind][12]=avg_crt
    teX[ind][13] = avg_alof
    teX[ind][14] = avg_clof
    
    p=(em,co)
    if(p in lrt):
        teX[ind][2]=lrt[p]
    if(p in art):
        teX[ind][3]=art[p]
    if(p in crt):
        teX[ind][4]=crt[p]
    if(p in lre):
        teX[ind][5]=lre[p]
    if(p in are):
        teX[ind][6]=are[p]
    if(p in cre):
        teX[ind][7]=cre[p]
    if(p in aso):
        teX[ind][8]=aso[p]
    if(p in cso):
        teX[ind][9]=cso[p]
    if (p in mnrt):
        teX[ind][10]=mnrt[p]
    if (p in mxrt):
        teX[ind][11]=mxrt[p]
    if(p in srt):
        teX[ind][12]=srt[p]
    if(p in alof):
        teX[ind][13] = alof[p]
    if(p in clof):
        teX[ind][14] = clof[p]
    if(dav[co]<0.25):
        a5[ind]=1
    ind+=1

teX=scaler.transform(teX)
a1=m1.predict_proba(teX)
a2=m2.predict_proba(teX)
a3=m3.predict_proba(teX)
a4=m4.predict_proba(teX)
a6=m6.predict_proba(teX)
a7=m7.predict_proba(teX)
a8=m8.predict_proba(teX)
a9=m9.predict_proba(teX)

ans=a1*2+a2*2+a3+a4+a6+a7*2+a8
temp=[]
for i in range(len(ans)):
    temp.append((ans[i][0]+a5[i]) / 11)
temp.sort()
thr=temp[int(len(ans)*0.187)]
print(thr)
print(temp)
# ans=[]
# for i in range(len(a1)):
#     if(a1[i]+a2[i]+a3[i]+a4[i]+a5[i]>=2):
#         ans.append(1)
#     else:
#         ans.append(0)

with open('test_pj.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["id", "left"])
    for i in range(len(ans)):
        hld=1
        if((ans[i][0]+a5[i])/11>=thr):
            hld=0
        writer.writerow([int(id1[i]), hld])
git
a, b = inpcsv('test_pj1.csv')
c, d = inpcsv('test_pj.csv')

ct = 0
cc = 0
for i in range(len(b)):
    #print(b[i][1], d[i][1])
    if b[i][1] == '1' and d[i][1] == '0':
        ct += 1
    elif d[i][1] == '1' and b[i][1] == '0':
        cc += 1

print(ct, cc)
