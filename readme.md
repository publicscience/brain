Public Science Brain
====================

## Setup
It's recommended that you use a virtualenv:
```
$ virtualenv-3.3 ~/envs/brain --no-site-packages
$ source ~/envs/brain/bin/activate
```

Run [MongoDB](http://www.mongodb.org/downloads):
```
$ mongod
```

Clone repo and then install dependencies:
```
$ git clone https://github.com/publicscience/brain.git
$ cd brain
$ pip install -r requirements.txt
```

Setup Flask configuration:
```
$ mv config-sample.py config.py
$ vi config.py
```

Setup [Twitter API](https://dev.twitter.com/apps) access:
```
$ mv app/brain/config-sample.json app/brain/config.json
$ vi app/brain/config.json
```
(see below for more info)

Run tests to make sure everything's working:
```
$ nosetests
```

Run the Flask application:
```
$ python application.py
```

Check out the site at `localhost:5000` (by default).

The important endpoints at the moment are `/muses/` and `/config/`.


## Twitter API
To setup Twitter API access for your Twitter account:

1. Authorize Twitter development access to your account [through
   here](https://dev.twitter.com/apps).

2. Register your application through that process.

3. On your app's page in the Twitter dev site, set its `Access level` to
   `Read and write`.

4. Then generate an access token for your app.

5. Set the required values in `app/brain/config.json`.


Dev Notes
=========

```
/flask_mongoengine/wtf/orm.py
line 225 has a Python 3 incompatibility.
It uses iteritems(), it should be items().
```