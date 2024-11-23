from flask import Flask
from flask import render_template
from flask import request
import mysql.connector
from flask_cors import CORS
import json
mysql = mysql.connector.connect(user='web', password='webPass',
  host='127.0.0.1',
  database='student')

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
app = Flask(__name__)
CORS(app)
@app.route("/test")
def test():
 return("Hello World!<BR/>THIS IS ANOTHER TEST!")

@app.route("/yest")
def yest():
 return("Hello World!<BR/>THIS IS YET ANOTHER TEST!")

@app.route("/add", methods=['GET', 'POST'])
def add():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    print(name,email)
    cur = mysql.cursor()
    s='''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name,email)
    app.logger.info(s)
    cur.execute(s)
    mysql.commit()
  else:
    return render_template('add.html')

  return '{"Result":"Success"}'
@app.route("/")
def hello():
  cur = mysql.cursor()
  cur.execute('''SELECT * FROM students''')
  rv = cur.fetchall()
  Results=[]
  for row in rv:
    Result={}
    Result['Name']=row[0].replace('\n',' ')
    Result['Email']=row[1]
    Result['ID']=row[2]
    Results.append(Result)
  response={'Results':Results, 'count':len(Results)}
  ret=app.response_class(
    response=json.dumps(response),
    status=200,
    mimetype='application/json'
  )
  return ret
if __name__ == "__main__":
  app.run(host='0.0.0.0',port='8080', ssl_context=('cert.pem', 'privkey.pem'))