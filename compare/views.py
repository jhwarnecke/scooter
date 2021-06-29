from abc import ABC
from os import error, name
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



def index(request):
    dx = df.to_html(header=False, index=False)
    return render(request, "input.html", {"metable":dx})


def calculation(request):
    global monday
    monday = False
    global tuesday
    tuesday = False
    global wednesday
    wednesday = False
    global thursday
    thursday = False
    global friday
    friday = False
    global saturday
    saturday = False
    global sunday
    sunday = False
    global monday2
    monday2 = False
    global tuesday2
    tuesday2 = False
    global wednesday2
    wednesday2 = False
    global thursday2
    thursday2 = False
    global friday2
    friday2 = False
    global saturday2
    saturday2 = False
    global sunday2
    sunday2 = False

    #time_of_use = sum(time_dict.values())
    time_per_use = int(request.POST['usetime'])
    uses_per_day = int(request.POST['usesday'])

    day = request.POST.getlist("day")
    day2 = request.POST.getlist("day2")

    if len(day) == 0:
        return(render(request, "error.html"))


    for z in range(0, len(day)):
        if day[z] == "monday":
            monday = True
        if day[z] == "tuesday":
            tuesday = True
        if day[z] == "wednesday":
            wednesday = True
        if day[z] == "thursday":
            thursday = True
        if day[z] == "friday":
            friday = True
        if day[z] == "saturday":
            saturday = True
        if day[z] == "sunday":
            sunday = True

    if day2 is not None:
        for z in range(0, len(day2)):
            if day2[z] == "monday":
                monday2 = True
            if day2[z] == "tuesday":
                tuesday2 = True
            if day2[z] == "wednesday":
                wednesday2 = True
            if day2[z] == "thursday":
                thursday2 = True
            if day2[z] == "friday":
                friday2 = True
            if day2[z] == "saturday":
                saturday2 = True
            if day2[z] == "sunday":
                sunday2 = True

    
    
    numdays = len(day)
    numdays2 = len(day2)


    uses = numdays * uses_per_day
    total_time = time_per_use * uses

    time_per_use2 = int(request.POST['usetime2'])
    uses_per_day2 = int(request.POST['usesday2'])
    uses2 = numdays2 * uses_per_day2
    total_time2 = time_per_use2 * uses2

    samedays = 0
    for z in range(0, len(day)):
        for y in range(0, len(day2)):
            if day[z] == day2[y]:
                samedays += 1



    days_sum = numdays + numdays2 - samedays
    uses_sum = uses + uses2
    total_time_sum = total_time + total_time2
    
 

    # new df to save costs and name in
    mydf = pd.DataFrame()

    # iterations for all the models, save costs and name in df
    for i in range(0, x[1]-1):
        total_costs = round(normal(i, days_sum, uses_sum, total_time_sum), 2)
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
    myhtmldf = mydf.to_html(index = False)
    
    # Falls 2 Tarife mit gleichen Kosten beide Ausgeben
    if mydf.at[0,'Kosten'] == mydf.at[1,'Kosten']:
        anbieter2 = mydf.at[1,'Name']
        return render(request, "result2.html", { "costs": minval, "name": anbieter,
                            "name2": anbieter2, "mytable": myhtmldf})


    return render(request, "result.html", { "costs": minval, "name": anbieter,
                            "mytable": myhtmldf})

# definition of the cost function
# missing variables for (Beschränkung Zeit, Preis nach 45)
def normal(j, days, uses, total_time):
    grund = df[2][j+1] * uses
    preispmin = df[3][j+1] * total_time
    preisppak = df[4][j+1]
    preispmon = df[5][j+1]
    preisptag = df[6][j+1] * days
    mylist = kontingent(j+1, total_time)
    konti = mylist[0]
    anteil_rest_konsten_konti = mylist[1]
    konti_plus = konti - anteil_rest_konsten_konti
    costs = grund + preispmin + preisptag + preisppak + preispmon + konti_plus
    return costs

# def für normal von kontingent
# Der Montag wird als Buchungszeitpunkt für den Konti-Tarif angesehen (sollte aber keinen großen Einfluss haben)
def kontingent(j, total_time):
    if df[7][j] != 0 and df[7][j] < total_time:
        konti = 0
        loop = 1
        new_total_time = total_time
        while loop == 1:
            konti = konti + df[4][j]
            new_total_time = new_total_time - df[7][j]
            if df[7][j] < new_total_time:
                loop = 1
            else:
                loop = 0
                rest =  df[7][j] - new_total_time
                anteil_rest = rest / total_time
                anteil_rest_kosten = anteil_rest * df[4][j]
                mylist = [konti, anteil_rest_kosten]

    else:
        konti = 0
        anteil_rest_kosten = 0
        mylist = [konti, anteil_rest_kosten]

    return mylist
