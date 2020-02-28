from flask import Flask
import os
import numpy as np
import flask
import pickle
import pandas as pd
from flask import Flask, render_template, request
model = pickle.load(open('model.pkl','rb'))

app =Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/result',methods = ['POST'])
def result():
	if request.method == 'POST':
		Current_City = request.form['Current City']
		Application_ID=request.form['Application_ID']
		Pi=request.form['Python (out of 3)']
		R=request.form['R Programming (out of 3)']
		datascience=request.form['Data Science (out of 3)']
		Otherskills=request.form['Other skills']
		Institute=request.form['Institute']
		Degree=request.form['Degree']
		Stream=request.form['Stream']
		CurrentYearOfGraduation=request.form['Current Year Of Graduation']
		Performance_PG=request.form['Performance_PG']
		Performance_UG=request.form['Performance_UG']
		Performance_12=request.form['Performance_12']
		Performance_10=request.form['Performance_10'] 
		df=pd.DataFrame({'Application_ID':[Application_ID],'Current City':[Current_City],'Python (out of 3)':[Pi],'R Programming (out of 3)':[R],'Data Science (out of 3)':[datascience],'Other skills':[Otherskills],'Institute':[Institute],'Degree':[Degree],'Stream':[Stream],'Current Year Of Graduation':[CurrentYearOfGraduation],'Performance_PG':[Performance_PG],'Performance_UG':[Performance_UG],'Performance_12':[Performance_12],'Performance_10':[Performance_10]})
		df.drop(['Application_ID','Current City','Institute','Stream','Performance_PG','Performance_UG','Performance_12','Performance_10'],axis=1,inplace=True)
		df=df.rename(columns={"Python (out of 3)": "Python", "R Programming (out of 3)": "R","Data Science (out of 3)": "Data Science"})
		df.loc[df['Python']==3,['Python']]=10
		df.loc[df['Python']==1,['Python']]=3
		df.loc[df['Python']==2,['Python']]=7
		df.loc[df['R'] == 3, ['R']] = 10
		df.loc[df['R'] == 1, ['R']] = 3
		df.loc[df['R'] == 2, ['R']] = 7
		df.loc[df['Data Science'] == 3, ['Data Science']] = 10
		df.loc[df['Data Science'] == 1, ['Data Science']] = 3
		df.loc[df['Data Science'] == 2, ['Data Science']] = 7 
		df['degreescore']=0
		df['skillscore']=0
		df.loc[(df["Degree"] == "Bachelor of Engineering (B.E)") | (df["Degree"] == "Bachelor of Technology (B.Tech)") | (df["Degree"] == "B.Tech (Hons.)") | (df["Degree"] == "Bachelor of Engineering (B.E) (Hons.)") | (df["Degree"] == "Integrated B.Tech & M.Tech") | (df["Degree"] == "Integrated B.Tech & MBA") & (int(df['Current Year Of Graduation']) > 2020) , "degreescore"] += 0
		df.loc[(df["Degree"] == "Bachelor of Engineering (B.E)") | (df["Degree"] == "Bachelor of Technology (B.Tech)") | (df["Degree"] == "B.Tech (Hons.)") | (df["Degree"] == "Bachelor of Engineering (B.E) (Hons.)") | (df["Degree"] == "Integrated B.Tech & M.Tech") | (df["Degree"] == "Integrated B.Tech & MBA") & (int(df['Current Year Of Graduation']) == 2020) , "degreescore"] += 10
		df.loc[(df["Degree"] == "Bachelor of Engineering (B.E)") | (df["Degree"] == "Bachelor of Technology (B.Tech)") | (df["Degree"] == "B.Tech (Hons.)") | (df["Degree"] == "Bachelor of Engineering (B.E) (Hons.)") | (df["Degree"] == "Integrated B.Tech & M.Tech") | (df["Degree"] == "Integrated B.Tech & MBA") & (int(df['Current Year Of Graduation']) == 2019) , "degreescore"] += 8
		df.loc[(df["Degree"] == "Bachelor of Engineering (B.E)") | (df["Degree"] == "Bachelor of Technology (B.Tech)") | (df["Degree"] == "B.Tech (Hons.)") | (df["Degree"] == "Bachelor of Engineering (B.E) (Hons.)") | (df["Degree"] == "Integrated B.Tech & M.Tech") | (df["Degree"] == "Integrated B.Tech & MBA") & (int(df['Current Year Of Graduation']) <= 2018) , "degreescore"] += 5
		df.loc[(df["Degree"] == "Master of Science (M.Sc)") |  (df["Degree"] == "Master of Technology (M.Tech)")| (df["Degree"] == "Integrated B.Sc. & M.Sc.")| (df["Degree"] == "Integrated M.Sc.")| (df["Degree"] == "Master of Science (M.S.)")| (df["Degree"] == "Master of Science (M.Sc) (Hons.)")| (df["Degree"] == "Integrated B.Tech & M.Tech") & (int(df["Current Year Of Graduation"]) > 2020) , "degreescore"] += 0
		df.loc[(df["Degree"] == "Master of Science (M.Sc)") |  (df["Degree"] == "Master of Technology (M.Tech)")| (df["Degree"] == "Integrated B.Sc. & M.Sc.")| (df["Degree"] == "Integrated M.Sc.")| (df["Degree"] == "Master of Science (M.S.)")| (df["Degree"] == "Master of Science (M.Sc) (Hons.)")| (df["Degree"] == "Integrated B.Tech & M.Tech") & (int(df["Current Year Of Graduation"]) == 2020) , "degreescore"] += 7
		df.loc[(df["Degree"] == "Master of Science (M.Sc)") |  (df["Degree"] == "Master of Technology (M.Tech)")| (df["Degree"] == "Integrated B.Sc. & M.Sc.")| (df["Degree"] == "Integrated M.Sc.")| (df["Degree"] == "Master of Science (M.S.)")| (df["Degree"] == "Master of Science (M.Sc) (Hons.)")| (df["Degree"] == "Integrated B.Tech & M.Tech") & (int(df["Current Year Of Graduation"]) <= 2019) , "degreescore"] += 3
		df.loc[(df['Other skills'].str.contains('Machine Learning',na=False)),"skillscore"] += 3
		df.loc[(df['Other skills'].str.contains('Deep Learning',na=False)),"skillscore"] += 3
		df.loc[(df['Other skills'].str.contains('Natural Language Processing (NLP)',na=False)),"skillscore"] += 3
		df.loc[(df['Other skills'].str.contains('Data Analytics',na=False)),"skillscore"] += 3
		df.loc[(df['Other skills'].str.contains('Amazon Web Services (AWS)',na=False)),"skillscore"] += 3
		df.loc[(df['Other skills'].str.contains('SQL',na=False)) | (df['Other skills'].str.contains('MySQL',na=False)) ,"skillscore"] += 3
		df.loc[(df['Other skills'].str.contains('MS-Excel',na=False)) | (df['Other skills'].str.contains('MS-Office',na=False)) ,"skillscore"] += 3
		df.drop(['Other skills','Degree','Current Year Of Graduation'],axis=1,inplace=True)
		df['total']=int(df['Python'])+int(df['R'])+int(df['Data Science'])+int(df['degreescore'])+int(df['skillscore'])
		df['lable']=0
		df.loc[(df["total"] >= 40),'lable']=1 
		df.drop(['total'],axis=1,inplace=True)   
		y=np.array(df['lable'])
		x=np.array(df.drop(['lable'],axis=1))
		pred=model.predict(x)
		if pred==1:
			prediction ='you will get data Science job'
		else:
			prediction = 'you will not get data science job'
	return render_template("result.html",prediction=prediction)    


if __name__ == '__main__':
    app.run(debug=True)       