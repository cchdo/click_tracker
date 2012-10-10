import sys
import json
import re
from flask import *
from sqlalchemy import create_engine, MetaData, Table, func, distinct
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from models import *
from datetime import timedelta
#from flask import make_response, request, current_app
from functools import update_wrapper
from crossdomain import *




app = Flask(__name__)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/show_clicks')
def show_clicks():
    return render_template('index.html')

@app.route('/get_latest')
@crossdomain(origin='*')
def get_latest():
    output = ""; s = ""; expo_dict = {};

    expocodes = session.query(distinct(Click.expocode)).all()
    for expo in expocodes:
        files = session.query(distinct(Click.file_type)).filter(Click.expocode == expo[0]).all()
        for file in files:
            count = session.query(Click).\
                    filter(Click.expocode == expo[0], Click.file_type == file[0]).\
                    count()
            print count
            s = "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(expo[0], file[0], count)
            output += s
    return output

@app.route('/', methods=['GET','POST', 'OPTIONS'])
@crossdomain(origin='*')
def index():
    expo_re = re.compile('expocode":"(.*)",.*file_type":"(.*)"')
    req = request.form
    st = str(req)
    result = expo_re.search(st)
    expocode = result.group(1)
    file_type = result.group(2)
    new_click = Click()
    new_click.expocode = expocode
    new_click.file_type= file_type
    session.add(new_click)
    session.commit()
    return "blah" #jsonify("{a:something}")

if __name__ == '__main__':
    app.run()
