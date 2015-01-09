"""
 # Copyright (c) 11 2014 | surya
 # 24/11/14 nanang.ask@kubuskotak.com
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
 #  index_promo_idx.py
"""
import os
import time

from pymongo import MongoClient
from whoosh import fields, analysis
from whoosh.index import create_in
from whoosh.lang.stopwords import stoplists


# INDEXDIR = os.path.abspath("promo-fix-idx")
INDEXDIR = os.path.abspath("promo-tags-idx")
ana = analysis.StemmingAnalyzer(stoplist=stoplists["en"], maxsize=40)
anaNgram = analysis.NgramWordAnalyzer(4)


class PromoIdxSchema(fields.SchemaClass):
    idx = fields.ID(unique=True, sortable=True)
    price = fields.NUMERIC(int, stored=True, sortable=True)
    start_date = fields.DATETIME(stored=True, sortable=True)
    end_date = fields.DATETIME(stored=True, sortable=True)
    promo_id = fields.NUMERIC(int, stored=True, sortable=True)
    disc_promo = fields.NUMERIC(int, stored=True, sortable=True)
    promo_name = fields.TEXT(stored=True, sortable=True, spelling=True, analyzer=anaNgram, phrase=False)
    promo_ngramword = fields.NGRAMWORDS
    promo_tags = fields.TEXT(sortable=True)
    packet_id = fields.NUMERIC(int, stored=True, sortable=True)
    packet_name = fields.TEXT(stored=True, sortable=True)
    tpl_hotel_airline = fields.TEXT(sortable=True, analyzer=ana)
    content_packet = fields.TEXT(sortable=True, spelling=True, analyzer=anaNgram, phrase=False)
    agent_id = fields.NUMERIC(int, stored=True, sortable=True)
    agent_name = fields.TEXT(stored=True, sortable=True)
    agent_city = fields.TEXT(stored=True, sortable=True)
    agent_slug = fields.TEXT(sortable=True)
    content_agent = fields.TEXT(sortable=True, analyzer=anaNgram, phrase=False)
    airline_name = fields.TEXT(sortable=True)
    status_promo = fields.NUMERIC(int, stored=True, sortable=True)
    # status_promo = fields.COLUMN(NumericColumn("i"))


def content_promo_tags(multi_tag):
    stray = []
    for key, value in dict(multi_tag).iteritems():
        for v in value:
            stray.append(key)
            stray.append(v)
    return ' '.join(stray).lower()

if not os.path.exists(INDEXDIR):
    os.mkdir(INDEXDIR)

# Initialize index
index = create_in(INDEXDIR, PromoIdxSchema)

# Initiate db connection
conn = MongoClient('localhost', 27017)
db = conn["ikhram"]
pro_idx = db.promo_idx

# Fill index with {index-mongo} from MongoDB
t = time.time()
with index.writer(limitmb=2048) as w:
    for row in pro_idx.find():
        # print(row.get('idx'))
        print(row.get('packet_id'))
        promotags = content_promo_tags(row.get('promo_tags', None))
        w.update_document(
            idx=unicode(row.get('idx')),
            price=row.get('price', 0),
            start_date=row.get('start_date'),
            end_date=row.get('end_date'),
            promo_id=row.get('promo_id'),
            disc_promo=row.get('disc_promo'),
            promo_name=row.get('promo_name'), promo_ngramword=row.get('promo_name'),
            promo_tags=unicode(promotags),
            packet_id=int(row.get('packet_id')),
            packet_name=row.get('packet_name'),
            tpl_hotel_airline=row.get('tpl_hotel_airline'),
            content_packet=row.get('content_packet'),
            agent_id=row.get('agent_id'),
            agent_name=row.get('agent_name'),
            agent_city=row.get('agent_city'),
            agent_slug=row.get('agent_slug'),
            content_agent=row.get('content_agent'),
            airline_name=row.get('airline_name'),
            status_promo=int(row.get('status_promo', 0)) if row.get('status_promo', 0) is not None and isinstance(
                row.get('status_promo', 0), int) else 0
        )
        print(time.time() - t)
print(time.time() - t)



 # promo_tags=','.join(row.get('promo_tags')) if len(row.get('promo_tags', [])) > 0 else u'',