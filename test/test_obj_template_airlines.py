"""
 # Copyright (c) 12 2014 | surya
 # 22/12/14 nanang.ask@kubuskotak.com
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
 #  test_obj_template_airlines.py
"""

import time

from pymongo import MongoClient
import mysql.connector as my


conn = MongoClient('localhost', 27017)
db = conn['ikhram']
idx = db.umrah_promotions.find()

conn = my.connect(user='root', password='root', database='ikhram')

query = ("SELECT tpl.id, tpl.description FROM template_facility_airlines tpl "
         "INNER JOIN airlines a ON  tpl.template_airline_id = a.template_airline_id "
         "WHERE a.id = %s")

t = time.time()


def template_maskapai(_id=None, _conn=None):
    lairline = []
    cursor = _conn.cursor(buffered=True)
    cursor.execute(query, (_id, ))
    for (tpl_id, name) in cursor:
        # append kedalam satu list kemudian di join
        lairline.append(str(name))
    cursor.close()
    return lairline

for ridx in idx:
    maskapai_kontent = []
    umrah = db.umrahs.find_one({'_id': ridx.get('umrah_id')})
    if umrah is not None:
        # cari id airline_id
        air_id = umrah.get('airline_id')
        if air_id is not None:
            maskapai_kontent.extend(template_maskapai(air_id, conn))
            print(time.time())
    # set untuk template_hotel
    print(''.join(maskapai_kontent))

print((time.time()) - t)
conn.close()
