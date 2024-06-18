from flask import Flask,render_template,request
import cv2
# from keras.models import load_model
import pickle
import numpy as np
import datetime
# img_size=100
app=Flask(__name__)
# model=load_model('Detection_Covid_19.h5')
# model2=load_model('models/Detection_Lungs_cancer.h5')

loaded_model = pickle.load(open("models/diabetes_model.sav", 'rb'))
loaded_model2=pickle.load(open("models/heart_disease_model.sav",'rb'))
loaded_model3=pickle.load(open("models/Covid_disease_detection_using_symptoms_model.sav",'rb'))
loaded_model4=pickle.load(open("models/Lung_cancer_using_symptoms_model.sav",'rb'))


@app.route('/')
def welcome():
    return render_template('Home.html')

@app.route('/symptom',methods=['GET','POST'])
def goingToSymptoms():
    return render_template('symptoms.html')



@app.route('/diabetes',methods=['GET','POST'])
def d():
    return render_template('diabetis.html')

@app.route('/heart',methods=['GET','POST'])
def h():
    return render_template('heart.html')

# @app.route('/covid_img',methods=['GET','POST'])
# def ci():
#     return render_template('covid_image.html')
@app.route('/covid_symp',methods=['GET','POST'])
def cs():
    return render_template('covid.html')

@app.route('/lung_symp',methods=['GET','POST'])
def ls():
    return render_template('lung.html')

# @app.route("/lung_img",methods=['POST'])
# def li():
#     return render_template('lungs_img.html')

# @app.route("/submit_lung_img" , methods=['POST'])
# def lung_img():
#     l=[]
#     for key in request.form:
#         l.append(request.form[key])
#     name=l.pop(0)
#     gender=l.pop(0)
#     dob=l.pop(0)
#     age=int(l.pop(0))
#     mobile=l.pop(0)
#     add=l.pop(0)
    

#     file=request.files['file']
#     prediction=predict_lung(file)
#     result=interpret_predictions2(prediction)
#     return render_template("result.html",res_ans=result,names_ans=name,sex_ans=gender,dob_ans=dob,age_ans=age,mobile_ans=mobile,date_ans=str(datetime.date.today()),address_ans=add)

# @app.route('/submit_covid_image',methods=['POST'])
# def covid_img():
#     l=[]
#     for key in request.form:
#         l.append(request.form[key])
#     name=l.pop(0)
#     gender=l.pop(0)
#     dob=l.pop(0)
#     age=int(l.pop(0))
#     mobile=l.pop(0)
#     add=l.pop(0)
    

#     file=request.files['file']
    
#     prediction=predict_covid(file)
#     result=interpret_predictions(prediction)
#     return render_template("result.html",res_ans=result,names_ans=name,sex_ans=gender,dob_ans=dob,age_ans=age,mobile_ans=mobile,date_ans=str(datetime.date.today()),address_ans=add)


@app.route('/submit_lung',methods=['GET','POST'])
def lung_symp():
    l=[i for i in request.form.values()]
    name=l.pop(0)
    gender=l.pop(0)
    dob=l.pop(0)
    age=int(l.pop(0))
    mobile=l.pop(0)
    add=l.pop(0)
    l.insert(0,age)
    if(gender=="Male"):
        l.insert(0,1)
    else:
        l.insert(0,0)
    
    name_list=[int(l[x]) for x in range(len(l))]
    result=lung_symp_prediction(name_list)
    return render_template("result.html",res_ans=result,names_ans=name,sex_ans=gender,dob_ans=dob,age_ans=age,mobile_ans=mobile,date_ans=str(datetime.date.today()),address_ans=add)





@app.route("/submit_covid_symp",methods=['POST'])
def covid_symp():
    l=[i for i in request.form.values()]
  
    name=l.pop(0)
    gender=l.pop(0)
    dob=l.pop(0)
    age=int(l.pop(0))
    mobile=l.pop(0)
    add=l.pop(0)
    name_list=[int(i) for i in l]
    result=covid_symp_prediction(name_list)
    return render_template("result.html",res_ans=result,names_ans=name,sex_ans=gender,dob_ans=dob,age_ans=age,mobile_ans=mobile,date_ans=str(datetime.date.today()),address_ans=add)
    






