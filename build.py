"""Automates the build process for my personal website.
Changes the name of my home file to index.html,
creates a image directory to upload images to,
rewrites all the references to images in the html source to the new location on my site"""

import os
from bs4 import BeautifulSoup
from os.path import basename, splitext
import shutil


# get the the path of the current directory and its contents
cwd = os.getcwd()
ls = os.listdir(cwd)


#Rename my home page to 'index.html'
if 'Will_Gertsch.html' in ls:
        os.rename('Will_Gertsch.html', 'index.html')
        print('Will_Gertsch.html renamed to index.html')


# create image folder if it doesn't exist
if "img" not in ls:
        os.makedirs("img")
        print("img directory created")
        

# save the path of the image directory		
img_path = cwd+os.sep+'img'


# process all the image links in the html files
for root, dirs, files in os.walk(cwd):
        
        for file in files:
                
                # checks if the file is an html file
                if ".html" in file:
                        file_path = root+os.sep+file
                        
                        # process html file
                        curr_file = open(file_path, 'r')
                        
                        contents = curr_file.read()
                        

                        soup = BeautifulSoup(contents, "html.parser")
                                                
                                                
                        for img in soup.findAll('img'):

                                #copy the files to the img directory
                                print("Found", img['src'], "copying to", img_path)

                                # get rid of the extra Windows file path
                                if 'file:///' in img['src']:
                                        shutil.copy2(img['src'][8:], img_path)
                                        
                                # this handles the LaTeX images since, for some reason, they are only given a local path
                                elif img['src'][:2] == "./":
                                        shutil.copy2(root + img['src'][1:], img_path)
                                else:
                                        shutil.copy2(img['src'], img_path)
                                
                                # change all references to web-host
                                print("Changing", img['src'], end=" ")
                                img['src'] = 'https://ljufin.github.io/img/'+ splitext(basename(img['src']))[0]+splitext(basename(img['src']))[1]
                                print("to", img['src'])

                        # now apply the changes to the file
                        contents = str(soup)
                        curr_file.close()

                        curr_file = open(file_path, 'w+') # 'w+' opens for reading and writing, overwrites the file
                        curr_file.write(contents)
                        curr_file.close()

print("Build completed")
