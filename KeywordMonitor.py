# -*- coding: utf-8 -*-
import urllib2
import sys
import os
import re
import urllib
import socket
import time
import random
import datetime
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 10
socket.setdefaulttimeout(timeout)
sleep_download_time = 3
today = datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)

def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

class SqlControl:
    def connects(self, host="localhost", user="root", passwd="123456", db="keywordmonitor", charset="utf8"):
        self.conn=MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset=charset)  
        self.cursor = self.conn.cursor() 

    def execsql(self, sql, param):
        try:
            self.cursor.execute(sql,param)
        except Exception, e:
            print e
            pass

    def selectsql(self, sql, param):
        data = []
        try:
            self.cursor.execute(sql,param)
            data = self.cursor.fetchall()
            return data
        except Exception, e:
            print e
            pass
    
    def commitsql(self):
        self.conn.commit()

    def getrowcount(self):
        return self.cursor.rowcount

    def closeconn(self):
        self.cursor.close()
        self.conn.close()



class PageVisit:
    def __init__(self):
        fn = open(cur_file_dir()+"\\proxys.txt")
        self.proxys = [x.strip() for x in fn.readlines() if x.strip()]
        fn.close()

    def visit(self, url, useproxy=False):
        #proxy = {'http':'111.161.126.84:80'}
        if not useproxy:
            proxys = ['111.161.126.88:8080', '111.161.126.91:8080', '111.161.126.92:8080']
        else:
            proxys = self.proxys
        proxy = {'http':proxys[random.randint(0, len(proxys)-1)]}
        i_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
        html = ''
        try:
            proxy_support = urllib2.ProxyHandler(proxy)
            opener = urllib2.build_opener(proxy_support)
            urllib2.install_opener(opener)
            req = urllib2.Request(url,headers=i_headers)
            response = urllib2.urlopen(req)
            html = response.read()
            response.close()
            print proxy,url
        except Exception, e:
            print e
            pass
        return html


class DataGet:
    def getdata(self, html, regex):
        result = regex.findall(html)
        return result

class SearchGet:
    def __init__(self, pv, dg):
        self.pv = pv
        self.dg = dg
        #baidupc
        self.regex_bd = '<div\s*?class="result c-container\s*?"\s*?id="(\d+)"\s*?srcid[\s\S]*?href\s*?=\s*?"(.*?)"[\s\S]*?<span\s*?class="g">(.*?)\/.*?&nbsp;(\d{4}-\d{2}-\d{2})[\s\S]*?</span>'
        self.searchurl_bd = 'http://www.baidu.com/s?wd='
        #360
        self.regex_360 = '<h3\s*?class="res-title\s*?">\s*?<a\s*?href="(.*?)"[\s\S]*?data-pos="(.*?)"[\s\S]*?<cite>.*?(\d{4}-\d{2}-\d{2})<\/cite>'
        self.searchurl_360 = 'http://www.so.com/s?q='
        #baiduwap
        self.regex_bdwap = '<div\s*?class="resitem"\s*?><a\s*?href="(.*?)">(.*?)&#160;[\s\S]*?<span\s*?class="site">(.*?)</span>&#160;<span\s*?class="date">(\d{4}-\d{1,2}-\d{1,2})</span>'
        self.searchurl_bdwap = 'http://wap.baidu.com/s?word='
        #sql语句
        self.sql1 = "insert into result(se, keyword, domain, url, rank, snap, hospital, uptime) values(%s, %s, %s, %s, %s, %s, %s, %s)"
        self.sql2 = "update keyword set uptime = %s where keyword = %s and hospital = %s"

    def getresult(self, setype=0, keyword='by thx'):
        regexstatement = ''
        searchurl = ''
        html = ''
        #搜索引擎类型 1-360 2-百度WAP 其他-百度PC
        if setype == 1:
            regexstatement = self.regex_360
            searchurl = self.searchurl_360
        elif setype == 2:
            regexstatement = self.regex_bdwap
            searchurl = self.searchurl_bdwap
        else:
            regexstatement = self.regex_bd
            searchurl = self.searchurl_bd
        #获取数据
        regex = re.compile(regexstatement)
        html = self.pv.visit("%s%s" % (searchurl, keyword), useproxy=True)
        #time.sleep(sleep_download_time)
        seresult = self.dg.getdata(html, regex)
        return seresult

    def parseresult(self, setype=0, keyword='by thx', hospital='huaxia', seresult=''):
        sqldata = []
        for keydata in seresult:
            if setype == 1:
                se = '360'
                domain = keydata[0].split('/')[2]
                url = keydata[0]
                rank = keydata[1]
                snap = keydata[2]
            elif setype == 2:
                se = '百度WAP'
                domain = keydata[2]
                url = "http://wap.baidu.com"+keydata[0].replace("&amp;","&")
                rank = keydata[1]
                snap = keydata[3]
            else:
                se = '百度'
                domain = keydata[2]
                url = keydata[1]
                rank = keydata[0]
                snap = keydata[3]
            sqldata.append([se.decode('gbk'), keyword, domain, url, rank, snap, hospital])
        return sqldata

    def upresult(self, setype=0, keyword='by thx', hospital='huaxia', sc=''):
        seresult = []
        #获取搜索结果
        while len(seresult) < 1:
            seresult = self.getresult(setype, keyword)
        #转换为所需要的数据
        sqldata = self.parseresult(setype, keyword, hospital, seresult)
        for keydata in sqldata:
            #print keydata
            se = keydata[0]
            keyword = keydata[1]
            domain = keydata[2]
            url = keydata[3]
            rank = keydata[4]
            snap = keydata[5]
            hospital = keydata[6]
            param1 = (se, keyword, domain, url, rank, snap, hospital, str(today))
            param2 = (str(today), keyword, hospital)
            #更新数据库
            sc.execsql(self.sql1, param1)
            sc.execsql(self.sql2, param2)