@app.route('/submit_heart',methods=['POST'])
def heart_disease():
    l=[str(i) for i in request.form.values()]
 
    name=l.pop(0)
    gender=l.pop(0)
    dob=l.pop(0)
    age=int(l.pop(0))
    mobile=l.pop(0)
    add=l.pop(0)
    name_list=[float(l[x]) for x in range(len(l))]
    if(gender=='Male'):
        name_list.insert(0,float(1))
    else:
        name_list.insert(0,float(0))
    name_list.insert(0,float(age))
    temp=name_list.pop()
    name_list.insert(8,temp)
    result=heart_prediction(name_list)
    return render_template("result.html",res_ans=result,names_ans=name,sex_ans=gender,dob_ans=dob,age_ans=age,mobile_ans=mobile,date_ans=str(datetime.date.today()),address_ans=add)


@app.route('/submit_diabetis',methods=['POST'])
def diabetis():
    l=[str(i) for i in request.form.values()]
    # print("\n\n\n\n\n\n\n\n")
    # print(l)
    name=l.pop(0)
    gender=l.pop(0)
    dob=l.pop(0)
    age=int(l.pop(0))
    mobile=l.pop(0)
    add=l.pop(0)
    name_list=[float(l[x]) for x in range(len(l))]
    name_list.append(float(age))
    result=diabetis_prediction(name_list)
    return render_template("result.html",res_ans=result,names_ans=name,sex_ans=gender,dob_ans=dob,age_ans=age,mobile_ans=mobile,date_ans=str(datetime.date.today()),address_ans=add)

def diabetis_prediction(input_data):
	input_data_as_numpy_array = np.asarray(input_data)
    
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    

	prediction = loaded_model.predict(input_data_reshaped)
	print(prediction)
    
	if (prediction[0] == 0):
		return 'The person is not diabetic'
	else:
		return 'The person is diabetic'
def lung_symp_prediction(input_data):
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    prediction = loaded_model4.predict(input_data_reshaped)
    print(prediction)
    if (prediction[0] == 0):
        return 'The person does not have lung cancer'
    else:
        return 'The person have lung cancer'

def heart_prediction(input_data):
    input_data_as_numpy_array=np.asarray(input_data)
    input_data_reshaped=input_data_as_numpy_array.reshape(1,-1)
    prediction=loaded_model2.predict(input_data_reshaped)
    if(prediction[0]==0):
        return 'The person does not have heart disease'
    else:
        return 'The person has heart disease'

def covid_symp_prediction(input_data):
    input_data_as_numpy_array=np.asarray(input_data)
    input_data_reshaped=input_data_as_numpy_array.reshape(1,-1)
    prediction=loaded_model3.predict(input_data_reshaped)
    if(prediction[0]==0):
        return 'The person does not have covid'
    else:
        return 'The person has covid disease'

def preprocess_image(image):
    image=cv2.imdecode(np.frombuffer(image.read(),np.uint8),cv2.IMREAD_COLOR)
    image=cv2.resize(image,(224,224))
    image=image/255.0
    return image

# def predict_covid(image):
#     preprocessed_image=preprocess_image(image)
#     preprocessed_image=np.expand_dims(preprocessed_image,axis=0)
#     prediction=model.predict(preprocessed_image)
#     return prediction

def interpret_predictions(prediction):
    if prediction[0][0]>0.5:
        return "Covid-19 detected"
    else:
        return "No covid detected"
# def predict_lung(image):
#     preprocessed_image=preprocess_image(image)
#     preprocessed_image=np.expand_dims(preprocessed_image,axis=0)
#     prediction=model2.predict(preprocessed_image)
#     return prediction

def interpret_predictions2(prediction):
    predicted_class=np.round(prediction)[0][0]

    if predicted_class==0:
        return "Patient is affected by lung cancer"
    else:
        return "Patient is not affected by lung cancer"
    

    

      
      
if __name__=="__main__":
      app.run(debug=True)
	     

