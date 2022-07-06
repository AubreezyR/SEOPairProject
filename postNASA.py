import requests
import pprint
import pandas as pd
import json
from IPython.display import display

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


#Still need to make sure year is valid
def get_inital_date():
    year = str(input("Enter year of your inital date: "))
    month = str(input("Enter the month of your inital date as a number (1 for jan, 2 for feb, etc.): "))
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


def valid_end_date(inital_date, end_year, end_month, end_day):
    if int(end_year) < int(inital_date[0:4]):
        return False
    if int(end_year) > int(inital_date[0:4]):
        return True
    if int(end_month) < int(inital_date[5:7]):
        return False
    if int(end_month) > int(inital_date[5:7]):
        return True
    if int(end_day) < int(inital_date[8:10]):
        return False
    if int(end_day) > int(inital_date[8:10]):
        return True
    return True


def get_final_date(inital_date):
    response = input("Would you like to only get the asteroids of 1 week? Type y/n: ")
    if response[0].lower() == 'y':
        return inital_date
    year = str(input("Enter year of your final date: "))
    month = str(input("Enter the month of your final date as a number (1 for jan, 2 for feb, etc.): "))
    while int(month) < 1 or int(month) > 12:
        month = input("Please enter a number between 1 and 12 for the month: ")
    day = str(input("Enter the day of your final date: "))
    while not day_in_month(int(day), int(month)):
        day = str(input("Enter a valid day for the month of " + month + ": "))
    
    if int(day) < 10:
        day = "0" + day
    if int(month) < 10:
        month = "0" + month
    
    if not valid_end_date(inital_date, year, month, day):
        print("Your end date must be after your start date.")
        return get_final_date(inital_date)
    return year + "-" + month + "-" + day

#def create_Dataframe(data):
    #asteroidDict ={"asteroid_names":[],
     #               "distance_from_earth":[],
  #                  "velocity":[]
#    }
 #   for i in range(len(data['near_earth_objects'][inital_date])-1):
  #      name = data['near_earth_objects'][inital_date][i]['name']
   #     asteroidDict["asteroid_names"].append(name)
    ##   asteroidDict["distance"].append(distanceFromEarth)
      #  velocity =data['near_earth_objects'][inital_date][i]['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']
       # asteroidDict["velocity"].append(velocity)
    
    #df = pd.DataFrame(asteroidDict)
    #return df


def create_dataframe(ids):
    asteroids = {}
    key = get_key()
    for id in ids:
        url = "https://api.nasa.gov/neo/rest/v1/neo/" + id + "?api_key=" + key
        response = requests.get(url)
        data = response.json()
        this_asteroid = {
            'name' : data['name'],
            'distances' : {},
            'velocities' : {}
        }
        for date in data['close_approach_data']:
            this_asteroid['velocities'][date['close_approach_date']] = date['relative_velocity']['kilometers_per_hour']
            this_asteroid['distances'][date['close_approach_date']] = date['miss_distance']['kilometers']
        asteroids[id] = this_asteroid
    df = pd.DataFrame(asteroids)
    return df


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


def main():
    inital_date = get_inital_date()
    final_date = get_final_date(inital_date)
    key = get_key()
    url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=" + inital_date + "&end_date=" + final_date + "&api_key=" + key
    response = requests.get(url)
    data = response.json()
    ids = get_unique_asteroids(data)
    pprint.pprint(create_dataframe(ids))


if __name__ == '__main__':
    main()