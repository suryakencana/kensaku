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
 #  test_obj_template_hotel.py
"""

import time

from pymongo import MongoClient
import mysql.connector as my


conn = MongoClient('localhost', 27017)
db = conn['ikhram']
idx = db.umrah_promotions.find()

conn = my.connect(user='root', password='root', database='ikhram')

query = ("SELECT tpl.id, tpl.description FROM template_facility_hotels tpl "
         "WHERE tpl.template_hotel_id = %s")

t = time.time()


def template_hotel(_id=None, _conn=None):
    lhotel = []
    hotel = db.hotels.find_one({'_id': _id})
    if hotel is not None:
        tpl_id = hotel.get('template_hotel_id')
        cursor = _conn.cursor(buffered=True)
        cursor.execute(query, (tpl_id, ))
        for (tpl_id, name) in cursor:
            # append kedalam satu list kemudian di join
            lhotel.append(str(name))
        cursor.close()
    return lhotel

for ridx in idx:
    hotel_content = []
    umrah = db.umrahs.find_one({'_id': ridx.get('umrah_id')})
    if umrah is not None:
        # cari id hotel_mecca_ids
        mecca_hotel = umrah.get('hotel_mecca_ids')
        if mecca_hotel is not None:
            for mecca_id in mecca_hotel:
                hotel_content.extend(template_hotel(mecca_id, conn))
            print(time.time())

        medinah_hotel = umrah.get('hotel_medinah_ids')
        if medinah_hotel is not None:
            for medinah_id in medinah_hotel:
                hotel_content.extend(template_hotel(medinah_id, conn))
            print(time.time())
    # set untuk template_hotel
    print(''.join(hotel_content))

print((time.time()) - t)
conn.close()
