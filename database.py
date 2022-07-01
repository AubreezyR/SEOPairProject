import sqlite3

country = input("Input a country: ")
year = input("Input a year: ")

connect = sqlite3.connect(country.capitalize()+'.db')
connectCursor = connect.cursor()

for i in connectCursor.execute('SELECT*FROM cuba'):
    print(i)
   
connectCursor.close()