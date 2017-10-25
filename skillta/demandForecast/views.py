import pandas as pd
import numpy as np

# from django.shortcuts import render
from django.http import JsonResponse
from .models import Skill, Country, DemandResult, DemandForecast

from fbprophet import Prophet


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
                demRes = demResModel.order_by('ds').values(
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
                df = pd.DataFrame(list(demRes))
                df['y'] = np.log(df['y'])
                df['cap'] = 8.5
                df.head()
                print(df)
                # Create Prophet
                # m = Prophet()
                # m.fit(df)
                #
                # # future
                # future = m.make_future_dataframe(periods=365)
                # future.tail()
                #
                # # forecast
                # forecast = m.predict(future)
                # forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
                #
                # m.plot(forecast)
                # m.plot_components(forecast)
                # print(m.plot_components(forecast))

    return JsonResponse(list(skills), safe=False)
