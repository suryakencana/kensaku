"""
 # Copyright (c) 02 2015 | surya
 # 06/02/15 nanang.ask@kubuskotak.com
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
 #  tasks.py
"""
import logging
from collections import defaultdict
import os
import re
import time
from datetime import datetime

from pymongo import MongoClient
import mysql.connector as my
from slugify import slugify

from whoosh import fields, analysis
from whoosh.index import create_in
from whoosh.lang.stopwords import stoplists
from pyramid_celery import celery_app as app


LOG = logging.getLogger(__name__)
# Initiate db connection
my_conn = my.connect(user='root', password='root', database='ikhram')
conn = MongoClient('localhost', 27017)
db = conn["ikhram"]


@app.task
def build_idx_mongo(*args, **kwargs):
    try:
        mongo_index()
        build_index_whoosh.delay()
    except(KeyError, ValueError, AttributeError) as e:
        LOG.error(e)


@app.task
def build_index_whoosh():
    try:
        whoosh_index()
    except(KeyError, ValueError, AttributeError) as e:
        LOG.error(e)


def mongo_index():
    # conn = MongoClient('localhost', 27017)
    # db = conn["ikhram"]
    promos = db.umrah_promotions
    # mix_promo = db.create_collection('promo_idx')
    mix_promo = db.promo_idx
    # my_conn = my.connect(user='root', password='root', database='ikhram')
    # ambil agent record
    t = time.time()
    for promo in promos.find():
        libPacket = None
        # print(promo.get('umrah_id'))
        # get Packet_id, Packet_tag, Packet_name dengan umroh_id
        umrahPacket = db.umrahs.find_one({'_id': promo.get('umrah_id')})

        if umrahPacket is not None:
            libPacket = db.libraries.find_one({'tag': 'PACKET', 'reference_id': umrahPacket.get('packet_id')})
        else:
            umrahPacket = {
                'packet_id': '',
                'packet_name': '',
                'packet_tags': []
            }

        if libPacket is None:
            libPacket = {
                'content': None
            }
        contentAgent = db.libraries.find_one({'tag': 'AGENT', 'reference_id': promo.get('agent_id')})
        if contentAgent is None:
            contentAgent = {
                'content': None
            }

        # template hotel

        def template_hotel(_id=None, _conn=None):
            query = ("SELECT tpl.id, tpl.description FROM template_facility_hotels tpl "
                     "WHERE tpl.template_hotel_id = %s")
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

        hotel_content = []
        umrah = db.umrahs.find_one({'_id': promo.get('umrah_id')})
        if umrah is not None:
            # cari id hotel_mecca_ids
            mecca_hotel = umrah.get('hotel_mecca_ids')
            if mecca_hotel is not None:
                for mecca_id in mecca_hotel:
                    hotel_content.extend(template_hotel(mecca_id, my_conn))
                    # print(time.time())

            medinah_hotel = umrah.get('hotel_medinah_ids')
            if medinah_hotel is not None:
                for medinah_id in medinah_hotel:
                    hotel_content.extend(template_hotel(medinah_id, my_conn))
                    # print(time.time())

        # template maskapai

        def template_maskapai(_id=None, _conn=None):
            query = ("SELECT tpl.id, tpl.description FROM template_facility_airlines tpl "
                     "INNER JOIN airlines a ON  tpl.template_airline_id = a.template_airline_id "
                     "WHERE a.id = %s")
            lairline = []
            cursor = _conn.cursor(buffered=True)
            cursor.execute(query, (_id, ))
            for (tpl_id, name) in cursor:
                # append kedalam satu list kemudian di join
                lairline.append(str(name))
            cursor.close()
            return lairline

        maskapai_kontent = []
        umrah = db.umrahs.find_one({'_id': promo.get('umrah_id')})
        last_book = 0
        if umrah is not None:
            # cari id airline_id
            air_id = umrah.get('airline_id')
            if air_id is not None:
                maskapai_kontent.extend(template_maskapai(air_id, my_conn))
                #print(time.time())
            # cari last_allowed_book
            last_book = umrah.get('last_allowed_book', 0)

        # print(''.join(maskapai_kontent))
        hotel_content.extend(maskapai_kontent)
        # set untuk template_hotel_airline
        tpl_hotel_airline = ''.join(hotel_content)

        #promo tag filter
        def filter_tag(tags=None):
            """fungsi filter promo tag menjadi dict type """
            tagdict = defaultdict(list)
            Besarkecil = lambda f: ' '.join(re.findall('[A-Z][^A-Z]*', f))
            for obj in list(tags):
                if len(obj.split(':')) == 2:
                    k, v = obj.split(':')
                    # filtering key Besarkecil, lowercase
                    k = str(Besarkecil(k)).lower()
                    # print(k)
                    if k in ['cari', 'jadwal', 'keberangkatan', 'maskapai', 'type', 'ibadah', 'jumlah hari', 'rute', 'tour']:
                        res = re.findall(r"(^[A-Z][^A-Z]+)|([^\W\d_]+|[\d+]+)", v)
                        arres = []
                        for resple in res:
                            arres.append(filter(None, resple)[0])
                            # print([e for e in resple])
                        # print(' '.join(arres))
                        tagdict[k].append(' '.join(arres))
            return tagdict
        multi_tag = promo.get('promo_tags', None)
        # print(multi_tag)
        if multi_tag is not None:
            promo_tag = filter_tag(multi_tag)
            promo_tag['hotel_mekkah'].extend(promo.get('hotel_mecca_name', '').split('/'))
            promo_tag['hotel_madinah'].extend(promo.get('hotel_medinah_name', '').split('/'))
        else:
            promo_tag = []

        # set rate hotel mecca dan madinah
        rates_hotel = []
        rates_hotel.extend(promo.get('mecca_hotel_rates', []))
        rates_hotel.extend(promo.get('medinah_hotel_rates', []))

        # chosen promo field
        mix_promo.update({'idx': promo.get('_id')}, {'$set': {
            'price': promo.get('starting_price', 0),
            'start_date': promo.get('start_date'),
            'end_date': promo.get('departure_date'),
            'promo_id': promo.get('promo_id'),
            'disc_promo': int(promo.get('discount', 0)),
            'promo_name': promo.get('title'),
            'promo_tags': promo_tag,
            'promo_slug': slugify(promo.get('title', ''), to_lower=True),
            'packet_id': umrahPacket.get('packet_id'),
            'packet_name': umrahPacket.get('name', None),
            'packet_slug': slugify(umrahPacket.get('name', ''), to_lower=True),
            'tpl_hotel_airline': tpl_hotel_airline,
            'rates_hotel': rates_hotel,
            'content_packet': libPacket.get('content', ''),
            'agent_id': promo.get('agent_id', None),
            'agent_name': promo.get('agent_name', None),
            'agent_city': promo.get('agent_city', None),
            'agent_slug': promo.get('agent_slug', None),
            'content_agent': contentAgent.get('content', ''),
            'airline_name': promo.get('airline_name', None),
            'status_promo': promo.get('status', 0),
            'viewed': promo.get('viewed', 0),
            'last_book': last_book
        }}, upsert=True)
    mix_promo.remove({"packet_id": None})
    mix_promo.remove({"packet_id": ''})
    print('success crontab')
    print(time.time() - t)


