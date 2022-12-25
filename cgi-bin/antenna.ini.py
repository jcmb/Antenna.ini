#! /usr/bin/env python3

import cgitb
#cgitb.enable()

import configparser
import argparse
import string
from pprint import pprint
import sys

parser = argparse.ArgumentParser(description='Display Information on antenna.ini.')

parser.add_argument('--version','-v',action="store_true", help='Display Version Information for the file')

parser.add_argument('--groups', '-s',action="store_true",
                   help='Display antenna group Information for the file')

parser.add_argument('--group', '-g',
                   help='Antennas in a group')

parser.add_argument('--html', '-H',action="store_true",
                   help='Output the information in a format for including into HTML')

parser.add_argument('--antenna', '-a',
                   help='Antenna Information')

args = parser.parse_args()
#print args.accumulate(args.integers)
#print args

config = configparser.ConfigParser(strict=False)


if  (config.read('/var/www/html/Antenna.ini/antenna.ini') == []) :
   if  (config.read('/Users/gkirk/Downloads/cfgfiles/antenna.ini') == []) :
      print("Could not open antenna.ini")
      quit(10)

if args.version :
   if args.html :
      print("Version:" , config.get("AntDatabaseInfo","Version") , "<br/>")
      print("Language:" ,config.get("AntDatabaseInfo","Language"))
   else:
      print(config.get("AntDatabaseInfo","Version"))
      print(config.get("AntDatabaseInfo","Language"))

if args.groups :
   groups= config.items("AntennaGroup")
   if args.html :
      print("Antenna Group: <select name=group>")

   for group in groups:
      if args.html :
         try :
            if group[1] == "SCS900" :
               print('<option selected value="' + group[1] + '">' + config.get(group[1],"Name") + '</option>')
            else:
               print('<option value="' + group[1] + '">' + config.get(group[1],"Name") + '</option>')
         except configparser.NoOptionError:
            print('<option value="' + group[1] + '">' + group[1] + '</option>')
      else:
         print(group[1])

   if args.html :
      print("</select>")


if args.group:
   try :
      antennas= config.items(args.group)
   except :
      print("Group" , args.group, "does not exist")
      quit(2)

   try :
      Name=config.get(args.group,"Name")
   except :
      Name=args.group

   if args.html :
      print("<h2>Antennas for group:")
      print(Name,"</h2>")
      print("Antennas: <select name=antenna>")
   else :
      print("Group Name: " , Name)
      print("Antennas:")

   antenna_index=1;
   antenna=config.get(args.group,"Ant"+str(antenna_index))
   antenna_names={}
   antenna_section_names={}
   antenna_type={}

   while antenna:
      antenna_section_names[antenna_index]=antenna.split(",")[0]

      try:
         antenna=config.get(args.group,"Ant"+str(antenna_index))
         antenna_names[antenna_index]=config.get(antenna_section_names[antenna_index],"Name")
         antenna_type[antenna_index]=config.get(antenna_section_names[antenna_index],"Type")
      except configparser.NoOptionError:
         antenna=""

      antenna_index+=1


   for antenna in sorted(antenna_names,key=antenna_names.get):
      if args.html:
          print('<option value="' + antenna_section_names[antenna] + '">' + antenna_names[antenna] + '</option>')
      else:
          print(antenna_section_names[antenna] + ': ' + antenna_names[antenna])


   antenna_index-=1

   if args.html :
      print("</select>")
   else :
      print("Number of Antennas: ", antenna_index)


