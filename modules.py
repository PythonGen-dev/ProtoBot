# немного модифицированный https://github.com/goldsmith/wikipedia и база даных на json
from __future__ import unicode_literals, print_function

import json
import os
import requests
import sys
from bs4 import BeautifulSoup


class storage(object):
    def __init__(self, location):
        self.location = os.path.expanduser(location)
        self.load(self.location)

    def load(self, location):
        if os.path.exists(location):
            self._load()
        else:
            self.db = {}
        return True

    def _load(self):
        self.db = json.load(open(self.location, "r"))

    def dumpdb(self):
        try:
            json.dump(self.db, open(self.location, "w+"))
            return True
        except:
            return False

    def set(self, key, value):
        try:
            self.db[str(key)] = value
            self.dumpdb()
        except:
            return False

    def get(self, key):
        try:
            return self.db[key]
        except KeyError:
            return '0'



API_URL = 'http://en.wikifur.com/w/api.php'
ODD_ERROR_MESSAGE = "This shouldn't happen. Please report on GitHub"


class wikifurException(Exception):
    def __init__(self, error):
        self.error = error

    def __unicode__(self):
        return "An unknown error occured: \"{0}\". Please report it on GitHub!".format(self.error)

    if sys.version_info > (3, 0):
        def __str__(self):
            return self.__unicode__()
    else:
        def __str__(self):
            return self.__unicode__().encode('utf8')


class PageError(wikifurException):
    def __init__(self, pageid=None, *args):
        if pageid:
            self.pageid = pageid
        else:
            self.title = args[0]

    def __unicode__(self):
        if hasattr(self, 'title'):
            return u"\"{0}\" does not match any pages. Try another query!".format(self.title)
        else:
            return u"Page id \"{0}\" does not match any pages. Try another id!".format(self.pageid)


class DisambiguationError(wikifurException):
    def __init__(self, title, may_refer_to):
        self.title = title
        self.options = may_refer_to

    def __unicode__(self):
        return u"\"{0}\" may refer to: \n{1}".format(self.title, '\n'.join(self.options))


class RedirectError(wikifurException):
    def __init__(self, title):
        self.title = title

    def __unicode__(self):
        return u"\"{0}\" resulted in a redirect. Set the redirect property to True to allow automatic redirects.".format(
            self.title)


class HTTPTimeoutError(wikifurException):
    def __init__(self, query):
        self.query = query

    def __unicode__(self):
        return u"Searching for \"{0}\" resulted in a timeout. Try again in a few seconds, and make sure you have rate limiting set to True.".format(
            self.query)


import functools


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
