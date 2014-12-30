"""
 # Copyright (c) 12 2014 | surya
 # 29/12/14 nanang.ask@kubuskotak.com
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
 #  test_multi_tag.py
"""
from collections import defaultdict
import re
from pymongo import MongoClient
import time

conn = MongoClient('localhost', 27017)
db = conn['ikhram']
# lib = db.umrahs
idx = db.promo_idx

#pisah kan slice ':' kemudian buat list dict per row
#filter value dengan memisahkan capitalize
#filter value hasil loop pertama dengan memisahkan angka dan huruf


# print(lib.find({"_id": 4}))
t = time.time()
# row = idx.find_one({'idx': 5138})
rows = idx.find_one({'idx': 5138})


def filter_tag(tags=None):
    tagdict = defaultdict(list)
    Besarkecil = lambda f: ' '.join(re.findall('[A-Z][^A-Z]*', f))
    for obj in list(tags):
        if len(obj.split(':')) == 2:
            k, v = obj.split(':')
            # filtering key Besarkecil, lowercase
            k = str(Besarkecil(k)).lower()
            # print(k)
            if k in ['cari', 'jadwal', 'keberangkatan', 'maskapai', 'type', 'jumlah hari']:
                res = re.findall(r"(^[A-Z][^A-Z]+)|([^\W\d_]+|[\d+]+)", v)
                arres = []
                for resple in res:
                    arres.append(filter(None, resple)[0])
                    # print([e for e in resple])
                # print(' '.join(arres))
                tagdict[k].append(' '.join(arres))
    return tagdict

for row in rows:
    multi_tag = row.get('promo_tags', None)
    print(multi_tag)
    if multi_tag is not None:
        # print(filter_tag(multi_tag))
        for key, value in filter_tag(multi_tag).iteritems():
            print(['{k} {val}'.format(k=key, val=str(v).lower()) for v in value])