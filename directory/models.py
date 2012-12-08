from django.db import models

# Create your models here.

class Town(models.Model):
	title = models.CharField(max_length = 100)
	slug = models.CharField(max_length = 100)
	status_id = models.BooleanField(default=True)
	firms_count = models.IntegerField()
	offers_count = models.IntegerField()
	def __unicode__(self):
		return self.title

	class Meta:
		db_table = 'towns'

class Node(models.Model):
	title = models.CharField(max_length = 255)
	slug = models.CharField(max_length = 100)
	breadcrumb = models.CharField(max_length = 160)
	parent_id = models.ForeignKey('self', db_column='parent_id')
	weight = models.IntegerField(default=1)
	lft = models.IntegerField()
	rgt = models.IntegerField()
	def __unicode__(self):
		return self.title

	class Meta:
		db_table = 'nodes'

class Firm(models.Model):
	town_id = models.ForeignKey(Town, db_column='town_id')
	title = models.CharField(max_length = 255)
	short_title = models.CharField(max_length = 160, null=True, blank=True, default=None)
	slug =  models.CharField(max_length = 300)
	global_id = models.CharField(max_length = 100)
	slug_name = models.CharField(max_length = 300)
	firm_nodes = models.ManyToManyField(Node, through='FirmNodes')
	def __unicode__(self):
		return self.title

	class Meta:
		db_table = 'firms'

class Text(models.Model):
	firm_id = models.ForeignKey(Firm, db_column='firm_id')
	message = models.CharField(max_length = 100)
	def __unicode__(self):
		return self.message

	class Meta:
		db_table = 'texts'

class FirmNodes(models.Model):
	node_id = models.ForeignKey(Node, db_column='node_id')
	firm_id = models.ForeignKey(Firm, db_column='firm_id')
	def __unicode__(self):
		return str(self.node_id) + ' - ' + str(self.firm_id)

	class Meta:
		db_table = 'firms_nodes'

class Chunk(models.Model):
	chunk_type_id = models.IntegerField()
	firm_id = models.ForeignKey(Firm, db_column='firm_id')
	value = models.CharField(max_length = 250)
	comment = models.CharField(max_length = 250, null=True, blank=True, default=None)
	id_address = models.IntegerField(null=True, blank=True, default=None)
	parent_id_address = models.ForeignKey('self', null=True, blank=True, default=None, db_column='parent_id_address')
	def __unicode__(self):
		return self.value

	class Meta:
		db_table = 'chunks'

class Offer(models.Model):
	title = models.CharField(max_length = 255)
	price = models.CharField(max_length = 160)
	bold = models.BooleanField(default=True)
	town_id = models.ForeignKey(Town, db_column='town_id')
	firm_id = models.ForeignKey(Firm, db_column='firm_id')
	pic_file_name = models.CharField(max_length = 100)
	pic_note = models.CharField(max_length = 600)
	node_id = models.ForeignKey(Node, db_column='node_id')
	node_lft = models.IntegerField()
	def __unicode__(self):
		return self.title

	class Meta:
		db_table = 'offers'