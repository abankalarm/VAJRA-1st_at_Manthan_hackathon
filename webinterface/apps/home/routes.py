# -*- encoding: utf-8 -*-
import html as htmlmodule
from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.offsec import *
from apps.home.asn import *
import sqlite3
import json
import urllib.request

def getfromdb(columns, values):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    query = "SELECT * FROM Fingerprints where "
    for i in range(0, len(columns)):
        if i == len(columns) - 1:
            query += columns[i] + " = '" + values[i] + "';"
        else:
            query += columns[i] + " = '" + values[i] + "' and "
    print(query)
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows

def storeInDB(content):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    s = "CREATE TABLE IF NOT EXISTS Fingerprints ( _id INTEGER PRIMARY KEY autoincrement,"
    col = ""
    for i in content:
        if i != 'audio':
            col += str(i) + ", "
            if i == 'ip' or i == 'cookie' or i == 'clientID':
                s += i + " TEXT, "
            else:
                s += i + " BLOB,"
        else:
            col += str(i) + ""
            s += i + " BLOB);"
    cur.execute(s)
    l = getfromdb(["clientID", "cookie", "ip"], [content["clientID"], content["cookie"], content["ip"]])
    if(len(l) == 0):
        s = "INSERT INTO Fingerprints (" + col + ") VALUES ("
        for i in content:
            if i == 'ip' or i == 'cookie' or i == 'clientID':
                s += "'" + str(content[i]) + "', "
            else:
                if i == 'audio':
                    s += str("'" + content[i] + "'") + ");"
                else:
                    j = json.dumps(content[i])
                    s += "'" + str(j) + "', "
        print(s)
        cur.execute(s)
        conn.commit()
        conn.close()
    else:
        s = "UPDATE Fingerprints SET "
        for i in content:
            if i == 'ip' or i == 'cookie' or i == 'clientID':
                #nothing
                print("match")
            else:
                if i == 'audio':
                    s += i + " = " + str("'" + content[i] + "'")
                else:
                    j = json.dumps(content[i])
                    s += i + " = '" + str(j) + "', "
        s += " where clientID = '" + content['clientID'] + "' and cookie = '" + content["cookie"] + "' and ip = '" + content["ip"] + "';"
        print(s)
        cur.execute(s)
        conn.commit()
        conn.close()

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            pass

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

@blueprint.route('/injection')
def injection():
    #request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip = request.environ['REMOTE_ADDR']
    return render_template('home/injection.html', segment='index', ip=ip)

@blueprint.route('/injection/post', methods=['POST'])
def injectionpost():
    content = request.json
    storeInDB(content)
    l = getfromdb(['clientID'], [content['clientID']])
    return render_template('home/page-404.html', segment='index'), 404

@blueprint.route('/search', methods=['GET','POST'])
def searchpost():
    if (request.method == 'POST'):
        search = request.form['search']
        print(search)
        isBad,asn,html=getDetails(search)
        print(isBad,asn)
        
        result = htmlmodule.unescape(html)
        return render_template('home/search.html', segment='index', result=result, ip = search)
    else:
        return render_template('home/search.html', segment='index')
    
@blueprint.route('/api/portscan', methods=['POST'])
def portscan():
    ip = request.form['ip']
    type = request.form['speed']
    if type=='top10':
        result = get_info(ip, top_10)
    if type=='top50':
        result = get_info(ip, top_50)
    if type=='top100':
        result = get_info(ip, top_100)

    return jsonify(result)


@blueprint.route('/api/vpnidentification/time', methods=['POST'])
def vpn_time():
    ip = request.form['ip']
    GEO_IP_API_URL  = 'http://ip-api.com/json/'

    req             = urllib.request.Request(GEO_IP_API_URL+ip)
    response        = urllib.request.urlopen(req).read()
    json_response   = json.loads(response.decode('utf-8'))

    # search in db for ip
    browser_timzone = ''

    if(json_response['timezone'] == browser_timzone):
        return jsonify("false")

    return jsonify("true")

@blueprint.route('/api/ip/identity', methods=['GET','POST'])
def ip_identity():
    ip = request.args['ip']
    GEO_IP_API_URL  = 'http://ip-api.com/json/'

    req             = urllib.request.Request(GEO_IP_API_URL+ip)
    response        = urllib.request.urlopen(req).read()
    json_response   = json.loads(response.decode('utf-8'))

    # search in db for ip
    browser_timzone = ''
    dict = {}
    try:
        dict["status"] = "successful"
        dict["lat"] = json_response["lat"]
        dict["lon"] = json_response["lon"]
        dict["regionName"] = json_response["regionName"]
        dict["region"] = json_response["region"]
        dict["city"] = json_response["city"]
        dict["zip"] = json_response["zip"]
        dict["country"] = json_response["country"]
        dict["countryCode"] = json_response["countryCode"]
        dict["isp"] = json_response["isp"]
        
    except:
        dict["status"] = "failed"

    return jsonify(dict)

