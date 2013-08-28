Dependencies
=========

[docopt](http://docopt.org/)
```sh
pip install docopt
```

Description
=========
Copies media files from source directory to destination folder
and splits them into folders by date.
e.g
* 2013 (year)
    + 02 (month)
        + image.jpg

or

* 2013-02 (year - month)
    + image.jpg


Usage
=========
```sh
$ python photcat.py SOURCE_DIR DESTINATION_DIR
```

```sh
$ python photcat.py DESTINATION_DIR
```
