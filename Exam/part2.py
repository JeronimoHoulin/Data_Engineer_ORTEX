# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 14:23:23 2022

@author: Usuario
"""

import pandas as pd
import numpy as np

df = pd.read_csv("2017.csv")
#list(df.columns.values)

#Quesiton 2
sumed_value = df.groupby(["currency"]).sum().sort_values(["value"], ascending=False).reset_index()
top3 = sumed_value[0:3]

print("\n")
print("Top 3 currencies by value traded:")
print(f" #1 {top3.currency[0]} with ${'{:,.2f}'.format(round(top3.value[0]))} in traded value.")
print(f" #2 {top3.currency[1]} with ${'{:,.2f}'.format(round(top3.value[1]))} in traded value.")
print(f" #3 {top3.currency[2]} with ${'{:,.2f}'.format(round(top3.value[2]))} in traded value.")

#Question 3
inrange = df[(df['inputdate'] - df['tradedate'] > 7*2)]

print("\n")
print(f"The total number of transactions with Input date > 2 weeks from Trade date is {len(inrange)}.")