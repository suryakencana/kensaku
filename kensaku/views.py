from collections import defaultdict
import json
import logging
import os
from datetime import datetime, timedelta

from pymongo import DESCENDING
from pyramid.response import Response
from pyramid.view import view_config
from whoosh import index, qparser
from whoosh.query.ranges import NumericRange, DateRange
from whoosh.scoring import TF_IDF
from whoosh.sorting import ScoreFacet


log = logging.getLogger(__name__)

SOURCEDIR = os.path.abspath("cpython/Doc")
# SOURCEDIR = os.environ.get("DEMOSOURCE", "cpython/Doc")
# INDEXDIR = os.environ.get("DEMOINDEX", "index")
INDEXDIR = os.path.abspath("promo-tags-idx")
#
# @view_config(route_name='results',
# renderer='templates/whoosh/results.mako')
# def results(request):
# terms = request.params.get("q", '')
# # return render_libraries(get_searcher(), terms, req=request)
# return render_promo(get_searcher(), terms, req=request)


class ListType:
    def __init__(self):
        pass

    PACKETS = 1
    AGENTS = 2


@view_config(route_name='promo', renderer='json')
def home(request):
    ref_id = request.matchdict['ref_id']
    ref_tag = request.matchdict['ref_tag']
    print('{0}_id: {1}'.format(ref_tag, ref_id))
    umrah = request.db['umrah_promotions']
    return [elem for elem in umrah.find({'{0}_id'.format(ref_tag): int(ref_id)})]
    # return {'info': 'Promo API'}


@view_config(route_name='upromo', renderer='json')
def umrahPromo(request):
    id = request.matchdict['id']
    return Response(
        body=json.dumps({'message': '{0} Custom `Not Found` message'.format(id)}),
        status='201 Created',
        charset='UTF-8',
        content_type='application/json;')


@view_config(route_name='testrails', renderer='json')
def test_rail(request):
    # type : match
    tipe = request.params.get('type')
    match = request.params.get('match')
    q = request.params.get('q')
    ix = get_searcher()
    with ix.searcher(weighting=TF_IDF()) as s:
        qp = qparser.MultifieldParser(["promo_tags",
                                       "content_packet",
                                       "content_agent",
                                       "promo_name",
                                       "tpl_hotel_airline"], s.schema)
        try:
            # api evolution
            linq = [q, "AND (" if not '' in tipe else None,
                    "agent_slug:{match}".format(match=match) if "agent" in tipe else None,
                    "packet_slug:{match}".format(match=match) if "packet" in tipe else None,
                    ")" if not '' in tipe else None]
            # /api/v1/test_rails?q=patuna&type=packet&match=paket-biru-by-qatar-via-jeddah
            # list join
            print(linq)
            terms = unicode(" ".join(filter(None, linq)))
            print(terms)
            q = qp.parse(terms)
            print(q)
            sts = NumericRange("status_promo", 1, 1)
            oldDate = DateRange("end_date", None, datetime.now())
            scores = ScoreFacet()
            results = s.search(q, limit=None, filter=sts, mask=oldDate,
                               sortedby=scores, groupedby=["packet_id", "agent_id"])
            feed = []
            # feed.extend(get_list_packet(s, results, req))
            # feed.extend(get_list_biro(s, results, req))
            print(len(results))
            for hit in results:
                feeder = []
                allow_date = (hit['end_date'] -
                              timedelta(days=hit['last_book'])) - datetime.now()
                # print("{0}, {1}".format(allow_date.days))
                if (allow_date.days - 1) >= 0:
                    # if hit.rank < 10:
                    data = {
                        "promo_id": hit['promo_id'],
                        "promo_name": hit['packet_name'],
                        "packet_slug": hit['packet_slug'],
                        "promo_tags": hit['promo_tags'],
                        "end_date": hit['end_date'].isoformat()
                    }
                    feeder.append(data)
                    feed.extend(feeder)
            print(len(feed))
        except (KeyError, ValueError) as e:
            feed = None
            log.error(e)
    return Response(
        body=json.dumps(feed),
        status='201 Created',
        charset='UTF-8',
        content_type='application/json;')


@view_config(route_name='kensaku', renderer='templates/kensaku/kensaku_page.mako')
def kensaku(request):
    return {'ok': 1}


