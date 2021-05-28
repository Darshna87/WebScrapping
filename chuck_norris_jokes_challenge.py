import requests
import json


url = "http://api.icndb.com/jokes/"
joke_IDs = [2, 3, 16, 20, 72, 1, 24]
json_str = ""

for joke_id in joke_IDs:

    response = requests.get(url+str(joke_id))
    #print(type(response.content))
    #print(response.content)

    # converting bytes into json
    json_data = json.loads(response.content)
    #print(json_data)
    print(json_data["value"]['joke'])

    # converting json data into string with csv format
    json_str += str(joke_id)+"," + json.dumps(json_data["value"]['joke'])+"\n"

json_str = json_str[:-1]
with open("jokes.csv", "w") as file:
    file.write(json_str)




