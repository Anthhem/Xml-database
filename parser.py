from typing import Type
from urllib.request import urlopen
from lxml import etree as ET
from datetime import datetime
from sqlalchemy import Unicode, null

#Define a class
class FozxRssFeedExtractor:
    def __init__(self):
        pass    
# write a function to parse url of xmlfile
    def parseXML(self,url):
        # open the url using urlopen
        url = urlopen(url)
        #parse the opened url using parse funtion from element tree library
        Doc=ET.parse(url)
        # use the getroot function to get the root of the xml file
        root = Doc.getroot()
        # create a empty list to store the contents of xml file
        Rss_items = []
        # use loops to iterate over items in file.
        for item in root.findall('./channel/item'):
            #create a dictionary to store item name and its text
            news = {}
        #use loops to iterate over all the childs we need.
            for child in item:
                if child.tag == 'id':
                    # if child is found then add its tag and text to the dictionary
                    news[child.tag] = child.text                 
                elif child.tag == 'Pcategory':
                    if child.text == null:
                        child.tag = "No data"
                    else:
                        news[child.tag] = child.text
                elif child.tag == 'title':
                    if child.text == null:
                        child.tag = "No title"
                    else:
                        news[child.tag] = child.text
                elif child.tag == 'author':
                    if child.text == null:
                        child.tag = "No author"
                    else:
                        news[child.tag] = child.text
                elif child.tag == 'source':
                    if child.text == null:
                        child.tag = "No source"
                    else:
                        news[child.tag] = child.text
                elif child.tag == 'pubDate':
                    parse_date= datetime.strptime(child.text,'%A, %B %d, %Y %I:%M %p %z')  #Sunday, July 31, 2022 11:33 PM +0530
                    news[child.tag] = parse_date
                elif child.tag == 'description':
                    if child.text == null:
                        child.tag = "No description"
                    else:
                        news[child.tag] = child.text
                elif child.tag == 'tags':
                    if child.text == null:
                        child.tag = "No tags"
                    else:
                        tag_list = child.text
                        tag_list = tag_list.split(',')
                        news[child.tag] = tag_list
                elif child.tag == 'image':
                    if child.text == null:
                        child.tag = "No image"
                    else:
                        news[child.tag] = child.text
                elif child.tag == 'imagecaption':
                    if child.text == null:
                        child.tag = "No caption"
                    else:
                        news[child.tag] = child.text
                elif child.tag == 'link':
                    if child.text == null:
                        child.tag = "No link"
                    else:
                        news[child.tag] = child.text
                    # After finding all the tag's append them to the created list
                    Rss_items.append(news)
                    #print the list
        print(Rss_items[0])

if __name__== '__main__':
    FozxRssFeedExtractor().parseXML('https://www.newindianexpress.com/World/rssfeed/?id=171&getXmlFeed=true')
