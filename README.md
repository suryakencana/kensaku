kensaku

layanan pencarian paket promo umroh ikhram.com

kensaku
pencarian untuk paket promo di ikhram.com yang menggunakan library pure-python: whoosh

dibangun diatas python 2.7
cli:
- pip install virtualvenv
- virtualvenv -p python2.7 pyr2-env
- source ~/.virtualvenv/pyr2-env/bin/activate

requirement:
- pyramid
- pyramid_mako
- pyramid_tm
- pyramid-debugtoolbar==1.0.9
- whoosh
- waitress
- gunicorn
- pymongo

build index di mongo
- python scripts/build_index_mongo.py

buat index untuk whoosh lib
- python scripts/index_promo_idx.py
