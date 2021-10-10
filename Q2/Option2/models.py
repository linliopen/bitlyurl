from __future__ import unicode_literals

from django.db import models
from django.db.models import constraints, fields

#database schema and model
class ShortUrl(models.Model):
    id = models.AutoField(primary_key=True) #auto_incrament id
    short_url = models.CharField(max_length=255) #record short_url as base-62 number
    pool = models.CharField(max_length=20) #record each redis cluster identity
    ori_url = models.TextField() #record orginal web site url
    createdtime = models.DateTimeField(auto_now_add=True) #created time
    isdeleted = models.BooleanField(default=False) #delete signal

    class Meta:
        db_table = 't_shorturl'