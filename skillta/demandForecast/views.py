import pandas as pd
import numpy as np

# from django.shortcuts import render
from django.http import HttpResponse
from skillta.demandForecast.models import DemandResult, DemandForecast

from fbprophet import Prophet

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the demand forecast index.")

def fbProphet():
    # Get data from database
    demandResults = DemandResult.objects.all()
    #print(demandResults)
    # demandForecast = DemandForecast()

    df = pd.read_sql_table('demand_forecast')
    df['y'] = np.log(df['y'])
    df['cap'] = 8.5

    m = Prophet()
    m.fit(df)

    # future
    future = m.make_future_dataframe(periods=365)
    future.tail()

    # forecast
    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

    m.plot(forecast)
    m.plot_components(forecast)
    return HttpResponse(m.plot_components(forecast))
