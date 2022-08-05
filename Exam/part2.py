# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 14:23:23 2022

@author: Usuario
"""

import pandas as pd
import numpy as np

df = pd.read_csv("2017.csv")
#list(df.columns.values)

#Quesiton 1
stats = pd.DataFrame()
for i in df.source.unique():
    
    country_df = df[df["source"] == i].transactionType.value_counts()
    stats.loc[i, 'Buy'] = country_df.Buy
    stats.loc[i, 'Sell'] = country_df.Sell
    
    stats["ratio"] = stats["Buy"]/stats["Sell"]
    
    stats.loc[i, "shares"] = df[df["source"] == i].shares.sum() 
    

    
stats["weights"] = stats['shares'].transform(lambda x: (x/x.sum()) * 100)
#print(stats["weights"].sum())

stats["weighted_ratio"] = stats["ratio"] * stats["weights"]
    
stats.sort_values(["weighted_ratio"], ascending=False).reset_index()


print("\n")
print("Question 1")
print("The top 3 sources by weighted Buy & Sell ratio are:")
print(f" #1 {stats.index[0]}.")
print(f" #2 {stats.index[1]}.")
print(f" #3 {stats.index[2]}.")


#Quesiton 2
sumed_value = df.groupby(["currency"]).sum().sort_values(["value"], ascending=False).reset_index()
top3 = sumed_value[0:3]

print("\n")
print("Question 2")
print("Top 3 currencies by value traded:")
print(f" #1 {top3.currency[0]} with ${'{:,.2f}'.format(round(top3.value[0]))} in traded value.")
print(f" #2 {top3.currency[1]} with ${'{:,.2f}'.format(round(top3.value[1]))} in traded value.")
print(f" #3 {top3.currency[2]} with ${'{:,.2f}'.format(round(top3.value[2]))} in traded value.")

#Question 3
inrange = df[(df['inputdate'] - df['tradedate'] > 7*2)]

print("\n")
print("Question 3")
print(f"The total number of transactions with Input date > 2 weeks from Trade date is {len(inrange)}.")