@view_config(route_name='valid', request_method='POST', renderer='json')
def valid_button(request):
    try:
        # args = request.params.get('arrPromo', '')
        start = request.params.get('startDate', datetime.now())
        end = request.params.get('endDate', datetime.now())
        whatPrice = request.params.get('whatPrice', '').split('~')
        tipe = request.params.get('type', '')
        match = request.params.get('match', '')
        terms = request.params.get('q', '')
        # arrPromo = args.split(',')
        linq = get_linq(terms, tipe, match)

        def deep(data):
            feed = []
            for hit in data:
                allow_date = (hit['end_date'] - timedelta(days=hit['last_book'])) - datetime.now()
                if (allow_date.days - 1) >= 0:
                    feed.append(hit['promo_id'])
            return feed

        arrPromo = get_search(get_searcher(), linq, deep)
        log.info(whatPrice[0])

        umroh = request.db['umrah_promotions']
        # dataSet = [elem for elem in umroh.find({'promo_id': {'$in': [int(ei) for ei in arrPromo]}})]

        if ':' in str(whatPrice[0]):
            log.info(str(whatPrice[0]).replace(':', ''))
            if str(whatPrice[0]).index(':') == 0:
                price = {
                    '$lte': int(str(whatPrice[0]).replace(':', ''))
                }
            elif str(whatPrice[0]).index(':') > 0:
                price = {
                    '$gte': int(str(whatPrice[0]).replace(':', ''))
                }
        elif '' in whatPrice:
            log.info('price => 0')
            price = {
                '$gte': 0
            }
        else:
            log.info('range price')
            price = {
                '$gte': int(whatPrice[0]), '$lte': int(whatPrice[-1])
            }

        # default isi query umrah_promotion
        sql = {
            'promo_id': {'$in': [int(ei) for ei in arrPromo]},
            'departure_date': {
                '$gte': datetime(int(start.split('-')[2]),
                                 int(start.split('-')[1]),
                                 int(start.split('-')[0])),
                '$lte': datetime(int(end.split('-')[2]),
                                 int(end.split('-')[1]),
                                 int(end.split('-')[0]))
            },
            'starting_price': price
        }

        dataset = umroh.find(sql)
        count = dataset.count()
        price = sorted([row.get('starting_price', 0) for row in dataset])
        # log.info(dataSet)
        log.info(price)
    except(KeyError, ValueError) as e:
        # log.debug(e.message)
        print(e)
    finally:
        return Response(
            body=json.dumps({'data': {
                'count': count,
                'price': price[0] if len(price) >= 1 else 0
            }}),
            status='201 Created',
            charset='UTF-8',
            content_type='application/json;')


@view_config(route_name='rest', renderer='json')
def rest(request):
    tipe = request.params.get('type', '')
    match = request.params.get('match', '')
    terms = request.params.get('q', '')
    # set term fix match AND
    linq = get_linq(terms, tipe, match)

    def deep(data):
        feed = []
        for hit in data:
            allow_date = (hit['end_date'] - timedelta(days=hit['last_book'])) - datetime.now()
            if (allow_date.days - 1) >= 0:
                feed.append(hit['promo_id'])
        # print(len(feed))
        return feed

    res = get_search(get_searcher(), linq, deep)

    return Response(
        body=json.dumps(res),
        status='201 Created',
        charset='UTF-8',
        content_type='application/json;')


@view_config(route_name='home', renderer='templates/whoosh/search.mako')
def search(request):
    return {'args': request.params}


@view_config(route_name='results', renderer='json')
def results(request):
    try:
        tipe = request.params.get('type', '')
        match = request.params.get('match', '')
        terms = request.params.get('q', '')
        if len(terms) <= 0:
            print('log terms kosong')
            # default term kosong
            return render_empty_term(req=request)
        # api evolution
        linq = get_linq(terms, tipe, match)
        # /api/v1/test_rails?q=patuna&type=packet&match=paket-biru-by-qatar-via-jeddah
        # list join
        return render_promo_by(get_searcher(), linq, req=request)
    except(KeyError, ValueError) as e:
        log.error(e.message)


