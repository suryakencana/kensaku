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
import json
from pymongo import MongoClient
import time
import re

conn = MongoClient('localhost', 27017)
db = conn['ikhram']
# lib = db.umrahs
idx = db.promo_idx

#pisah kan slice ':' kemudian buat list dict per row
#filter value dengan memisahkan capitalize
#filter value hasil loop pertama dengan memisahkan angka dan huruf


# print(lib.find({"_id": 4}))
t = time.time()
row = idx.find_one({'idx': 5140})
# jsobj = ",".join(list(row.get("included_facility_airline", None)))
tagdict = {}
angkaHuruf = lambda f: ' '.join(re.findall('[^\W\d_]+|\d+', f))
Besarkecil = lambda f: ' '.join(re.findall('[A-Z][^A-Z]*', f))

for obj in list(row.get('promo_tags', [])):
    k, v = obj.split(':')
    print(v)
    # k, v = Besarkecil(k), Besarkecil(v)
    # k, v = angkaHuruf(k), angkaHuruf(v)
    # (?<=\d)(?=\D)|(?<=\D)(?=\d)|(?<=[a-z])(?=[A-Z])
    # ([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)

    """
    (                # begin capture
      [A-Z]            # one uppercase letter  \ First Word
      [a-z]+           # 1+ lowercase letters  /
      (?=\s[A-Z])      # must have a space and uppercase letter following it
      (?:                # non-capturing group
        \s               # space
        [A-Z]            # uppercase letter   \ Additional Word(s)
        [a-z]+           # lowercase letter   /
      )+              # group can be repeated (more words)
    )
    """

    # print(re.findall('([^\W\d_]+|\d+)', v))
    print(re.findall('([A-Z][^A-Z]+|(?:[A-Z][A-Z]+)+)', v))
    print(re.findall('([A-Z][^A-Z]+)', v))


    tagdict.update({k: v})
    # print(k + v)
    # print(re.findall('([^\W\d_]+|\d+)([A-Z][^A-Z]*)', obj))
    # print(' '.join(re.findall('([^\W\d_]+|\d+)', obj)))
    # print(tagdict)
    # print(json.dumps(jsobj))
    # for row in lib.find():
    #     jsobj = row.get("included_facility_airline", None)
    #     if jsobj is not None:
    #         # str(jsobj).replace('')
    #         ld = json.loads(str(jsobj))
    #         print(ld)
    #     # print(jsobj)
    # print((time.time()) - t)