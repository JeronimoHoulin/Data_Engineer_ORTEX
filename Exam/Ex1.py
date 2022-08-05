# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 13:45:48 2022

@author: Jeronimo H
"""

import os
import csv
from csv import DictReader
from typing import List, Dict


os.chdir('C:/Users/Usuario/Desktop/ProyectosPy/Interviews/ORTEX/Python_Dev_Challenge/Aswers')

print(f"We will be using the following DB: {os.listdir(os.getcwd())[0]}")


with open('2017.csv', 'r', encoding="utf8") as csvfile:
    csv_reader = csv.reader(csvfile)
    
    headers = next(csv_reader)
    
    
#print(headers)


file = open('2017.csv', 'r', encoding="utf8")
csv_reader = DictReader(file)

table = []

for row in csv_reader:
    float_row = {}
    for column in row:
        row[column] = row[column]
        
    table.append(row)
    
#print(table[0])

exchange_trades = []

for row in table:
    exchange_trades.append(row[f"{headers[-1]}"])

def MaxTraded(arr):
    return max(set(arr), key=arr.count)

print("")
print(f"The exchamge with most trdes is: {MaxTraded(exchange_trades)}.")

august_table = []

for row in table:
    if int(row["inputdate"]) > 20170731 and int(row["inputdate"]) < 20170831:
        august_table.append({
            "Name": row["companyName"], 
            "EUR": row["valueEUR"]
            })

august_values = []

for row in august_table:
    august_values.append({
        "Name": row["Name"]
        })
    row["Name"]

file.close()









































