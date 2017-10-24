from django.db import models


# DemandForecast Model.
class DemandForecast(models.Model):
    result_id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=20)
    skill_id = models.BigIntegerField()
    query_id = models.BigIntegerField()
    execution_date = models.DateTimeField()
    jobs_since = models.DateTimeField()
    period_days = models.IntegerField()
    day = models.IntegerField()
    week = models.IntegerField()
    year = models.IntegerField()
    result = models.IntegerField()

# DemandResult Model.
class DemandResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=20)
    skill_id = models.BigIntegerField()
    query_id = models.BigIntegerField()
    execution_date = models.DateTimeField()
    jobs_since = models.DateTimeField()
    period_days = models.IntegerField()
    day = models.IntegerField()
    week = models.IntegerField()
    year = models.IntegerField()
    result = models.IntegerField()
