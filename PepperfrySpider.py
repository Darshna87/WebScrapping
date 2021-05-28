import scrapy
import os
import json
import requests


class PepperfrySpider(scrapy.Spider):

    name = "Pepperfry_Spider"
    BASE_DIR = "..\Pepperfry Data\\"
    ITEM_COUNT = 10
    PRODUCT_COUNT = 20
    META_IMAGE_COUNT = 5

    def start_requests(self):

        BASE_URL = 'https://www.pepperfry.com/site_product/search?q='

        items = ["sofa set", "Garden sitting", "3 Seater Sofas", "Dining Sets", "Shoe Racks", "Wardrobes", "King Size Beds",
               "Arm Chairs", "Chest of Drawers", "Bean Bags", "Swings", "Office Tables", "Benches"
               ]

        urls = []
        dir_names = []

        for item in items:
            query_string = '+'.join(item.split(" "))
            urls.append(BASE_URL+query_string)

            dir_name = ' '.join(item.split(' '))
            dir_names.append(dir_name)

            dir_path = self.BASE_DIR+dir_name
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        for i in range(len(urls)):
            '''d={
                'dir_name':dir_names[i]
            }'''
            self.log(urls[i])
            resp = scrapy.Request(url=urls[i], callback=self.parse, dont_filter=True)
            resp.meta['dir_name'] = dir_names[i]
            yield resp


    def parse(self, response, **meta):

        product_urls = response.xpath('//div/div/div/a[@target="_blank"]/@href').extract()
        #print(len(product_urls))

        count = 1
        for prod_url in product_urls:
            self.log(prod_url)
            res = scrapy.Request(url=prod_url, callback=self.parse_item, dont_filter=True)
            res.meta['dir_name'] = response.meta['dir_name']
            if count == self.PRODUCT_COUNT:
                break
            if res is not None:
                count += 1
            yield res

    def parse_item(self, response):
     #   self.log(response.content)
        item_title = response.xpath('//div/div/div/h1/text()').extract()[0]
        self.log(item_title)
        item_price = response.xpath('//div/div/div/span[@class="v-offer-price-amt pf-medium-bold-text"]/text()').extract()[0]
        item_savings = response.xpath('//div/div/div/span'
                                      '[@class="v-price-save-ttl-amt pf-medium-bold-text total_saving"]/text()').extract()[0]
        item_description = response.xpath('//div[@itemprop="description"]/p/text()').extract()

        item_details_keys = response.xpath('//div/div/div/span[@class="v-prod-comp-dtls-listitem-label"]/text()').extract()
        item_details_values = response.xpath('//div/div/div/span'
                                             '[@class="v-prod-comp-dtls-listitem-value pf-text-grey"]/text()').extract()

        # cleaning with key-value pairs and make a dictionary
        brand = response.xpath('//span[@itemprop="brand"]/text()').extract()
        item_details_values[0] = brand[0]

        stop_words = ["(all dimensions in inches)", "(all dimensions in inches )", "( all dimensions in inches)"]
        item_details_values = [word.strip() for word in item_details_values if word not in stop_words]

        a = len(item_details_keys)
        b = len(item_details_values)
        idetails={}

        for i in range(min(a, b)):
            idetails[item_details_keys[i][:-1]] = item_details_values[i]#[:-1 to remove : from key]


        stop_lines = ["Pepperfry.com", "So go ahead and buy with confidence.", "we also offer you a",
                    "Brand will upfront contact you for assembly"]
        item_description = filter(lambda x: all([not y.lower() in x.lower() for y in stop_lines]), item_description)
        item_description = '\n'.join(item_description)

        image_url_list = response.xpath('//li[@class="vipImage__thumb-each noClickSlide"]/a/@data-img').extract()

        if len(image_url_list) > 3: #extracting only if having more than three images
            d = {
                'Item Title': item_title,
                'Price': item_price,
                'Savings': item_savings,
                'Description': item_description,
                'Details': idetails
            }

            CATEGORY_NAME = response.meta['dir_name']

            ITEM_DIR_URL = os.path.join(self.BASE_DIR, os.path.join(CATEGORY_NAME, item_title))
            print(ITEM_DIR_URL)
            if not os.path.exists(ITEM_DIR_URL):
                os.makedirs(ITEM_DIR_URL)

            with open(os.path.join(ITEM_DIR_URL, 'metadata.txt'), "w") as f:
                json.dump(d,f)


            for i, img_url in enumerate(image_url_list):
                r = requests.get(img_url)
                with open(os.path.join(ITEM_DIR_URL, "image_{}.jpg".format(i)), "wb") as f:
                    f.write(r.content)
            print("-------successfully saved data at "+ITEM_DIR_URL+" for item "+item_title+"----------")

            yield d
        yield None