class ClassMove:
    def __init__(self, pv):
        self.pv = pv
        self.sql1 = 'select id,url from result where uptime = %s and classtime <> %s'
        self.param1 = (str(today), str(today))
        self.sql2 = 'update result set classes = %s where id = %s'
        self.sql3 = 'update result set classtime = %s'
        self.param3 = (str(today))
        self.huaxia = ['邢台华夏', '华夏医院', 'xthxyy.com', '3567777.com', '1811388650', '0319-3099000', '03193099000', '转运街99号', '1920633299', 'PAT39611796', 'LUT95559508']
        self.xiandai = ['邢台现代', '现代医院', '200809351', '0319-3166888', '03193166888', '新华南路128号', 'LRW62920295', 'xt-120.com', 'xtxdnk.com', '3166888.com', 'xtnk120.com', 'xtxdfk.com', 'xtxdyy.cn']
        self.kangnan = ['邢台康男', '康男中医院', 'PAT84081309', '1871291803', '0319-3224888', '03193224888', '邢州北路693号', 'xtsnkyy.net']
        self.xiehe = ['邢台协和', '协和医院', 'BFT64380744', 'xtxh120.com', '519993120', '0319-3696666', '03193696666', '中兴东大街73号', 'xingtaixiehe.com', 'xtxh120.net', '2850956899']
        self.zhongshan = ['邢台中山', '中山医院', 'BFT41889732', 'xtzs120.net', 'xtzs120.com', '0319-3860666', '03193860666', '515515120', '400-6756-120', '4006756120', '开元北路178号']
        self.fuke = ['NET42234672', 'xtfkyy.com', '团结东大街195号', '2336984930', '763220441', '0319-3687009', '03193687009']
        self.fuchan = ['PLT25988635', 'xtfcyy.com', '0319-2136999', '03192136999', '800020708', '公园东街交叉口', '03192136999.com']
        self.hptags = [self.huaxia, self.xiandai, self.kangnan, self.xiehe, self.zhongshan, self.fuke, self.fuchan]
        self.getnum = 2

    def getdata(self, sc):
        return [x for x in [y for y in sc.selectsql(self.sql1, self.param1)]]

    def moveclass(self, sc):
        urldatas = self.getdata(sc)
        for urldata in urldatas:
            urlid = urldata[0]
            url = urldata[1]
            html = self.pv.visit(url)
            tagnum = []
            hpname = ['huaxia', 'xiandai', 'kangnan', 'xiehe', 'zhongshan', 'fuke', 'fuchan']
            for i in range(len(self.hptags)):
                sum = 0
                for tagname in self.hptags[i]:
                    num = html.count(tagname)
                    sum = sum + num
                tagnum.append([hpname[i], sum])
            print tagnum
            tagnum.sort(lambda x,y:cmp(x[1],y[1]),reverse=True)
            tmpnum = tagnum[0][1]
            hp = tagnum[0][0]
            #print hp, tmpnum
            #print sum
            if tmpnum >= self.getnum:
                param2 = (hp, urlid)
                sc.execsql(self.sql2, param2)
        sc.execsql(self.sql3, self.param3)

