import pandas as pd
import numpy as np
import datetime, random, json

# from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.utils.dateformat import DateFormat
from fbprophet import Prophet
from .models import Skill, Country, DemandResult, DemandForecast


def fbProphet(request):
    # Get data of skill.
    skills = Skill.objects.all()
    # Get data of country.
    countries = Country.objects.all()
    # for skill in skills:
    #     for country in countries:
            # Get data of demand results
            # For each skill/country combination, run the full history of values
    demResModel = DemandResult.objects \
        .filter(skill_id=3) \
        .filter(country_code='ca')
    if demResModel.count() > 0:
        demRes = demResModel.order_by('year').order_by('week')  # [:100]

        # try:
        dat = {
            'country_code': [],
            'skill_id': [],
            'ds': [],
            'y': [],
            'year': [],
            'week': [],
            'day': [],
        }
        for o in demRes:
            dat['country_code'].append(o.country_code)
            dat['skill_id'].append(o.skill_id)
            dat['y'].append(o.y)
            dat['year'].append(str(o.year))
            dat['week'].append(str(o.week))
            dat['day'].append(str(o.day))
            dat['ds'].append(
                datetime.datetime.strptime(str(o.year) + '-' + str(o.week), '%Y-%W')
            )
        # Create DataFrame
        df = pd.DataFrame(data=dat)
        df['y'] = np.log(df['y'])
        df['cap'] = 8.0
        df.head()
        # Create Prophet
        model = Prophet()
        model.fit(df)
        # future
        future = model.make_future_dataframe(periods=365, freq='D', include_history=False)
        future.tail()
        forecast = model.predict(future)
        data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

                # forecast
                # forecast = model.predict(future)
                # data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
                # Calculate execution_date
        today = datetime.date.today()
                # Calculator
        model_instances = [DemandForecast(
            result_id=random.seed(a='int'),
            country_code='ca',
            skill_id=3,
            execution_date=list(dat['ds'])[0],
            day=today.weekday(),
            week=int(today.strftime("%W")),
            year=int(today.strftime("%Y")),
            result=r
        ) for r in data['yhat']]
        print(model_instances)
                # Create DemandForecast
        # DemandForecast.objects.bulk_create(model_instances)
                # Save plot to picture
                # model.plot(forecast).savefig('storage/images/demand_forecast_' + str(country.country_code) + '_' + str(skill.skill_id) + '.png')
                #     # model.plot_components(forecast)
                #     # model.plot_components(forecast).show()
                #     # model.plot_components(forecast).savefig('demand_forecast_components.png')
                #     # except Exception as e:
                #     #     print(str(e))

    # res = serializers.serialize("json", skills)
    return HttpResponse("Done")
    # return HttpResponse(res, content_type="text/application-json")
