from abc import ABC
from os import name
from django.shortcuts import render
import numpy as np
import pandas as pd
from pandas.io.formats import style



# reading excel sheet, index_col = none so we can get indices instead of names as headers
# that's why we will always start with row '1' and not '0'
# for columns we will start with '2' because there the values (variables) start
df = pd.read_excel(r'scooter.xlsx', index_col=None, header=None)
# get shape of excel sheet (to know number of iterations)
x = df.shape

# test test test


def index(request):
    return render(request, "input.html")


def calculation(request):

    #time_of_use = sum(time_dict.values())
    time_per_use = int(request.POST['usetime'])
    uses_per_day = int(request.POST['usesday'])
    days = int(request.POST['days'])
    uses = days * uses_per_day
    total_time = time_per_use * uses
 

    # new df to save costs and name in
    mydf = pd.DataFrame()
   
    # iterations for all the models, save costs and name in df
    for i in range(0, x[1]-1):
        total_costs = tester(i, days, uses, total_time)
        mytempname = ((df[0][i + 2])+" "+(df[1][i + 2]))
        mytempdf = pd.DataFrame({'Name': [mytempname], 'Kosten': [total_costs]})
        mydf = mydf.append(mytempdf, ignore_index=True)

    
    # SORTIEREN DER Tabelle NACH KOSTEN
    mydf = mydf.sort_values(by=['Kosten'])
    mydf = mydf.reset_index(drop=True)
   
    # Kosten und Name des günstigsten Modells in Variablen speichern
    minval = mydf.at[0,'Kosten']
    anbieter = mydf.at[0,'Name']
    
    # convert df to html table
    myhtmldf = mydf.to_html()


    return render(request, "result.html", { "costs": minval, "name": anbieter,
                            "mytable": myhtmldf})

# definition of the cost function
# missing variables for (Beschränkung Zeit, Preis nach 45)
def tester(j, days, uses, total_time):
    grund = df[2][j+1] * uses
    preispmin = df[3][j+1] * total_time
    preisppak = df[4][j+1]
    preispmon = df[5][j+1]
    preisptag = df[6][j+1] * days
    konti = kontingent(j+1, total_time)
    costs = grund + preispmin + preisptag + preisppak + preispmon + konti
    return costs

# definition für tester von kontingent
def kontingent(j, total_time):
    if df[7][j] != 0 and df[7][j] < total_time:
        konti = (total_time - df[7][j]) * df[8][j]
    else:
        konti = 0
    return konti
