"""
 # Copyright (c) 11 2014 | surya
 # 17/11/14 nanang.ask@kubuskotak.com
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
 #  index_mongo_promo.py
"""
import os
import time

from pymongo import MongoClient
from whoosh import fields, analysis
from whoosh.index import create_in
from whoosh.lang.stopwords import stoplists


INDEXDIR = os.path.abspath("mongo-idx")
ana = analysis.StemmingAnalyzer(stoplist=stoplists["en"], maxsize=40)


class PromoSchema(fields.SchemaClass):
    id_idx = fields.ID(stored=True)
    title = fields.TEXT(stored=True, sortable=True, spelling=True, analyzer=ana)
    tgrams = fields.NGRAMWORDS
    content = fields.TEXT(stored=True, spelling=True, analyzer=ana)
    path_id = fields.NUMERIC(stored=True)
    path_table = fields.TEXT(stored=True)
    tag = fields.KEYWORD(stored=True)


if not os.path.exists(INDEXDIR):
    os.mkdir(INDEXDIR)

#Initialize index
index = create_in(INDEXDIR, PromoSchema)

# Initiate db connection
conn = MongoClient('localhost', 27017)
db = conn["shafira"]
lib = db.libraries

strTolist = lambda x: x.strip().replace('\'', '').replace('[', '').replace(']', '').split(',')
# for r in lib.find({}, {'tag': 1, '_id': 0}):
#     print(strTolist(r.get('tag'))[0][:2])


# Fill index with {index-mongo} from MongoDB
# with ix.writer(limitmb=2048) as w:
t = time.time()
with index.writer() as w:
    for row in lib.find():
        # print(lib.find(row.get('_id')))
        taglist = strTolist(str(row.get('tag')))
        # idx = strTolist(row.get('tag'))[0][:2]
        w.add_document(
            id_idx=str(taglist[0][:2]) + str(row.get('reference_id')),
            title=row.get('name'), tgrams=row.get('name'),
            content=row.get('content'),
            path_id=row.get('reference_id'),
            path_table=row.get('reference_table'),
            tag=str(taglist[0]).lower()
        )
        print(time.time() - t)
print(time.time() - t)
