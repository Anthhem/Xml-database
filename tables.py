from email.mime import image
from email.utils import parsedate
from itertools import count
from posixpath import split
from select import select
import sys
from msilib.schema import Class
from time import timezone
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from flask_migrate import Migrate
from sqlalchemy import DateTime
import datetime
from sqlalchemy.orm import session
import test
import mysql.connector
import pytz

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:vinay@localhost:3306/rssdata'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Image(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    image = db.Column(db.LargeBinary)
    image_caption = db.Column(db.String(220))

    def __init__(self,image,image_caption):
        self.image = str.encode(image)
        self.image_caption = image_caption


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    P_category = db.Column(db.String(50)) 
    title = db.Column(db.String(220))
    author = db.Column(db.String(45))
    source = db.Column(db.String(45))
    pubdate = db.Column(db.DateTime(timezone=True),nullable = False)
    description = db.Column(db.String(220))
    link = db.Column(db.String(200))
    image_id = db.Column(db.Integer,db.ForeignKey('image.id'), nullable = False) # to be autoincremented
    id_tables = db.relationship('Id_table',  backref=db.backref('item', lazy=False))
    

    def __init__(self,id,p_category,title,author,source,pubdate,description,link,image_id):
        self.id = id
        self.P_category = p_category

        self.title = title
        self.author = author
        self.source = source
        self.pubdate = pubdate
        self.description = description
        self.link = link
        self.image_id = image_id
        
       
class Id_table(db.Model):
    items_id = db.Column(db.Integer, db.ForeignKey('item.id'),primary_key = True,nullable = False)
    tags_id= db.Column(db.Integer,db.ForeignKey('tag.id'),primary_key = True,nullable = False )
    def __init__(self,items_id,tags_id):
        self.items_id = items_id
        self.tags_id = tags_id


class Tag(db.Model):
    id = db.Column(db.Integer,index = True, primary_key = True )
    tag = db.Column(db.String(220))
    id_tables = db.relationship ('Id_table',backref=db.backref('tag', lazy=False))

    def __init__(self,tag):
        self.tag = tag


call_dataloader = test.Dataloader()
database_connector = call_dataloader.establish_db_connection()
connector = database_connector[1]
cursor = database_connector[0]

object_of_class = test.RssFeedExtractor()
parsed_data = object_of_class.parsexml('https://www.newindianexpress.com/World/rssfeed/?id=171&getXmlFeed=true')
#print(parsed_data)

#function to add and commit
def add_and_commit(list):
    to_add = db.session.add(list)
    to_commit = db.session.commit()
    return(to_add,to_commit)

#Load data into image table
for i in parsed_data:
    image_list= []
    for key,val in i.items():
        if key=='image' or key=='imagecaption':
            image_list.append(val)
    image_table = Image(f'{image_list[0]}',f'{image_list[1]}')
    add_and_commit(image_table)

#Convert timezone to UTC
new_pubdate=[]
for i in parsed_data:
    for key,val in i.items():
        if key == 'pubDate':
            newtz= val.replace(tzinfo=pytz.UTC)
            new_pubdate.append(newtz)

#Fetch image id
imageeee= Image.query.all()
image_id_list=[]
for i in imageeee:
    image_id_list.append(i.id)
#print(image_id_list)

#Load data into item table
db_item_id= Item.query.all()
save_item_id=[]
for i in db_item_id:
    save_item_id.append(i.id)

r=0
for i in parsed_data:
    item_list = []
    for key,val in i.items():
        if key=='id' or key=='Pcategory' or key=='title' or key=='author' or key=='source' or key=='pubDate' or key=='description' or key=='link':
            item_list.append(val)
    item_table = Item(f'{item_list[0]}',f'{item_list[1]}',f'{item_list[2]}',f'{item_list[3]}',f'{item_list[4]}',f'{new_pubdate[r]}',f'{item_list[6]}',f'{item_list[7]}',f'{image_id_list[r]}')
    r+=1
    add_and_commit(item_table)

#load data into tag table

tag_name_list= []
for i in parsed_data:
    for key,val in i.items():
        if key == "tags":
            for i in val:
               tag_name_list.append(i)
#tag_list= set(tag_name_list)
#print(tag_name_list)
new_tag_list=set(tag_name_list)
tag_list=list(new_tag_list)
#print(new_tag_list)
m=0
for l in tag_list:
    tag_table = Tag(f'{tag_list[m]}')
    m+=1  
    add_and_commit(tag_table)

'''#fetch item id
item_table = Item.query.all()
id_item = []
for i in item_table:
    id_item.append(i.id)

#fetch tag id
tag_table = Tag.query.all()
id_tag = []
for i in tag_table:
    id_tag.append(i.id)

#Dataloader for id_table by appending from lists of item_id and tag_id.
n=0
for i in parsed_data:
    id_table = Id_table(f'{id_item[n]}',f'{id_tag[n]}')
    n+=1
    #add_and_commit(id_table)'''







