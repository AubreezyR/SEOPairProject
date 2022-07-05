import requests
import json
import pandas
import sqlalchemy as db
from matplotlib import pyplot as plt
# Correct country name? and test for invalid country names in API
def is_from_country(id, country):
    url = ("http://lookup-service-prod.mlb.com/json/"
           + "named.player_info.bam?sport_code='mlb'&"
           + "player_id=" + str(id))
    response = requests.get(url)
    if (response.json()['player_info']['queryResults']
            ['row']['birth_country'].lower() == country.lower()):
        return True
    return False
# Find out if this can return invalid teams
def get_teams(year):
    team_ids = []
    fake_teams = [
     '', 'no team', 'office of the commissioner',
     'to be determined', 'national league all-stars',
     'national league champion', 'american league champion',
     'american league all-stars'
      ]
    url = ("http://lookup-service-prod.mlb.com/json/"
           + "named.team_all_season.bam?sport_code='mlb'&season="
           + str(year) + "&team_all_season.col_in=mlb_org_id&"
           + "team_all_season.col_in=name_display_full")
    response = requests.get(url)
    data = response.json()['team_all_season']['queryResults']['row']
    for i in data:
        if i['name_display_full'].lower() not in fake_teams:
            team_ids.append(i['mlb_org_id'])
    return team_ids
def get_players(country, year):
    teams = get_teams(year)
    players = []
    for i in teams:
        roster_url = ("http://lookup-service-prod.mlb.com/json/"
                      + "named.roster_team_alltime.bam?start_season="
                      + str(year) + "&end_season="
                      + str(year) + "&team_id=" + str(i) + "")
        response = requests.get(roster_url)
        try:
            data = (response.json()['roster_team_alltime']
                    ['queryResults']['row'])
        except ValueError or TypeError:
            continue
        for j in data:
            try:
                if is_from_country(j['player_id'], country):
                    players.append(j['player_id'])
            except ValueError or TypeError:
                continue
    return players
# Make sure these catch invalid inputs
def get_start_year():
    try:
        year = int(input("Enter the starting year: "))
    except ValueError or TypeError:
        print("Year must be an integer")
        get_start_year()
    if year < 1876 or year > 2022:
        print("Year must be between 1876 and 2022")
        get_start_year()
    return year
def get_end_year(start_year):
    try:
        year = int(input("Enter the starting year: "))
    except ValueError or TypeError:
        print("Year must be an integer")
        get_end_year()
    if year < 1876 or year > 2022 or year < start_year:
        print("Year must be between 1876 and 2022,"
              + " and after the starting year")
        get_end_year()
    return year
# Test country in is_from_country, or allow invalid countries?
def get_country():
    country = input("Enter a country: ")
    usa = ['united states', 'unitedstates', 'us', 'unitedstatesofamerica',
           'united states of america', 'america']
    if country in usa:
        country = 'usa'
    return country
# Test for file errors, format json file
# and make axes discrete? maybe move files to seperate directories
def save_files(data, start_year, end_year, country, num_of_players):
    with open(str("json/" + country.capitalize() + str(start_year) + "_"
              + str(end_year) + ".json"), "w") as json_file:
        json.dump(data, json_file)
    plt.plot(list(range(start_year, (end_year + 1))), num_of_players)
    plt.xlabel("Year")
    plt.ylabel("Players from " + country.capitalize())
    plt.title("MLB players from " + country.capitalize())
    plt.savefig("graphs/" + country.capitalize() + str(start_year)
                + "_" + str(end_year) + ".png")
# Make sure this works overall
def sql_database(data, country):
    pandas_data = pandas.DataFrame.from_dict(data, orient='index')
    engine = db.create_engine('sqlite:///data.db')
    pandas_data.to_sql(country, con=engine,
                       if_exists='replace', index=False)
    query_result = engine.execute("SELECT * FROM " + country + ";").fetchall()
    print(pandas.DataFrame(query_result))
def main():
    print("This program will create a graph of the number"
          + "of mlb players from a certain country over time")
    start_year = get_start_year()
    end_year = get_end_year(start_year)
    country = get_country()
    print("Creating graph, this may take a while.  Press ctrl + C to quit")
    num_of_players = []
    data = {}
    for i in range(start_year, (end_year + 1)):
        print("Processing " + str(i))
        try:
            data[str(i)] = get_players(country, i)
            num_of_players.append(len(data[str(i)]))
        except ValueError or TypeError:
            continue
    save_files(data, start_year, end_year, country, num_of_players)
    sql_database(data, country)
if __name__ == '__main__':
    main()
