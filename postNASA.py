import requests
import pprint
import pandas as pd
import json
from IPython.display import display
import matplotlib.pyplot as plt
import sqlite3 as sql


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
    print("Here are links to pages about all the asteroids"
          + "near earth that week:")
    for id in ids:
        key = get_key()
        url = ('https://api.nasa.gov/neo/rest/v1/neo/'
               + str(id) + '?api_key=' + key)
        response = requests.get(url)
        data = response.json()
        if data['is_potentially_hazardous_asteroid']:
            print(data['name'].upper()
                  + '\t\tIS A POTENTIALLY HAZARDOUS ASTEROID')
        print(data['name'] + '\t\t' + data['nasa_jpl_url'])

def create_Table(data):

    asteroidDict = {"Asteroid Names": [],
                    "Distnace From Earth": [],
                    "Velocity(km/hr)": [],
                    "Threat": []
                    }
    # Crate table
    for inital_date in data['near_earth_objects']:
        for i in range(len(data['near_earth_objects'][inital_date])):
            name = data['near_earth_objects'][inital_date][i]['name']
            asteroidDict["Asteroid Names"].append(name)
            distanceFromEarth = round(float(data['near_earth_objects'][inital_date][i]
                                            ['close_approach_data'][0]['miss_distance']
                                            ['kilometers']), 2)
            asteroidDict["Distnace From Earth"].append(distanceFromEarth)
            velocity = round(float(data['near_earth_objects'][inital_date][i]
                                   ['close_approach_data'][0]['relative_velocity']
                                   ['kilometers_per_hour']))
            asteroidDict["Velocity(km/hr)"].append(velocity)
            threat = data['near_earth_objects'][inital_date][i]['is_potentially_hazardous_asteroid']
            asteroidDict["Threat"].append(threat)

    # Create Distance graph
    create_Graph(
        asteroidDict["Asteroid Names"],
        asteroidDict["Distnace From Earth"],
        "Asteroid  Distance (km)",
        "Asteroid Names",
        "Distance From Earth (km)",
        asteroidDict["Asteroid Names"],
        asteroidDict["Velocity(km/hr)"],
        "Asteroid Velocity (km/hr)",
        "Asteroid Names",
        "Asteroid Velocity (km/hr))",
        "DataGraph")

    # Print table
    df = pd.DataFrame(asteroidDict)
    display(df)


def create_Graph(xv, yv, title, xl, yl, xv2, yv2, title2, xl2, yl2, fn):
    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    ax1.bar(xv, yv)
    ax1.set_xticklabels(
        xv,
        rotation=45,
        horizontalalignment='right',
        fontsize='7')
    ax1.set_title(title, fontsize="12")
    ax1.set_ylabel(yl)

    ax2.bar(xv2, yv2)
    ax2.set_xticklabels(
        xv2,
        rotation=45,
        horizontalalignment='right',
        fontsize='7')
    ax2.set_title(title2, fontsize="12")
    ax2.set_ylabel(yl2)
    plt.savefig(fn)

def database(data):
    closest_known_misses = []
    conn = sql.connect('database.db')
    c = conn.cursor()
    table = ("CREATE TABLE IF NOT EXISTS asteroids ("
             + "id text,"
             + "name text,"
             + "size text,"
             + "closest_miss_distance text)")
    c.execute(table)

    for date in data['near_earth_objects']:
        for asteroid in data['near_earth_objects'][date]:
            query = ("SELECT closest_miss_distance from asteroids "
                     + "WHERE id=?;")
            c.execute(query, (str(asteroid['id']),))
            miss_distance = c.fetchall()

            if len(miss_distance) > 0:
                miss_distance = miss_distance[0]
            else:
                miss_distance = None

            new_miss_distance = float(asteroid['close_approach_data']
                                      [0]['miss_distance']['kilometers'])
            if miss_distance is not None and miss_distance > new_miss_distance:
                update = ("UPDATE asteroids "
                          + "SET closest_miss_distance = ? "
                          + "WHERE id = ?;")
                c.execute(update, (str(new_miss_distance),
                          str(asteroid['id']),))
                closest_known_misses.append(miss_distance)
            else:
                update = ("REPLACE INTO asteroids"
                          + "(id, name, size, closest_miss_distance)"
                          + "VALUES(?, ?, ?, ?);")
                c.execute(update, (str(asteroid['id']), asteroid['name'],
                          str(asteroid['estimated_diameter']['kilometers']),
                          str(new_miss_distance),))
                closest_known_misses.append(new_miss_distance)
    return closest_known_misses


def main():
    date = get_date()
    key = get_key()
    url = ("https://api.nasa.gov/neo/rest/v1/feed?start_date="
           + date + "&api_key=" + key)
    response = requests.get(url)
    data = response.json()
    print(database(data))
    ids = get_unique_asteroids(data)
    get_info(ids)
    create_Graph(data, date)


if __name__ == '__main__':
    main()
