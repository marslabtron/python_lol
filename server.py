#!/usr/bin/python
# -*- coding=utf-8 -*-
from functools import wraps
from flask import Flask, jsonify , make_response
import urllib2
import json
# 解决unicode错误
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# ------- cors --------
def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun


# ------- methods -------
def get_user_list_by_summoner_name(summoner):
    request_url = 'http://api.lolbox.duowan.com/api/v2/player/search/?player_name_list=%s&callback=jQuery111200161216930093' \
          '95033_1470488155157&_=1470488155158' % summoner
    res = urllib2.urlopen(request_url)
    return res_handler(res);


def get_detail_by_user_id(area,id):
    path = area + "/" + id
    request_url = "http://api.lolbox.duowan.com/api/v3/player/%s/?callback=jQuery111101163928349854364_1489317803513&_=1489317803514" \
    % path
    res = urllib2.urlopen(request_url)
    return res_handler(res);

def res_handler(res):
    raw = res.read()
    first_char_index = raw.index('(')+1
    return raw[first_char_index:-1]


# ------- server -------
application = Flask(__name__)
@application.route("/")
@allow_cross_domain
def hello():
    return "<h1 style='color:blue'>Hello Summoner!</h1>"

@application.route("/search/<summoner>")
@allow_cross_domain
def search(summoner):
    return get_user_list_by_summoner_name(summoner)

@application.route("/user/detail/<area>/<id>")
@allow_cross_domain
def userDetail(area,id):
    return get_detail_by_user_id(area,id)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
