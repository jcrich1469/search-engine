from urllib.request import urlopen
from link_searcher import LinkFinder
from file_manager import *
from domain import *

import os, sys

from traceback import print_exc

class Spider:

    # class level variables, shared among instances
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):

        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('first spider', Spider.base_url)
    
    # static method, do not need to pass self here.
    @staticmethod
    def boot():
        # for the first spider
        # convert the file to a variable, faster
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):

        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' , crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        # after connecting to server, convert form bytes to string.   
        html_string = ''
        # connecting, this is the strategy stuff that I will put in...
        try:
            response = urlopen(page_url)
            # print('response successful')

            # checling it is html
            # if response.getheader('Content-Type') == 'text/html':
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8") # works 99% of the time

            # print(html_string)

            finder = LinkFinder(Spider.base_url, page_url)

            finder.feed(html_string)
        
        except Exception as e:
            
            print('Error: cannot crawl page')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return set()

        return finder.page_links()
    
    ## either this or update files has a bug.
    @staticmethod
    def add_links_to_queue(links):

        for url in links:

            if (url in Spider.queue) or (url in Spider.crawled):
                continue

            if Spider.domain_name != get_domain_name(url):
                continue

            Spider.queue.add(url)

    @staticmethod
    def update_files():

        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)


    

