"""
 # Copyright (c) 12 2014 | surya
 # 09/12/14 nanang.ask@kubuskotak.com
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
 #  testjsonobject.py
"""
from collections import defaultdict
import json

import bson
from datetime import datetime, timedelta
from pymongo import MongoClient, DESCENDING
import time
import re

conn = MongoClient('localhost', 27017)
db = conn['ikhram']
# lib = db.umrahs
idx = db.promo_idx

# pisah kan slice ':' kemudian buat list dict per row
#filter value dengan memisahkan capitalize
#filter value hasil loop pertama dengan memisahkan angka dan huruf


# print(lib.find({"_id": 4}))
t = time.time()
# row = idx.find_one({'idx': 5138})
# rows = idx.find()
# jsobj = ",".join(list(row.get("included_facility_airline", None)))
# tagdict = defaultdict(list)
# angkaHuruf = lambda f: ' '.join(re.findall('[^\W\d_]+|\d+', f))
# Besarkecil = lambda f: ' '.join(re.findall('[A-Z][^A-Z]*', f))

# for obj in list(row.get('promo_tags', [])):
#     k, v = obj.split(':')
#     # filtering key Besarkecil, lowercase
#     k = str(Besarkecil(k)).lower()
#     print(k)
#     if k in ['cari', 'jadwal', 'keberangkatan', 'maskapai', 'type', 'jumlah hari']:
#         # k, v = Besarkecil(k), Besarkecil(v)
#         # k, v = angkaHuruf(k), angkaHuruf(v)
#         # (?<=\d)(?=\D)|(?<=\D)(?=\d)|(?<=[a-z])(?=[A-Z])
#         # ([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)
#
#         """
#         (                # begin capture
#           [A-Z]            # one uppercase letter  \ First Word
#           [a-z]+           # 1+ lowercase letters  /
#           (?=\s[A-Z])      # must have a space and uppercase letter following it
#           (?:                # non-capturing group
#             \s               # space
#             [A-Z]            # uppercase letter   \ Additional Word(s)
#             [a-z]+           # lowercase letter   /
#           )+              # group can be repeated (more words)
#         )
#         """
#
#         # set filter key multi tag : ['cari', 'jadwal', 'keberangkatan', 'maskapai', 'type', 'jumlah hari']
#         # print [r.match(string).groups() for string in v]
#         # print(re.findall('([^\W\d_]+|\d+)', v))
#         # print(re.findall('([A-Z][^A-Z]+|(?:[A-Z][A-Z]+)+)', v))
#         # print(re.findall('([A-Z][^A-Z]+|(?:[^\W\d_]))', v))
#         # set date [^\W\d_]+|[\d+]+
#         # print(str(v).isalpha())
#         # res = re.search(r"(?P<capital>[A-Z][^A-Z]+)([^\W\d_]+)(\d+)|([A-Z][^A-Z]+)|(?P<date>[^\W\d_]+|[\d+]+)", v)
#         res = re.findall(r"(^[A-Z][^A-Z]+)|([^\W\d_]+|[\d+]+)", v)
#         arres = []
#         for resple in res:
#             arres.append(filter(None, resple)[0])
#             # print([e for e in resple])
#         print(' '.join(arres))
#         # print(len(res))
#         # print(re.findall(r'[^\W\d_]+|[\d+]+', v))
#         # print(re.findall(r"[\d+]+", v))
#
#         tagdict[k].append(' '.join(arres))
#         # print(k + v)
#         # print(re.findall('([^\W\d_]+|\d+)([A-Z][^A-Z]*)', obj))
#         # print(' '.join(re.findall('([^\W\d_]+|\d+)', obj)))
#         # print(tagdict)
#         # print(json.dumps(jsobj))
#         # for row in lib.find():
#         #     jsobj = row.get("included_facility_airline", None)
#         #     if jsobj is not None:
#         #         # str(jsobj).replace('')
#         #         ld = json.loads(str(jsobj))
#         #         print(ld)
#         #     # print(jsobj)
#         # print((time.time()) - t)
#
# print(tagdict)
#
# for key, value in tagdict.iteritems():
#     print(['{k} {val}'.format(k=key, val=str(v).lower()) for v in value])
#     # print('{k} {val}'.format(k=key, val=', '.join(value)))

# for row in rows:
#     stray = []
#     multi_tag = row.get('promo_tags', None)
#     print(row.get('idx'))
#     # if '' in multi_tag and multi_tag is not None:
#     # print(filter_tag(multi_tag))
#     for key, value in dict(multi_tag).iteritems():
#         for v in value:
#             stray.append(key)
#             stray.append(v)
#         # stray.append(key)
#     print(' '.join(stray).lower())

#
# stray.append(' '.join(['{k} {val}'.format(k=str(key).encode(encoding='utf-8'),
#                                            val=str(v).encode(encoding='utf-8').lower()) for v in
#                         value]))
# db.things.map_reduce(mapper, reducer, "myresults")
# mapper = bson.Code("""
#                function () {
#
#                    emit(this.promo_name, 1);
#
#                }
#                """)
# reducer = bson.Code("""
#                 function (key, values) {
#                   var total = 0;
#                   for (var i = 0; i < values.length; i++) {
#                     total += values[i];
#                   }
#                   return total;
#                 }
#                 """)
#
# res = idx.map_reduce(mapper, reducer, "myresults")
# for r in res.find():
#     print(r)

results = idx.find({
    'end_date': {
        '$gte': datetime.now()
    },
    'status_promo': 1
}).sort('viewed', DESCENDING)
n = 0
for i, row in enumerate(results):
    if n >= 10:
        break
    # (end_date - (last_book + 1)) - now >= 0
    allow_date = (row.get("end_date", datetime.now()) -
                  timedelta(days=row.get('last_book', 0)+1)) - datetime.now()
    if allow_date.days >= 0:
        n += 1
        print("{3} | {2} : {0} - {1}".format(row.get("viewed"), row.get("promo_name"), allow_date, i))
