kensaku

:untuk git new repo
touch README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/suryakencana/kensaku.git
git push -u origin master

:untuk git exists repo
git remote add origin https://github.com/suryakencana/kensaku.git
git push -u origin master

:untuk install mysql connector python
shell> pip install mysql-connector-python
  Could not find any downloads that satisfy the requirement
    mysql-connector-python
  Some externally hosted files were ignored
    (use --allow-external mysql-connector-python to allow).

- mongorestore --dbpath /srv/mongodb
- mongorestore --host mongodb1.example.net --port 37017 --username user --password pass /opt/backup/mongodump-2011-10-24

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
