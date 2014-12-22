"""
 # Copyright (c) 12 2014 | surya
 # 18/12/14 nanang.ask@kubuskotak.com
 # This program is free software; you can redistribute it and/or
 # modify it under the terms of the GNU General Public License
 # as published by the Free Software Foundation; either version 2
 # of the License, or (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with this program; if not, write to the Free Software
 # Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 #  test_content_airline.py
"""
# pip install --allow-external mysql-connector-python mysql-connector-python
from collections import defaultdict

import csv
from pymongo import MongoClient
import mysql.connector as my
import time


conn = MongoClient('localhost', 27017)
db = conn['ikhram']
idx = db.promo_idx.find()

conn = my.connect(user='root', password='root', database='ikhram')


query = ("SELECT tpl.id, tpl.description FROM template_facility_airlines tpl "
         "INNER JOIN airlines a ON  tpl.template_airline_id = a.template_airline_id "
         "WHERE a.id = %s")
# cursor.execute(query, (1,))
# for row in cursor:
#     print(row)
#
# engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/ikhram')
# conn = engine.connect()
airline_list = defaultdict(list)
t = time.time()

with open('maskapai.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    for ridx in idx:

        cursor = conn.cursor(buffered=True)
        air_id = db.umrahs.find_one({'packet_id': ridx.get('packet_id')}).get('airline_id')
        cursor.execute(query, (air_id, ))
        for (tpl_id, name) in cursor:
            airline_list[str(ridx)].append(str(name))
            # spamwriter.writerow([str(ridx.get('promo_id')), str(ridx.get('packet_id')), str(tpl_id), str(name)])
            # print(str(ridx.get('promo_id')) + ' --- ' + str(ridx.get('packet_id')) + ' --- template_id: ' + str(tpl_id) + 'Maskapai: ' + str(name))
        cursor.close()
        print(time.time())
print((time.time()) - t)
conn.close()

print(airline_list)