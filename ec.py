from flask import Flask, render_template, request
import pickle
import numpy as np
import datetime
import random
from datetime import date
import pandas as pd

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("test.html")

def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,8)
    to_predict1 = loaded_model1.transform(to_predict)
    result = loaded_model.predict(to_predict1)
    return result[0]

@app.route('/aicalculatorresult',methods = ['POST'])
def aicalculatorresult():
    prediction=''
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
       


        
     
        df=pd.read_excel('/Users/lota/Downloads/Demo自動配對.xlsx')
        df = df.drop(df.columns[[ 7,8,9,10,11,12,13,14,15,16,17,18,19 ]], axis=1)
        df=df.loc[df['失效日期'].dt.date>=date.today()]
        df.派單上限=df.派單上限.fillna(10)
        df.預算上限=df.預算上限.fillna(20)
        df['超標']=df['派單上限']-df['9月派單']
        df=df.where(df['超標']>0)
        df=df.dropna()
        df3=df
        df = df.drop(df.columns[[0,8]], axis=1)
        df=pd.get_dummies(df,columns=['預算上限','風格'])
        pp=0
        for i in df['預算上限_40']:
            if i==1:
                    df['預算上限_20'][df.index[pp]]=df['預算上限_20'][df.index[pp]]+1
            pp+=1
        pp=0
        for i in df['預算上限_50']:
            if i==1:
                    df['預算上限_20'][df.index[pp]]=df['預算上限_20'][df.index[pp]]+1
                    df['預算上限_40'][df.index[pp]]=df['預算上限_40'][df.index[pp]]+1
            pp+=1
        customer=pd.DataFrame([[str(to_predict_list['z1']),str(to_predict_list['z2']),str(to_predict_list['z3']),str(to_predict_list['z4'])]], columns=['名字', '預算上限', '風格','裝修/設計'],index=[1000])
        customer=customer.drop(customer.columns[[0]], axis=1)
        zz=pd.get_dummies(customer,columns=['預算上限','風格'])
        df=df.append(zz)
        df=df.drop(df.columns[[2,3]], axis=1)
        df=df.fillna(0)
        num=df.index[-1]
        if df['預算上限_40'][num]==1:
            df['預算上限_20'][num]=df['預算上限_20'][num]+1
        if df.iloc[df.shape[0]-1,:]['預算上限_50']==1:
            df['預算上限_20'][num]=df['預算上限_20'][num]+1
            df['預算上限_40'][num]=df['預算上限_40'][num]+1
        df=df.where(df['裝修/設計']==df['裝修/設計'][1000])
        df=df.dropna()
        df3=df
        df = df.drop(df.columns[[1,2]], axis=1)
        cha=['預算上限_20', '預算上限_40', '預算上限_50', '預算上限_50-100', '風格_古典風',
            '風格_現代風']
        cc=1
        ca=0
        big=[]
        finalrow=df.shape[0]-1
        for e in range(6):
            z=0
            ind=[]
            if df.iloc[finalrow,:][cc]==1:
                for i in df.iloc[0:finalrow,:][cha[ca]]:
                    if i==df.iloc[finalrow,:][cc]:
                        ind.append(z)
                        
                    z+=1
                big.append(ind)
            cc+=1
            ca+=1
        import itertools
        v=set.intersection(set(big[0]),*itertools.islice(big,1,None))
        cnn=1
        for i in list(v):
            if cnn!=4:
                
                cnn+=1
            else:
                break
        df3['neworder']=list(range(df3.shape[0]))
        df3=df3.set_index('neworder')
        cq=df3['評分'].to_dict()
        ra={}
        for i in list(v):
            q={i:cq[i]}
            ra.update(q)
        finallist={k: v for k, v in sorted(ra.items(), key=lambda item: item[1],reverse=True)}
        newv=list(finallist.keys())[0:3]
        cnn=1
        com=[]
        for i in newv:
            if cnn!=4:
                com.append(df.iloc[i,:][0])
                cnn+=1
            else:
                break
        try:
            c1=com[0]
        except:
            c1='沒有匹配'
        try:
            c2=com[1]
        except:
            c2='沒有匹配'
        try:
            c3=com[2]
        except:
            c3='沒有匹配'
        
        from keras.preprocessing import image

        a='YBJ'
        image_path="/Users/lota/Downloads/c21/static/{}.jpg".format(a)
        img = image.load_img(image_path)

        return render_template("aicalculatorresult.html",com=com,c1=c1,c2=c2,c3=c3,img=img)

@app.route("/aicalculator", methods=['POST','GET'])
def aicalculator():
        return render_template('aicalculator.html')

@app.route("/test", methods=['POST','GET'])
def test():

        return render_template('test.html')
@app.route("/result", methods=['POST','GET'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        name=to_predict_list['userame']
        place=to_predict_list['place']
        budget=to_predict_list['budget']
        consider=to_predict_list['consider']
        favour=to_predict_list['favour']
        ft=str(to_predict_list['userame'])+'正在'+str(to_predict_list['place'])+'尋找一所樓盤，樓盤中的'+str(to_predict_list['consider'])+'對他來說非常重要。'
        if str(to_predict_list['place'])=='九龍':
    
            g2=random.choice([2,3]) 
            if g2==2:
                a1='彩明苑'
            else:
                a1='富澤花園'
            g3=random.choice([5,6]) 
            if g3==5:
                a2='新峰花園'
            else:
                a2='麗港城'
            g4=random.choice([8,9]) 
            if g4==8:
                a3='帝景臺'
            else:
                a3='康柏苑'
        elif str(to_predict_list['place'])=='新界':
        
            g2=random.choice([11,12])
            if g2==11:
                a1='大興花園'
            else:
                a1='沙田第一城' 
            g3=random.choice([14,15])
            if g3==14:
                a2='荃灣中心'
            else:
                a2='瓊華樓' 
            g4=random.choice([17,18]) 
            if g4==17:
                a3='栢慧豪園'
            else:
                a3='翠濤閣'
        elif str(to_predict_list['place'])=='香港島':
            
            g2=random.choice([4,7])
            if g2==4:
                a1='白居二'
            else:
                a1='康山花園'  
            g3=random.choice([10,13]) 
            if g3==10:
                a2='年豐大廈'
            else:
                a2='民新大廈' 
            g4=random.choice([16,19]) 
            if g4==16:
                a3='南里壹號'
            else:
                a3='丹拿花園'
    
        return render_template('result.html',name=name,place=place,budget=budget,consider=consider,favour=favour,ft=ft,g2=g2,g3=g3,g4=g4,a2=a2,a3=a3,a1=a1)

@app.route('/',methods = ['POST'])
def home1():
    if request.method == 'POST':
        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
