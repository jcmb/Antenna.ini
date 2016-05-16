#! /usr/bin/python

import cgitb

import matplotlib
matplotlib.use('Agg')


import re
import sys
from pprint import pprint
import matplotlib.pyplot as plt
import base64
import tempfile
import numpy as np
from array import array

import math
import cgi

def parse_antenna_ini (File_Name):
   file=open("/var/www/Antenna.ini/"+File_Name,"r")
   Biases=[]
   Elev_Labels=[]
   Have_L1=False
   Have_L2=False
   L1_Biases={}
   L2_Biases={}



   for line in file:
   #   print line
   #   print len(line)
      line=line.rstrip()
      if len(line) > 0:
         if line[0] != ";":
            match =re.match("L1NominalOffset *= *([-+]?\d*\.\d+|\d+) +([-+]?\d*\.\d+|\d+) +([-+]?\d*\.\d+|\d+)",line)
            if match:
               L1_N=float(match.group(1))
               L1_E=float(match.group(2))
               L1_U=float(match.group(3))
               Have_L1=True
            else:
               match =re.match("L2NominalOffset *= *([-+]?\d*\.\d+|\d+) +([-+]?\d*\.\d+|\d+) +([-+]?\d*\.\d+|\d+)",line)
               if match:
                  L2_N=float(match.group(1))
                  L2_E=float(match.group(2))
                  L2_U=float(match.group(3))
                  Have_L2=True
               else:
                  match =re.match("ElevationRange *= *([-+]?\d*\.\d+|\d+) +([-+]?\d*\.\d+|\d+) +([-+]?\d*\.\d+|\d+)",line)
                  if match:
                     Elev_Start=int(match.group(1))
                     Elev_Stop=int(match.group(2))
                     Elev_Step=int(match.group(3))
                  else:
                     match =re.match("AzimuthStep *= *([-+]?\d*\.\d+|\d+)",line)
                     if match:
                        Az_Step=int(match.group(1))
                        if Az_Step==0:
                           Az_Step=360
#                           sys.exit("Azimuth Dependent Files are not supported")
                     else:
                        match =re.match("AZ *= *([-+]?\d*\.\d+|\d+)",line)
                        if match:
                           pass
                           #print match.group(1)
                        else:
                           match=re.match("( *[-+]?\d*\.\d+|\d+)",line)
                           while match:
                              Biases.append(float(match.group(1)))
                              line=line[len(match.group(1)):]
                              match=re.match("( *[-+]?\d*\.\d+|\d+)",line)
   #                           print numbers
   #print Elev_Start,Elev_Stop,Elev_Step
   for elev in xrange(Elev_Start,Elev_Stop+Elev_Step,Elev_Step): #We need to make sure we get the last item in the list
      Elev_Labels.append(elev)

   i=0

   for Az in xrange(0,360,Az_Step):
      L1_Biases[Az]=[]
      L2_Biases[Az]=[]

      if Have_L1:
         for elev in xrange(Elev_Start,Elev_Stop+Elev_Step,Elev_Step): #We need to make sure we get the last item in the list
            #   print elev, Biases[i]
            L1_Biases[Az].append(Biases[i])
            i=i+1
      #   print "L1: ", L1_Biases

      if Have_L2:
         for elev in xrange(Elev_Start,Elev_Stop+Elev_Step,Elev_Step): #We need to make sure we get the last item in the list
            L2_Biases[Az].append(Biases[i])
         #   print elev, Biases[i]
            i=i+1
      #   print "L2: ", L2_Biases
   file.close()

   if Have_L1:
      L1=(L1_N,L1_E,L1_U)
   else:
      L1=None

   if Have_L2:
      L2=(L2_N,L2_E,L2_U)
   else:
      L2=None

   return (L1,L2,Az_Step,Elev_Labels,L1_Biases,L2_Biases,Elev_Start,Elev_Stop,Elev_Step)

