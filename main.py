import threading
from queue import Queue

from spider import Spider
from domain import *
from file_manager import *

PROJECT_NAME = 'university of Cincinnatti'
HOMEPAGE = 'http://www.lindenwood.edu/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 1
queue = Queue()

Spider(PROJECT_NAME,HOMEPAGE, DOMAIN_NAME)

# Do the next job in the queue

def work():

    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

# create worker threads, will terminate after main.

def create_workers():
    for _ in range(NUMBER_OF_THREADS):

        t = threading.Thread(target=work)
        # daemons die whenever they end the process
        t.daemon = True
        t.start()



# each queued link is a new job

def create_jobs():

    for link in file_to_set(QUEUE_FILE):

        queue.put(link)

    queue.join()
    crawl()

# Check if there are items in the q, if so crawl
def crawl():

    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:

        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()



create_workers()
crawl()