def render_empty_term(req):
    try:
        feed = []
        feeder = []
        grouppop = []
        groupprice = []
        groupdisc = []
        groupdate = []
        promo = req.db['promo_idx']
        results = promo.find({
            'end_date': {
                '$gte': datetime.now()
            },
            'status_promo': 1
        }).sort('viewed', DESCENDING)
        # print(datetime.now())
        # for row in results:
        # print(row)
        n = 0
        if results:
            for row in results:
                if n >= 10:
                    break
                # (end_date - (last_book + 1)) - now >= 0
                allow_date = (row.get("end_date", datetime.now()) -
                              timedelta(days=row.get('last_book', 0))) - datetime.now()
                if (allow_date.days - 1) >= 0:
                    n += 1
                    grouppop.extend([row.get('promo_id', None)])
                    groupprice.extend([row.get('price', 0)])
                    groupdisc.extend([row.get('disc_promo', 0)])
                    groupdate.extend([row.get('end_date', 0).isoformat()])
                    nameo = row.get('packet_name', 'No title')
                    agent_slug = row.get('agent_slug', None)
                    packet_slug = row.get('packet_slug', None)
                    airline_name = str(row.get('airline_name', '').split("/")[0]).replace(' ', '').lower()
                    rates_hotel = sorted(row.get('rates_hotel', None))[-1] if len(row.get('rates_hotel', [])) > 0 else 0
                    feeder.append({
                        "Name": row.get('promo_name', 'No title'),
                        "IsDefault": True,
                        "IsTitle": False,
                        "HasImage": False,
                        "Header": None,
                        "ObjectId": row.get('promo_id', None),
                        "AgentId": None,
                        "agent_slug": agent_slug,
                        "airline_name": airline_name,
                        "rates_hotel": rates_hotel,
                        "PacketId": row.get('promo_id', None),
                        "NoOfPromo": 1,
                        "GroupOfPromo": row.get('promo_id', None),
                        "PromoText": str(row.get('promo_name', 'No title')),
                        "GroupOfPrice": 0,
                        "startPrice": row.get('price', 0),
                        "endPrice": 0,
                        "GroupOfDisc": 0,
                        "startDisc": row.get('disc_promo', 0),
                        "endDisc": row.get('disc_promo', 0),
                        "startDate": row.get('end_date', 0).isoformat(),
                        "endDate": row.get('end_date', 0).isoformat(),
                        "ResultText": nameo,
                        "ResultAddress": nameo,
                        "Image": None,
                        "RetinaImage": None,
                        "BgImageLoader": None,
                        "type": 'promo',
                        "match": row.get('promo_slug', ''),
                        "tagging": "PAKET"
                    })
            groupprice = sorted(groupprice)
            groupdate = sorted(groupdate)
            groupdisc = sorted(groupdisc)
            feed.append({
                "Name": None,
                "IsDefault": True,
                "IsTitle": True,
                "HasImage": False,
                "Header": "Paket Populer",
                "ObjectId": 0,
                "AgentId": 0,
                "agent_slug": None,
                "airline_name": None,
                "PacketId": 0,
                "NoOfPromo": len(grouppop),
                "GroupOfPromo": grouppop,
                "PromoText": None,
                "GroupOfPrice": groupprice,
                "startPrice": groupprice[0] if len(groupprice) > 0 else 0,
                "endPrice": groupprice[-1] if len(groupprice) > 0 else 0,
                "GroupOfDisc": groupdisc,
                "startDisc": groupdisc[0] if len(groupdisc) > 0 else 0,
                "endDisc": groupdisc[-1] if len(groupdisc) > 0 else 0,
                "startDate": groupdate[0] if len(groupdate) > 0 else 0,
                "endDate": groupdate[-1] if len(groupdate) > 0 else 0,
                "ResultText": "Semua Paket Umroh Populer",
                "ResultAddress": "Semua Paket Umroh Populer",
                "Image": None,
                "RetinaImage": None,
                "BgImageLoader": None,
                "type": 'promo',
                "match": None,
                "tagging": None
            })
            feed.extend(feeder)
    except (KeyError, ValueError) as e:
        log.error(e.message)
    return Response(
        body=json.dumps(feed),
        status='201 Created',
        charset='UTF-8',
        content_type='application/json;')


def get_searcher():
    try:
        return index.open_dir(INDEXDIR)
    except (KeyError, ValueError) as e:
        log.error(e.message)


def get_linq(terms, tipe, match):
    return unicode(" ".join(
        filter(None, [terms, "AND (" if not '' in tipe else None,
                      "agent_slug:{match}".format(match=match) if "agent" in tipe else None,
                      "packet_slug:{match}".format(match=match) if "packet" in tipe else None,
                      "promo_slug:{match}".format(match=match) if "promo" in tipe else None,
                      ")" if not '' in tipe else None])))


