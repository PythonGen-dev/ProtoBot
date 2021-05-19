from __future__ import unicode_literals, print_function
import random
import json
import os
import sys
from io import BytesIO
import utils.aiopg as aiopg
import requests
from PIL import Image
from bs4 import BeautifulSoup
import struct, zlib, base64
import os
import aiohttp
from utils.exceptions import *
import functools

with open('./locals/translates.json') as json_file:
    translatesdata = json.load(json_file)
with open('./locals/emojis.json') as json_file:
    emojisdata = json.load(json_file)



with open("config.json", "r") as configjson:
    configdata = json.load(configjson)
    fetchusertoken = configdata["fetchusertoken"]
    configjson.close()
def translations(lang, val):
    try:
        return(translatesdata[lang][val])
    except: return "None"

def arraytostring(array):
    if len(array) != 1:
        string = str()
        for i in array:
            string+=i+", "
        string = string[:-2]+"."
        return string
    return array[0]+"."

def getproxies():
    proxysources = [
    "https://www.socks-proxy.net/",
    "http://free-proxy-list.net/",
    "https://sslproxies.org/",
    "https://spys.one/en/",
    "http://www.freeproxylists.net/",
    "https://advanced.name/freeproxy"]
    proxies = list()
    for i in proxysources:
        try:
            req = requests.get(i)
            part = str(req.text)
            part = part.split("<tbody>")
            part = part[1].split("</tbody>")
            part = part[0].split("<tr><td>")
        except: pass
        for proxy in part:
            proxy = proxy.split("</td><td>")
            try:
                if proxy[0] + ":" + proxy[1] not in proxies:
                    proxies.append(proxy[0] + ":" + proxy[1])
            except:
                pass
    return(proxies)

def getcustomemote(self, emote, ctx):
    if ctx.guild.me.guild_permissions.use_external_emojis:
        try: return emojisdata[emote]
        except: return ""
    else: return ''

def getcolorfromurl(imgurl):
    img = Image.open(requests.get(imgurl, stream=True).raw)
    width, height = Image.open(BytesIO(requests.get(imgurl).content)).size
    img = img.copy()
    img.thumbnail((round(width/2), round(height/2)))
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=2)
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    colorone =None
    colortwo=None
    ranga=0
    for i in range(2):
        ranga = ranga + 1
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]
        if ranga == 1: colorone = dominant_color
        else: colortwo = dominant_color
    if colorone[0] == 0 and colorone[1] == 0 and colorone [2] == 0:  return colortwo
    else: return colorone

async def apifetchuser(id):
    async with aiohttp.ClientSession(headers={'authorization': 'Bot ' + fetchusertoken}) as session:
        async with session.get(url = f"https://discordapp.com/api/v6/users/{id}") as getdata:
            return await getdata.json()

async def aiogetlang(ctx):
    try:
        lang = await aiopg.aiogetrow("langs", [["guildid", ctx.guild.id]])
        lang = lang[-1]
    except:
        lang = "RU"
    return lang

API_URL = 'http://en.wikifur.com/w/api.php'
ODD_ERROR_MESSAGE = "This shouldn't happen. Please report on GitHub"

class cache(object):
    def __init__(self, fn):
        self.fn = fn
        self._cache = {}
        functools.update_wrapper(self, fn)

    def __call__(self, *args, **kwargs):
        key = str(args) + str(kwargs)
        if key in self._cache:
            ret = self._cache[key]
        else:
            ret = self._cache[key] = self.fn(*args, **kwargs)
        return ret

    def wikifurclear_cache(self):
        self._cache = {}


def wikifurstdout_encode(u, default='UTF8'):
    encoding = sys.stdout.encoding or default
    if sys.version_info > (3, 0):
        return u.encode(encoding).decode(encoding)
    return u.encode(encoding)


@cache
def wikifursearch(query, results=10, suggestion=False):
    search_params = {
        'list': 'search',
        'srprop': '',
        'srlimit': results,
        'limit': results,
        'srsearch': query
    }
    if suggestion:
        search_params['srinfo'] = 'suggestion'
    raw_results = _wiki_request(search_params)
    if 'error' in raw_results:
        if raw_results['error']['info'] in ('HTTP request timed out.', 'Pool queue is full'):
            raise HTTPTimeoutError(query)
        else:
            raise wikifurException(raw_results['error']['info'])
    search_results = (d['title'] for d in raw_results['query']['search'])
    if suggestion:
        if raw_results['query'].get('searchinfo'):
            return list(search_results), raw_results['query']['searchinfo']['suggestion']
        else:
            return list(search_results), None
    return list(search_results)


@cache
def wikifursuggest(query):
    search_params = {
        'list': 'search',
        'srinfo': 'suggestion',
        'srprop': '',
    }
    search_params['srsearch'] = query
    raw_result = _wiki_request(search_params)
    if raw_result['query'].get('searchinfo'):
        return raw_result['query']['searchinfo']['suggestion']
    return None


@cache
def wikifursummary(title, sentences=0, chars=0, auto_suggest=True, redirect=True):
    page_info = wikifurpage(title, auto_suggest=auto_suggest, redirect=redirect)
    title = page_info.title
    pageid = page_info.pageid
    query_params = {
        'prop': 'extracts',
        'explaintext': '',
        'titles': title
    }
    if sentences:
        query_params['exsentences'] = sentences
    elif chars:
        query_params['exchars'] = chars
    else:
        query_params['exintro'] = ''
    request = _wiki_request(query_params)
    summary = request['query']['pages'][pageid]['extract']
    return summary


