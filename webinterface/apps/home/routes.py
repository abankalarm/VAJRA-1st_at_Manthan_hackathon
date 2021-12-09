# -*- encoding: utf-8 -*-
import html
import numpy
import os
from sqlite3.dbapi2 import connect
import ipaddress
from werkzeug.datastructures import ContentRange
from apps.home import blueprint
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.offsec import *
from apps.home.vpnproto import *
from apps.home.asn import *
import sqlite3
import json
import urllib.request
from ua_parser import user_agent_parser
from flask import send_from_directory
import time
import pandas
import base64
import pickle 
from datetime import datetime
from user_agents import parse
import string
import random
# import rsplit


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
        ##print(i, ": ", content[i], " ", type(content[i]))
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
    ##print(col)
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
    ##print(s)
    cur.execute(s)
    conn.commit()
    conn.close()

@blueprint.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
    # call db unique name
    ip = request.environ['REMOTE_ADDR']
    parsed_string = user_agent_parser.Parse( str(request.headers.get('User-Agent')))
    #print(parsed_string)
    data={
        "ip":ip,
        "id":filename,
        "timestamp":str(time.time()),
        "userAgent": parsed_string
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
    ##print(query)
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
    conn.commit()
    conn.close()

def storeIpCommentTable(name, comment):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    s = "CREATE TABLE IF NOT EXISTS TrackingComments ( id TEXT, comment TEXT);"
    cur.execute(s)
    l = getfromdb('TrackingComments', ['id'], name)
    if len(l) == 0:
        s = "INSERT INTO TrackingComments (id, comment) VALUES ('" + name + "', '" + comment + "');"
        cur.execute(s)
        conn.commit()
    else:
        s = "UPDATE TrackingComments SET comment = '" + comment + "' WHERE id = '" + name + "';"
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
    ##print(col)
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
        #print(s)
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
        ##print(s)
        cur.execute(s)
        conn.commit()
        conn.close()


def storeInAttackingTable(content):
    #print(content)
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
        ##print(s)
        #print(s)
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
    #print(s)
    cur.execute(s)
    rows = cur.fetchall()
    #print(rows[0][0])
    return str(rows[0][0])

@blueprint.route('/index')
@login_required
def index():
    return redirect("/dashboard", code=302)

@blueprint.route('/nmap')
@login_required
def nmap():
    oports = {}
    return render_template('home/nmaps.html', segment='nmaps', oports = oports)

@blueprint.route('/dashboard')
@login_required
def dash():
    allData = {}
    allData["IP"]=[]
    
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT (ip) FROM Fingerprints;")
    desc = cur.description 
    column_names = [col[0] for col in desc] 
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    #print(data)
    
    allData["IP"]=data
    
    #allData["IP"]=json.loads(  vpnDetails(allData["IP"]).data  ) 

    
        
    allData['uniqueIpCount'] = len(allData["IP"])
    #print(allData)
    
    cur.execute("SELECT countryCode as id, COUNT( DISTINCT ip) as value FROM Fingerprints GROUP BY countryCode; ")
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
    
    cur.execute("SELECT ip, isVpnTime, parentDomain, timestamp FROM Fingerprints; ")
    desc = cur.description 
    column_names = [col[0] for col in desc] 
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    allData['distinctIp'] = data

    cur.execute("SELECT COUNT( DISTINCT ip) as cnt FROM Fingerprints where isVpnTime = 'true' or isVpnASN = 'True'; ")
    desc = cur.description 
    column_names = [col[0] for col in desc] 
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    allData['vpns'] = data
    
    cur.execute("SELECT ip FROM Fingerprints WHERE bookmarked=1 ;")
    desc = cur.description 
    column_names = [col[0] for col in desc] 
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    allData['flaggedIp'] = data
    conn.close()
    
    return render_template('home/dashboard.html', segment='dash', allData = allData)

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
    return render_template('home/fulldomainlist.html', segment='fdl', allData = allData)


@blueprint.route('/bookmarks')
@login_required
def bkmark():
    #receive an IP and call flagBookmarkDB(ip)
    return render_template('home/bookmarks.html', segment='bookmarks')

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
            s = "SELECT cookie, clientId, timestamp, bookmarked, userAgent, timezone, isTor, isVpnTime, isVpnASN, countryCode, region, regionName, isp, lat, lon, city, country, parentDomain FROM Fingerprints where ip ='" + i['ip'] + "';"
            cur.execute(s)
            desc = cur.description
            column_names = [col[0] for col in desc]
            data1 = [dict(zip(column_names, row)) for row in cur.fetchall()]
            allData[i['ip']] = data1
        allData['keyList'] = ips
        conn.close()
    except:
        print('No data')
    return render_template('home/fulliplog.html', segment='ipl', allData = allData)


@blueprint.route('/<template>')
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




def getAllRelatedIP(search):
    ips=[]
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("Select cookie from Fingerprints where ip='"+str(search)+"'")
    desc = cur.description 
    column_names = [col[0] for col in desc] 
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    

    for e in data:
        cur.execute("Select ip from Fingerprints where cookie='"+e["cookie"]+"'")
        desc1 = cur.description 
        column_names1 = [col[0] for col in desc1] 
        data1 = [dict(zip(column_names1, row)) for row in cur.fetchall()]
        temp=[]
        if len(data1)>0:
            #print(data1)
            temp=[x["ip"] for x in data1]
            #print("$$$$$$",temp)
        ips.extend(temp)
        
    
    cur.execute("Select clientID from Fingerprints where ip='"+str(search)+"'")
    desc = cur.description 
    column_names = [col[0] for col in desc] 
    try:
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    except:
        data = []
    for e in data:
        cur.execute("Select ip from Fingerprints where clientID='"+e["clientID"]+"'")
        desc1 = cur.description 
        column_names1 = [col[0] for col in desc1] 
        data1 = [dict(zip(column_names1, row)) for row in cur.fetchall()]
        temp=[]
        if len(data1)>0:
            #print(data1)
            temp=[x["ip"] for x in data1]
            #print("$$$$$$",temp)
        
        ips.extend(temp)
    #print(ips,type(ips))
    uip = list(set(ips))
    allDataIP={}
    print(ips)
    print(uip)

    for ip in uip:
        cur.execute("Select * from Fingerprints where ip='"+ip+"'" )
        desc = cur.description 
        column_names = [col[0] for col in desc] 
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        allDataIP[ip]=data
    conn.close()
    return allDataIP







def getRiskVal(allData,search):
    riskData={}
    try:
        if allData["bad"] :
            riskData["badAsnVal"]=80
            riskData["badAsn"]=" Is a Bad ASN"
        else:
            riskData["badAsnVal"]=0
            riskData["badAsn"]="Not a Bad ASN "
    except:
        riskData["badAsnVal"]=0
        riskData["badAsn"]="Not a Bad ASN"
    
    try:
        if allData["dc"] :
            riskData["dataCenterVal"]=50
            riskData["dataCenter"]= "Is a Data Center"
        else:
            riskData["dataCenterVal"]=0
            riskData["dataCenter"]="Not a Data Center"
    except:
        riskData["dataCenterVal"]=0
        riskData["dataCenter"]="Not a Data Center"
    try:
        if allData["bl"] :
            riskData["blacklistedVal"]=100
            riskData["blacklisted"]="Blacklisted"
        else:
            riskData["blacklistedVal"]=0
            riskData["blacklisted"]="Not Blacklisted"
    except:
        riskData["blacklistedVal"]=0
        riskData["blacklisted"]="Not Blacklisted"
    
    
    conn1 = sqlite3.connect('ip-index.db')
    cur1=conn1.cursor()
    intip=int(ipaddress.ip_address(search))
    s="SELECT country FROM Countries WHERE start ="+ search.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"
    cur1.execute(s)
    desc1 = cur1.description 
    column_names1 = [col[0] for col in desc1] 
    data = [dict(zip(column_names1, row)) for row in cur1.fetchall()][0]
    cname=data['country']
    conn1.close()
    
    conn = sqlite3.connect('db.sqlite3')
    cur=conn.cursor()
    cur.execute("Select blocked from Countries where id='"+cname.upper()+"'")
    desc = cur.description 
    column_names = [col[0] for col in desc] 
    data = [dict(zip(column_names, row)) for row in cur.fetchall()][0]

    
    try:   
        if data["blocked"]==1 :
            riskData["grey"]=50
        else:
            riskData["grey"]=0
    except:
        riskData["grey"]=0

    try:
        if data["blocked"]==2 :
            riskData["black "]=100
        else:
            riskData["black"]=0

    except:
        riskData["black"]=0


    return riskData


def getAllIpDetails(allDataIP,search,riskData,dataWithThisIp):
    details={"isVPN":"False"}
    try:
        
        if allDataIP[search][0]["isVpnTime"]:
            riskData["Timezone"]=70
        else:
            riskData["Timezone"]=0

    except:
        riskData["Timezone"]=0

    riskData["per"]=riskData["Timezone"]+riskData["black"]+riskData["grey"]+ riskData["blacklistedVal"]+riskData["dataCenterVal"]+riskData["badAsnVal"]
    details["ratingcolor"] = "green"
    if(riskData["per"]>30):
        details["ratingcolor"] = "orange"
    if(riskData["per"]>100):
        riskData["per"] = 100
        details["ratingcolor"] = "red"


    try:
        if riskData['blacklistedVal']+ riskData['Timezone'] + riskData['badAsnVal'] >0:
            riskData["isVPN"] = "True"
    except:
        details["isVPN"]="False"
    try:
        details["isp"] = allDataIP[search][0]['isp']
        details["region"] = allDataIP[search][0]['regionName']
        details["zipcode"] = allDataIP[search][0]['zip']
        details["lat_long"] = str(allDataIP[search][0]["lat"]) + " & " + str(allDataIP[search][0]["lon"])
        details["country"] = allDataIP[search][0]['country']
    except:
        try:
            
            GEO_IP_API_URL  = 'http://ip-api.com/json/'
            req             = urllib.request.Request(GEO_IP_API_URL+search)
            response        = urllib.request.urlopen(req).read()
            json_response   = json.loads(response.decode('utf-8'))
            
            
            #details["regionName"] = json_response["regionName"]
            print(json_response)
            details["region"] = json_response["region"]
            #details["city"] = json_response["city"]
            details["zipcode"] = json_response["zip"]
            details["country"] = json_response["country"]
            details["isp"] = json_response["isp"]
            print("here")
            details["lat_long"] = str(json_response["lat"])+" & "+str(json_response["lon"])
        
        except:
            print("whyyyyyyy")
            details["isp"]="Not Available"
            details["country"]="Not Available"
            details["region"]="Not Available"
            details["zipcode"]="Not Available"
            details["lat_long"]="Not Available"
    #print(allData.keys())

    ##print("@@@@@@",Alldata_for_searched_ip)
    try:
        allDataIP['keyList'] = list(allDataIP.keys())
        allDataIP['cols'] = ['cookie', 'timezone', 'userAgent', 'timestamp']
        

        dataWithThisIp['data'] = allDataIP[search]
        dataWithThisIp['cols'] = ['cookie', 'userAgent', 'timestamp', 'parentDomain']
    except:
        dataWithThisIp={}
    return details
def getTrackIP(search):
    trackIp={}
    conn = sqlite3.connect('db.sqlite3')
    cur=conn.cursor()
    cur.execute("Select * from Attacking where ip ='"+ search +"'")
    desc = cur.description
    column_names = [col[0] for col in desc] 
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    for i in data:
        if i['timestamp'] != "Not Attacked":
            i['timestamp'] = datetime.utcfromtimestamp(int(float(i['timestamp']) + 19800)).strftime('%Y-%m-%d %H:%M:%S')
        i['js'] = str(i['js']).replace('"', "'")
    trackIp['attack'] = data 
    cur.execute("Select * from Tracking where ip ='"+ search +"'")
    desc = cur.description
    column_names = [col[0] for col in desc] 
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    for i in data:
        i['timestamp'] = datetime.utcfromtimestamp(int(float(i['timestamp']) + 19800)).strftime('%Y-%m-%d %H:%M:%S')
    trackIp['track'] = data
    return trackIp
@blueprint.route('/search', methods=['GET','POST'])
@login_required
def searchpost():
    if (request.method == 'POST'):

        search = request.form['search']

        allDataIP=getAllRelatedIP(search)

        allData=json.loads(vpnDetails(search).data)
        
        riskData=getRiskVal(allData,search)
        
        dataWithThisIp = {}
        trackIp = {}

        details=getAllIpDetails(allDataIP,search,riskData,dataWithThisIp)
        trackIp=getTrackIP(search)

        return render_template('home/search.html', ip = str(search), allDataIP=allDataIP,  segment='search',riskData=riskData,details=details,allData=allData, dataWithThisIp = dataWithThisIp, trackIp = trackIp)
    else:

        return render_template('home/search.html', segment='search',riskData={} ,allData={},  dataWithThisIp = {}, allDataIP = {},details={}, trackIp = {})




@blueprint.route('/injection')
def injection():
    #request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    #ip="111.223.26.202"
    ip = request.environ['REMOTE_ADDR']
    return render_template('home/injection.html', segment='injection', ip=ip)

@blueprint.route('/injection/post', methods=['POST'])
def injectionpost():
    content = request.json
    #print(content)
    if checkBookmarkDB(content['ip']):
        content['bookmarked'] = 1
    
    pstr = pickle.dumps(content['plugins'], pickle.HIGHEST_PROTOCOL)
    bstr = base64.b64encode(pstr).decode()
    content['plugins'] = bstr
    content['canvas'] = ','.join(content['canvas'])
    content['webgl'] = ','.join(content['webgl'])
    content['fonts'] = ''.join(content['fonts'])
    content['touchSupport'] = ','.join(str(e) for e in content['touchSupport'])
    
    storeInDB(content)
    #l = getfromdb(['ip'], [content['ip']])
    return jsonify('true')
    
@blueprint.route('/api/portscan')
@login_required
def portscan():
    ip = request.args['ip']
    type = request.args['speed']
    
    if type=='top10':
        hostname, hoststate, oports = get_info(ip, top_10)
    elif type=='top50':
        hostname, hoststate, oports = get_info(ip, top_50)
    elif type=='top100':
        hostname, hoststate, oports = get_info(ip, top_100)
    else:
        hostname = ""
        hoststate = "" 
        oports = ""
    
    return render_template('home/nmaps.html', segment='nmaps', hostname = hostname, hoststate = hoststate, oports = oports)


@blueprint.route('/api/vpnidentification/time', methods=['POST'])
def vpn_time():
    ip = request.form['ip']
    timezone = request.form['time']
    GEO_IP_API_URL  = 'http://ip-api.com/json/'

    req             = urllib.request.Request(GEO_IP_API_URL+ip)
    response        = urllib.request.urlopen(req).read()
    json_response   = json.loads(response.decode('utf-8'))

    # search in db for ip
    browser_timzone = timezone

    if(json_response['timezone'] == browser_timzone):
        return jsonify("false")
    elif( json_response['timezone'] != browser_timzone and len(browser_timzone)>5):
        return jsonify("false")


    return jsonify("unknown")

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
    parsed_string = parse(userAgent)
    #print(parsed_string)
    return str(parsed_string)

@blueprint.route('/tracking', methods=['GET','POST'])
@login_required
def uploadfiles():
    if(request.method == 'POST'):
        ip = request.environ['REMOTE_ADDR'] + ":443"
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        mode = request.form.get('mode')
        if(mode=="upload"):
            uploadf = request.files['inputfile']
            comment = request.form.get('comment')
            N = 7
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
            name =  str(res) + '.' + uploadf.filename.rsplit('.', 1)[1].lower()
            
            #print(name)
            # name = request.form['outputfile'] + '.' + request.form['extension']
            if(uploadf):
                try:
                    uploadf.save(os.path.join('webinterface/apps/static/uploads/', name))
                except:
                    uploadf.save(os.path.join('apps/static/uploads/', name))
                # return redirect(url_for('download_file', name=name))      
        
            #print(name)
            storeIpCommentTable(name,comment)
            searchData = {}
            trackingdata = {}
            allData = {}
        else:
            uploadf = {}
            allData = {}
            name = request.form.get('idsearch')
            cur.execute("Select comment from TrackingComments where id = '" + name + "';" )
            desc = cur.description 
            column_names = [col[0] for col in desc] 
            data = [dict(zip(column_names, row)) for row in cur.fetchall()]
            allData['comment'] = data
            
            
            
            try:
                cur.execute("Select ip, userAgent, timestamp from Tracking where id ='" + name + "';" )
                desc = cur.description
                column_names = [col[0] for col in desc] 
                data = [dict(zip(column_names, row)) for row in cur.fetchall()]
                allData['ips'] = str(data)
            except:
                allData['ips'] = "Nothing to show"

        searchData = {}
        try:
            cur.execute("SELECT id, comment FROM TrackingComments;")
            desc = cur.description
            column_names = [col[0] for col in desc] 
            data = [dict(zip(column_names, row)) for row in cur.fetchall()]
            ids = []
            comments = []
            for i in data:
                ids.append(i['id'])
                comments.append(i['comment'])
                s = "SELECT ip, timestamp, userAgent from Tracking where id ='" + i['id'] + "';"
                cur.execute(s)
                desc = cur.description
                column_names = [col[0] for col in desc]
                data1 = [dict(zip(column_names, row)) for row in cur.fetchall()]
                searchData[i['id']] = data1
            searchData['keyList'] = ids
            searchData['comments'] = comments
        except:
            searchData={}

        conn.close()
        return render_template('home/tracking.html', segment='tracking', uploadf=uploadf, name = name, allData=allData, searchData=searchData, ip = ip)
    else:
        try:
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            searchData = {}
            cur.execute("SELECT id, comment FROM TrackingComments;")
            desc = cur.description
            column_names = [col[0] for col in desc] 
            data = [dict(zip(column_names, row)) for row in cur.fetchall()]
            ids = []
            comments = []
            for i in data:
                ids.append(i['id'])
                comments.append(i['comment'])
                s = "SELECT ip, timestamp, userAgent from Tracking where id ='" + i['id'] + "';"
                cur.execute(s)
                desc = cur.description
                column_names = [col[0] for col in desc]
                data1 = [dict(zip(column_names, row)) for row in cur.fetchall()]
                searchData[i['id']] = data1
            searchData['keyList'] = ids
            searchData['comments'] = comments
            conn.close()
        except:
            searchData = {}
        return render_template('home/tracking.html', segment='tracking',searchData=searchData)

@blueprint.route('/api/vpnIsASN', methods=['POST'])
def vpnIsASN():
    if request.method == 'POST':
        ip = request.form['ip']
        intip=int(ipaddress.ip_address(ip))
        s="SELECT * FROM blacklisted WHERE start ="+ ip.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"
        conn = sqlite3.connect('ip-index.db')
        cur=conn.cursor()
        cur.execute(s)
        c=cur.fetchall()
        conn.close()
        #print("->>>",c)
        if len(c)>0 :
            return "True"
    return "false"

@blueprint.route('/api/vpnDetails')
def vpnDetails(data):
    conn = sqlite3.connect('ip-index.db')
    ip=data
    intip=int(ipaddress.ip_address(ip))
    data={}
    data["bl"]={}
    data["dc"]={}
    data["asn"]={}
    data["cn"]={}
    data["bad"]=False
    cur=conn.cursor()
    #print(ip,type(ip),intip,type(intip))
    s="SELECT * FROM blacklisted WHERE start ="+ ip.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"    
    cur.execute(s)
    desc = cur.description 
    column_names = [col[0] for col in desc] 
    a = [dict(zip(column_names, row)) for row in cur.fetchall()]
    
    s="SELECT * FROM datacenters WHERE start ="+ ip.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"
    cur.execute(s)
    desc = cur.description 
    column_names = [col[0] for col in desc] 
    b = [dict(zip(column_names, row)) for row in cur.fetchall()]
    
    s="SELECT * FROM asns WHERE start ="+ ip.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"
    cur.execute(s)
    desc = cur.description 
    column_names = [col[0] for col in desc] 
    c = [dict(zip(column_names, row)) for row in cur.fetchall()]
    s="SELECT * FROM countries WHERE start ="+ ip.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"
    cur.execute(s)
    desc = cur.description 
    column_names = [col[0] for col in desc] 
    d = [dict(zip(column_names, row)) for row in cur.fetchall()]
    conn.close()
    data={}
    if(len(a)>0):
        data["bl"]=a[0]
    if(len(b)>0):
        data["dc"]=b[0]
    if(len(c)>0):
        data["asn"]=c[0]
    if(len(d)>0):
        data["cn"]=d[0]
        data["cn"]["country"]=data["cn"]["country"]
    print(a,b,c,d)
    inBad=c[0]['id'] in badASN
    data["bad"]=inBad
    print(data)

    print()
        
    return jsonify(data)



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
        storeInAttackingTable(content)
        return js


@blueprint.route('/attack',methods=['GET','POST'])
@login_required
def attack():
    allData = {}
    try:
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute("Select count(*) as cnt from Attacking;" )
        desc = cur.description 
        column_names = [col[0] for col in desc] 
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        l = getfromdb('Attacking', ['timestamp'], ['Not Attacked'])
        allAttacked = int(data[0]['cnt']) - 1
        allIpsToBeAttacked = len(l) - 1
        #s="SELECT * FROM blacklisted WHERE start ="+ ip.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"
        #cur.execute(s)
        #a=cur.fetchall()
        conn.close()
    except:
        allAttacked = 0
        allIpsToBeAttacked = 0
    allData['allAttacked'] = allAttacked
    allData['allIpsToBeAttacked'] = allIpsToBeAttacked
    try:
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute("Select * from Attacking where ip != '0.0.1.0';" )
        data = cur.fetchall()
        allData['data'] = []
        allData['js'] = []
        for i in range (0, len(data)):
            if data[i][2] == "Not Attacked":
                allData['data'].append({'ip': str(data[i][0]), 'js': str(data[i][1]).replace('"', "'"), 'timestamp': str(data[i][2])})
            else:
                allData['data'].append({'ip': str(data[i][0]), 'js': str(data[i][1]).replace('"', "'"), 'timestamp': datetime.utcfromtimestamp(int(float(data[i][2]) + 19800)).strftime('%Y-%m-%d %H:%M:%S')})
        allData['cols'] = ['ip', 'js', 'timestamp']
    except:
        allData['data'] = {}
    if(request.method == 'POST'):
        if request.form.get('mode') == "add":
            # store a ip and js pair together , make it unique and overwrite
            IP = request.form.get('ipaddr')
            JS = request.form.get('jsoffsec')
            content = {}
            content['ip'] = IP
            content['js'] = JS
            content['timestamp'] = "Not Attacked"
            storeInAttackingTable(content)
            return redirect("/attack", code=302)
        if request.form.get('mode') == "search":
            IP = request.form.get('ipaddr')
            content = {}
            content["ip"] = IP
            # search for js respective to partivular ip
            l = getfromdb("Attacking",["ip"], [content["ip"]])
            try:
                tsAttack = datetime.utcfromtimestamp(int(float(l[0][2]) + 19800)).strftime('%Y-%m-%d %H:%M:%S')
            except:
                tsAttack = "Not Attacked"
            #print("######", l[0][0], " ", l[0][1], " ", tsAttack, " ")
            return render_template('home/attack.html', segment='attack', search = content, ipOfAttack = l[0][0], jsOfAttack = l[0][1], ts = tsAttack, allData = allData)
    else:
        content = {}
        content['ip'] = '0.0.1.0'
        content['js'] = ''
        content['timestamp'] = 'Not Attacked'
        # store a ip and js pair together , make it unique and overwrite
        storeInAttackingTable(content)
        #getfromdb("Attacking", ["ip","js"],[content["ip"],content["js"]])
        search = ""
        ipOfAttack = ""
        jsOfAttack = ""
        ts = ""
        return render_template('home/attack.html', segment='attack', search=search, ipOfAttack = ipOfAttack, jsOfAttack = jsOfAttack,ts = ts, alldetails = content, allData = allData)



@blueprint.route('/blockManage',methods=['GET','POST'])
@login_required
def countryblock():  

    if(request.method == 'POST'):
        if "Bid" in request.form.keys():
            #print("here")
            id = request.form.get('Bid')
            #print(id)
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            cur.execute('Update Countries set blocked = 2 where id = "' + id + '";')
            conn.commit()
            conn.close()
        if "Uid" in request.form.keys():
            id = request.form.get('Uid')
            #print(id)
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            cur.execute('Update Countries set blocked = 0 where id = "' + id + '";')
            conn.commit()
            conn.close()
        if "Gid" in request.form.keys():
            id = request.form.get('Gid')
            #print(id)
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            cur.execute('Update Countries set blocked = 1 where id = "' + id + '";')
            conn.commit()
            conn.close()
    
    
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("Create table if not exists Countries (id text, name text, blocked integer);")
    l = getfromdb("Countries", ["name"], ["India"])
    if len(l) == 0:
        df = pandas.read_csv('countrylist.csv')
        s = "Insert into Countries values "
        for i in range (0, len(df['country'])):
            s += '("' + str(df['country'][i]) + '", "' + str(df['name'][i]) + '", 0), '
        m = list(s)
        m[-1] = ';'
        m[-2] = ' '
        s = ''.join(m)
        #print(s)
        cur.execute(s)
        conn.commit()
    allData = {}
    cur.execute('select id, name, blocked from Countries where blocked=0')
    desc = cur.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    allData['unblocked'] = data
    
    cur.execute('select id, name, blocked from Countries where blocked=1')
    desc = cur.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    allData['grey'] = data

    cur.execute('select id, name, blocked from Countries where blocked=2')
    desc = cur.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    allData['blocked'] = data
    conn.close()
    
    return render_template('home/blockManage.html', segment='blockManage', allData = allData)

@blueprint.route('/block',methods=['POST'])
def block():  
    try:
        if(request.method == 'POST'):
            name = request.form.get('name')
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            cur.execute('Update Countries set blocked = 1 where name = "' + name + '";')
            conn.commmit()
            conn.close()
    except:
        print('Table DNE')
    
    
@blueprint.route('/unblock')
def unblock():  
    try:
        if(request.method == 'POST'):
            name = request.form.get('name')
            conn = sqlite3.connect('db.sqlite3')
            cur = conn.cursor()
            cur.execute('Update Countries set blocked = 0 where name = "' + name + '";')
            conn.commit()
            conn.close()
    except:
        print('Table DNE')


@blueprint.route('/ipDetail/<template>')
def ipDetail(template):  
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("select * from Fingerprints where ip = '" + template + "';")
    desc = cur.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)

