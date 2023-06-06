from flask import Flask,render_template,request,session, redirect
from src.pipeline.predict_pipeline import PredictPipeline,CustomData
from src.exception import CustomException
import sys
from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo


app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Establish Database Connection
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.login_users


# Decorators  : allowing define a func inside another/nested functions
def login_required(f):

  # preserve the original metadata of a wrapped function using @wraps from functools
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')

  return wrap


# the Routing
@app.route('/user/signup', methods=['POST'])
def signup():
  from user.models import User
  return User().signup()

@app.route('/user/signout')
def signout():
  from user.models import User
  return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
  from user.models import User
  return User().login()


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')


@app.route('/home/')
def home():
    return render_template('home.html')


@app.route('/predict',methods=['GET','POST'])
def predict_data():

    try:

        if request.method == 'GET':
            return render_template('home.html')
        
        else:

            data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))

            )

            pred_df=data.get_data_as_dataframe()
            # print(pred_df)


            predict_pipeline=PredictPipeline()

            res=predict_pipeline.predict(pred_df)

           

            return render_template('home.html',res="Predicted Score: " + str(res[0]))
    except Exception as ex:

        raise CustomException(ex,sys)



if __name__ == "__main__":
  app.run(debug=True)