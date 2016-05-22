'''
Convert via http://www.gpsvisualizer.com de GPS uit Garmin naar een GPX file.
Zorg er dan voor dat het bestand begint met <trk> en eindigt met </trk>, haal alles ervoor en erna weg

Na het uitvoeren van dit bestand 'convert_images.sh'  uitvoeren.
Als laatste stap dient ffmpeg uitgevoerd te worden, om een film van het geheel te maken
/home/dave/ffmpeg/bin/ffmpeg -framerate 10/1 -i caption_%04d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4

'''

import xml.etree.ElementTree as ET
import urllib.request
tree = ET.parse('/path/to/test.gpx')
root = tree.getroot()
import math
import os
import shutil
import os.path
import math


old_lat = 0
old_lon = 0
new_lat = 0
total_km = 0
diff_km = 0
old_km = 0
new_km = 0

bestandsnaam="/tmp/files"
bestandsnaam_maps="/tmp/maps"
bestandnaam_logging="/tmp/error_logging"
sleutel="google_key"
new_lon = 0
var = input("Wil je de afbeeldingen ook al downloaden? [N\j]")
if var.lower() == "j":
    print("Alle bestanden worden ook gedownload")
else:
    print("De waardes worden alleen geprint")
    
skip_already_downloaded = input("Wil je bestaande bestanden overschrijven?")
if skip_already_downloaded.lower() == "j":
    print("Alles wordt opnieuw gedownload")
else:
    print("Bestaande bestanden worden niet opnieuw gedownload")    
    
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

    return compass_bearing

def calculate_in_between_points(old_lat, old_lon, new_lat, new_lon):
    p = 0.017453292519943295
    c = math.cos
    a = 0.5 - math.cos((new_lat - old_lat) * p)/2 + math.cos(old_lat * p) * math.cos(new_lat * p) * (1-math.cos((new_lon-old_lon) * p )) /2
                       
    return 12742 * math.asin(math.sqrt(a))

number = 0
i = 0
aantal = 0

directory="/tmp/googlemaps_gps"
if number == 0:
    if not os.path.exists(directory):
        print("Maak directory \""+directory+"\" aan")
        os.makedirs(directory)
    elif skip_already_downloaded == "j":
        print("Verwijder directory \""+directory+"\"")
        shutil.rmtree(directory)
        os.makedirs(directory)
for amount in root.iter('trkpt'):
    aantal+=1
bestandsnaam_file_write_file = open(bestandsnaam, 'w')
bestandsnaam_maps_write_file =  open(bestandsnaam_maps, 'w')
bestandsnaam_logging_write_file =  open(bestandnaam_logging, 'w')


for gps in root.iter('trkpt'):
    i+=1
 
    if i >= number:
        try:
            number_download = str(i).zfill(len(str(aantal)))
            old_lat = new_lat
            old_lon = new_lon
            new_lat = float(gps.attrib['lat'])
            new_lon = float(gps.attrib['lon'])
            string = geturl(str(new_lat), str(new_lon), str(calculate_initial_compass_bearing(old_lat,old_lon,new_lat,new_lon)))
            if i > 2:
                diff_km = calculate_in_between_points(old_lat, old_lon,new_lat, new_lon)
                total_km += diff_km
                #print("%s:%s -- %s:%s --> %s"%(old_lat, old_lon, new_lat, new_lon, round(total_km,2)))
            maps_string = getmaps(str(new_lat), str(new_lon))
            bestandsnaam_write=str('/tmp/googlemaps_gps/%s.jpg'%(number_download)) 
            bestandsnaam_maps_write=str('/tmp/googlemaps_gps/maps_%s.jpg'%(number_download)) 
            bestand_naam_write_total_km = open('/tmp/googlemaps_gps/km_%s.txt'%(number_download),'w')
            bestand_naam_write_total_km.write(str(round(total_km,2)))
            bestand_naam_write_total_km.close()
            bestandsnaam_file_write_file.write(maps_string+"\n")
            bestandsnaam_maps_write_file.write(string+"\n")
            if var.lower() == "j":            
                if (os.path.isfile(bestandsnaam_write) == True and skip_already_downloaded == "j") or os.path.isfile(bestandsnaam_write) == False :
                    print("Download foto %s/%s (%s)"%(number_download,aantal,string))
                    urllib.request.urlretrieve(string, filename=bestandsnaam_write)
                if (os.path.isfile(bestandsnaam_maps_write) == True and skip_already_downloaded == "j") or os.path.isfile(bestandsnaam_maps_write) == False :
                    print("Download maps %s (%s)"%(number_download,maps_string))
                    urllib.request.urlretrieve(maps_string, filename=bestandsnaam_maps_write)
        except Exception as e:
            bestandsnaam_logging_write_file.write("ERROR met foto: "+str(number_download)+" "+ str(e) +" \n")
            
bestandsnaam_file_write_file.close()
bestandsnaam_maps_write_file.close()