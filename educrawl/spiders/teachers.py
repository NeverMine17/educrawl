# -*- coding: utf-8 -*-
import base64
import re

import scrapy

from educrawl.items import Teacher
import requests


class TeachersSpider(scrapy.Spider):
    name = 'teachers'
    allowed_domains = ['education.simcat.ru']
    start_urls = ['http://education.simcat.ru/']
    regexp = re.compile(r'school(\d+)')

    def parse(self, response):
        for school in response.css("[width='220'] tbody a.red_link"):
            if school.attrib['href'].startswith('school'):
                yield scrapy.Request('http://education.simcat.ru/' + school.attrib['href'] + 'teacher/',
                                     self.parse_pages)

    def parse_pages(self, response):
        pages = len(response.css("td[colspan='3'] a")) + 1
        for pagenum in range(1, pages):
            yield scrapy.Request(response.urljoin('page{}/'.format(pagenum)), self.parse_page)

    def parse_page(self, response):
        for teacherurl in response.css("[height='10'] a"):
            yield scrapy.Request(response.urljoin(teacherurl.attrib['href']), self.parse_teacher)

    def parse_teacher(self, response):
        yield Teacher(
            name=response.css('#central > tbody > tr > td:nth-child(1) > table > tbody > tr > td:nth-child(2) > div > '
                              'table > tbody > tr:nth-child(3) > td > h2').get().replace('<h2>', '').replace(
                '</h2>', '').replace('\xf9', ''),
            prof=response.css('#central > tbody > tr > td:nth-child(1) > table > tbody > tr > td:nth-child(2) > div > '
                              'table > tbody > tr:nth-child(4) > td:nth-child(2) > center > b').get().replace(
                '<b>', '').replace('</b>', '').replace('\xf9', ''),
            about=response.css('#central > tbody > tr > td:nth-child(1) > table > tbody > tr > td:nth-child(2) > div >'
                               ' table > tbody > tr:nth-child(5) > td > div').get().replace('<br>', '\n').replace(
                '<div style="text-align:justify;">', '').replace('</div>', '').replace('\xf9', ''),
            school=self.regexp.search(response.url).group(1),
            image=base64.b64encode(requests.get(response.urljoin(response.css("[height='10'] img")[0].attrib['src'])).content).decode()
        )
