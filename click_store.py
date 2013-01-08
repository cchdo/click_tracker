import json
import re
import socket

from flask import *

from sqlalchemy import distinct
from sqlalchemy.orm import sessionmaker

import pygeoip

from crossdomain import *

from models import *


app = Flask(__name__)

Session = sessionmaker(bind=engine)

GEOIP = pygeoip.GeoIP('GeoIP.dat')


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
        socket.setdefaulttimeout(0.1)
    try:
        hostname = socket.gethostbyaddr(ip)
    except Exception:
        hostname = None
    if hostname:
        hostname = hostname[0]
    else:
        hostname = 'unable to find'
    dns_record = str(GEOIP.record_by_addr(ip))
    return hostname, dns_record


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
        hostname, dns_record = _hostname_record(user_ip)
        output += ('<tr><td>{0}</td><td>{1}</td><td>{2}</td><td><abbr title="{3}">hover for record</abbr></td>'
            '<td></td></tr>').format(user_ip, count, hostname, dns_record)
    return output


@app.route('/', methods=['GET', 'POST'])
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
