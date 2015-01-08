import json
import logging
import os
from datetime import datetime
from pymongo import DESCENDING

from pyramid.response import Response
from pyramid.view import view_config
from whoosh import index, qparser
from whoosh.query.ranges import NumericRange, DateRange
from whoosh.scoring import TF_IDF
from whoosh.sorting import Best


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


"""
Bagian untuk proses search action
"""


@view_config(route_name='kensaku', renderer='templates/kensaku/kensaku_page.mako')
def kensaku(request):
    return {'ok': 1}


"""
Bagian untuk proses finishing UI search botton
"""

#
# @view_config(route_name='suggest', request_method='POST', render='json')
# def suggest(request):
# return ['info', 1]
"""
Bagian untuk proses range date and price search
"""


@view_config(route_name='valid', request_method='POST', renderer='json')
def valid_button(request):
    dataSet = 0
    try:
        args = request.params.get('arrPromo', '')
        start = request.params.get('startDate', datetime.now())
        end = request.params.get('endDate', datetime.now())
        whatPrice = request.params.get('whatPrice', '').split('~')
        arrPromo = args.split(',')

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
        dataSet = 0
    finally:
        return Response(
            body=json.dumps({'data': {
                'count': count,
                'price': price[0] if len(price) >= 1 else 0
            }}),
            status='201 Created',
            charset='UTF-8',
            content_type='application/json;')


@view_config(route_name='home', renderer='templates/whoosh/search.mako')
def search(request):
    return {'args': request.params}


