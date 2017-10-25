import pandas as pd
import numpy as np
import json

# from django.shortcuts import render
from django.http import JsonResponse
from django.utils.dateformat import DateFormat
from fbprophet import Prophet
from .models import Skill, Country, DemandResult, DemandForecast


def fbProphet(request):
    # create new DemandForcast
    demFot = DemandForecast()

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
                demRes = demResModel.order_by('ds') \
                    .values(
                    'country_code',
                    'skill_id',
                    'query_id',
                    'execution_date',
                    'period_days',
                    'day',
                    'week',
                    'year',
                    'ds',
                    'y'
                )
                # Pandas using DataFrame to get list QuerySet from database
                # ls = {
                #     'ds': [],
                #     'y': []
                # }
                # for de in demRes:
                #     ls['ds'].append(DateFormat(de.ds).format('Y-m-d'))
                #     ls['y'].append(de.y)

                df = pd.DataFrame(data=list(demRes))
                df['ds'] = df['jobs_since']
                df['y'] = np.log(df['result'])
                df['cap'] = 8.5
                df.head()

                # Create Prophet
                model = Prophet()
                model.fit(df)
                #
                # print(df)
                # # future
                # future = model.make_future_dataframe(periods=365)
                # future.tail()
                #
                # # forecast
                # forecast = model.predict(future)
                # forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
                #
                # model.plot(forecast)
                # model.plot_components(forecast)
                # print(model.plot_components(forecast).show())

    return JsonResponse(json.dumps(skills), safe=False)
