import sys
import getopt
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule
from pytrends.request import TrendReq
import pandas as pd

def get_params():
    """Get parameters on startup
    :return: Dictionary of Params
    """
    try:
        optlist,args = getopt.gnu_getopt(sys.argv,"",["startDate=","filename=","frequency=","keyword=","endDate"])
    except getopt.GetoptError as err:
        print(err)
        exit(2)
    
    #convert list of tuple to dictionary
    return dict((o, a) for o, a in optlist)

def get_trends(startDate, endDate, keyword):
    """Collect google trends keyword data
    :return: Panda Dataframe of trend data
    """
    # init Google Trends Request Object
    # tz 360 US CST Timezone offset
    pt = TrendReq(hl="en-US", tz=360)

    # break request into one per year
    # pytrends does not return full dataset for date ranges greater then 8 months
    data = None
    for date in rrule.rrule(rrule.MONTHLY, interval=8, dtstart=startDate, until=endDate):
        rangeEndDate = date + relativedelta(months=8) - relativedelta(days=1)

        # prevent data past end date
        if endDate < rangeEndDate: 
            rangeEndDate = endDate 
        
        # set the keyword & timeframe
        pt.build_payload([keyword], timeframe= f'{date.strftime("%Y-%m-%d")} {rangeEndDate.strftime("%Y-%m-%d")}')
        yearData = pt.interest_over_time()
        data = pd.concat([yearData,data]) if data is not None else yearData
    return data

def clean_data(data, frequency):
    """Clear date index and group by frequency
    :return: Panda Dataframe of cleaned data
    """
    # convert index column to number so date can be grouped
    data = data.reset_index()
    return data.groupby([pd.Grouper(key='date', freq=frequency)])[keyword].sum()

if __name__ == "__main__":
    params = get_params()

    # parameter defaults
    filename = "data.csv"
    startDate = datetime.now() - relativedelta(months=1)
    endDate = datetime.now()
    keyword = "bitcoin"
    frequency = 'D'

    if "--filename" in params:
        filename = params["--filename"]
    
    if "--startDate" in params:
        startDate = datetime.strptime(params["--startDate"], '%Y-%m-%d') 
    
    if "--endDate" in params:
        endDate = datetime.strptime(params["--endDate"], '%Y-%m-%d') 

    if "--keyword" in params:
        keyword = params["--keyword"]

    if "--frequency" in params:
        frequency = params["--frequency"]

    #prevent frequencies less then day
    if frequency not in ["D", "W", "M", "Y"]:
        raise Exception(f'Invalid frequency: {frequency}')

    data = get_trends(startDate, endDate, keyword)
    data = clean_data(data, frequency)
    data.to_csv(filename)
    




