# Author: Peter Vaucher
# Use: Scrape class notes for CSCI 163B and store them in a directory
#      Change path to desired download location
# Requires: Beautiful Soup 4
#           In terminal: pip3 install beautifulsoup4

import requests, bs4 as bs, os

def preorder(url, path, level):
    level += 1;
    response = requests.get(url)
    response.raise_for_status()
    soup = bs.BeautifulSoup(response.text, "lxml")
    # get all <a> tags inside a <td>
    selection = soup.select('td a')
    for i in range(1, len(selection)):
        link = selection[i]
        if link.has_attr('href'):
            # display file tree 
            for i in range(level):
                print('    ', end='')
            print(link.attrs['href'])
            #print(path)
            #print(url)

            child = link.attrs['href']
            next_url = url + link.attrs['href']
        
            if (child[-1] == '/'):
                next_path = path + child
                if not os.path.exists(next_path):
                    os.mkdir(next_path)
            else:
                next_path = path #save for recursive call
                # download file
                try:
                    file = requests.get(next_url, stream=True)                                      
                    fileName = path + child
                    #if not os.path.exists(fileName):
                    new_file = open(fileName, 'wb')
                    for chunk in file.iter_content(512*1024):
                        new_file.write(chunk)
                    new_file.close()
                except:
                     print("Failed to download", child)

                
            preorder(next_url, next_path, level)

url = "https://terminus.scu.edu/~ntran/csci163b-s18/notes/"
path = '/Users/petervaucher/Documents/SCU/spring/CSCI 163B/class_notes/'
level = 0;
if not os.path.exists(path):
    os.makedirs(path)
print('class_notes/')
preorder(url, path, level)
