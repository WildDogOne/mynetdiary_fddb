import requests
import json
from bs4 import BeautifulSoup
from config import cookie
from pprint import pprint


def get_fddb_data(url, custom_food):
    URL = url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find("h3")
    title = title.text
    custom_food["foodName"] = title

    data = []
    table_body = soup.findAll("table")[1]
    rows = table_body.findAll("tr")
    for row in rows:
        cols = row.findAll("td")
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values
    for x in data:
        amount, unit = unit_splitter(x[1])
        if x[0] == "Kalorien":
            custom_food["calories"] = {"value": amount, "unit": None}
        if x[0] == "Protein":
            custom_food["protein"] = {"value": amount, "unit": unit}
        if x[0] == "Kohlenhydrate":
            custom_food["totalCarbs"] = {"value": amount, "unit": unit}
        if x[0] == "Fett":
            custom_food["totalFat"] = {"value": amount, "unit": unit}
    #pprint(custom_food)
    return custom_food


def unit_splitter(data):
    data = data.replace(",", ".")
    data = data.split(" ")
    amount = data[0]
    unit = data[1]
    return amount, unit


def push_to_mynetdiary(custom_food):
    url = "https://www.mynetdiary.com/muiSaveCustomFood.do"

    payload = {
        "customFood": custom_food,
        "mealTypeId": 4,
        "sortOrder": "a",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Origin": "https://www.mynetdiary.com",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://www.mynetdiary.com/meals.do",
        "Cookie": cookie,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
    }
    pprint(payload)
    response = requests.request("POST", url, headers=headers, json=payload)

    pprint(response.text)


def main():
    custom_food = {
        "imageId": 13,
        "servingWeightUnit": "g",
        "foodName": "Test 2",
        "foodNameError": None,
        "servingOrCaloriesError": None,
        "servingName": "1",
        "servingNameError": None,
        "servingWeight": "100",
        "servingWeightError": None,
    }
    url = "https://fddb.mobi/de/avopri_indonesian_soy_sauce_kecap_asin.html"
    url = input("Food to Import: ")
    custom_food = get_fddb_data(url, custom_food)
    push_to_mynetdiary(custom_food)


if __name__ == "__main__":
    main()
