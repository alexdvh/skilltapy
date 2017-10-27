import random

from django.db import models


# Skill Model.
class Skill(models.Model):
    class Meta:
        db_table = 'skill'

    skill_id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=255)
    level1 = models.CharField(max_length=255)
    level2 = models.CharField(max_length=255)
    level3 = models.CharField(max_length=255)
    level4 = models.CharField(max_length=255)
    level5 = models.CharField(max_length=255)
    level6 = models.CharField(max_length=255)
    excluded = models.IntegerField()
    hierarchical_name = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    level = models.IntegerField()
    parent = models.IntegerField()
    user_hide = models.IntegerField()
    # order = models.IntegerField()


# Country Model.
class Country(models.Model):
    class Meta:
        db_table = 'country'

    country_code = models.CharField(primary_key=True, max_length=20)
    country_name = models.CharField(max_length=255)
    active_flag = models.CharField(max_length=255)
    image_flag = models.CharField(max_length=255)


# DemandForecast Model.
class DemandForecast(models.Model):
    class Meta:
        db_table = 'demand_forecast'

    result_id = models.CharField(primary_key=True, max_length=20, db_column='result_id')
    country_code = models.CharField(max_length=20, db_column='country_code')
    skill_id = models.BigIntegerField(db_column='skill_id')
    query_id = models.BigIntegerField(db_column='query_id')
    execution_date = models.DateTimeField(db_column='execution_date')
    jobs_since = models.DateTimeField(db_column='jobs_since')
    period_days = models.IntegerField(db_column='period_days')
    day = models.IntegerField(db_column='day')
    week = models.IntegerField(db_column='week')
    year = models.IntegerField(db_column='year')
    result = models.FloatField(db_column='result')

    def save(self):
        if not self.result_id:
            self.result_id = random.seed(a='int')
            super(DemandForecast, self).save()


# DemandResult Model.
class DemandResult(models.Model):
    class Meta:
        db_table = 'demand_result'

    result_id = models.AutoField(primary_key=True, db_column='result_id')
    country_code = models.CharField(max_length=20, db_column='country_code')
    skill_id = models.BigIntegerField(db_column='skill_id')
    query_id = models.BigIntegerField(db_column='query_id')
    execution_date = models.DateTimeField(db_column='execution_date')
    jobs_since = models.DateTimeField(db_column='jobs_since')
    period_days = models.IntegerField(db_column='period_days')
    day = models.IntegerField(db_column='day')
    week = models.IntegerField(db_column='week')
    year = models.IntegerField(db_column='year')
    y = models.IntegerField(default=0, db_column='result')