if args.antenna:
   try :
      antenna=config.options(args.antenna)
   except :
      print("Antenna", args.antenna, "does not exist")
      quit(3)
   if args.html:
      print("<table border=\"1\"><thead><caption>Antenna Information:</caption></thead><tbody>")
      print("<tr><td>Antenna Section</td><td>" , args.antenna,"</td>")
      print("<tr><td>Antenna Name</td><td>" , config.get(args.antenna,"Name"),"</td>")
      print("<tr><td>Antenna Short (DC) Name</td><td>" , config.get(args.antenna,"DCName"),"</td>")
      print("<tr><td>Manufacturer</td><td>" , config.get(args.antenna,"Manufacturer"),"</td>")
      print("<tr><td>Part Number</td><td>" , config.get(args.antenna,"PartNumber"),"</td>")
      print("<tr><td>ID (Character Code)</td><td>" , config.get(args.antenna,"CharCode"),"</td>")
      print("<tr><td>ID (Type)</td><td>" , config.get(args.antenna,"Type"),"</td>")

      try:
         if config.get(args.antenna,"L5Capable") == "1":
            print("<tr><td>Freq</td><td> Triple </td>")
         else:
            if config.get(args.antenna,"Freq") == "2":
               print("<tr><td>Freq</td><td> Dual </td>")
            else:
               print("<tr><td>Freq</td><td> Dual </td>")
      except:
        if config.get(args.antenna,"Freq") == "2":
           print("<tr><td>Freq</td><td> Dual </td>")
        else:
           print("<tr><td>Freq</td><td> Dual </td>")


      try:
         if config.get(args.antenna,"WCapable") =="1":
            print("<tr><td>GLONASS</td><td> Yes </td>")
         else:
            print("<tr><td>GLONASS</td><td> No </td>")
      except:
         print("<tr><td>GLONASS</td><td> NO </td>")

      try:
         if config.get(args.antenna,"Beacon") :
            print("<tr><td>Beacon</td><td> Yes </td>")
         else:
            print("<tr><td>Beacon</td><td> No </td>")
      except:
            print("<tr><td>Beacon</td><td> NO </td>")


      print("<tr><td>Class</td><td>" , config.get(args.antenna,"Class"),"</td>")
      print("<tr><td>Added</td><td>" , config.get(args.antenna,"AddDate"),"</td>")

      print("</tbody>")
      print("</table><p/>")
   else:
      print("Antenna Information:")
      print("Antenna Section" , args.antenna)
      print("Antenna Name: " , config.get(args.antenna,"Name"))
      print("Antenna Short (DC) Name: " , config.get(args.antenna,"DCName"))
      print("Manufacturer: " , config.get(args.antenna,"Manufacturer"))
      print("Part Number: " , config.get(args.antenna,"PartNumber"))
      print("ID (Character Code): " , config.get(args.antenna,"CharCode"))
      print("ID (Type): " , config.get(args.antenna,"Type"))
      print("Freq: " , config.get(args.antenna,"Freq"))
      print("Class: " , config.get(args.antenna,"Class"))
      print("Added: " , config.get(args.antenna,"AddDate"))



   if args.html:
      print("<p/><table border=\"1\"><thead><caption>Antenna Measurement Methods:</caption>")
      print("<tr><th>ID</th><th>Method</th><th>Horizontal Offset (m)</th><th>Vertical Offset (m)</th></tr></thead><tbody>")
   else:
      print("")
      print("Measurement Methods:")

   method_index=0
   method=config.get(args.antenna,"MeasMethod"+str(method_index))
   while method:
      method_details=method.split("=")[0]
      (H_Offset,V_Offset,Tape_Offset,Method_Name)=method_details.split(",",3) # Some of the methods may have , in them so we have to use a max splits
      Method_Name=Method_Name.strip("\"")

      if args.html:
         print("<tr><td>{0}</td><td><a href=\"/antenna.html?HOffset={2}&VOffset={3}\">{1}</a></td><td>{2}</td><td>{3}</td></tr>".format(method_index,Method_Name,H_Offset,V_Offset))
      else:
         print(" Method ID: " ,  method_index , "Name:", Method_Name)
         print(" Horizontal Offset:", H_Offset, "(m)    Vertical Offset:", V_Offset, "(m)")
      method_index+=1
      try:
         method=config.get(args.antenna,"MeasMethod"+str(method_index))
      except configparser.NoOptionError:
         method=""

   if args.html:
      print("</tbody>")
      print("</table>")
   else :
      print("Number of measurment methods: ", method_index)
      print("Rinex Method:" ,config.get(args.antenna,"RINEXMethod"))


   if args.html:
      print("<p/><table border=\"1\"><thead><caption>Antenna Models:</caption></thead>")
      print("<tr><th>Type</th><th>File</th></tr>")
      print("<tbody>")
      try:
         if config.get(args.antenna,"PhaseCorrTable"):
            print('<tr><td>Trimble APC Model<td> <a target="_blank" href="/cgi-bin/Antenna.ini/pct_html.py?Name={0}&File={1}">{1}</a></td></tr>'.format(config.get(args.antenna,"Name"),config.get(args.antenna,"PhaseCorrTable")))
      except:
         pass

      try:
         if config.get(args.antenna,"NGSCorrTable"):
            print('<tr><td>NGS APC Model<td> <a target="_blank" href="/cgi-bin/Antenna.ini/pct_html.py?Name={0}&File={1}">{1}</a></td></tr>'.format(config.get(args.antenna,"Name"),config.get(args.antenna,"NGSCorrTable")))
      except:
         pass

      try:
         if config.get(args.antenna,"IFECorrTable"):
            print('<tr><td>IFE APC Model<td> <a target="_blank" href="/cgi-bin/Antenna.ini/pct_html.py?Name={0}&File={1}">{1}</a></td></tr>'.format(config.get(args.antenna,"Name"),config.get(args.antenna,"IFECorrTable")))
      except:
         pass

      print("</tbody>")
      print("</table></p>")

#      print "Image: ", config.get(args.antenna,"GraphicsFile")
      if config.get(args.antenna,"GraphicsFile"):
         print('<img src="/Antenna.ini/{0}">'.format(config.get(args.antenna,"GraphicsFile")))

   else:
      print("")
      print("Antenna Models:")
      print("Trimble APC Model: " , config.get(args.antenna,"PhaseCorrTable"))
      print("NGS APC Model: " , config.get(args.antenna,"NGSCorrTable"))
      print("IFE APC Model: " , config.get(args.antenna,"IFECorrTable"))

# The Rinex names section of the antenna.ini is nuts in that it has mutiple keys with the same name instead of a number like the methods
# The standard python parsers doesn't deal with this by default and since it is the Rinex names I am ignoreing this
#   print ""
#   print "Rinex Names:"
#   rinex=config.get(args.antenna,"RinexName")
#   print rinex

