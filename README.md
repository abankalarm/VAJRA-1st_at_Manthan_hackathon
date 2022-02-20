# VAJRA BY TEAM INDRA - Rendering VPNs obsolete
### *WINNERS (1st RANK)* AT MANTHAN 2021 Organised BY: The Bureau of Police Research and Development, Ministry of Education's Innovation Cell (MIC) & AICTE (India)

### Novel Approach
The solution creates a c2 server that can be integrated with N number of websites, this allows the authority to track any visitor irrespective of whether they use a vpn or not. 

It is a complete solution that has been deployed and tested live, other than just this it also boasts additional integration of tracking pixels as well as an attack module that allows the authority to serve a unique javascript/response to a targeted visitor in real time irrespective of whether they use a vpn or not. All of which integrates with the main view.

It also provides a map like approach which gives a pictorial representation of how the connection was tunneled across web with source and destination arrows.

Other features:
- Attack unseen ips and search for them
- country wise black listing (as well as grey lists)
- Internal network scan
- Port scan through browser
- Tor detection

Vpn Detection using:
- ASN lists
- blacklist ip
- realtime detection if ip offers vpn protocols
- browser time and ip location time mismatch

Getting hidden IP:
- Webrtc leaks
- browser fingerprint matching
- cookie matching
- tracking pixels

# A simple overview using a diagram
![Functioning](https://github.com/abankalarm/VAJRA-1st_at_Manthan_hackathon/blob/main/Network%20diagram%20example.png)

# Amount of info[REDACTED] accumulated for each visitor
```
[
  {
    "_id": 1, 
    "addBehavior": 0, 
    "audio": "124.04347527516074", 
    "availableScreenResolution": "[824, 1536]", 
    "bookmarked": 0, 
    "browserLat": 404, 
    "browserLong": 404, 
    "canvas": "canvas winding:yes,canvas fp:data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAB9AAAADICAYAAACwGnoBAAAAAXNSR0IArs4c6QAAIABJREFUeF7s3Xl8XXWd//HXSdJ9A1qgLdBSSssmWwVEBkXUEQUXGBUcBa0shQFBmRGdGWVE0RkVHRUUoSx2Rp2Hy8yAg6AwjKDwQ0AEC7JT6AZlaaEb3ZLc83t8Tu5Jb25vknuTmzShr+/jwSNN7vku53luwh/v+/l+EwZ4S0l3AfYH9gGmA1OBScCE4r8r3cEiYDmwDIh/LwAeBR5KSJ7NO6Sko4B9gf1Kvm4PjACGF7/Gv/P/ouv6sv82FL9/BXgYeCT/mpC82r6.....................VRAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQIECgpIKCX1DWbAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAAECBKoRENCrOZVFCRAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQKCkgIBeUtdsAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgQIEKhGQECv5lQWJUCAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIGSAgJ6SV2zCRAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQKAaAQG9mlNZlAABAgQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgRKCgjoJXXNJkCAAAECBAgQIECAAAECBAgQIECAAAECBAgQIECAAIFqBAT0ak5lUQIECBAgQIAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAoKfAxezO2TxnqrJ4AAAAASUVORK5CYII=", 
    "city": "Delhi", 
    "clientID": "20de5b3fc1607c8eab366427bba71bb9", 
    "colorDepth": 24, 
    "cookie": "20de5b3fc1607c8eab366427bba71bb9", 
    "country": "India", 
    "countryCode": "IN", 
    "cpuClass": "not available", 
    "deviceMemory": 4, 
    "domain": "http://127.0.0.1:5000/injection", 
    "fonts": "ArialArial BlackArial NarrowBook AntiquaBookman Old StyleCalibriCambriaCambria MathCenturyCentury GothicCentury SchoolbookComic Sans MSConsolasCourierCourier NewGeorgiaHelveticaImpactLucida BrightLucida CalligraphyLucida ConsoleLucida FaxLucida HandwritingLucida SansLucida Sans TypewriterLucida Sans UnicodeMicrosoft Sans SerifMonotype CorsivaMS GothicMS PGothicMS Reference Sans SerifMS Sans SerifMS SerifPalatino LinotypeSegoe PrintSegoe ScriptSegoe UISegoe UI LightSegoe UI SemiboldSegoe UI SymbolTahomaTimesTimes New RomanTrebuchet MSVerdanaWingdingsWingdings 2Wingdings 3", 
    "hardwareConcurrency": 8, 
    "hasLiedBrowser": 0, 
    "hasLiedLanguages": 0, 
    "hasLiedOs": 0, 
    "hasLiedResolution": 0, 
    "indexedDb": 1, 
    "ip": "11xxxxx02", 
    "isTOR": 0, 
    "isVpnASN": "false", 
    "isVpnSomething": "NA", 
    "isVpnTime": "false", 
    "isp": "Bencxxxxtech", 
    "language": "en-IN", 
    "lat": 2xxx2, 
    "localStorage": 1, 
    "lon": 7xxxxx73, 
    "openDatabase": 1, 
    "openPorts": "80, 21, 22", 
    "parentDomain": "127.0.0.1", 
    "platform": "Win32", 
    "plugins": "gAWVEgIAA...............................................kZpRlZWVlLg==", 
    "region": "DL", 
    "regionName": "National Capital Territory of Delhi", 
    "screenResolution": "[864, 1536]", 
    "sessionStorage": 1, 
    "timestamp": "Wed Dec 08 2021 15:20:31 GMT+0530 (India Standard Time)", 
    "timezone": "Asia/Calcutta", 
    "timezoneOffset": -330, 
    "touchSupport": "2,False,False", 
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36", 
    "webdriver": 0, 
    "webgl": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAACW.............................................sion:0,webgl fragment shader medium int precision rangeMin:31,webgl fragment shader medium int precision rangeMax:30,webgl fragment shader low int precision:0,webgl fragment shader low int precision rangeMin:31,webgl fragment shader low int precision rangeMax:30", 
    "webglVendorAndRenderer": "Google........14046.3)", 
    "zip": "11...4"
  },
```

# Pictures

Vajra is well capable and was tested with more than 20 ips linked in a complex relationship, and 100 ips in total. 
Below is just few ss that I put together quickly without simulating any scenrios.

## Dashboard
![](https://github.com/abankalarm/VAJRA-1st_at_Manthan_hackathon/blob/main/pics/dash.png)

## A safe ip with info in map about a vpn used previously in graph
![](https://github.com/abankalarm/VAJRA-1st_at_Manthan_hackathon/blob/main/pics/whitelist.jpg)

## Scanning for protocols
![](https://github.com/abankalarm/VAJRA-1st_at_Manthan_hackathon/blob/main/pics/protocols.png)

## Design 
![](https://github.com/abankalarm/VAJRA-1st_at_Manthan_hackathon/blob/main/pics/menu.png)

## Tacking pixels 
![](https://github.com/abankalarm/VAJRA-1st_at_Manthan_hackathon/blob/main/pics/pixels.png)

## Attack page
![](https://github.com/abankalarm/VAJRA-1st_at_Manthan_hackathon/blob/main/pics/attack%20page.png)
