Dependencies
=========

[Flask]( http://flask.pocoo.org/)
```sh
pip install flask
```

[SQLAlchemy](http://www.sqlalchemy.org/)
```sh
pip install sqlalchemy
```

[Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/)
```sh
pip install flask_sqlalchemy
```

[WTForms](http://wtforms.simplecodes.com/)
```sh
pip install WTForms
```
[WTForms-Alchemy](http://wtforms-alchemy.readthedocs.org/en/latest/)
```sh
pip install WTForms-Alchemy
```

[SImpleXml](https://github.com/marcelnicolay/simplexml)
```sh
pip install python-simplexml
```

Run
=========
in debug mode
```sh
$ python ./main.py
```
in production
```sh
$ python -O -OO ./main.py
```

Usage
=========

  List of all available commands [http://localhost:5050/api/v.0.1/](http://localhost:5050/api/v.0.1/)

|  URL        | Method      | Description                  |
| ----------- |:-----------:| ----------------------------:|
| /users/     | GET             | Gives a list of all users    |
| /users/         | POST            | Creates a new user           |
| /users/id   | GET         | Shows a single user          |
| /users/id   | PUT             | Updates a single user        |
| /users/id   | DELETE      | Deletes a single user        |


List of available query options:
  * ?with=['relation'] - [http://localhost:5050/api/v.0.1/news/?with=["author"]](http://localhost:5050/api/v.0.1/news/?with=["author"])
  * ?per_page=50 - will return 50 records with total count of records. Will work only for collections. [http://localhost:5050/api/v.0.1/news/?per_page=2](http://localhost:5050/api/v.0.1/news/?per_page=2)
  * ?page=1 - page number(pagination). [http://localhost:5050/api/v.0.1/news/?per_page=2&page=2](http://localhost:5050/api/v.0.1/news/?per_page=2&page=2)
  * ?order_by="column_in_db type" - type is optional. [http://localhost:5050/api/v.0.1/news/?order_by="link"](http://localhost:5050/api/v.0.1/news/?order_by="link"), [http://localhost:5050/api/v.0.1/news/?order_by="link desc"](http://localhost:5050/api/v.0.1/news/?order_by="link desc")
  * ?filter={ dict }



simple filtering
___
```javascript
{ "author_id": 1}
//or
{ "author_id": [1,2,3]}
```

filtering >, <, <>(!=), between
___
```javascript
{
    "created_at": {
          "comparison_key": "<>",
          "value": 1
     }
}
//   or
{
    "created_at": {
        "comparison_key": "<>",
        "value": [1,2,3]
    }
}
```

___
[http://localhost:5050/api/v.0.1/news/?filter={"created_at":{"comparison_key":">", "value":"2013-04-02"}}](http://localhost:5050/api/v.0.1/news/?filter={"created_at":{"comparison_key": ">", "value":"2013-04-02"}})

___
Complex query
====
____
[http://localhost:5050/api/v.0.1/news/?filter={"created_at":{"comparison_key": "<", "value":"2013-04-02"}}&with=["author"]&per_page=2&page=2](http://localhost:5050/api/v.0.1/news/?filter={"created_at":{"comparison_key": "<", "value":"2013-04-02"}}&with=["author"]&per_page=2&page=2)

Simple http_load test
=========
```sh
$ http_load -parallel 10 -seconds 5 ./urls
514 fetches, 10 max parallel, 2.10279e+06 bytes, in 5 seconds
4091.03 mean bytes/connection
102.8 fetches/sec, 420557 bytes/sec
msecs/connect: 0.0876381 mean, 0.382 max, 0.04 min
msecs/first-response: 95.8978 mean, 136.396 max, 13.04 min
HTTP response codes:
  code 200 -- 514
```
urls file
```
http://localhost:5050/api/v.0.1/news/?with=%5B%22author%22%5D
http://localhost:5050/api/v.0.1/news/?per_page=2
http://localhost:5050/api/v.0.1/users/
```


[http://librelist.com/browser/flask/2011/9/8/hosting-multiple-flask-applications-in-a-single-apache-instance-on-webfaction/] (http://librelist.com/browser/flask/2011/9/8/hosting-multiple-flask-applications-in-a-single-apache-instance-on-webfaction/)
