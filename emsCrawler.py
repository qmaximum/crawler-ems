__author__ = 'qmax'

import sys
import urllib
import urllib2
import os
import cookielib
import re
import cStringIO
from codeCrack import CrackOcr
import config as cg

from threading import Thread
import time
import random
from Queue import Queue

queue = Queue(10)


class Crawler:

    def __init__(self, codemask):
        self.codemask = codemask
        url = cg.ems_singlequery_url
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(self.opener)
        resp = urllib2.urlopen(url)
        self.crack = CrackOcr(self.codemask)

    def crawl(self, waybilllist):

        list_crawl_rst =[]

        # for index, cookie in enumerate(cj):
            # print '[',index, ']',cookie;

        rand_url = cg.ems_rand_code_url
        request = urllib2.Request(rand_url)

        f = self.opener.open(request)

        # content =  f.read()

    # if we should write a temp png every time

        # with open(os.getcwd() + "/temp.png",'wb') as code:
        # code.write(content)
        # crackcode =  ocr("temp.png")

    # we can write to a memory buffer just like this
        file_like = cStringIO.StringIO(f.read())
        crackcode = self.crack.ocr(file_like)
        # print self.codemask
        # print crackcode

        multinum = ''
        for i in xrange(len(waybilllist) ):
            multinum = "\n".join([multinum, waybilllist[i]])

        data = {'checkCode': str(crackcode), 'muMailNum':  multinum }

        request = urllib2.Request(
                url=cg.ems_multiquery_url,
                data=urllib.urlencode(data)
        )

        f = self.opener.open(request)

        fmain = f.read()

    # we need to handle the error if crackcode is wrong
    # here is a typo originally appeared in ems website !verfication!
        m = re.match(r"Validation Failure, please re-enter verfication code.", fmain)
        if not m:
            exp_text = re.compile(cg.exp_text_pattern)
            exp_li = re.compile(cg.exp_li_pattern)
            exp_num = re.compile(cg.exp_num_pattern)
            exp0 = re.compile(cg.exp0_pattern)
            exp1 = re.compile(cg.exp1_pattern)
            exp2 = re.compile(cg.exp2_pattern)

            for multiresult in exp_text.findall(fmain):
                for singresult in exp_li.findall(multiresult):
                    strrst = ''
                    for num in exp_num.findall(singresult):
                        num_str = num.strip()
                        #print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
                        #print num_str[0:13]
                        strrst += num_str[0:13]
                        break
                    for restable in exp0.findall(singresult):
                        # print restable
                        headflag = 1
                        for row in exp1.findall(restable):
                            if headflag == 1:
                                headflag = 0
                                continue
                            else:
                                #print '==============='
                                strtbl = ""
                                for col in exp2.findall(row):
                                    #print col.replace('&nbsp;', ' ').strip()
                                    strtbl = "##".join([strtbl,col.replace('&nbsp;', ' ').strip()])

                                strrst = " ".join([strrst, strtbl])
                        list_crawl_rst.append(strrst)
        else:
            print "error"
        #print list_crawl_rst
        return list_crawl_rst


class ProducerThread(Thread):
    def run(self):
        global queue
        ems_crawler = Crawler(cg.codemask)
        while True:
            waybilllist = ['5032982334103', '1234567890121']
            rst = ems_crawler.crawl(waybilllist)
            queue.put(rst)
            #print "Produced", rst
            time.sleep(random.random())
            break


class ConsumerThread(Thread):
    def run(self):
        global queue
        while True:
            rst = queue.get()
            queue.task_done()
            print "Consumed", rst
            time.sleep(random.random())
            break



if __name__ == '__main__':

    ProducerThread().start()
    ConsumerThread().start()


