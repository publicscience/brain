Dev Notes
=========

```
/flask_mongoengine/wtf/orm.py
line 225 has a Python 3 incompatibility.
It uses iteritems(), it should be items().
```