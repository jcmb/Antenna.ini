#! /usr/bin/env python3

import configparser
import argparse
import string
import sys
from pprint import pprint

from JCMBSoftPyLib import HTML_Unit

def get_RINEX_Names(Section_Start_Line_Number,Antenna_ini):
   current_line=Section_Start_Line_Number
#   print ("Getting RINEX Names")
   RINEX_Names=[]
   while current_line < len(Antenna_ini)-1:
      current_line+=1
      if len(Antenna_ini[current_line])!=0:
         if Antenna_ini[current_line][0]=="[" and Antenna_ini[current_line][-1]=="]":
#            print ("Section {}".format(Antenna_ini[current_line]))
            break #Found a [] section header
         if Antenna_ini[current_line].lower().startswith("rinexname="): # We don't do this to the whole file to make sure the antenna lookup still works and we want the antenna name with the correct case
            RINEX_Name=Antenna_ini[current_line][len("rinexname="):]
#            print ("Checking")
            RINEX_Names.append(RINEX_Name)
   return(RINEX_Names)



def RINEX_Names(Antenna,Antenna_ini):
   Found=False
   line_number=0
   Antenna_Section="[{}]".format(Antenna)
   for line in Antenna_ini:
      if line == Antenna_Section:
         Found=True
         break
      line_number+=1

   if Found:
#      print ("Found Antenna {}".format(Antenna))
      return(get_RINEX_Names(line_number,Antenna_ini))
   else:
      print(("ERROR Did not Find Antenna {}".format(Antenna)))
      return([])



def read_antenna_ini(antenna_ini_path,HTML_File_Path):

   config = configparser.ConfigParser(strict=False)
   if  (config.read(antenna_ini_path) == []) :
      print ("Could not open antenna.ini")
      quit(10)

   with open (antenna_ini_path, "r") as myfile:
       antenna_ini_lines=myfile.read().splitlines()

   Antenna_Version=config.get("AntDatabaseInfo","Version")

   print("{}/{}.html".format(HTML_File_Path,Antenna_Version))
   HTML_File=open("{}/{}.html".format(HTML_File_Path,Antenna_Version),"w")

   HTML_Unit.output_html_header(HTML_File,"Antenna.INI Antennas for file version {}".format(Antenna_Version),120)
   HTML_Unit.output_html_body(HTML_File)




   HTML_File.write ("Version:{}</br>".format(Antenna_Version))

   groups= config.items("AntennaGroup")

   HTML_Unit.output_table_header(HTML_File,"Rinex Name","RINEX",["Trimble Name","Antenna","Name 1","Name 2","Name 3","Name 4","Name 5","Name 6","Name 7","Name 8","Name 9"])

   antenna_names={}
   antenna_type={}
   antenna_RINEX={}

   for group_details in groups:
      group=group_details[1]
#      pprint(group)
      antennas= config.items(group)

      antenna_index=1;
      try:
         antenna=config.get(group,"Ant"+str(antenna_index))
      except:
         continue

      while antenna:
         antenna_index+=1
         antenna_name=antenna.split(",")[0]
         if antenna_name=="Unkown Ext":
            antenna_name="Unknown Ext"

         antenna_trimble_name=config.get(antenna_name,"Name",fallback=antenna_name)
         antenna_names[antenna_name]=antenna_trimble_name
         antenna_RINEX[antenna_name]=RINEX_Names(antenna_name,antenna_ini_lines)

         try:
            antenna=config.get(group,"Ant"+str(antenna_index))

         except configparser.NoOptionError:
            antenna=""


      antenna_index-=1

   for antenna in sorted(antenna_names,key=antenna_names.get):
      HTML_Unit.output_table_row(HTML_File,[antenna_names[antenna],antenna]+antenna_RINEX[antenna])

   HTML_Unit.output_table_footer(HTML_File)
   HTML_Unit.output_html_footer(HTML_File,["RINEX"])
   HTML_File.close()


def main():

   parser = argparse.ArgumentParser(description='Display Information on antenna.ini.')

   parser.add_argument('--html', '-H',action="store_true",
                      help='Output the information in a format for including into HTML')

   parser.add_argument("file", help='Antenna.ini file')

   parser.add_argument("HTML", help='HTML Output directory')


   args = parser.parse_args()
   #print args.accumulate(args.integers)
   #print args

   read_antenna_ini(args.file,args.HTML)

#            pprint(SNM941_Results[SNM941])
#   HTML_File.write("<hr>Generated: {}".format(datetime.datetime.now()))

if __name__ == "__main__":
#    print(sys.argv)
#    print(len(sys.argv))

    main()
