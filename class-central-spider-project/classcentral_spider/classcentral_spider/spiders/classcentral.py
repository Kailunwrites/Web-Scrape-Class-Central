# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class ClasscentralSpider(Spider):
    name = 'classcentral'
    allowed_domains = ['classcentral.com']
    start_urls = ['https://www.classcentral.com/subjects']

    def __init__(self, subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            subject_url = response.xpath('//a[contains(@title, "' + self.subject + '")]/@href').extract_first()
            absolute_subject_url1 = response.urljoin(subject_url)
            #absolute_subject_url = absolute_subject_url1 + '?certificate=true' + '&lang=english' + '&session=recent'+'&sort=rating-up'
            absolute_subject_url = absolute_subject_url1 + '?&lang=spanish'
            yield Request(absolute_subject_url,
                          callback=self.parse_subject)
        else:
            self.log('Scraping all subjects.')
            subjects = response.xpath('//h3/a[1]/@href').extract()
            for subject in subjects:
                absolute_subject_url1 = response.urljoin(subject)
                #absolute_subject_url = absolute_subject_url1 + '?certificate=true' + '&lang=english' + '&session=recent'+'&sort=rating-up'
                absolute_subject_url = absolute_subject_url1 + '?&lang=spanish'
                yield Request(absolute_subject_url,
                              callback=self.parse_subject)

    def parse_subject(self, response):
        subject_name = response.xpath('//h1/text()').extract_first()

        courses = response.xpath('//tr[@itemtype="http://schema.org/Event"]')
        #durations= response.xpath('//td[2]/div[2]/span/span[2]/text()')

        for course in courses:
            course_name = course.xpath('.//*[@itemprop="name"]/text()').extract_first()
            
            #course_institution = course.xpath('.//a[@data-track-click="listing_click"]/@data-track-props').extract_first()
             #note to self# try this on another course, should also work [98:180]

            ##course_provider= course.xpath('.//a[@data-track-click="listing_click"]/@data-track-props').extract_first()
            #course_provider = course.xpath('./td[2]/div[2]/span/span[1]/a').extract_first()[19:29]

            #course_rating= course.xpath('.//*[data-timestamp]').extract()
            #course_rating=course_rating[1]
            #[1][837-3:837].strip[' '] 837 comes from locating Reviews 
            #course_rating= course.xpath('//*[@id="course-listing-tbody"]/tr[2]/td[4]/div/span[2]/span/text()').extract()
            #num_of_ratings= course.xpath('//*[@id="course-listing-tbody"]/tr[2]/td[4]/div/span[3]/text()').extract()
            
            ##course_duration= course.xpath('./td[2]/div//span//text()').extract()[5:6]  # note to self# [5:6]
            ##course_start= course.xpath('.//*[@itemprop="startDate"]/@content').extract()
            
            #certificate= 1
            language= 'Spanish'
            #rank= counter
           
            course_url = course.xpath('.//a[@itemprop="url"]/@href').extract_first()
            absolute_course_url = response.urljoin(course_url)

            yield {'subject_name': subject_name,
                   'course_name': course_name,
                   'language': language,
                   'absolute_course_url': absolute_course_url}
        
        next_page = response.xpath('//link[@rel="next"]/@href').extract_first()

        if next_page:
            absolute_next_page = response.urljoin(next_page)
            yield Request(absolute_next_page,
                          callback=self.parse_subject)
        