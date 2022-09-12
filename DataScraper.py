import sys
import getopt
import datetime
from pytrends.request import TrendReq
import pandas as pd

# params 
# --frequency D,W,M,Y
# --filename trend.csv (optional)
# --startdate 2016-07-06 (optional)
# --keyword football (optional)

def getParams():
    """Get parameters on startup
    :return: Dictionary of Params
    """
    try:
        optlist,args = getopt.gnu_getopt(sys.argv,"",["startdate=","filename=","frequency=","keyword="])
    except getopt.GetoptError as err:
        print(err)
        exit(2)
    
    #convert list of tuple to dictionary
    return dict((o, a) for o, a in optlist)

if __name__ == "__main__":
    params = getParams()
    filename = "data.csv"
    startDate = "2020-01-01".date()
    endDate = datetime.datetime.now()
    keyword = "bitcoin"
    frequency = 'D'

    if "--filename" in params:
        filename = params["--filename"]
    
    if "--startDate" in params:
        startDate = params["--startDate"]

    if "--keyword" in params:
        keyword = params["--keyword"]

    if "--frequency" in params:
        frequency = params["--frequency"]
    
    # initialize a new Google Trends Request Object
    # tz 360 US CST Timezone offset
    pt = TrendReq(hl="en-US", tz=360)

    # set the keyword & timeframe
    pt.build_payload([keyword], timeframe= f'{startDate.strftime("%Y-%m-%d")} {endDate.strftime("%Y-%m-%d")}')
    data = pt.interest_over_time()

    # convert index column to number so date can be grouped
    data =  data.reset_index()
    data = data.groupby([pd.Grouper(key='date', freq=frequency)])[keyword].sum()
    data.to_csv(filename)