def get_search(ix, terms, callback):
    with ix.searcher(weighting=TF_IDF()) as s:
        qp = qparser.MultifieldParser(["promo_tags",
                                       "content_packet",
                                       "content_agent",
                                       "promo_name",
                                       "tpl_hotel_airline"], s.schema)
        try:
            q = qp.parse(terms)
            sts = NumericRange("status_promo", 1, 1)
            scores = ScoreFacet()
            result = s.search(q, limit=None,
                              filter=sts, mask=DateRange("end_date", None, datetime.now()),
                              sortedby=scores, groupedby=["packet_id", "agent_id"])
            return callback(result)
        except (KeyError, ValueError) as e:
            log.error(e.message)
            return None


def render_promo_by(ix, terms, req):
    with ix.searcher(weighting=TF_IDF()) as s:
        qp = qparser.MultifieldParser(["promo_tags",
                                       "content_packet",
                                       "content_agent",
                                       "promo_name",
                                       "tpl_hotel_airline"], s.schema)
        try:
            # terms = u"{term} AND (agent_slug:{match})".format(term=terms, match=u"al-amsor")
            q = qp.parse(terms)
            print(q)
            sts = NumericRange("status_promo", 1, 1)
            oldDate = DateRange("end_date", None, datetime.now())
            scores = ScoreFacet()
            results = s.search(q, limit=None, filter=sts, mask=oldDate,
                               sortedby=scores, groupedby=["packet_id", "agent_id"])
            feed = []
            # set all promo on search
            feed.extend(list_all_promo(results))
            paket = results.groups('packet_id')
            feed.extend(get_list_json(s, paket, ListType.PACKETS))
            biro = results.groups('agent_id')
            feed.extend(get_list_json(s, biro, ListType.AGENTS))
        except (KeyError, ValueError) as e:
            feed = None
            s._field_caches.clear()
            log.error(e.message)
    return Response(
        body=json.dumps(feed),
        status='201 Created',
        charset='UTF-8',
        content_type='application/json;')


