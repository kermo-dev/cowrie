#!/usr/bin/env python
# *-* coding: iso-8859-1 *-*

print("############################################")
print("# Honey Pot Crowie activity analyser  v1.0 #")
print("#------------------------------------------#")
print("#- v1.0 | creation               |06/2020 -#")
print("#------------------------------------------#")
print("# from daily logs analyse visits           #")
print("#- cmd.txt   : all commands type           #")
print("#- ip.txt    : ip address and localisation #")
print("#- map.html  : graphical localisation      #")
print("############################################")

#libraries module
import unicodedata
import os
import sys
import json
import geoip2.webservice
import geoip2.database
import folium
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
print ("# 1-> libraries import done")

#open log file
recup = []
fichier = open("./log/cowrie.log.2020-06-02", "r")
for line in fichier:
    recup.append(line)
print("# 2-> " + str(len(recup)) + " line(s) imported")
fichier.close()

#Extract IP, password, add localisation information
table = []
j=0
reader = geoip2.database.Reader('GeoLite2-City.mmdb')
for i in range(len(recup)):
  x=str(recup[i])
  scanning = x.find("succeeded")
  if scanning > 0:
    work = x.split(",")
    fin_ip = work[2].find("]")
    ip=work[2][:fin_ip]
    temp=work[2].split("'")
    pwd=temp[3]
    geo = reader.city(ip)
    city = geo.city.name
    toto = geo.location.latitude
    connect = ip + ";" + str(city) + ";" + pwd + ";" + str(geo.location.latitude) + ";" + str(geo.location.longitude) + ";"
    table.append(connect)
    j+=1
reader.close()

#Output ip / password information file
print("# 3-> IP/PWD file  : ip.txt")
fichier = open("ip.txt", "w")
for i in range(len(table)):
  fichier.write(table[i]+"\n")
fichier.close()

#Extract commands
cmd = []
j=0
for i in range(len(recup)):
  x=str(recup[i])
  scanning = x.find("Command found:")
  if scanning > 0:
    _cmd = x[scanning+15:len(x)-1]+";"
    cmd.append(_cmd)
    j+=1

#Output commands information file
print("# 4-> CMD file : cmd.txt")
fichier = open("cmd.txt", "w")
for i in range(len(cmd)):
  fichier.write(cmd[i]+"\n")
fichier.close()

#Preparation for map construction
affiche = []
for i in range(len(table)):
  x=table[i].split(";")
  loc = []
  lat=x[3]
  long=x[4]
  loc.append(float(x[3]))
  loc.append(float(x[4]))
  affiche.append(table[i]+str(loc)+";")

carte = []
for i in range(len(affiche)):
  x=affiche[i].split(";")
  rec = x[5]
  cpt=1
  for j in range(len(affiche)):
    y=affiche[j].split(";")
    if y[5] == rec:
      cpt+=1
  carte.append(affiche[i]+ str(cpt)+ ";")
print("# 5-> " + str(len(carte)) + " plots build")  

#Build a world map with the plots
m = folium.Map(location=[20,0], zoom_start=1)

for i in range(len(carte)):
  x=carte[i].split(";")

  loc = []
  lat=x[3]
  long=x[4]
  loc.append(float(x[3]))
  loc.append(float(x[4]))
  zone = int(x[6])*2000
  folium.Circle(location=loc,
             radius=zone,
             color='red',
             weight=1,
             popup=x[1]+":"+x[6]).add_to(m)
  
m.save('map.html')
print("# 6-> map file : map.html")
print("############################################")
