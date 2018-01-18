# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import datetime


def checkYear(year):
    #checks that the year inputted is correct for the datetime format.
    #does not check for sane dates.
    
    try:
        newdate = datetime.datetime(year)
        correctDate = True
    except ValueError:
        correctDate=False
    
    return correctDate
    
    