def get_list_json(s, glist, ltype):
    """Fungsi list promo umroh berdasarkan biro"""
    try:
        feed = []
        feeder = []
        grouppromo = []
        groupprice = []
        groupdate = []
        groupdisc = []
        # print(len(agents))
        if ltype == ListType.PACKETS:
            name = 'packet_name'
            mtype = 'packet_slug'
            tipe = 'packet'
            tagging = 'PACKETS'
            header = 'Paket Umroh'
            allpick = 'Semua Paket Umroh'
        if ltype == ListType.AGENTS:
            name = 'agent_name'
            mtype = 'agent_slug'
            tipe = 'agent'
            tagging = 'AGENT'
            header = 'Travel Umroh'
            allpick = 'Semua Biro Umroh'
        n = 0
        for i, docid in enumerate(glist):
            doclist = glist[docid]
            # group_id : packet_id || agent_id
            nameo = s.stored_fields(doclist[0])[name]
            # match = s.stored_fields(doclist[0])[mtype]
            groupdoc = defaultdict(list)
            for docnum in doclist:
                allow_date = (s.stored_fields(docnum)['end_date'] -
                              timedelta(days=s.stored_fields(docnum)['last_book'])) - datetime.now()
                if (allow_date.days - 1) >= 0:
                    # group packet slug
                    groupdoc["gpslug"].append(s.stored_fields(docnum)[mtype])
                    # group promo per group
                    groupdoc["gpromo"].append(s.stored_fields(docnum)['promo_id'])
                    # group price per promo untuk mencari range paling murah
                    groupdoc["gprice"].append(s.stored_fields(docnum)['price'])
                    # group departure date per promo untuk mencari range tanggal keberangkatan paling awal
                    groupdoc["gdate"].append(s.stored_fields(docnum)['end_date'])
                    # group disc promo
                    groupdoc["gdisc"].append(s.stored_fields(docnum)['disc_promo'])
                    # group agent_city
                    groupdoc["gagcity"].append(s.stored_fields(docnum)['agent_city'])
                    # group agent_slug
                    groupdoc["gagslug"].append(s.stored_fields(docnum)['agent_slug'])
                    # group airline_name
                    groupdoc["gairname"].append(s.stored_fields(docnum)['airline_name'])
                    # group rate_hotel
                    groupdoc["gratehotel"].append(s.stored_fields(docnum)['rates_hotel'])
            groupdoc["gpslug"] = filter(None, sorted(groupdoc["gpslug"]))
            groupdoc["gpromo"] = filter(None, sorted(groupdoc["gpromo"]))
            groupdoc["gprice"] = filter(None, sorted(groupdoc["gprice"]))
            groupdoc["gdate"] = filter(None, sorted(groupdoc["gdate"]))
            groupdoc["gdisc"] = filter(None, sorted(groupdoc["gdisc"]))
            groupdoc["gagcity"] = filter(None, sorted(groupdoc["gagcity"]))
            groupdoc["gairname"] = filter(None, sorted(groupdoc["gairname"]))
            groupdoc["gratehotel"] = filter(None, sorted(groupdoc["gratehotel"]))

            # print(groupdoc["gratehotel"])
            if len(groupdoc["gpromo"]) > 0:
                # tampilkan data rank 10
                if n <= 10:
                    n += 1
                    feeder.append({
                        "Name": nameo.upper(),
                        "IsDefault": False,
                        "IsTitle": False,
                        "HasImage": False,
                        "Header": None,
                        "ObjectId": docid,
                        "AgentId": docid,
                        "agent_city": groupdoc["gagcity"][0] if len(groupdoc["gagcity"]) > 0 else 'Kota _',
                        "agent_slug": groupdoc["gagslug"][0] if len(groupdoc["gagslug"]) > 0 else 'agent_kosong',
                        "airline_name": groupdoc["gairname"][0].split("/")[0].replace(' ', '').lower() if len(
                            groupdoc["gairname"]) > 0 else 'airline_empty',
                        "rates_hotel": groupdoc["gratehotel"][-1] if len(groupdoc["gratehotel"]) > 0 else 0,
                        "PacketId": 0,
                        "NoOfPromo": len(groupdoc["gpromo"]),
                        "GroupOfPromo": groupdoc["gpromo"],
                        "PromoText": nameo,
                        "GroupOfPrice": groupdoc["gprice"],
                        "startPrice": groupdoc["gprice"][0] if len(groupdoc["gprice"]) > 0 else 0,
                        "endPrice": groupdoc["gprice"][-1] if len(groupdoc["gprice"]) > 0 else 0,
                        "GroupOfDisc": groupdoc["gdisc"],
                        "startDisc": groupdoc["gdisc"][0] if len(groupdoc["gdisc"]) > 0 else 0,
                        "endDisc": groupdoc["gdisc"][-1] if len(groupdoc["gdisc"]) > 0 else 0,
                        "startDate": groupdoc["gdate"][0].isoformat() if len(
                            groupdoc["gdate"]) > 0 else datetime.now().isoformat(),
                        "endDate": groupdoc["gdate"][-1].isoformat() if len(
                            groupdoc["gdate"]) > 0 else datetime.now().isoformat(),
                        "ResultText": nameo,
                        "ResultAddress": nameo,
                        "Image": None,
                        "RetinaImage": None,
                        "BgImageLoader": None,
                        "type": tipe,
                        "match": groupdoc["gpslug"][0],
                        "tagging": tagging
                    })

                """group list untuk params header"""
                grouppromo.extend(groupdoc["gpromo"])
                groupprice.extend(groupdoc["gprice"])
                groupdate.extend(groupdoc["gdate"])
                groupdisc.extend(groupdoc["gdisc"])

        """kategori agent group promo """
        grouppromo = sorted(grouppromo)
        groupprice = sorted(groupprice)
        groupdate = sorted(groupdate)
        groupdisc = sorted(groupdisc)
        feed.append({
            "Name": None,
            "IsDefault": False,
            "IsTitle": True,
            "HasImage": False,
            "Header": header,
            "ObjectId": 0,
            "AgentId": 0,
            "agent_city": None,
            "agent_slug": None,
            "airline_name": None,
            "rates_hotel": 0,
            "PacketId": 0,
            "NoOfPromo": len(grouppromo),
            "GroupOfPromo": grouppromo,
            "PromoText": None,
            "GroupOfPrice": groupprice,
            "startPrice": groupprice[0] if len(groupprice) > 0 else 0,
            "endPrice": groupprice[-1] if len(groupprice) > 0 else 0,
            "GroupOfDisc": groupdisc,
            "startDisc": groupdisc[0] if len(groupdisc) > 0 else 0,
            "endDisc": groupdisc[-1] if len(groupdisc) > 0 else 0,
            "startDate": groupdate[0].isoformat() if len(groupdate) > 0 else 0,
            "endDate": groupdate[-1].isoformat() if len(groupdate) > 0 else 0,
            "ResultText": allpick,
            "ResultAddress": allpick,
            "Image": None,
            "RetinaImage": None,
            "BgImageLoader": None,
            "type": None,
            "match": None,
            "tagging": None
        })
        feed.extend(feeder)
        return feed
    except (KeyError, ValueError, TypeError) as e:
        s._field_caches.clear()
        log.error(e)