def create_plot (Title,L1,L2,Az_Step,Elev_Labels,L1_Biases,L2_Biases):
   plt.figure(figsize=(8,6),dpi=100)

   Have_L1=L1!=None
   Have_L2=L2!=None

   if Have_L1:
      if Az_Step != 360:
         for Az in xrange(0,360,Az_Step):
            plt.plot(Elev_Labels,L1_Biases[Az],label="L1 " + str(Az))
      else:
         plt.plot(Elev_Labels,L1_Biases[0],label="L1" )


   if Have_L2:
      if Az_Step != 360:
         for Az in xrange(0,360,Az_Step):
            plt.plot(Elev_Labels,L2_Biases[Az],label="L2 " + str(Az))
      else:
         plt.plot(Elev_Labels,L2_Biases[0],label="L2")

   plt.ylabel("Bias (mm)")
   plt.xlabel("Elevation (degrees)")
   if Az_Step == 360:
      plt.legend()
   plt.title("Antenna Phase Biases: " + Title)
   #plt.suptitle("Antenna Phase Biases")
   #plt.grid()
   #plt.show()
   tmp_file=tempfile.SpooledTemporaryFile()
   plt.savefig(tmp_file,format="Png")
   tmp_file.seek(0)
   img_data=base64.b64encode(tmp_file.read(-1))
   tmp_file.close()
   return(img_data)


def html_header(Title,Filename):
   print '<html><head><link rel="stylesheet" type="text/css" href="/css/tcui-styles.css"><style type="text/css">th, td {width: 80px;};</style><style type="text/css">img {display: block; margin-left: auto; margin-right: auto ;};</style>'
   print "<title>Antenna Phase Biases for {} ({})</title></head>".format(Title,Filename)
   print """
<body class="page">
<div class="container clearfix">
  <div style="padding: 10px 10px 10px 0 ;"> <a href="http://construction.trimble.com/">
        <img src="/images/trimble-logo.jpg" alt="Trimble Logo" id="logo"> </a>
      </div>
  <!-- end #logo-area -->
</div>
<div id="top-header-trim"></div>
<div id="content-area">
<div id="content">
<div id="main-content" class="clearfix">
"""
   print "<h1 align=\"center\">Antenna Phase Biases for {}<br/>{}</h1><p/>".format(Title,Filename)

def html_footer():
   print """
</body>
</html>
"""

def output_graph (GraphName,img_data):

   print "<img src=\"data:image/jpg;base64,"

   print img_data
   print '" alt="'+ GraphName + '"/><p/>'


def plot_polar_contour(Title,values, azimuths, zeniths):
    """Plot a polar contour plot, with 0 degrees at the North.

    Arguments:

     * `values` -- A list (or other iterable - eg. a NumPy array) of the values to plot on the
     contour plot (the `z` values)
     * `azimuths` -- A list of azimuths (in degrees)
     * `zeniths` -- A list of zeniths (that is, radii)

    The shapes of these lists are important, and are designed for a particular
    use case (but should be more generally useful). The values list should be `len(azimuths) * len(zeniths)`
    long with data for the first azimuth for all the zeniths, then the second azimuth for all the zeniths etc.

    This is designed to work nicely with data that is produced using a loop as follows:

    values = []
    for azimuth in azimuths:
      for zenith in zeniths:
        # Do something and get a result
        values.append(result)

    After that code the azimuths, zeniths and values lists will be ready to be passed into this function.

    """
    theta = np.radians(azimuths)
    zeniths = np.array(zeniths)

    values = np.array(values)
    values = values.reshape(len(azimuths), len(zeniths))

    r, theta = np.meshgrid(zeniths, np.radians(azimuths))
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    ax.set_theta_zero_location("N")
    ax.set_theta_direction("clockwise")
    plt.title("Antenna Phase Biases: " + Title)

    ax.set_rgrids([30,60],labels=["30","60"],angle=[0,0],fmt=None,visible=False)
    cax = plt.contourf(theta, r, values, 30)
    cb = fig.colorbar(cax)
    cb.set_label("Bias (mm)")

    return cax

def create_plot_radial(Title,Az_Step,Biases,Elev_Start,Elev_Stop,Elev_Step):

   Az_Labels=[]
   for Az in xrange(0,360+Az_Step,Az_Step): #We need to make sure we get the last item in the list
      Az_Labels.append(Az)

   flat=[]
   Az_Index=1
   Bias_Index=1
   for Az in xrange(0,360+Az_Step,Az_Step):
      if Az != 360 :
         Bias_Index=1
         for Bias in Biases[Az]:
            flat.append(Bias)
            Bias_Index+=1
      else:
         Bias_Index=1
         for Bias in Biases[0]:
            flat.append(Bias)
            Bias_Index+=1
      Az_Index+=1

   Elev_Reverse_Labels=[]
   for elev in xrange(Elev_Stop,Elev_Start-Elev_Step,-Elev_Step): #We need to make sure we get the last item in the list
      Elev_Reverse_Labels.append(elev)

