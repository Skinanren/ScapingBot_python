from flask import Flask
from flask import Flask, render_template, redirect, url_for

from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from urllib.request import Request, urlopen

from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from loguru import logger
import re
import datetime
import random
import os
import json
from scrapingbee import ScrapingBeeClient

import ssl
import re
ssl._create_default_https_context = ssl._create_unverified_context

random.seed(9)

PATH = os.path.join(os.getcwd(), 'data')
os.makedirs(PATH, exist_ok=True)
logger.debug(f"PATH: {PATH}")

# Additional Code 
FILE_NAME = f"{PATH}/cache_data.json"  
PAGE_NAME = f"{PATH}/test.json"
ALL_NUM = f"{PATH}/all_num.json"
CHAT_DATA = f"{PATH}/chat.json"
TEXT_DATA = f"{PATH}/text.json"


class NameForm(FlaskForm):
    name = StringField('Which site is your favorite?', validators=[DataRequired(), Length(10, 40)])
    submit = SubmitField('Submit')



class crawler:
    def getInternalLinks(bs, includeUrl):
        includeUrl = '{}://{}'.format(urlparse(includeUrl).scheme, urlparse(includeUrl).netloc)
        internalLinks = []
        #Finds all links that begin with a "/"
        for link in bs.find_all('a', href=re.compile('^(/|.*'+includeUrl+')')):
            # print("internal link = ",link, link.get_text())
            if link.attrs['href'] is not None:
                if link.attrs['href'] not in internalLinks:
                    if(link.attrs['href'].startswith('/')):
                        internalLinks.append(includeUrl+link.attrs['href'])
                    else:
                        internalLinks.append(link.attrs['href'])
        return internalLinks
                
            #Retrieves a list of all external links found on a page
    def getExternalLinks(bs, excludeUrl):
        externalLinks = []
        #Finds all links that start with "http" that do
        #not contain the current URL
        for link in bs.find_all('a', href=re.compile('^(http|www)((?!'+excludeUrl+').)*$')):
            # print("external link = ",link , link.get_text())
            if link.attrs['href'] is not None:
                if link.attrs['href'] not in externalLinks:
                    externalLinks.append(link.attrs['href'])
        return externalLinks
    
app = Flask(__name__)
app.secret_key = 'tO$&!|0wkamvVia0?n$NqIRVWOG'
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)


