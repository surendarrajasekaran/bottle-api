import googlemaps
from datetime import datetime
from bottle import request, response
from bottle import post, get, put, delete
import os
from bottle import route, run, template
import xml.etree.ElementTree as ET
import io
import json
import ast

gmaps = googlemaps.Client(key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

@route('/getAddressDetails', method='POST')
def do_login():
    output = { "coordinates": { "lat": "lat", "lng": "lng"}, "address": "address" } 
    xml_output='''<?xml version="1.0" encoding="UTF-8"?> 
    <root>
<address></address>
<coordinates> <lat></lat> <lng></lng>
</coordinates> 
</root>
'''
    requestBody=request.body
    byte_str = requestBody.read()
    text_obj = byte_str.decode('UTF-8')
    r=ast.literal_eval(text_obj)
    s1 = json.dumps(r)
    s =json.loads(s1)
    geocode_result = gmaps.geocode(s['address'])
    lat=geocode_result[0]['geometry']['location']['lat']
    lng=geocode_result[0]['geometry']['location']['lng']
    if(s['output_format']=="json"):
        output['coordinates']["lat"]=lat
        output['coordinates']["lng"]=lng
        output['address']=s['address']
        return output
    elif(s['output_format']=="xml"):
        myroot = ET.fromstring(xml_output)
        myroot.find('address').text=s['address']
        print(myroot.find('address').text)
        for x in myroot.findall('coordinates'):
            x.find('lat').text=str(lat)
            x.find('lng').text=str(lng)
        xmlstr = ET.tostring(myroot, encoding='utf8', method='xml')
        return xmlstr
    else:
        return "unsupported output_format Format"
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    run(host='0.0.0.0', port=port, debug=True)
