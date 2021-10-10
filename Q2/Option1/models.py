from __future__ import unicode_literals

from django.db import models
from django.db.models import constraints, fields

#database schema and model
class ShortUrl(models.Model):
    id = models.AutoField(primary_key=True)   #auto_incrament id, use it as base id to generate unqiue shorturl.
    short_url = models.CharField(max_length=255) #record short_url as base-62 number
    ori_url = models.TextField() #record orginal web site url
    createdtime = models.DateTimeField(auto_now_add=True) #created time
    isdeleted = models.BooleanField(default=False) #delete signal

    class Meta:
        db_table = 't_shorturl'