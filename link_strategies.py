from urllib.request import urlopen, Request
import requests # seperate requests library

import abc

##STRATEGY PATTERN IN PYTHON

#The client, just a context class for now....
class Context:
    """
    Define the interface of interest to clients.
    Maintain a reference to a Strategy object.
    """

    def __init__(self, strategy):

        # the current strategy object. single underscore signals 'private' am.
        self._strategy = strategy

    def context_interface(self):


        # running this method here....
        self._strategy.fix_algorithm('https://sullivan.edu/')

class Linkable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def link_opening_algorithm(self, link):
        pass


#A CONCRETE fix strategy for dealing with links that do not work on the first pass with 403.
#Create new ones as appropriate.

class Concrete_link_strategy_skip_link(Linkable):

    def link_opening_algorithm(self, url):
        print('using Skip strategy as this will not work, not passing url or html...')
        return 'skip'



class Concrete_link_strategy_normal(Linkable):

    def link_opening_algorithm(self, url):
        print('using NORMAL strategy')
        return urlopen(url)



##
# For HTTPerrors
##
class Concrete_link_strategy_403(Linkable):

    def link_opening_algorithm(self,url):
        # forbidden, I am a bot.
        # request link, not as a spider.... but as a 'legitimate' browser.
        print('using HTTP ERROR 403 strategy')
        con = None

        try:

            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            con = urlopen(req)

            # print(con.read())

        except Exception as e:

            print(e)

        # return (req, ('403', isResolved))
        return con
##
# For URLerrors
##
#Fix URL 111 errors which is connection refused....

class Concrete_link_strategy_url_111(Linkable):

    def link_opening_algorithm(self,url):
        # forbidden, I am a bot.
        # request link, not as a spider.... but as a 'legitimate' browser.
        print('using URL ERROR 111 strategy')
        con = None
        try:

            print(url)
            url = url.replace("https", "http")
            print('replaced: '+ url)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            con = urlopen(req)

            # print(con.read())

        except Exception as e:

            print(e)

        return con

#Fix Certificate Errors
class Concrete_link_strategy_CE(Linkable):

    def link_opening_algorithm(self,url):
        # forbidden, I am a bot.
        # request link, not as a spider.... but as a 'legitimate' browser.

        print('using CERTIFICATE ERROR strategy')#

        try:
            #strategy is to bypass te certificate verification fo this site.
            print('CE strategy')
            response = requests.get(url, verify=False)
            # print(response.content)

        except Exception as e:

            print(e)
            # to be resolved if exception thrown.

        return response

class Concrete_link_strategy_url_ssl_ce(Linkable):

    def link_opening_algorithm(self, url):
        # forbidden, I am a bot.
        # request link, not as a spider.... but as a 'legitimate' browser.

        print('using URL SSL C ERROR  strategy')
        try:
            # strategy is to bypass te certificate verification fo this site.

            response = requests.get(url, verify=False)
            print(response.content)

        except Exception as e:

            print(e)

        return response





def main():

    #set the link
    cls403 = Concrete_link_strategy_403()
    cls403.link_opening_algorithm('https://floridapoly.edu/')

    cls111 = Concrete_link_strategy_url_111()
    cls111.link_opening_algorithm('https://floridapoly.edu/')

    clsCE = Concrete_link_strategy_CE()
    clsCE.link_opening_algorithm('https://floridapoly.edu/')

    cfs_url_ssl = Concrete_link_strategy_CE()
    cfs_url_ssl.link_opening_algorithm('http://www.chesapeake.edu/')

    cfs_ssl = Concrete_link_strategy_url_ssl_ce()
    cfs_ssl.link_opening_algorithm('https://floridapoly.edu/')

    clsn = Concrete_link_strategy_normal()
    clsn.link_opening_algorithm('https://floridapoly.edu/')

    #print(client.fix('https://sullivan.edu/'))

# a test
if __name__ == "__main__":
    main()
    # Must instantiate first....
    #headers={'User-Agent': "Magic Browser"}
    #{'User-Agent': 'Mozilla/5.0'}
