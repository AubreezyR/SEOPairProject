import requests
import pprint
import json
from datetime import date

# Add exception if file does not exist or no string in file


def day_in_month(day, month):
    if month in (1, 3, 5, 7, 8, 10, 12):
        if day < 1 or day > 31:
            return False
        return True
    if month in (4, 6, 9, 11):
        if day < 1 or day > 30:
            return False
        return True
    if month == 2:
        if day < 1 or day > 28:
            return False
        return True
    return False


# Still need to make sure year is valid
def get_date():
    year = str(input("Enter year of your inital date: "))
    month = str(input("Enter the month of your inital date as a number"
                 + "(1 for jan, 2 for feb, etc.): "))
    while int(month) < 1 or int(month) > 12:
        month = input("Please enter a number between 1 and 12 for the month: ")
    day = str(input("Enter the day of your inital date: "))
    while not day_in_month(int(day), int(month)):
        day = str(input("Enter a valid day for the month of " + month + ": "))    
    if int(day) < 10:
        day = "0" + day
    if int(month) < 10:
        month = "0" + month
    return year + "-" + month + "-" + day


def get_key():
    with open('key.txt', 'r') as key_file:
        key = key_file.readlines()[0]
    return key


def get_unique_asteroids(data):
    ids = set()
    for date in data['near_earth_objects']:
        for asteroid in data['near_earth_objects'][date]:
            ids.add(asteroid['id'])
    return ids


def get_info(ids):
    print("Here are links to pages about all the asteroids near earth that week:")
    for id in ids:
        key = get_key()
        url = 'https://api.nasa.gov/neo/rest/v1/neo/' + str(id) + '?api_key=' + key
        response = requests.get(url)
        data = response.json()
        if data['is_potentially_hazardous_asteroid']:
            print(data['name'].upper() + 'IS A POTENTIALLY HAZARDOUS ASTEROID')
        print(data['name'] + '\t' + data['nasa_jpl_url'])


def main():
    date = get_date()
    key = get_key()
    url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=" + date + "&api_key=" + key
    response = requests.get(url)
    data = response.json()
    ids = get_unique_asteroids(data)
    get_info(ids)


if __name__ == '__main__':
    main()
