from bs4 import BeautifulSoup
import requests

url = "https://www.passiton.com/inspirational-quotes?page=2"
response = requests.get(url)
# print(response.content)

soup = BeautifulSoup(response.content, features="html5lib")

container_element = soup.findAll("div", {"id": "all_quotes"})
#print(container_element)

container = container_element[0]
div_element = container.findAll("div")
print(div_element[0])

for i, element in enumerate(div_element):
    with open("scrap_image{}.jpg".format(i), "wb") as file:
        img_element = element.findAll("img")[0]
        img_url = img_element.attrs["src"]
        r = requests.get(img_url)
        file.write(r.content)


