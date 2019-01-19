import os

# Every website crawled is a new folder created

def create_project_dir(directory):

    if not os.path.exists(directory):
        print('Making a new directory for the project named' + directory)
        os.makedirs(directory)

def create_data_files(project_name, base_url):

    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'

    if not os.path.isfile(queue):
        # base_url starts from the selected page.
        write_file(queue,base_url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')

# create a new file

def write_file(path, data):

    f = open(path, 'w')
    f.write(data)
    f.close()

def append_to_file(path, data):

    with open(path, 'a') as file:
        file.write(data + '\n')

# Delete the contents of a file

def delete_file_contents(path):

    with open(path, 'w'):
        pass

## File/set functions
# read a file adn convert each line to a set.

def file_to_set(file_name):

    results = set()

    with open(file_name, 'rt') as f:

        for line in f:

            results.add(line.replace('\n', ''))

    return results

# Iterate through a set, each item will be a new line in the file

def set_to_file(links, file):

    delete_file_contents(file)
    for link in sorted(links):

        append_to_file(file, link)



##TODO sort out the directory structure...

# create_project_dir('universities')

# # The data files, that need to be made, 'crawled' and 'queued'
# create_data_files('universities', 'https://www.uc.edu/')