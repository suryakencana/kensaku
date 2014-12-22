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
 #  example-mongo.py
"""
import os

from whoosh.fields import Schema, ID, KEYWORD, TEXT
from whoosh.index import create_in
from whoosh.query import Term

from pymongo import Connection
from bson.objectid import ObjectId

# Set index, we index title and content as texts and tags as keywords.
# We store inside index only titles and ids.
schema = Schema(title=TEXT(stored=True), content=TEXT,
                nid=ID(stored=True), tags=KEYWORD)

# Create index dir if it does not exists.
if not os.path.exists("index"):
    os.mkdir("index")

# Initialize index
index = create_in("index", schema)

# Initiate db connection
connection = Connection('localhost', 27017)
db = connection["cozy-home"]
posts = db.posts

# Fill index with posts from DB
writer = index.writer()
for post in posts.find():
    writer.update_document(title=post["title"],
                           content=post["content"],
                           nid=str(post["_id"]),
                           tags=post["tags"])
writer.commit()

# Search inside index for post containing "test", then it displays
# results.
with index.searcher() as searcher:
    result = searcher.search(Term("content", u"test"))[0]
    post = posts.find_one(ObjectId(result["nid"]))
    print(result["title"])
    print(post["content"])