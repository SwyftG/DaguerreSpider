# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy import Request
from bs4 import BeautifulSoup
from Daguerre.settings import ROOT_URL, LOCAL_FILE_ROOT, MAX_PAGES
from Daguerre.items import DaguerrePostItem


class SuperspiderSpider(scrapy.Spider):
    root_url = ROOT_URL
    local_file_root = LOCAL_FILE_ROOT
    max_pages = MAX_PAGES
    name = 'superspider'
    allowed_domains = ['bc.ghuws.men']
    start_urls = ['http://bc.ghuws.men/thread0806.php?fid=16&search=&page=1']

    def parse(self, response):
        content = response.body
        soup = BeautifulSoup(content, "html.parser")
        a_list = soup.find_all('a', attrs={'href': True, 'id': True})
        for item in a_list:
            temp_result = item['href'].split('/')
            if len(temp_result) == 4:
                year_month = temp_result[2]
                post_id = temp_result[3].split('.')[0]
                if int(year_month) > 1800 and len(post_id) > 6:
                    post_url = self.root_url + item['href']
                    yield Request(url=post_url, callback=self.parse_post_page, meta={'post_id': post_id})
        cur_page = int(response.url.split('=')[-1])
        next_page = cur_page + 1
        if next_page <= MAX_PAGES:
            next_page_url = response.url[:-len(str(cur_page))] + str(next_page)
            yield Request(url=next_page_url, callback=self.parse)

    def parse_post_page(self, response):
        content = response.body
        soup = BeautifulSoup(content, "html.parser")
        temp_title_list = soup.find_all('h4')
        post_id = response.meta['post_id']
        post_url = response.url
        post_title = ""
        if len(temp_title_list) != 0:
            post_title = temp_title_list[0].text
        # print(post_title + " URL: " + response.url)
        temp_img_list = soup.find_all('input', attrs={'type': 'image'})
        img_list = []
        post_image_list = []
        for i in range(len(temp_img_list)):
            if i == 1:
                src1 = temp_img_list[0]['src'].split('/')[2]
                src2 = temp_img_list[1]['src'].split('/')[2]
                if src1 != src2:
                    img_list.remove(temp_img_list[0])
            img_list.append(temp_img_list[i])
        for item in img_list:
            image_url = item['src']
            post_image_list.append(item['src'])
            yield Request(url=image_url, callback=self.down_load_image,
                          meta={'post_id': post_id, 'post_title': post_title, 'index': img_list.index(item)},
                          dont_filter=True)
        item = DaguerrePostItem()
        item['post_id'] = post_id
        item['post_title'] = post_title
        item['post_url'] = post_url
        item['post_image_list'] = post_image_list
        yield item

    def down_load_image(self, response):
        content = response.body
        index = response.meta['index']
        post_id = response.meta['post_id']
        post_title = response.meta['post_title']
        pic_format = response.url.split('.')[-1]
        # 创建本地目录的操作
        if response.status == 200:
            file_dir = self.local_file_root + post_title + "/"
            filename = file_dir + str(index) + "." + pic_format
            exist = os.path.exists(file_dir)
            if not exist:
                os.makedirs(file_dir)
            # 写入文件的操作
            with open(filename, 'xb') as file:
                file.write(content)


