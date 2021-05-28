import requests
from bs4 import BeautifulSoup


userin = input("Enter what type of images you want to scrap")
keyword_list = userin.split(" ")
keyword_string = ""

for word in keyword_list:
    keyword_string += word + "+"

keyword_string = keyword_string[:-1]
print(keyword_string)

url = "https://www.snapdeal.com/search?keyword="
response = requests.get(url + keyword_string)
#print(response.content)

soup = BeautifulSoup(response.content, 'html.parser')

div_elements = soup.findAll("div", {"class": "product-tuple-image"})

for div in div_elements:

    for i, div in enumerate(div_elements):

        with open("snapdeal_{0}{1}.jpg".format(userin, i), "wb") as file:
            img_element = div.findAll("img")[0]

            if img_element.has_attr('src') is True:
                r = requests.get(img_element.attrs['src'])
                print(r.content)
                file.write(r.content)
            elif img_element.has_attr('data-src') is True:
                r = requests.get(img_element.attrs['data-src'])
                print(r.content)
                file.write(r.content)
            else:
                pass





