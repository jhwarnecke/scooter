from django.shortcuts import render
import numpy as np
import pandas as pd

# Create your views here.

# reading excel sheet, index_col = none so we can get indices instead of names as headers
# that's why we will always start with row '1' and not '0'
# for columns we will start with '2' because there the values (variables) start
df = pd.read_excel(r'scooter.xlsx', index_col=None, header=None)
# get shape of excel sheet (to know number of iterations)
x = df.shape

def index(request):
    # get Names of Models and Names of Cost-Structure-Elements into two Lists
    mylist = []
    myseclist = []
    for a in range(0, x[1]):
        mylist.append((df[0][a + 1])+" "+(df[1][a + 1]))

    # for b in range(2, x[2]):
    #     myseclist.append(df[b][0])
    # print(myseclist)

    dx = df.to_html(header=False, index=False)

    return render(request, "edittable/edittable.html", {"mylist": mylist, "myseclist": myseclist, "metable":dx})


def editfunc(request):
    return render(request, "test.html")