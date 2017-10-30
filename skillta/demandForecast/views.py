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
    for skill in skills:
        for country in countries:
            # Get data of demand results
            # For each skill/country combination, run the full history of values
            demResModel = DemandResult.objects \
                .filter(skill_id=skill.skill_id) \
                .filter(country_code=country.country_code)
            if demResModel.count() > 0:
                demRes = demResModel.order_by('year').order_by('week')
                try:
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
                    df.head(52)
                    # Create Prophet
                    model = Prophet()
                    model.fit(df)
                    # future
                    future = model.make_future_dataframe(periods=365, freq='D', include_history=False)
                    future.tail()
                    # forecast
                    forecast = model.predict(future)
                    data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
                    # Calculate execution_date
                    today = datetime.date.today()
                    # Calculator
                    model_instances = [DemandForecast(
                        result_id=random.seed(a='int'),
                        country_code=country.country_code,
                        skill_id=skill.skill_id,
                        execution_date=r[1],
                        day=r[1].weekday(),
                        week=int(r[1].strftime("%W")),
                        year=int(r[1].strftime("%Y")),
                        result=r[2]
                    ) for r in data.reset_index().values]
                
                    # Create DemandForecast
                    DemandForecast.objects.bulk_create(model_instances)
                    # Save plot to picture
                    model.plot(forecast).savefig('storage/images/demand_forecast_' + str(country.country_code) + '_' + str(skill.skill_id) + '.png')
                # model.plot_components(forecast)
                # model.plot_components(forecast).show()
                # model.plot_components(forecast).savefig('demand_forecast_components.png')
                except Exception as e:
                    print(str(e))
        # res = serializers.serialize("json", data.reset_index().values)
    return HttpResponse("Done")
    # return HttpResponse(res, content_type="text/application-json")