def wikifurpage(title=None, pageid=None, auto_suggest=True, redirect=True, preload=False):
    if title is not None:
        if auto_suggest:
            results, suggestion = wikifursearch(title, results=1, suggestion=True)
            try:
                title = suggestion or results[0]
            except IndexError:
                raise PageError(title)
        return wikifurPage(title, redirect=redirect, preload=preload)
    elif pageid is not None:
        return wikifurPage(pageid=pageid, preload=preload)
    else:
        raise ValueError("Either a title or a pageid must be specified")


class wikifurPage(object):
    def __init__(self, title=None, pageid=None, redirect=True, preload=False, original_title=''):
        if title is not None:
            self.title = title
            self.original_title = original_title or title
        elif pageid is not None:
            self.pageid = pageid
        else:
            raise ValueError("Either a title or a pageid must be specified")
        self.__load(redirect=redirect, preload=preload)
        if preload:
            for prop in ('content', 'summary', 'images', 'references', 'links', 'sections'):
                getattr(self, prop)

    def __repr__(self):
        return wikifurstdout_encode(u'<wikifurPage \'{}\'>'.format(self.title))

    def __eq__(self, other):
        try:
            return (
                    self.pageid == other.pageid
                    and self.title == other.title
                    and self.url == other.url
            )
        except:
            return False

    def __load(self, redirect=True, preload=False):
        query_params = {
            'prop': 'info|pageprops',
            'inprop': 'url',
            'ppprop': 'disambiguation',
            'redirects': '',
        }
        if not getattr(self, 'pageid', None):
            query_params['titles'] = self.title
        else:
            query_params['pageids'] = self.pageid
        request = _wiki_request(query_params)
        query = request['query']
        pageid = list(query['pages'].keys())[0]
        page = query['pages'][pageid]
        if 'missing' in page:
            if hasattr(self, 'title'):
                raise PageError(self.title)
            else:
                raise PageError(pageid=self.pageid)
        elif 'redirects' in query:
            if redirect:
                redirects = query['redirects'][0]
                if 'normalized' in query:
                    normalized = query['normalized'][0]
                    assert normalized['from'] == self.title, ODD_ERROR_MESSAGE
                    from_title = normalized['to']
                else:
                    from_title = self.title
                assert redirects['from'] == from_title, ODD_ERROR_MESSAGE
                self.__init__(redirects['to'], redirect=redirect, preload=preload)
            else:
                raise RedirectError(getattr(self, 'title', page['title']))
        elif 'pageprops' in page:
            query_params = {
                'prop': 'revisions',
                'rvprop': 'content',
                'rvparse': '',
                'rvlimit': 1
            }
            if hasattr(self, 'pageid'):
                query_params['pageids'] = self.pageid
            else:
                query_params['titles'] = self.title
            request = _wiki_request(query_params)
            html = request['query']['pages'][pageid]['revisions'][0]['*']
            lis = BeautifulSoup(html).find_all('li')
            filtered_lis = [li for li in lis if not 'tocsection' in ''.join(li.get('class', []))]
            may_refer_to = [li.a.get_text() for li in filtered_lis if li.a]
            raise DisambiguationError(getattr(self, 'title', page['title']), may_refer_to)
        else:
            self.pageid = pageid
            self.title = page['title']
            self.url = page['fullurl']

    def __continued_query(self, query_params):
        query_params.update(self.__title_query_param)
        last_continue = {}
        prop = query_params.get('prop', None)
        while True:
            params = query_params.copy()
            params.update(last_continue)
            request = _wiki_request(params)
            if 'query' not in request:
                break
            pages = request['query']['pages']
            if 'generator' in query_params:
                for datum in pages.values():
                    yield datum
            else:
                for datum in pages[self.pageid][prop]:
                    yield datum
            if 'continue' not in request:
                break
            last_continue = request['continue']

    @property
    def __title_query_param(self):
        if getattr(self, 'title', None) is not None:
            return {'titles': self.title}
        else:
            return {'pageids': self.pageid}

    def wikifurhtml(self):
        if not getattr(self, '_html', False):
            query_params = {
                'prop': 'revisions',
                'rvprop': 'content',
                'rvlimit': 1,
                'rvparse': '',
                'titles': self.title
            }
            request = _wiki_request(query_params)
            self._html = request['query']['pages'][self.pageid]['revisions'][0]['*']
        return self._html

    @property
    def wikifurcontent(self):
        if not getattr(self, '_content', False):
            query_params = {
                'prop': 'extracts|revisions',
                'explaintext': '',
                'rvprop': 'ids'
            }
            if not getattr(self, 'title', None) is None:
                query_params['titles'] = self.title
            else:
                query_params['pageids'] = self.pageid
            request = _wiki_request(query_params)
            self._content = request['query']['pages'][self.pageid]['extract']
            self._revision_id = request['query']['pages'][self.pageid]['revisions'][0]['revid']
            self._parent_id = request['query']['pages'][self.pageid]['revisions'][0]['parentid']
        return self._content


def _wiki_request(params):
    params['format'] = 'json'
    if not 'action' in params:
        params['action'] = 'query'
    headers = {
        'User-Agent': 'wikifur'
    }
    r = requests.get(API_URL, params=params, headers=headers)
    return r.json()
