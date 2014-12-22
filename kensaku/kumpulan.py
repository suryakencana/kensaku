"""
 # Copyright (c) 12 2014 | surya
 # 03/12/14 nanang.ask@kubuskotak.com
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
 #  kumpulan.py
"""
from pymongo import MongoClient
from whoosh import qparser, highlight
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh.sorting import Facets
from whooshsearch.views import SOURCEDIR


def render_results(s, terms, req):
    qp = qparser.QueryParser("content", s.schema)
    qp = qparser.MultifieldParser(["tgrams", "content"], s.schema)

    # Add the DateParserPlugin to the parser
    qp.add_plugin(DateParserPlugin())

    q = qp.parse(terms)

    results = s.search(q, limit=100)
    results = s.search(q, limit=100, sortedby="title", reverse=True)
    results = s.search(q, limit=100, groupedby="chapter")
    q = results.q

    hf = highlight.HtmlFormatter()
    results.highlighter = highlight.Highlighter(formatter=hf)

    qc = None
    if not results:
        corrected = s.correct_query(q, terms, prefix=1)
        if corrected.query != q:
            qc = corrected.format_string(hf)

    def hilite(hit):
        with open(SOURCEDIR + hit["path"], "rb") as hitfile:
            text = hitfile.read().decode("utf-8")
        return hit.highlights("content", text)

    return {'qs': terms,
            'q': q,
            'results': results,
            'hilite': hilite,
            'corrected': qc,
            'args': req.params}


def render_libraries(s, terms, req):
    qp = qparser.QueryParser("content", s.schema)
    qp = qparser.MultifieldParser(["tgrams", "content"], s.schema)

    # Add the DateParserPlugin to the parser
    qp.add_plugin(DateParserPlugin())

    q = qp.parse(terms)
    pathFacet = Facets()
    pathFacet.add_field("path_table")
    pathFacet.add_field("tag", allow_overlap=True)
    results = s.search(q, limit=100)
    # results = s.search(q, limit=100, sortedby="title")
    results = s.search(q, limit=100, groupedby=pathFacet)
    q = results.q

    hf = highlight.HtmlFormatter()
    results.highlighter = highlight.Highlighter(formatter=hf)

    qc = None
    if not results:
        corrected = s.correct_query(q, terms, prefix=1)
        if corrected.query != q:
            qc = corrected.format_string(hf)

    def hilite(hit):
        # with open(SOURCEDIR + hit["path"], "rb") as hitfile:
        conn = MongoClient('localhost', 27017)
        db = conn['ikhram']
        lib = req.db['libraries']
        # lib = db.libraries
        promo = req.db['umrah_promotions']
        # promo = db.umrah_promotions
        # text = lib.find_one({'reference_id': hit["path_id"]})
        count = promo.find({'{}_id'.format(hit["tag"]): hit["path_id"]}).count()
        # text = hitfile.read().decode("utf-8")
        # print(count)
        # return hit.highlights("content", text=hit["title"])
        return 'promo ({0})'.format(count)

    return {'qs': terms,
            'q': q,
            'results': results,
            'hilite': hilite,
            'corrected': qc,
            'args': req.params}


def render_promo(s, terms, req):
    # s.set_caching_policy(save=False)
    qp = qparser.QueryParser("content_packet", s.schema)
    qp = qparser.MultifieldParser(["promo_ngramword",
                                   "content_packet",
                                   "content_agent"], s.schema)

    # Add the DateParserPlugin to the parser
    # qp.add_plugin(DateParserPlugin())
    # qp.add_plugin(GtLtPlugin())
    # terms = u'{0} status_promo:[0 TO 2]'.format(terms)
    q = qp.parse(terms)

    # pathFacet = Facets()
    # # pathFacet.add_facet("status_promo", facet=RangeFacet())
    # numFacet = RangeFacet("promo_id", 0, 2, 100)
    # pathFacet.add_field("packet_id")
    # pathFacet.add_field("agent_id")
    # filter_sts = NumericRange("promo_id", 0, 1000)
    # results = s.search(q, limit=100, filter=filter_sts)

    results = s.search_page(q, 1, 10, sortedby="status_promo", maptype=Best)
    # results = s.search(q, limit=10, sortedby="promo_name")
    # results = s.search(q, limit=20, filter=filter_sts)
    # results = s.search(q, limit=10,  groupedby=["packet_id", "agent_id"])
    results = s.search_page(q, 1, 10, groupedby=["packet_id", "agent_id"])
    q = results.results

    # print(s.suggest('content_packet', terms))
    packets = results.results.groups('packet_id')
    # # print(len(packets))
    #
    for i, packg in enumerate(packets):
        if i > 1:
            break
        doclist = packets[packg]
        paket = req.db['promo_idx']
        pp = paket.find_one({'packet_id': packg})
        print(packg)
        print("By Paket Packet {0} Promo Total: {1}".format(pp['packet_name'], len(doclist)))

        # doclist = packets[packg]
        # print(doclist)
        # print("Packet Promo Total: {0}".format(len(doclist)))
        # for docnum in doclist:
        # print(s.stored_fields(docnum)['promo_name'])
        #     # for docnum, score in doclist[:5]:
    else:
        print('break else')

    print("=================================================================")

    agents = results.results.groups('agent_id')
    # print(len(packets))

    for i, agent in enumerate(agents):
        if i > 1:
            break
        doclist = agents[agent]
        # agent
        print(agent)
        paket = req.db['promo_idx']
        pp = paket.find_one({'agent_id': agent})
        # print(packg)
        print("By Agent {2} Packet {0} Promo Total: {1}".format(pp['packet_name'], len(doclist), pp['agent_name']))

        # for docnum in doclist:
        #     print(s.stored_fields(docnum))
        #     # for docnum, score in doclist[:5]:
    else:
        print('break else')

    hf = highlight.HtmlFormatter()
    # print(s.correct_query(q, terms, prefix=1).string)
    results.highlighter = highlight.Highlighter(formatter=hf)

    # qc = Nonedd
    # if not results:
    # corrected = s.correct_query(q, terms, prefix=1)
    #     if corrected.query != q:
    #         qc = corrected.format_string(hf)

    # def hilite(hit):
    #     # with open(SOURCEDIR + hit["path"], "rb") as hitfile:
    #     conn = MongoClient('localhost', 27017)
    #     db = conn['ikhram']
    #     lib = req.db['libraries']
    #     # lib = db.libraries
    #     promo = req.db['umrah_promotions']
    #     # promo = db.umrah_promotions
    #     # text = lib.find_one({'reference_id': hit["path_id"]})
    #     count = promo.find({'{}_id'.format(hit["tag"]): hit["path_id"]}).count()
    #     # text = hitfile.read().decode("utf-8")
    #     # print(count)
    #     # return hit.highlights("content", text=hit["title"])
    #     return 'promo ({0})'.format(count)

    return {'qs': terms,
            'q': q,
            'results': results.results,
            'resultpages': results,
            # 'hilite': hilite,
            # 'corrected': qc,
            'args': req.params}
    # return {'top': 1}

