# -*- coding: utf-8 -*-

# This file is part of Python Challenge Solutions
# https://github.com/scorphus/PythonChallengeSolutions

# Licensed under the BSD-3-Clause license:
# https://opensource.org/licenses/BSD-3-Clause
# Copyright (c) 2018-2020, Pablo S. Blum de Aguiar <scorphus@gmail.com>

# http://www.pythonchallenge.com/

from base64 import encodebytes
from cache import autocached
from urllib.request import Request
from urllib.request import urlopen


credentials = {
    "http://www.pythonchallenge.com/pc/return": b"huge:file",
    "http://www.pythonchallenge.com/pc/hex": b"butter:fly",
    "http://www.pythonchallenge.com/pc/ring": b"repeat:switch",
    "http://www.pythonchallenge.com/pc/rock": b"kohsamui:thailand",
}


def get_credentials(url):
    base_url = url.rsplit("/", 1)[0]
    return credentials.get(base_url, b"")


def open_url(url, headers={}):
    auth = encodebytes(get_credentials(url)).decode().rstrip()
    headers = {"Authorization": f"Basic {auth}", **headers} if auth else headers
    return urlopen(Request(url=url, headers=headers))


@autocached
def read_url(url, headers={}):
    return open_url(url, headers).read()


@autocached
def read_url_and_headers(url, headers={}):
    resp = open_url(url, headers)
    return resp.read(), resp.headers


def read_riddle(url, headers={}):
    """Reads and returns the content of the mission at `url`"""
    return read_url(url, headers).decode()


def get_last_attr(url, attr):
    """Extracts the URL of the last `attr` attribute in the mission at `url`"""
    return read_riddle(url).split(f'{attr}="')[-1].split('"')[0]


def get_last_attr_url(url, attr):
    """Extracts the URL of the last `attr` attribute in the mission at `url`"""
    attr = get_last_attr(url, attr)
    return "{}/{}".format(url.rsplit("/", 1)[0], attr)


def get_last_src_url(url):
    """Extracts the URL of the last `src` attribute in the mission at `url`"""
    return get_last_attr_url(url, "src")


def get_last_href_url(url):
    """Extracts the URL of the last `href` attribute in the mission at `url`"""
    return get_last_attr_url(url, "href")


def get_longest_line(url):
    return max(read_riddle(url).splitlines(), key=len)


def get_nth_comment(url, n):
    return read_riddle(url).split("<!--", n)[n].split("-->", 1)[0]
