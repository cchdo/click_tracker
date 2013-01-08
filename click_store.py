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

@app.route('/get_latest_files')
@crossdomain(origin='*')
def get_latest_files():
    output = ""; s = ""; expo_dict = {};

    expocodes = session.query(distinct(Click.expocode)).all()
    for expo in expocodes:
        files = session.query(distinct(Click.file_type)).filter(Click.expocode == expo[0]).all()
        for file in files:
            count = session.query(Click).\
                    filter(Click.expocode == expo[0], Click.file_type == file[0]).\
                    count()
            s = "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(expo[0], file[0], count)
            output += s
    return output

@app.route('/get_latest_users')
@crossdomain(origin='*')
def get_latest_users():
    output = ""; s = ""; expo_dict = {};

    users = session.query(distinct(Click.source_location)).all()
    for user in users:
        if user[0] == None:
            continue
        count = session.query(Click).filter(Click.source_location == user[0]).count()
        s = "<tr><td>{0}</td><td>{1}</td><td></td></tr>".format(user[0], count)
        output += s
    return output


expo_re = re.compile('expocode":"(.*)",.*file_type":"(.*)"')


@app.route('/', methods=['GET','POST', 'OPTIONS'])
@crossdomain(origin='*')
def index():
    remote_addr = request.remote_addr 
    form = request.form
    st = ''.join(form.keys())
    try:
        result = json.loads(st)
	expocode = result['expocode']
	file_type = result['file_type']
	new_click = Click()
	new_click.expocode = expocode
	new_click.file_type= file_type
	new_click.source_location = remote_addr
	session.add(new_click)
	session.commit()
        return '{"status": "stored"}'
    except KeyError:
        return '{"status": "bad key"}'
    except Exception:
        return '{"status": "bad request"}'
    return '{"status": "ok"}'

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=60000)