def list_all_promo(glist):
    feed = []
    groupprice = []
    for hit in glist:
        allow_date = (hit['end_date'] - timedelta(days=hit['last_book'])) - datetime.now()
        if (allow_date.days - 1) >= 0:
            feed.append(hit['end_date'])
            groupprice.append(hit['price'])
    feed = sorted(feed)
    groupprice = sorted(groupprice)
    return [{"Name": None,
             "IsDefault": True,
             "IsTitle": True,
             "HasImage": False,
             "Header": "Tampilkan semua paket",
             "ObjectId": 0,
             "AgentId": 0,
             "agent_city": None,
             "agent_slug": None,
             "airline_name": None,
             "rates_hotel": 0,
             "PacketId": 0,
             "NoOfPromo": len(feed),
             "GroupOfPromo": None,
             "PromoText": None,
             "GroupOfPrice": None,
             "startPrice": 0,
             "endPrice": 0,
             "GroupOfDisc": None,
             "startDisc": groupprice[0] if len(groupprice) > 0 else 0,
             "endDisc": groupprice[-1] if len(groupprice) > 0 else 0,
             "startDate": feed[0].isoformat() if len(feed) > 0 else 0,
             "endDate": feed[-1].isoformat() if len(feed) > 0 else 0,
             "ResultText": "Tampilkan semua paket",
             "ResultAddress": "Tampilkan semua paket",
             "Image": None,
             "RetinaImage": None,
             "BgImageLoader": None,
             "type": None,
             "match": None,
             "tagging": None}]


# digunakan untuk proses building analisa
@view_config(route_name='kensaku_build', renderer='templates/kensaku/kensaku_beta.mako')
def kensaku_build(request):
    return {'ok': 1}


@view_config(route_name='results_build', renderer='json')
def results_build(request):
    try:
        tipe = request.params.get('type', '')
        match = request.params.get('match', '')
        terms = request.params.get('q', '')
        if len(terms) <= 0:
            print('log terms kosong')
            # default term kosong
            return render_empty_term(req=request)
        # api evolution
        linq = get_linq(terms, tipe, match)
        # /api/v1/test_rails?q=patuna&type=packet&match=paket-biru-by-qatar-via-jeddah
        # list join
        return render_promo_beta(get_searcher(), linq, req=request)
    except(KeyError, ValueError) as e:
        log.error(e.message)


def render_promo_beta(ix, terms, req):
    with ix.searcher(weighting=TF_IDF()) as s:
        qp = qparser.MultifieldParser(["promo_tags",
                                       "content_packet",
                                       "content_agent",
                                       "promo_name",
                                       "tpl_hotel_airline"], s.schema)
        try:
            # terms = u"{term} AND (agent_slug:{match})".format(term=terms, match=u"al-amsor")
            q = qp.parse(terms)
            print(q)
            sts = NumericRange("status_promo", 1, 1)
            oldDate = DateRange("end_date", None, datetime.now())
            scores = ScoreFacet()
            results = s.search(q, limit=None, filter=sts, mask=oldDate,
                               sortedby=scores, groupedby=["packet_id", "agent_id"])
            feed = []
            # set all promo on search
            feed.extend(list_all_promo(results))
            paket = results.groups('packet_id')
            feed.extend(get_list_json(s, paket, ListType.PACKETS))
            biro = results.groups('agent_id')
            feed.extend(get_list_json(s, biro, ListType.AGENTS))

        except (KeyError, ValueError) as e:
            qp = None
            feed = None
            s._field_caches.clear()
            log.error(e.message)
    return Response(
        body=json.dumps(feed),
        status='201 Created',
        charset='UTF-8',
        content_type='application/json;')
