#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

###
# @nishiokya 
#
# OpenFlights Data(https://openflights.org/data.html)のairports.dat (CSV)をTableau上で表示できるようになる
#
# Python = 2.7
###

from tableausdk import Type
from tableausdk.Extract import *
import csv,codecs


# Where the origin data comes from
#csvLocation = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'
csvLocation = 'airports.dat'

# Where the TDE will be written
extractLocation = 'all_airport.tde'

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
table_definition.addColumn('Airport ID', Type.INTEGER)  # column 0
table_definition.addColumn('Name', Type.UNICODE_STRING)#1
table_definition.addColumn('City', Type.UNICODE_STRING)#2
table_definition.addColumn('Country', Type.UNICODE_STRING)#3
table_definition.addColumn('IATA', Type.UNICODE_STRING)#4
table_definition.addColumn('ICAO', Type.UNICODE_STRING)#5
table_definition.addColumn('geometry', Type.SPATIAL)#6
table_definition.addColumn('Timezone', Type.INTEGER)#7
table_definition.addColumn('DST', Type.UNICODE_STRING)#8
table_definition.addColumn('Tz database time zone', Type.UNICODE_STRING)
table_definition.addColumn('Type', Type.UNICODE_STRING)#10
table_definition.addColumn('Source', Type.UNICODE_STRING)#11

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
with codecs.open(csvLocation, 'r') as csvfile:
  csvreader = csv.reader(csvfile, delimiter=',')

  
  for row in (csvreader):
    """WKT POINT(LON LAT)"
    https://ja.wikipedia.org/wiki/Well-known_text
    """
    point = 'POINT('+(row[7])+' '+(row[6])+')'
    print (point)
   
    new_row.setInteger(0, int(row[0]))
    new_row.setString(1, row[1].decode('utf-8'))
    new_row.setString(2, row[2].decode('utf-8'))
    new_row.setString(3, row[3].decode('utf-8'))
    new_row.setString(4, row[4])
    new_row.setString(5, row[5])
    new_row.setSpatial(6, point)
    new_row.setInteger(7, int(row[8]))
    new_row.setString(8, row[9])
    new_row.setString(9, row[10])
    new_row.setString(10, row[11])
    new_row.setString(11, row[12])
   
    new_table.insert(new_row)

# 7. Save the table and extract
new_extract.close()

# 8. Release the extract API
ExtractAPI.cleanup()
