#-*- coding:utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import json
import requests
import re
from lxml import etree

class WechatInterface:
    
    #构建模板路径
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root,'templates')
        self.render = web.template.render(self.templates_root)
        
    def GET(self):
    #获取token的验证请求
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token = "fuckyou8236618" 
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
    #hash加密token并返回数据
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            return echostr
        
    def POST(self):
        str_xml = web.data()
        xml = etree.fromstring(str_xml)
        mstype = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        
        if mstype == "event":
            mscontent = xml.find("Event").text
            if mscontent == "subscribe":
                replyText = '你竟然可以找到我！厉害了我的哥！可以直接和我聊天哦，绝对秒回！！'
                return self.render.reply_text(fromUser,toUser,int(time.time()),replyText)
            
        elif mstype == "text":
            mscontent = xml.find("Content").text
            if mscontent == u'电影':
                replyText = '该功能正在测试'
                return self.render.reply_text(fromUser,toUser,int(time.time()),replyText)
            
            elif mscontent == u'电影资源':
                resourceUrl = 'http://mp.weixin.qq.com/mp/homepage?__biz=MzA4MTE4Mzc5OA==&hid=3&sn=117a0a6e9302923543b3d6c839f75af6#wechat_redirect'
                title = u'最新电影资源'
                description = u'资源来自Mithril影视资讯'
                a = re.compile('<div class="img js_img" style="background-image: url(.*?);"></div>')
                r = requests.get(resourceUrl).text
                pic_str = re.search(a, r).group(1)
                picUrl = pic_str[2:-2]
                return self.render.reply_resource(fromUser,toUser,int(time.time()),title,description,picUrl,resourceUrl)
            elif mscontent == u'电视剧资源':
                resourceUrl = 'http://mp.weixin.qq.com/mp/homepage?__biz=MzA4MTE4Mzc5OA==&hid=1&sn=037008398dfb43c7ba0fe25d84e826d4#wechat_redirect'
                title = u'最新电视剧资源'
                description = u'资源来自Mithril影视资讯'
                a = re.compile('<div class="img js_img" style="background-image: url(.*?);"></div>')
                r = requests.get(resourceUrl).text
                pic_str = re.search(a, r).group(1)
                picUrl = pic_str[2:-2]
                return self.render.reply_resource(fromUser,toUser,int(time.time()),title,description,picUrl,resourceUrl)
            
            else:
                api = 'http://www.tuling123.com/openapi/api'
                info = mscontent.encode('utf-8')
                user_data = {
                              "key": 'c2c18958ade7460ba11553baddfe8e2c',
                              "info": '123',
                              "userid": '123'
                             }
                user_data["info"] = info
                user_data["userid"] = fromUser
                r = requests.post(api,user_data).text
                reply_json = json.loads(r)
                if reply_json.has_key('url'):
                    replyText = reply_json["text"] + reply_json["url"]
                    return self.render.reply_text(fromUser,toUser,int(time.time()),replyText)
                else:
                    replyText = reply_json["text"]
                    return self.render.reply_text(fromUser,toUser,int(time.time()),replyText)
                
                