"""Automates the build process for my personal website"""
"""
Apply a few HTML patches
Test by launching page in browser
Fix anything that breaks
Commit and push
"""
import os
from bs4 import BeautifulSoup
from os.path import basename, splitext
import shutil


cwd = os.getcwd()
ls = os.listdir(cwd)

#print(cwd)
#print(ls)

#Rename my home page to 'index.html'

if 'Will_Gertsch.html' in ls:
        os.rename('Will_Gertsch.html', 'index.html')
        print('Will_Gertsch.html renamed to index.html')


#create image folder if it doesn't exist
if "img" not in ls:
        os.makedirs("img")
        print("img directory created")
        
img_path = cwd+os.sep+'img'

walk = os.walk(cwd)

# process all the image links in the html files
for root, dirs, files in walk:
        
        for file in files:
                
                # checks if the file is an html file
                if ".html" in file:
                        file_path = root+os.sep+file

                        """print(file_path)"""
                        
                        # process html file
                        
                        curr_file = open(file_path, 'r')
                        
                        contents = curr_file.read()
                        

                        soup = BeautifulSoup(contents, "html.parser")
                                                
                                                
                        for img in soup.findAll('img'):

                                #copy the files to the img directory
                                print("Found", img['src'], "copying to", img_path)

                                # get rid of the windows  file thingy
                                if 'file:///' in img['src']:
                                        shutil.copy2(img['src'][8:], img_path)
                                        
                                # this handles the LaTeX images since, for some reason, are only given a local path
                                elif img['src'][:2] == "./":
                                        shutil.copy2(root + img['src'][1:], img_path)
                                else:
                                        shutil.copy2(img['src'], img_path)
                                
                                #change all references to web-host
                                print("Changing", img['src'], end=" ")
                                img['src'] = 'https://ljufin.github.io/img/'+ splitext(basename(img['src']))[0]+splitext(basename(img['src']))[1]
                                print("to", img['src'])

                        # now apply the changes to the file
                        contents = str(soup)
                        #print(contents)
                        curr_file.close()

                        curr_file = open(file_path, 'w+') # 'w+' opens for reading and writing, overwrites the file
                        curr_file.write(contents)
                        curr_file.close()

print("Build completed")
