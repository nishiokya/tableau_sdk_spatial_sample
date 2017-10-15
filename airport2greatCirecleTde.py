#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

###
# @nishiokya 
#
# OpenFlights Data(https://openflights.org/data.html)のairports.dat (CSV)をTableau上で表示できるようになる
#
# Python = 2.7
# pip install  geographiclib

###

from tableausdk import Type
from tableausdk.Extract import *
from geographiclib.geodesic import Geodesic
import csv,codecs


# Where the origin data comes from
#csvLocation = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
csvLocation = 'airports.dat'

# Where the TDE will be written
extractLocation = 'greate_circle_airport.tde'

# csv column number for origin/destination coordinates (start count at 0 for the first col in your csv)

#####################################################################
## Process the data and write the TDE
#####################################################################

# 1. initialize a new extract
ExtractAPI.initialize()

# 2. Create a table definition
new_extract = Extract(extractLocation)

# 3. Add column definitions to the table definition
table_definition = TableDefinition()
table_definition.addColumn('Airline', Type.UNICODE_STRING)  # column 0
table_definition.addColumn('Airline ID', Type.INTEGER)#1
table_definition.addColumn('Source airport', Type.UNICODE_STRING)#2
table_definition.addColumn('Source airport ID', Type.INTEGER)#3
table_definition.addColumn('Destination airport', Type.UNICODE_STRING)#4
table_definition.addColumn('Destination airport ID', Type.INTEGER)#5
table_definition.addColumn('Codeshare', Type.UNICODE_STRING)#6
table_definition.addColumn('Stops', Type.INTEGER)#7
table_definition.addColumn('Equipment', Type.UNICODE_STRING)#8
table_definition.addColumn('geometry', Type.SPATIAL)#9
table_definition.addColumn('Source airport Country', Type.UNICODE_STRING)#10
table_definition.addColumn('Source airport Name', Type.UNICODE_STRING)#11
table_definition.addColumn('Destination airport Country', Type.UNICODE_STRING)#12
table_definition.addColumn('Destination airport Name', Type.UNICODE_STRING)#13


# 4. Initialize a new table in the extract
if (new_extract.hasTable('Extract') == False):
  new_table = new_extract.addTable('Extract', table_definition)
else:
  new_table = new_extract.openTable('Extract')

# 5. Create a new row
new_row = Row(table_definition)  # Pass the table definition to the constructor

# 6. walk through the origin/destination data from CSV, write each path to TDE
#f = codecs.open(csvLocation,'r','utf-8')
#f =codecs.open(csvLocation, 'r', 'utf8')
airport  = {}
with codecs.open(csvLocation, 'r') as csvfile:
  csvreader = csv.reader(csvfile, delimiter=',')

  
  for row in (csvreader):
    """WKT POINT(LON LAT)"
    https://ja.wikipedia.org/wiki/Well-known_text
    """
   
    airport[(row[0])] = [row[7],row[6],
      row[1].decode('utf-8'),
      row[2].decode('utf-8'),
      row[3].decode('utf-8')]
    
   

with codecs.open("routes.dat", 'r') as csvfile:
  csvreader = csv.reader(csvfile, delimiter=',')

  
  for row in (csvreader):
    """WKT POINT(LON LAT)"
    https://ja.wikipedia.org/wiki/Well-known_text
    """
    o = []
    d = []#init list
    if row[3] in airport:
      #print(airport[row[3]])
      o = airport[row[3]]
    if row[5] in airport:
      #print(airport[row[5]])
      d = airport[row[5]]
    
    #空港の緯度経度とAirplan IDが取れている場合に出力
    if len(o) >0 and len(d)>0 and row[1].isdigit() == True :
        olat = float(o[1])
        olon = float(o[0])
        oname = o[2]
        ocountry = o[4]

        dlat = float(d[1])
        dlon = float(d[0])
        dname = d[2]
        dcountry = d[4]
      
        p = Geodesic.WGS84.Inverse(olat, olon, dlat, dlon)
        l = Geodesic.WGS84.Line(p['lat1'], p['lon1'], p['azi1'])
        if (p['s12'] >= 1000000):
          num = int(p['s12'] / 100000)
        else:
          num = 10
        output = ''
        linestring = 'LINESTRING('
        for i in range(num + 1):
          b = l.Position(i * p['s12'] / num, Geodesic.STANDARD | Geodesic.LONG_UNROLL)
          output += repr(b['lon2']) + ',' + repr(b['lat2']) + ', '
          linestring += str(b['lon2']) + ' ' + str(b['lat2']) + ', '
        # remove the ',' after the last coordinate and close the WKT string with a ')'
        linestring = linestring[:-2] + ')'
        #print(linestring)

        new_row.setString(0, row[0])
        new_row.setInteger(1, int(row[1]))
        new_row.setString(2, row[2])
        #print(row[3])
        new_row.setInteger(3, int(row[3]))
        new_row.setString(4, row[4])
        #print(row[5])
        #print(d)
        new_row.setInteger(5, int(row[5]))
        new_row.setString(6, row[6])
        new_row.setInteger(7, int(row[7]))
        new_row.setString(8, row[8])
        new_row.setSpatial(9, linestring)
        new_row.setString(10, ocountry)
        new_row.setString(11, oname)
        new_row.setString(12, dcountry)
        new_row.setString(13, dname)


        new_table.insert(new_row)

# 7. Save the table and extract
new_extract.close()

# 8. Release the extract API
ExtractAPI.cleanup()