#   pprint (Elev_Reverse_Labels)
#   pprint (Elev_Labels)
#   pprint (flat)
#   pprint (flat)
#   print len(flat), len(Az_Labels) * len(Elev_Reverse_Labels)
   plot_polar_contour(Title,flat, Az_Labels, Elev_Reverse_Labels)

   tmp_file=tempfile.SpooledTemporaryFile()
   plt.savefig(tmp_file,format="Png")
   tmp_file.seek(0)
   img_data=base64.b64encode(tmp_file.read(-1))
   tmp_file.close()
   return(img_data)

def output_offsets(Title,L1_Offsets,L2_Offsets):
   print "<table align=\"center\" border='1'><caption><b>{} (mm)</b></caption>".format(Title)
   print "<thead><th>Band</th><th>Northing</th><th>Easting</th><th>Up</th><th>2D</th><th>Spin Error</th></thead>"
   if L1_Offsets != None:
      print "<tr><td>L1</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td></th>".format(
            L1_Offsets[0],L1_Offsets[1],L1_Offsets[2],math.sqrt(L1_Offsets[0]**2+L1_Offsets[1]**2), 2*math.sqrt(L1_Offsets[0]**2+L1_Offsets[1]**2))
   if L2_Offsets != None:
      print "<tr><td>L2</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td><td>{:.1f}</td></th>".format(
            L2_Offsets[0],L2_Offsets[1],L2_Offsets[2],math.sqrt(L2_Offsets[0]**2+L2_Offsets[1]**2), 2*math.sqrt(L2_Offsets[0]**2+L2_Offsets[1]**2))
   print "</table></br>"


def create_html(Title,File_Name):
   html_header(Title,File_Name)
   (L1,L2,Az_Step,Elev_Labels,L1_Biases,L2_Biases,Elev_Start,Elev_Stop,Elev_Step)=parse_antenna_ini (File_Name)
   output_offsets("Antenna Offsets",L1,L2)

   if Az_Step == 360:
      img_data = create_plot(Title,L1,L2,Az_Step,Elev_Labels,L1_Biases,L2_Biases)
      output_graph(Title,img_data)
   else:
      img_data = create_plot(Title+" (Az 0)",L1,L2,360,Elev_Labels,L1_Biases,L2_Biases)
      output_graph(Title+" (Az 0)",img_data)

      img_data = create_plot(Title+" (Az Dependent L1)",L1,None,Az_Step,Elev_Labels,L1_Biases,L2_Biases)
      output_graph(Title+" (L1)",img_data)

      img_data = create_plot(Title+" (Az Dependent L2)",None,L2,Az_Step,Elev_Labels,L1_Biases,L2_Biases)
      output_graph(Title+" (L2)",img_data)

      img_data=create_plot_radial(Title+" Radial (L1)",Az_Step,L1_Biases,Elev_Start,Elev_Stop,Elev_Step)
      output_graph(Title+" (L1 Radial)",img_data)

      img_data=create_plot_radial(Title+" Radial (L2)",Az_Step,L2_Biases,Elev_Start,Elev_Stop,Elev_Step)
      output_graph(Title+" (L2 Radial)",img_data)

      html_footer()

if __name__ == "__main__":
#   create_html("Zephyr 3 Rover","t10500010.pct")
#   create_html("Zephyr 3 Rover","t10500010.ife")
#   create_html("Zephyr 3 Base","t11500010.pct")
#   create_html("Zephyr 3 Base","t11500010.ife")
   print "Content-Type: text/html"     # HTML is following
   print                               # blank line, end of headers
   cgitb.enable()
   form = cgi.FieldStorage()
   if "Name" not in form or "File" not in form:
      print "<H1>Internal Error</H1>"
      print "Please fill in the Name and File fields."
   else:
      create_html(form["Name"].value,form["File"].value)
      