@blueprint.route('/cookieDetail/<template>')
def cookieDetail(template):  
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("select * from Fingerprints where cookie = '" + template + "';")
    desc = cur.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)

@blueprint.route('/parentDomain/<template>')
def parentDomainDetail(template):  
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("select * from Fingerprints where parentDomain = '" + template + "';")
    desc = cur.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    conn.close()
    return jsonify(data)

@blueprint.route('/vpn/pptp', methods=['GET','POST'])
def pptp():  
    ip = request.args["ip"]
    hostname, hoststate, oports = get_pptp(ip)
    values = {}
    values["hostname"] = hostname
    values["hoststate"] = hoststate
    values["oports"] = oports
    return jsonify(values)

@blueprint.route('/vpn/l2tp_ipsec', methods=['GET','POST'])
def l2tp():  
    ip = request.args["ip"]
    hostname, hoststate, oports, ike = get_l2tp_ipsec(ip)
    values = {}
    values["hostname"] = hostname
    values["hoststate"] = hoststate
    values["oports"] = oports
    values["IKE"] = ike
    return jsonify(values)

@blueprint.route('/vpn/openvpn', methods=['GET','POST'])
def ovpn():  
    ip = request.args["ip"]
    isOpenVpn = get_openvpn_tcp(ip)
    values = {}
    values["isOpenVpn"] = isOpenVpn
    return jsonify(values)

@blueprint.route('/vpn/sstp', methods=['GET','POST'])
def sstp():  
    ip = request.args["ip"]
    _sstp = get_sstp(ip)
    values = {}
    values["sstp"] = _sstp
    return jsonify(values)

@blueprint.route('/vpn/ike', methods=['GET','POST'])
def ike():  
    ip = request.args["ip"]
    ike = get_IKEv2(ip)
    values = {}
    values["ike"] = ike
    return jsonify(values)