@view_config(route_name='results', renderer='json')
def results(request):
    try:
        terms = request.params.get("q", '')
        if len(terms) <= 0:
            print('log terms kosong')
            # default term kosong
            return render_empty_term(req=request)
        return render_promo_by(get_searcher(), terms, req=request)
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
        promo = req.db['umrah_promotions']
        results = promo.find({
            'departure_date': {
                '$gte': datetime.now()
            },
            'status': 1
        }).sort('viewed', DESCENDING).limit(10)
        # print(datetime.now())
        # for row in results:
        #     print(row)
        if results:
            for row in results:
                grouppop.extend([row.get('promo_id', None)])
                groupprice.extend([row.get('starting_price', 0)])
                groupdisc.extend([row.get('discount', 0)])
                groupdate.extend([row.get('departure_date', 0).isoformat()])
                feeder.append({
                    "Name": str(row.get('title', 'No title')).capitalize(),
                    "IsDefault": True,
                    "IsTitle": False,
                    "HasImage": False,
                    "Header": None,
                    "ObjectId": None,
                    "AgentId": None,
                    "PacketId": row.get('promo_id', None),
                    "NoOfPromo": 1,
                    "GroupOfPromo": 1,
                    "PromoText": str(row.get('title', 'No title')),
                    "GroupOfPrice": 0,
                    "startPrice": row.get('starting_price', 0),
                    "endPrice": 0,
                    "GroupOfDisc": 0,
                    "startDisc": row.get('discount', 0),
                    "endDisc": row.get('discount', 0),
                    "startDate": row.get('departure_date', 0).isoformat(),
                    "endDate": row.get('departure_date', 0).isoformat(),
                    "ResultText": str(row.get('title', 'No title')).upper(),
                    "ResultAddress": str(row.get('title', 'No title')).upper(),
                    "Image": None,
                    "RetinaImage": None,
                    "BgImageLoader": None,
                    "tagging": "PAKET"
                })

            feed.append({
                "Name": None,
                "IsDefault": True,
                "IsTitle": True,
                "HasImage": False,
                "Header": "Paket Populer",
                "ObjectId": 0,
                "AgentId": 0,
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


def get_list_biro(s, results, req):
    """Fungsi list promo umroh berdasarkan biro"""
    try:
        feed = []
        feeder = []
        groupagent = []
        groupprice = []
        groupdate = []
        groupdisc = []
        agents = results.results.groups('agent_id')
        # print(len(packets))

        for i, agent in enumerate(agents):
            if i > 10:
                break
            doclist = agents[agent]
            # agent
            print(agent)
            paket = req.db['libraries']
            pp = paket.find_one({'tag': 'AGENT', 'reference_id': agent})
            if pp is not None:
                #     print(packg)
                print("By Agent {1}  Promo Total: {0}".format(pp['name'], len(doclist), pp['name']))

                # for docnum in doclist:
                #     print(s.stored_fields(docnum))
                #     # for docnum, score in doclist[:5]:
                nameo = unicode(pp.get('name', 'Nama Agen')).capitalize()
                # group promo per agent
                gpagent = [s.stored_fields(docnum)['promo_id'] for docnum in doclist]
                # group price per promo untuk mencari range paling murah
                gpprice = sorted([s.stored_fields(docnum)['price'] for docnum in doclist])
                # group departure date per promo untuk mencari range tanggal keberangkatan paling awal
                gpdate = sorted([s.stored_fields(docnum)['end_date'] for docnum in doclist])
                # group disc promo
                gpdisc = sorted([s.stored_fields(docnum)['disc_promo'] for docnum in doclist])

                # print(gpdate)
                # print(gpdate[-1].isoformat())

                """group list untuk params header"""
                groupagent.extend(gpagent)
                groupprice.extend(gpprice)
                groupdate.extend(gpdate)
                groupdisc.extend(gpdisc)
                feeder.append({
                    "Name": nameo.upper(),
                    "IsDefault": False,
                    "IsTitle": False,
                    "HasImage": False,
                    "Header": None,
                    "ObjectId": agent,
                    "AgentId": agent,
                    "PacketId": 0,
                    "NoOfPromo": len(doclist),
                    "GroupOfPromo": gpagent,
                    "PromoText": nameo,
                    "GroupOfPrice": gpprice,
                    "startPrice": gpprice[0],
                    "endPrice": gpprice[-1],
                    "GroupOfDisc": gpdisc,
                    "startDisc": gpdisc[0],
                    "endDisc": gpdisc[-1],
                    "startDate": gpdate[0].isoformat(),
                    "endDate": gpdate[-1].isoformat(),
                    "ResultText": nameo.upper(),
                    "ResultAddress": nameo.upper(),
                    "Image": None,
                    "RetinaImage": None,
                    "BgImageLoader": None,
                    "tagging": "AGENT"
                })
        else:
            print('break else')

        """
        kategori agent group promo
        """
        feed.append({
            "Name": None,
            "IsDefault": False,
            "IsTitle": True,
            "HasImage": False,
            "Header": "Travel Umroh",
            "ObjectId": 0,
            "AgentId": 0,
            "PacketId": 0,
            "NoOfPromo": len(groupagent),
            "GroupOfPromo": groupagent,
            "PromoText": None,
            "GroupOfPrice": groupprice,
            "startPrice": groupprice[0] if len(groupprice) > 0 else 0,
            "endPrice": groupprice[-1] if len(groupprice) > 0 else 0,
            "GroupOfDisc": groupdisc,
            "startDisc": groupdisc[0] if len(groupdisc) > 0 else 0,
            "endDisc": groupdisc[-1] if len(groupdisc) > 0 else 0,
            "startDate": groupdate[0].isoformat() if len(groupdate) > 0 else 0,
            "endDate": groupdate[-1].isoformat() if len(groupdate) > 0 else 0,
            "ResultText": "Semua Biro Umroh",
            "ResultAddress": "Semua Biro Umroh",
            "Image": None,
            "RetinaImage": None,
            "BgImageLoader": None,
            "tagging": None
        })

        feed.extend(feeder)
        return feed

    except (KeyError, ValueError) as e:
        qp = None
        s._field_caches.clear()
        log.error(e.message)


def get_list_packet(s, results, req):
    """Fungsi list promo umroh berdasarkan paket umroh"""

    try:
        feed = []
        feeder = []
        grouppacket = []
        groupprice = []
        groupdate = []
        groupdisc = []
        packets = results.results.groups('packet_id')
        for i, packg in enumerate(packets):
            if i > 10:
                break
            doclist = packets[packg]
            paket = req.db['promo_idx']
            pp = paket.find_one({'packet_id': packg})

            if pp is not None:
                # print(packg)
                print("By Paket Packet {0} Promo Total: {1}".format(pp['packet_name'], len(doclist)))

                # doclist = packets[packg]
                # print(doclist)
                # print("Packet Promo Total: {0}".format(len(doclist)))
                # for docnum in doclist:
                #     print(s.stored_fields(docnum)['promo_name'])
                #     # for docnum, score in doclist[:5]:
                nameo = unicode(pp['packet_name']).capitalize()
                _objid = pp.get('packet_id', 0)
                """List untuk group fields params"""
                gppackets = [s.stored_fields(docnum)['promo_id'] for docnum in doclist]
                # group price per promo untuk mencari range paling murah
                gpprice = sorted([s.stored_fields(docnum)['price'] for docnum in doclist])
                # group departure date per promo untuk mencari range tanggal keberangkatan paling awal
                gpdate = sorted([s.stored_fields(docnum)['end_date'] for docnum in doclist])
                # group disc
                gpdisc = sorted([s.stored_fields(docnum)['disc_promo'] for docnum in doclist])

                print(gpdate)
                """group list untuk params header"""
                grouppacket.extend(gppackets)
                groupprice.extend(gpprice)
                groupdate.extend(gpdate)
                groupdisc.extend(gpdisc)

                feeder.append({
                    "Name": nameo.upper(),
                    "IsDefault": False,
                    "IsTitle": False,
                    "HasImage": False,
                    "Header": None,
                    "ObjectId": _objid,
                    "AgentId": 0,
                    "PacketId": _objid,
                    "NoOfPromo": len(doclist),
                    "GroupOfPromo": gppackets,
                    "PromoText": nameo,
                    "GroupOfPrice": gpprice,
                    "startPrice": gpprice[0],
                    "endPrice": gpprice[-1],
                    "GroupOfDisc": gpdisc,
                    "startDisc": gpdisc[0],
                    "endDisc": gpdisc[-1],
                    "startDate": gpdate[0].isoformat(),
                    "endDate": gpdate[-1].isoformat(),
                    "ResultText": nameo,
                    "ResultAddress": nameo,
                    "Image": None,
                    "RetinaImage": None,
                    "BgImageLoader": None,
                    "tagging": "PACKETS"
                })
        else:
            print('break else')

        """
        kategori packet group promo
        """
        groupprice = sorted(groupprice)
        feed.append({
            "Name": None,
            "IsDefault": False,
            "IsTitle": True,
            "HasImage": False,
            "Header": "Paket Umroh",
            "ObjectId": 0,
            "AgentId": 0,
            "PacketId": 0,
            "NoOfPromo": len(grouppacket),
            "GroupOfPromo": grouppacket,
            "PromoText": None,
            "GroupOfPrice": groupprice,
            "startPrice": groupprice[0] if len(groupprice) > 0 else 0,
            "endPrice": groupprice[-1] if len(groupprice) > 0 else 0,
            "GroupOfDisc": groupdisc,
            "startDisc": groupdisc[0] if len(groupdisc) > 0 else 0,
            "endDisc": groupdisc[-1] if len(groupdisc) > 0 else 0,
            "startDate": groupdate[0].isoformat() if len(groupdate) > 0 else 0,
            "endDate": groupdate[-1].isoformat() if len(groupdate) > 0 else 0,
            "ResultText": "Semua Paket Umroh",
            "ResultAddress": "Semua Paket Umroh",
            "Image": None,
            "RetinaImage": None,
            "BgImageLoader": None,
            "tagging": None
        })

        feed.extend(feeder)
        return feed
    except (KeyError, ValueError) as e:
        qp = None
        s._field_caches.clear()
        log.error(e.message)


def render_promo_by(ix, terms, req):
    with ix.searcher(weighting=TF_IDF()) as s:
        # og = qparser.OrGroup.factory(0.9)
        # qp = qparser.QueryParser("content_packet", s.schema)
        qp = qparser.MultifieldParser(["promo_tags",
                                       "content_packet",
                                       "promo_name",
                                       "tpl_hotel_airline"], s.schema)

        try:
            q = qp.parse(terms)
            sts = NumericRange("status_promo", 1, 1)
            oldDate = DateRange("end_date", None, datetime.now())
            results = s.search_page(q, 1, 10, sortedby="status_promo", maptype=Best)
            results = s.search_page(q, 1, 10, filter=sts, mask=oldDate, groupedby=["packet_id", "agent_id"])
            q = results.results


            # print("=================================================================")
            feed = []
            feed.extend(get_list_packet(s, results, req))
            feed.extend(get_list_biro(s, results, req))

            # feeder = []
            # groupagent = []
            # agents = results.results.groups('agent_id')
            # # print(len(packets))
            #
            # for i, agent in enumerate(agents):
            #     if i > 10:
            #         break
            #     doclist = agents[agent]
            #     # agent
            #     print(agent)
            #     paket = req.db['libraries']
            #     pp = paket.find_one({'tag': 'AGENT', 'reference_id': agent})
            #     if pp is not None:
            #         #     print(packg)
            #         print("By Agent {1}  Promo Total: {0}".format(pp['name'], len(doclist), pp['name']))
            #
            #         # for docnum in doclist:
            #         #     print(s.stored_fields(docnum))
            #         #     # for docnum, score in doclist[:5]:
            #         nameo = unicode(pp.get('name', 'Nama Agen')).capitalize()
            #         # group promo per agent
            #         gpagent = [s.stored_fields(docnum)['promo_id'] for docnum in doclist]
            #         # group price per promo untuk mencari range paling murah
            #         gpprice = sorted([s.stored_fields(docnum)['price'] for docnum in doclist])
            #         # group departure date per promo untuk mencari range tanggal keberangkatan paling awal
            #         gpdate = sorted([s.stored_fields(docnum)['end_date'] for docnum in doclist])
            #         # print(gpdate)
            #         # print(gpdate[-1].isoformat())
            #         groupagent.extend(gpagent)
            #         feeder.append({
            #             "Name": nameo.upper(),
            #             "IsTitle": False,
            #             "HasImage": False,
            #             "Header": None,
            #             "ObjectId": agent,
            #             "AgentId": agent,
            #             "PacketId": 0,
            #             "NoOfPromo": len(doclist),
            #             "GroupOfPromo": gpagent,
            #             "PromoText": nameo,
            #             "GroupOfPrice": gpprice,
            #             "startPrice": gpprice[0],
            #             "endPrice": gpprice[-1],
            #             "startDate": gpdate[0].isoformat(),
            #             "endDate": gpdate[-1].isoformat(),
            #             "ResultText": nameo.upper(),
            #             "ResultAddress": nameo.upper(),
            #             "Image": None,
            #             "RetinaImage": None,
            #             "BgImageLoader": None,
            #             "tagging": "AGENT"
            #         })
            # else:
            #     print('break else')
            #
            # """
            # kategori agent group promo
            # """
            # feed.append({
            #     "Name": None,
            #     "IsTitle": True,
            #     "HasImage": False,
            #     "Header": "Travel Umroh",
            #     "ObjectId": 0,
            #     "AgentId": 0,
            #     "PacketId": 0,
            #     "NoOfPromo": len(groupagent),
            #     "GroupOfPromo": groupagent,
            #     "GroupOfDiscount":
            #     "PromoText": None,
            #     "GroupOfPrice": 0,
            #     "startPrice": 0,
            #     "endPrice": 0,
            #     "startDate": None,
            #     "endDate": None,
            #     "ResultText": None,
            #     "ResultAddress": None,
            #     "Image": None,
            #     "RetinaImage": None,
            #     "BgImageLoader": None,
            #     "tagging": None
            # })
            #
            # feed.extend(feeder)

            # print("+++++++++++++++++++++++++++++++++++++++")

            # feeder = []
            # grouppacket = []
            # packets = results.results.groups('packet_id')
            # for i, packg in enumerate(packets):
            #     if i > 10:
            #         break
            #     doclist = packets[packg]
            #     paket = req.db['promo_idx']
            #     pp = paket.find_one({'packet_id': packg})
            #
            #     if pp is not None:
            #         # print(packg)
            #         print("By Paket Packet {0} Promo Total: {1}".format(pp['packet_name'], len(doclist)))
            #
            #         # doclist = packets[packg]
            #         # print(doclist)
            #         # print("Packet Promo Total: {0}".format(len(doclist)))
            #         # for docnum in doclist:
            #         #     print(s.stored_fields(docnum)['promo_name'])
            #         #     # for docnum, score in doclist[:5]:
            #         nameo = unicode(pp['packet_name']).capitalize()
            #         _objid = pp.get('packet_id', 0)
            #         gppackets = [s.stored_fields(docnum)['promo_id'] for docnum in doclist]
            #         # group price per promo untuk mencari range paling murah
            #         gpprice = sorted([s.stored_fields(docnum)['price'] for docnum in doclist])
            #         # group departure date per promo untuk mencari range tanggal keberangkatan paling awal
            #         gpdate = sorted([s.stored_fields(docnum)['end_date'] for docnum in doclist])
            #         print(gpdate)
            #         grouppacket.extend(gppackets)
            #         feeder.append({
            #             "Name": nameo.upper(),
            #             "IsTitle": False,
            #             "HasImage": False,
            #             "Header": None,
            #             "ObjectId": _objid,
            #             "AgentId": 0,
            #             "PacketId": _objid,
            #             "NoOfPromo": len(doclist),
            #             "GroupOfPromo": gppackets,
            #             "PromoText": nameo,
            #             "GroupOfPrice": gpprice,
            #             "startPrice": gpprice[0],
            #             "endPrice": gpprice[-1],
            #             "startDate": gpdate[0].isoformat(),
            #             "endDate": gpdate[-1].isoformat(),
            #             "ResultText": nameo,
            #             "ResultAddress": nameo,
            #             "Image": None,
            #             "RetinaImage": None,
            #             "BgImageLoader": None,
            #             "tagging": "PACKETS"
            #         })
            # else:
            #     print('break else')
            #
            # """
            # kategori packet group promo
            # """
            # feed.append({
            #     "Name": None,
            #     "IsTitle": True,
            #     "HasImage": False,
            #     "Header": "Paket Umroh",
            #     "ObjectId": 0,
            #     "AgentId": 0,
            #     "PacketId": 0,
            #     "NoOfPromo": len(grouppacket),
            #     "GroupOfPromo": grouppacket,
            #     "PromoText": None,
            #     "GroupOfPrice": 0,
            #     "startPrice": 0,
            #     "endPrice": 0,
            #     "startDate": None,
            #     "endDate": None,
            #     "ResultText": None,
            #     "ResultAddress": None,
            #     "Image": None,
            #     "RetinaImage": None,
            #     "BgImageLoader": None,
            #     "tagging": None
            # })
            #
            # feed.extend(feeder)

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