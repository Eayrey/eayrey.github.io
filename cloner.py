import os
import sys
import re
import shutil
import requests

def get_links():
    links = []
    for root, subdirs, files in os.walk(os.getcwd()):
        for oneFile in files:
            if oneFile == "cloner.py" or ".git/" in root:
                continue
            with open(os.path.join(root, oneFile)) as openFile:
                print oneFile
                for quote in re.findall('"([^"]*)"', openFile.read()):
                    if "static1.squarespace.com" in quote:
                        print "creating {}".format(root)
                        quote = quote.split("?")[0]
                        links.append((os.path.join(root,oneFile), quote.split("?")[0]))
    return links


def clone_links(links):
    for link in links:
        print link[1]
        realLink = link[1].split("//")[1]
        if realLink.endswith("/"):
            realLink = realLink[:-1]
        fileName = realLink.split("/")[-1]
        directory = "/".join(realLink.split("/")[:-1])
        try:
            os.makedirs(directory)
        except OSError:
            pass
        url = link[1]
        if url.startswith("//"):
            url = url.replace("//", "https://")
        if not os.path.isfile(realLink):
            r = requests.get(url, stream=True)
            print "fetching {}".format(url)
            with open(realLink, "wb") as writeToThis:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, writeToThis)
                print "writing to {}".format(realLink)

def correct_links(links):
    for link in links:
        with open(link[0], "r") as fileToFix:
            original = fileToFix.read()
            fixedLink = link[1].split("//")[1]
            fixedLink = "/" + fixedLink
            if fixedLink.endswith("/"):
                fixedLink = fixedLink[:-1]
            fixed = original.replace(link[1], fixedLink)
        with open(link[0], "w") as fileToFix:
            print "fixing {}".format(link[0])
            fileToFix.write(fixed)

def main():
    links = get_links()
    clone_links(links)
    correct_links(links)

main()
