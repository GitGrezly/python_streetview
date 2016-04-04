import xml.etree.ElementTree as ET
import urllib
tree = ET.parse('/path/to//test.gpx')
root = tree.getroot()
import math
#print root.tag
old_lat = 0
old_lon = 0
new_lat = 0
sleutel="google_key"
new_lon = 0
bestandsnaam="/tmp/files"
bestandsnaam_maps="/tmp/maps"
var = raw_input("Wil je de afbeeldingen ook al downloaden? [N\j]")
if var.lower() == "j":
    print "Alle bestanden worden ook gedownload"
    open(bestandsnaam, 'w').close()
    open(bestandsnaam_maps, 'w').close()
else:
    print "De waardes worden alleen geprint"
    
def geturl(lat,lon, heading):
    return "https://maps.googleapis.com/maps/api/streetview?size=700x700&key="+ sleutel+"&location="+lat+","+lon+"&heading="+str(heading)+"&pitch=-0"

def getmaps(lat,lon):
    return "https://maps.googleapis.com/maps/api/staticmap?zoom=13&size=150x150&maptype=roadmap&markers=color:blue|label:S|"+lat+","+ lon +"&key="+ sleutel

def calculate_initial_compass_bearing(pointAlat,pointAlon, pointBlat, pointBlon):
    lat1 = math.radians(pointAlat)
    lat2 = math.radians(pointBlat)

    diffLong = math.radians(pointBlon - pointAlon)

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)
    compass_bearing = math.degrees(initial_bearing)
   # compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
number = 0
i = 0
aantal = 0
import os
import shutil
directory="/tmp/googlemaps_gps"
if number == 0:
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        shutil.rmtree(directory)
        os.makedirs(directory)
for amount in root.iter('trkpt'):
    aantal+=1

for gps in root.iter('trkpt'):
    i+=1
    if i >= number:
        old_lat = new_lat
        old_lon = new_lon
        new_lat = float(gps.attrib['lat'])
        new_lon = float(gps.attrib['lon'])
        string = geturl(str(new_lat), str(new_lon), str(calculate_initial_compass_bearing(old_lat,old_lon,new_lat,new_lon)))
        maps_string = getmaps(str(new_lat), str(new_lon))
        bestandsnaam_write=str('/tmp/googlemaps_gps/%s.jpg'%(i)) 
        bestandsnaam_maps_write=str('/tmp/googlemaps_gps/maps_%s.jpg'%(i)) 
        if var.lower() == "j":
            print "Download foto %s/%s (%s)"%(i,aantal,string)
            urllib.urlretrieve(string, filename=bestandsnaam_write)
            print "Download maps %s (%s)"%(i,maps_string)
            urllib.urlretrieve(maps_string, filename=bestandsnaam_maps_write)
