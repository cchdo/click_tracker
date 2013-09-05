import json
import re
import socket
import ast
from datetime import date

from flask import *

from sqlalchemy import distinct
from sqlalchemy.orm import sessionmaker

import pygeoip

from threading import Timer
import thread, time, sys

from crossdomain import *

from models import *


app = Flask(__name__)

Session = sessionmaker(bind=engine)

GEOIP = pygeoip.GeoIP('GeoIP.dat')


def timeout():
    raise Exception


@app.route('/show_clicks')
def show_clicks():
    return render_template('index.html')


@app.route('/get_latest_files')
@crossdomain(origin='*')
def get_latest_files():
    output = ""

    session = Session()
    expocodes = session.query(distinct(Click.expocode)).all()
    for expo in expocodes:
        files = session.query(distinct(Click.file_type)).filter(Click.expocode == expo[0]).all()
        for file in files:
            count = session.query(Click).\
                    filter(Click.expocode == expo[0], Click.file_type == file[0]).\
                    count()
            output += "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(expo[0], file[0], count)
    return output


def _hostname_record(ip):
    if hasattr(socket, 'setdefaulttimeout'):
        socket.setdefaulttimeout(0.005)
    try:
        hostname = socket.gethostbyaddr(ip)
    except Exception:
        hostname = None
    if hostname:
        hostname = hostname[0]
    else:
        hostname = 'unable to find'
    try:
        dns_record = str(GEOIP.record_by_addr(ip))
    except:
        dns_record = None
    return hostname, dns_record


@app.route('/click_tracker.js')
@crossdomain(origin='*')
def serve_click_tracker():
    return render_template('click_stats.js')

@app.route('/get_latest_users')
@crossdomain(origin='*')
def get_latest_users():
    output = ""
    session = Session()
    users = session.query(distinct(Click.source_location)).all()
    for user in users:
        user_ip = user[0]
        if user_ip is None:
            continue
        count = session.query(Click).filter(Click.source_location == user_ip).count()
        try:
            Timer(0.12, timeout).start()
            hostname, dns_record = _hostname_record(user_ip)
            dns = ast.literal_eval(dns_record)
            formatted_dns = dns['city'] + ", " + dns['country_name']
        except:
            hostname = ""; dns_record = ""; formatted_dns = ""
        output += (u'<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>').format(user_ip, count, hostname, formatted_dns )
    return output


@app.route('/', methods=['GET', 'POST'])
@crossdomain(origin='*')
def index():
    if request.method == 'GET':
        return redirect('/show_clicks')
    remote_addr = request.remote_addr 
    form = request.form
    st = ''.join(form.keys())
    try:
        result = json.loads(st)
	expocode = result['expocode']
	file_type = result['file_type']
	new_click = Click()
	new_click.expocode = expocode
        new_click.date = date.today()
	new_click.file_type = file_type
	new_click.source_location = remote_addr
        session = Session()
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
