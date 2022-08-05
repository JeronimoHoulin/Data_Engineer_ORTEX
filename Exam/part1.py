# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 11:05:56 2022

@author: JeronimoH
"""

import psycopg2
import pandas as pd

df = pd.read_csv("2017.csv")

#Editing data types on th Pandas df so that it can merge with postgradeSQL
replacements = {
    'object': 'varchar',
    'int64': 'int'
}
df.dtypes.replace(replacements)

df = df [["exchange", "inputdate", "companyName", "valueEUR", "tradeSignificance"]]

df.to_csv('trades_recap.csv', header=df.columns, index=False, encoding='utf-8')

my_file = open('trades_recap.csv')


#Openning connection to PostgradeSQL db
conn = psycopg2.connect(
   database="2017", user='postgres', password='', host='127.0.0.1', port= '5432'
)
cursor = conn.cursor()

cursor.execute("select version()")

data = cursor.fetchone()
#print("Connection established to: ", data)

#Doping TRADES table if already exists.
cursor.execute("DROP TABLE IF EXISTS TRADES")

sql ='''CREATE TABLE TRADES(
   EXCHANGE VARCHAR NOT NULL,
   INPUTDATE INT,
   COMPANYNAME VARCHAR,
   VALUEEUR FLOAT,
   TRADESIG INT
)'''
cursor.execute(sql)
#print("Table created successfully!.")
conn.commit()

#Pushing the 2017.csv data into the table

sql_upload = """
    COPY TRADES FROM STDIN WITH
    CSV
    HEADER
"""

cursor.copy_expert(sql=sql_upload, file=my_file)
#print("File pushed to db!")

#First question:
sql = """
    SELECT EXCHANGE, Count(EXCHANGE) as TotalTrades
    FROM TRADES
    Group By Exchange
    Order By TotalTrades DESC
"""

cursor.execute(sql)
resp = cursor.fetchall()
print("\n")
print("TOP 3 Exchanges by trades:")
print(f" #1: {resp[0][0]} with {resp[0][1]} trades.")
print(f" #2: {resp[1][0]} with {resp[1][1]} trades.")
print(f" #3: {resp[2][0]} with {resp[2][1]} trades.")

#Second question
sql = """
    SELECT * FROM TRADES
    WHERE 20170801 <= INPUTDATE and INPUTDATE < 20170901
"""
cursor.execute(sql)
resp = cursor.fetchall()
df_august = pd.DataFrame(resp, columns =['exchange', 'date', 'name', 'eur', 'significance'])

sum_company = df_august.groupby(["name"]).sum().sort_values(["eur"], ascending=False).reset_index()
top2 = sum_company[0:2]
print("\n")
print("Companies with highest ValueEUR in August:")
print(f" #1: {top2.name[0]} with ${'{:,.2f}'.format(round(top2.eur[0], 1))} Euros.")
print(f" #2: {top2.name[1]} with ${'{:,.2f}'.format(round(top2.eur[1], 1))} Euros.")

#Third question
sql = """
    SELECT * FROM TRADES
    WHERE TRADESIG = 3
"""
cursor.execute(sql)
resp = cursor.fetchall()

df_3 = pd.DataFrame(resp, columns =['exchange', 'date', 'name', 'eur', 'significance'])
#I will use Value EUR as the referance for transaction volume, as it will be displayed in %.. so it doesn't matter if its USD
df_3['month'] =  pd.to_datetime(df_3['date'], format='%Y%m%d').dt.month

df_3['percent'] = df_3['eur'].transform(lambda x: (x/x.sum()) * 100)

monthly_perc = df_3.groupby(["month"]).sum()
#print(round(monthly_perc["percent"].sum()))

monthly_perc.drop(["date", "eur", "significance"], axis=1, inplace=True)

monthly_perc["percent"] = round(monthly_perc["percent"], 2)

print("\n")
print("Monthly percentage of transactions with trade significance 3: ")
print("\n")
print(monthly_perc)
#Closing the connection
conn.close()
































