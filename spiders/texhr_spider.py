# -*- coding: utf-8 -*-
import scrapy
import urlparse
import time
from scrapy import  Requsest
import pandas as pd
from pprint import pprint
import codecs

from texhr.items import TexhrItem
import re

class TexhrSpiderSpider(scrapy.Spider):
    name = 'texhr_spider'
    # allowed_domains = [' texhr.cn']
    start_urls = ['http://www.texhr.cn/personal/login.html']
    data = []
    # labels = ['公司', '企业类型', '产品种类', '人数', '地址', '网页', '简介']
    # # data['name'] =[]
    # f = codecs.open('output.txt', 'a+')
    # f.write(str(labels).encode('utf-8') + '\n')
    # f.close()
    def parse(self,response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username':'hypachong','password':'hypachong123'},
            callback = self.after_login
        )

    def after_login(self, response):
        url = 'http://www.texhr.cn/search/zhiwei.asp?request_edu=0&request_experience=0&keywords=0&zhaopin_bigname=0&edittime=0&hidJobArea=0&hidFuntype=0&province2=0&keywordtype=5&invite_salary=0&px=146&mpage=20&isjj=&page=706'
        yield Request(url, callback=self.get_urls)

    def get_urls(self,response):
        urls = response.css('div.cname > a::attr(href)').extract()
        output = []
        for url in urls:
            if url not in output:
                output.append(url)
        print output
        for url in output:
            time.sleep(3)
            yield scrapy.Request(url = url, callback = self.parse_details)

        next_ur = response.xpath('//*[@id="wrapper"]/div[3]/div[7]/div[4]/div/a/@href').extract()[-1]

        if next_ur:
            next_page_url=urlparse.urljoin('http://www.texhr.cn/search/zhiwei.asp', next_ur)
            print '------------sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss'
            print next_page_url
            yield scrapy.Request(url = next_page_url,callback=self.get_urls )

    def parse_details(self,response):

        item = TexhrItem()
        # print response.body
        try:
            item['companyHead'] =  response.css('div.companyHead > h1::text').extract_first()

        except IndexError:
            item['companyHead'] = ''
            pass
        # ver1 = response.xpath(u'//*[@class="zp_info"]/ul/li[1]/span[contains(text(),"企业性质")]')
        try:
            item['sfund'] =  response.css('div.zp_info > ul > li::text').extract()[0]
        except IndexError:
            item['sfund']=''
            pass
        try:
            item['productype'] = response.css('div.zp_info > ul > li::text').extract()[1]
        except IndexError:
            item['productype']=''
            pass
        try:
            item['people'] = response.css('div.zp_info > ul > li::text').extract()[2]
        except IndexError:
            item['people']=''
            pass
        try:
            item['location'] = response.css('div.zp_info > ul > li::text').extract()[3]
        except IndexError:
            item['location']=''
            pass
        try:
            item['website'] = response.css('div.zp_info > ul > li::text').extract()[4]
        except IndexError:
            item['website']=''
            pass
        try:
            item['common'] =  [''.join([x.rstrip() for x in response.css('div.jswz  ::text').extract()])[5:]]
            # item['common'] =  [''.join(response.css('div.jswz  ::text').extract())].read().splitlines()

        except IndexError:
            item['common']=''
            pass
        data = ([item['companyHead'], item['sfund'],item['productype'],item['people'],item['location'], item['website'] ,item['common'] ])
        f = codecs.open('output.txt', 'a+',encoding="utf-8")
        f.write(str(data).decode('unicode_escape') +'\n')
        f.close()

        # table = response.xpath('//*[@id="ckslx"]/table/tr/td[1]/table')
        # print table
        # df = pd.read_html(table)[0]  # get the first parsed dataframe
        # pprint(df.values.tolist())
        # print df.values.tolist()
        # for div in divs:
        #     item = TestBotItem()
        #     item['var1'] = div.select('./td[2]/p/span[2]/text()').extract()
        #     item['var2'] = div.select('./td[3]/p/span[2]/text()').extract()
        #     item['var3'] = div.select('./td[4]/p/text()').extract()
        #
        #     yield item
        # item['productype'] = response.css('div.zp_info > ul > li::text').extract()[1]
        # item['people'] = response.css('div.zp_info > ul > li::text').extract()[2]
        # item['location'] = response.css('div.zp_info > ul > li::text').extract()[3]
        # # item['address'] = response.css('div.zp_info > ul > li::text').extract()[4]
        # item['website'] = response.css('div.zp_info > ul > li::text').extract()[4]
        # item['common'] = response.css('div.jswz::text').extract_first()

        # print 'sfund'+ item['sfund']
        # print 'productype'+item['productype']
        # print 'people'+item['people']
        # print 'location'+item['location']
        # # print item['address']
        # print 'website'+item['website']
        # print item['common']
        # item['common']
        # yield {
        #     'sfund': response.css('div.zp_info > ul > li::text').extract()[0],
        #     'productype': response.css('div.zp_info > ul > li::text').extract()[1],
        #     'people': response.css('div.zp_info > ul > li::text').extract()[2],
        #     'location': response.css('div.zp_info > ul > li::text').extract()[3],
        #     'website': response.css('div.zp_info > ul > li::text').extract()[4],
        #     'common': response.css('div.jswz::text').extract_first()
        # }