@app.route('/',methods=['GET', 'POST'])
def index():
    # names = get_names(ACTORS)
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    names = 'killer'
    empty = []
    with open(TEXT_DATA, "w") as outfile:
        json.dump(empty,outfile,indent=4)
    def getAllExternalLinks(siteUrl):
        req = Request(
            url=siteUrl, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        print("getallexternal number = ",siteUrl)
        try:
            # print("siteurl =",siteUrl)
            # client = ScrapingBeeClient(api_key='4TAO8EV5D7WVT292QPGGEVJY9L4NQC67CJ6WPSW4RDZTEPZIMJOCL0DJH4XP8XCKHXFNWWZRJ6HG6MA1')
            # response = client.get(siteUrl)
            # bs = BeautifulSoup(response.content, "html.parser")

            html = urlopen(req).read()
        except:
            pass
        domain = '{}://{}'.format(urlparse(siteUrl).scheme,
                              urlparse(siteUrl).netloc)
       
        bs = BeautifulSoup(html, 'html.parser')   
       
        internalLinks = crawler.getInternalLinks(bs, domain)
        externalLinks = crawler.getExternalLinks(bs, domain)
    
        for link in externalLinks:
            if link not in allExtLinks:
                allExtLinks.add(link)
                # print(link)
                
        for link in internalLinks:
            if link not in allIntLinks:
                allIntLinks.add(link)               
                if len(allIntLinks) < 4:
                    getAllExternalLinks(link)                            
          
    
    form = NameForm()
    message = ""
    allExtLinks = set()
    allIntLinks = set()
    if form.validate_on_submit():
        name = form.name.data
        print("start")
        allIntLinks.add(name)
        getAllExternalLinks(name)
    
    newdata = []
    alldata = []
    max_num = 0
    for idx, url in enumerate(allIntLinks):
        one_dic = {'key':idx,
                    'url':url
                }
        if idx < 10:
            newdata.append(one_dic)
        if max_num < idx:
            max_num = idx
       
        alldata.append(one_dic)
    
    with open(FILE_NAME, "w") as outfile:
        json.dump(alldata,outfile,indent=4)
    num_obj1 = [{'num':1}]
    with open(PAGE_NAME, "w") as outfile:
        json.dump(num_obj1,outfile,indent=4)
    num_obj2 = [{'all_num':max_num}]
    with open(ALL_NUM,"w") as outfile:
        json.dump(num_obj2,outfile,indent=4)
   
    
    if len(allIntLinks) > 0:
        return render_template('result.html',name=names, form=form, message=newdata,num1 = 0,num2 = 9,all_num = max_num)
    else:
        return render_template('index.html',name=names, form=form, message=allIntLinks)
@app.route('/test',methods=['GET', 'POST'])
def pagenum():
    with open(PAGE_NAME,"r") as json_data:
        file_data = json.load(json_data)
    with open(ALL_NUM,"r") as json_data:
        file_json = json.load(json_data)
    file_data.append(file_json[0])
    
    return file_data

@app.route('/chart',methods=['GET', 'POST'])
def chatdraw():
    form = NameForm()
    message = ""
    with open(FILE_NAME,"r") as json_data:
        file_data = json.load(json_data)
    with open(CHAT_DATA,"r") as ch_json_data:
        chat_data = json.load(ch_json_data)

    for i_data in file_data:
        print("i_data['url] = ",i_data['url'])
        req = Request(
            url=i_data['url'], 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        html = urlopen(req).read()
        bs = BeautifulSoup(html, 'html5lib') 
        # client = ScrapingBeeClient(api_key='4TAO8EV5D7WVT292QPGGEVJY9L4NQC67CJ6WPSW4RDZTEPZIMJOCL0DJH4XP8XCKHXFNWWZRJ6HG6MA1')
        # response = client.get(i_data['url'])
        # bs = BeautifulSoup(response.content, "html.parser")
  
        for link in bs.find_all('a', href=re.compile('^(/|.*'+i_data['url']+')')):
            # print(link.get_text())
            link_text = {'text':link.get_text(),
                         'count':1}
            with open(TEXT_DATA,"r+") as text_data:
                tex_data = json.load(text_data)
                pos = -1
                set_pos = -1
                print("tex_data = ",tex_data)
                for i_text in tex_data:
                    pos += 1
                    print("i_text = ",i_text['text'])
                    print("link_text =",link_text['text'])
                    if link_text['text'] == i_text['text']:
                        set_pos = pos
                        print("set_pos =",set_pos)    
                if set_pos == -1:
                    tex_data.append(link_text)
                    print("tex_data",tex_data)
                else:
                    tex_data[set_pos]['count'] = tex_data[set_pos]['count'] + 1
                print(tex_data[set_pos]['count'])   
            with open(TEXT_DATA,"w") as wri_data:
                json.dump(tex_data,wri_data,indent=4)
                
    with open(TEXT_DATA,"r") as ch_data:
        json_d = json.load(ch_data)
    sum = 0
    newdatapoint = []
    for i_text in json_d:
        sum += i_text['count']
    for i_text  in json_d:
        pro = "{:.2f}".format(i_text['count']/sum)
        pro = float(pro) * 100
        new = {
            "label":i_text['text'],
            "x":i_text['count'],
            "y":pro,
            "legendText":i_text['text']
        }
        newdatapoint.append(new)
   
    
    return json.dumps(newdatapoint)
@app.route('/<num>',methods=['GET', 'POST'])
def detail(num):
    try:
        pages = int(num)
    except:
        pass
    newdata = []
    form = NameForm()
    num_obj = [{'num':num}]
    with open(PAGE_NAME, "w") as outfile:
        json.dump(num_obj,outfile,indent=4)
    with open(FILE_NAME,"r") as json_data:
        file_data = json.load(json_data)
    with open(ALL_NUM,'r') as pri_data:
        al_data = json.load(pri_data)
    maxi_num = al_data[0]['all_num']
    if maxi_num < pages *10 :
        num2_v = maxi_num
    else:
        num2_v = pages*10 - 1
    for idx,url in enumerate(file_data):
        if idx >= (pages-1) * 10 and idx <= pages*10 - 1:
           one_dic = {'key':idx,
                    'url':url['url']
                }
           newdata.append(one_dic)
    return render_template('result.html', name=num, form=form, message=newdata,num1 = (pages - 1)*10,num2 = num2_v,all_num = maxi_num)

if __name__ == "__main__":
    app.run()