class PlatformGet:
    def __init__(self):
        self.sql1 = 'select domain from result where uptime = %s'
        self.param1 = (str(today))
        self.sql2 = 'select * from platform where domain = %s'
        self.sql3 = 'insert into platform(domain) values(%s)'

    def getplatform(self, sc):
        platdatas = [x[0] for x in [y for y in sc.selectsql(self.sql1, self.param1)]]
        for domain in platdatas:
            #判断平台是否存在，不存在则入库
            param2 = (domain)
            platformdata = sc.selectsql(self.sql2, param2)
            if sc.getrowcount() < 1:
                param3 = (domain)
                sc.execsql(self.sql3, param3)

class DataParse:
    def __init__(self):
        self.sql1 = "select keyword,hospital from keyword where uptime = %s"
        self.param1 = (str(today))
        self.sql2 = 'select id from result where se = %s and keyword = %s and classes = %s'
        self.hpname = ['huaxia', 'xiandai', 'kangnan', 'xiehe', 'zhongshan', 'fuke', 'fuchan']
        self.sename = ['百度', '360', '百度WAP']
        self.sql3 = 'insert into searchresult(setype, hospital, keyword, ranknum) values(%s, %s, %s, %s)'

    def parsedata(self, sc):
        keydatas = [x for x in [y for y in sc.selectsql(self.sql1, self.param1)]]
        #print keydatas
        for keydata in keydatas:
            keyword = keydata[0]
            hospital = keydata[1]
            for se in self.sename:
                for hospital in self.hpname:
                    param2 = (se.decode('gbk'), keyword, hospital)
                    tmp = sc.selectsql(self.sql2, param2)
                    #print se, hospital, keyword, sc.getrowcount()
                    param3 = (se.decode('gbk'), hospital, keyword, sc.getrowcount())
                    sc.execsql(self.sql3, param3)

class HtmlCreate:
    def createhtml(self):
        pass


def main():
    sc = SqlControl()
    pv = PageVisit()
    dg = DataGet()
    sg = SearchGet(pv, dg)
    cm = ClassMove(pv)
    pg = PlatformGet()
    dp = DataParse()
    #连接数据库
    sc.connects(host="localhost", user="root", passwd="123456", db="keywordmonitor", charset="utf8")
    #获取当天未更新关键词
    sql = "select keyword,hospital from keyword where uptime <> %s"
    param = (str(today))
    keydatas = [x for x in [y for y in sc.selectsql(sql, param)]]
    for keydata in keydatas:
        keyword = keydata[0]
        hospital = keydata[1]
        #采集百度结果入库
        sg.upresult(0, keyword, hospital, sc)
        #采集360结果入库
        sg.upresult(1, keyword, hospital, sc)
        #采集百度WAP结果入库
        sg.upresult(2, keyword, hospital, sc)
    sc.commitsql()
    #分类
    cm.moveclass(sc)
    sc.commitsql()
    #获取平台
    pg.getplatform(sc)
    sc.commitsql()
    #获取目标数据
    #dp.parsedata(sc)
    #sc.commitsql()
    sc.closeconn()

if __name__ == '__main__':
    main()
    print "Down!"