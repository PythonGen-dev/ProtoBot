from discord.ext import commands


import sys


ODD_ERROR_MESSAGE = "This shouldn't happen. Please report on GitHub: github.com/goldsmith/Wikipedia"


class NoPremiumException(commands.CheckFailure):
    #no premium exception
    pass

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