def whoosh_index():
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
        promo_slug = fields.TEXT(stored=True, sortable=True)
        promo_ngramword = fields.NGRAMWORDS
        promo_tags = fields.TEXT(sortable=True)
        packet_id = fields.NUMERIC(int, stored=True, sortable=True)
        packet_name = fields.TEXT(stored=True, sortable=True)
        packet_slug = fields.TEXT(stored=True, sortable=True)
        tpl_hotel_airline = fields.TEXT(sortable=True, analyzer=anaNgram)
        content_packet = fields.TEXT(sortable=True, spelling=True, analyzer=anaNgram, phrase=False)
        agent_id = fields.NUMERIC(int, stored=True, sortable=True)
        agent_name = fields.TEXT(stored=True, sortable=True)
        agent_city = fields.TEXT(stored=True, sortable=True)
        agent_slug = fields.TEXT(stored=True, sortable=True)
        content_agent = fields.TEXT(sortable=True, analyzer=anaNgram, phrase=False)
        rates_hotel = fields.NUMERIC(int, stored=True)
        airline_name = fields.TEXT(stored=True, sortable=True)
        status_promo = fields.NUMERIC(int, stored=True, sortable=True)
        last_book = fields.NUMERIC(int, stored=True, sortable=True)

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

    # # Initiate db connection
    # conn = MongoClient('localhost', 27017)
    # db = conn["ikhram"]
    pro_idx = db.promo_idx
    start = unicode(datetime.now())
    try:
        # Fill index with {index-mongo} from MongoDB
        t = time.time()
        with index.writer(limitmb=1024) as w:
            for row in pro_idx.find({
                'end_date': {
                    '$gte': datetime.now()
                }
            }):
                # print(row.get('idx'))
                print(row.get('packet_id'))
                promotags = content_promo_tags(row.get('promo_tags', None))
                rates_hotels = sorted(row.get('rates_hotel'))[-1] if len(row.get('rates_hotel', [])) > 0 else 0
                w.update_document(
                    idx=unicode(row.get('idx')),
                    price=row.get('price', 0),
                    start_date=row.get('start_date'),
                    end_date=row.get('end_date'),
                    promo_id=row.get('promo_id'),
                    disc_promo=row.get('disc_promo'),
                    promo_name=row.get('promo_name', u''), promo_ngramword=row.get('promo_name'),
                    promo_tags=unicode(promotags),
                    promo_slug=row.get('promo_slug', u'promo-slug'),
                    packet_id=int(row.get('packet_id')),
                    packet_name=row.get('packet_name', u''),
                    packet_slug=row.get('packet_slug', u'packet-slug'),
                    tpl_hotel_airline=row.get('tpl_hotel_airline'),
                    content_packet=row.get('content_packet'),
                    agent_id=row.get('agent_id'),
                    agent_name=row.get('agent_name'),
                    agent_city=row.get('agent_city'),
                    agent_slug=row.get('agent_slug'),
                    content_agent=row.get('content_agent'),
                    airline_name=row.get('airline_name'),
                    rates_hotel=rates_hotels,
                    status_promo=int(row.get('status_promo', 0)) if row.get('status_promo', 0) is not None and isinstance(
                        row.get('status_promo', 0), int) else 0,
                    last_book=int(row.get('last_book', 0)) if row.get('last_book', 0) is not None and isinstance(
                        row.get('last_book', 0), int) else 0
                )
                # print(time.time() - t)
        print(time.time() - t)
    except(KeyError, ValueError) as e:
        print(e)
