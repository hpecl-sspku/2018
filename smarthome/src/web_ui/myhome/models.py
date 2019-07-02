from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Nodedata(models.Model):
	time = models.TextField(max_length = 64)
	localshortaddr = models.TextField(max_length = 64)
	gateway_id = models.TextField(max_length = 64)
	slaveId = models.TextField(max_length = 64)
	humidity = models.IntegerField(default = 0)
	temperature = models.IntegerField(default = 0)
	light = models.IntegerField(default = 0)
	noise = models.IntegerField(default = 0)
	co2_simulation = models.IntegerField(default = 0)
	co2_binarization  = models.IntegerField(default = 0)

	def __unicode__(self):
		return '%s' % (self.catname)

	def toJSON(self):
		import json
		return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

class Commands(models.Model):
	intent = models.TextField(max_length = 64)
	slots  = models.TextField(max_length = 64)


