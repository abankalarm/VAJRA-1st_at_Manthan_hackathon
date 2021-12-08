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

    # cur.execute("SELECT DISTINCT (ip) FROM Fingerprints;")
    # desc = cur.description 
    # column_names = [col[0] for col in desc] 
    #data = [dict(zip(column_names, row)) for row in cur.fetchall()]
    # #print(data)
    
    # allData["IP"]=data
    
    allData["IP"]=json.loads(  vpnDetails(allData["IP"]).data  ) 

    
        
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

    cur.execute("SELECT COUNT( DISTINCT ip) as cnt FROM Fingerprints where isVpnTime = 'true'; ")
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

@blueprint.route('/injection')
def injection():
    #request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ip="111.223.26.202"
    #ip = request.environ['REMOTE_ADDR']
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

@blueprint.route('/search', methods=['GET','POST'])
@login_required
def searchpost():
    if (request.method == 'POST'):
        #print("WWW",request.form)
        search = request.form['search']
        isBad,asn,result=getDetails(search)
        ips=[]
        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()
        cur.execute("Select cookie from Fingerprints where ip='"+str(search)+"'")
        desc = cur.description 
        column_names = [col[0] for col in desc]
        try: 
            data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        except:
            data = []

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



        for ip in uip:
            cur.execute("Select * from Fingerprints where ip='"+ip+"'" )
            desc = cur.description 
            column_names = [col[0] for col in desc] 
            data = [dict(zip(column_names, row)) for row in cur.fetchall()]
            allDataIP[ip]=data
            #print(allData[ip])
        riskData=[{"IP":search}]
        #print(allDataIP)


        vpnDetails(riskData)
        #print(riskData)
        allData={}
        ASN_name = riskData[0]['asn'][4]
        try:

            if isBad :
                allData["Bad ASN"]=80
                badASN=" Is a Bad ASN"
            else:
                allData["Bad ASN"]=0
                badASN="Not a Bad ASN "
        except:
            allData["Bad ASN"]=0
            badASN="Not a Bad ASN"
        
        try:

            if riskData[0]["dc"] :
                allData["data center"]=50
                datacenter= "Is a Data Center"
            else:
                allData["data center"]=0
                datacenter="Not a Data Center"
        except:
            allData["data center"]=0
            datacenter="Not a Data Center"
        try:
            if riskData[0]["bl"] :
                allData["blacklisted"]=100
                blacklisted="Blacklisted"
            else:
                allData["blacklisted"]=0
                blacklisted="Not Blacklisted"
        except:
            allData["blacklisted"]=0

        # change hardcoded
        Alldata_for_searched_ip = {}
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("Select * from Fingerprints where ip='"+str(search)+"'")
    
        Alldata_for_searched_ip = {}
        
        desc = cur.description 
        column_names = [col[0] for col in desc] 
        data = [dict(zip(column_names, row)) for row in cur.fetchall()]
        #Alldata_for_searched_ip["data"] = data
        Alldata_for_searched_ip['data'] = data
        
    
        # return Alldata_for_searched_ip
        # all data returned for ip is what you need for most of the top part of search page
        conn1 = sqlite3.connect('ip-index.db')
        cur1=conn1.cursor()
        intip=int(ipaddress.ip_address(search))
        s="SELECT country FROM Countries WHERE start ="+ search.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"
        cur1.execute(s)
        cname=cur1.fetchall()[0][0]
        conn1.close()
        
        cur.execute("Select blocked from Countries where id='"+cname.upper()+"'")
        desc = cur.description 
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) for row in cur.fetchall()][0]

        #print("@@@@@@@",data)
        
        try:   
            if data["blocked"]==1 :
                allData["grey "]=50
            else:
                allData["grey"]=0
        except:
            allData["grey"]=0

        try:
            if data["blocked"]==2 :
                allData["black "]=100
            else:
                allData["black"]=0

        except:
            allData["black"]=0

        cur.execute("Select isVpnTime from Fingerprints where ip='"+search+"'")
        desc = cur.description 
        column_names = [col[0] for col in desc] 
        try:

            data = [dict(zip(column_names, row)) for row in cur.fetchall()][0]
            
            if data["isVpnTime"]:
                allData["Timezone"]=70
            else:
                allData["Timezone"]=0

        except:
            allData["Timezone"]=0

        allData["per"]=allData["Timezone"]+allData["black"]+allData["grey"]+ allData["blacklisted"]+allData["data center"]+allData["Bad ASN"]
        ratingcolor = "green"
        if(allData["per"]>100):
            ratingcolor = "orange"
        if(allData["per"]>100):
            allData["per"] = 100
            ratingcolor = "red"


        try:
            if Alldata_for_searched_ip["data"][0]['isVpnASN'] or Alldata_for_searched_ip["data"][0]['isVpnTime']:
                isVPN = "True"
        except:
            isVPN="False"
        try:
            isp = Alldata_for_searched_ip["data"][0]['isp']
        except:
            isp="Not Available"
        try:
            region = Alldata_for_searched_ip["data"][0]['regionName']
        except:
            region="Not Available"
        try:
            zipcode = Alldata_for_searched_ip["data"][0]['zip']
        except:
            zipcode="Not Available"
        try:
            lat_long = str(Alldata_for_searched_ip["data"][0]["lat"]) + " & " + str(Alldata_for_searched_ip["data"][0]["lon"])
        except:
            lat_long="Not Available"
        try:
            country = Alldata_for_searched_ip["data"][0]['country']
        except:
            country="Not Available"
        #print(allData.keys())
        cur.execute("Select * from Fingerprints where ip ='" + search + "'")
        desc = cur.description 
        column_names = [col[0] for col in desc] 
        try:
            data = [dict(zip(column_names, row)) for row in cur.fetchall()][0]
        except:
            data = []
        
        conn.close()
        ##print("@@@@@@",Alldata_for_searched_ip)
        allDataIP['keyList'] = list(allDataIP.keys())
        allDataIP['cols'] = ['cookie', 'timezone', 'userAgent', 'timestamp']
        dataWithThisIp = {}
        dataWithThisIp['data'] = data
        dataWithThisIp['cols'] = ['cookie', 'userAgent', 'timestamp', 'parentDomain']
        return render_template('home/search.html', isVPN=isVPN,allDataIP=allDataIP, isp=isp, region=region, zipcode=zipcode, lat_long=lat_long, country=country, segment='search',badASN=badASN, datacentre = datacenter, blacklisted=blacklisted, ASN_name=ASN_name, result=result, ip = search, asn = asn, bad = isBad, Alldata_for_searched_ip = Alldata_for_searched_ip,allData=allData, dataWithThisIp = dataWithThisIp)
    else:
        allDataIP = {}
        dataWithThisIp = {}
        print(dataWithThisIp)
        ratingcolor = "green"
        allData={}
        allData["per"]=0
        allData["Timezone"]=0
        allData["black"]=0
        allData["grey"]=0
        allData["blacklisted"]=0
        allData["data center"]=0
        allData["Bad ASN"]=0
        Alldata_for_searched_ip = {}
        return render_template('home/search.html', ratingcolor=ratingcolor, segment='search', allData=allData, Alldata_for_searched_ip = Alldata_for_searched_ip, dataWithThisIp = dataWithThisIp, allDataIP = allDataIP)
    
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
        return render_template('home/tracking.html', segment='tracking', uploadf=uploadf, name = name, allData=allData, searchData=searchData)
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
    if data==[]:
        ip = request.environ['REMOTE_ADDR']
        #TODO delete default value after hosting
        ip='203.192.236.244'
        data=[{"IP":ip}]
    for i in range (len(data)):
        try:
            ip=data[i]["IP"]
            intip=int(ipaddress.ip_address(ip))
            cur=conn.cursor()
            #print(ip,type(ip),intip,type(intip))
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
            data[i]["bl"]=a
            data[i]["dc"]=b
            data[i]["asn"]=c[0]
            data[i]["cn"]=d[0]
            #print(a,b,c,d)
            inBad=c[0][3] in badASN
            data[i]["bad"]=inBad
        except:
            data[i]["bl"]=[]
            data[i]["dc"]=[]
            data[i]["asn"]=[]
            data[i]["cn"]=[]
            data[i]["bad"]=False
            
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
        l = getfromdb('Attacking', ['timestamp'], [''])
        allAttacked = int(data[0]['cnt']) - 1
        allIpsToBeAttacked = len(l) - 1

        s="SELECT * FROM blacklisted WHERE start ="+ ip.split(".")[0]+ " AND " + str(intip)+" between first AND last LIMIT 1"
        cur.execute(s)
        a=cur.fetchall()
        conn.close()
    except:
        allAttacked = 0
        allIpsToBeAttacked = 0
    allData['allAttacked'] = allAttacked
    allData['allIpsToBeAttacked'] = allIpsToBeAttacked
    if(request.method == 'POST'):
        if request.form.get('mode') == "add":
            # store a ip and js pair together , make it unique and overwrite
            IP = request.form.get('ipaddr')
            JS = request.form.get('jsoffsec')
            content = {}
            content['ip'] = IP
            content['js'] = JS
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
        content['timestamp'] = ''
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