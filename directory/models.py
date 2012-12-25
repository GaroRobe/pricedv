from django.db import models
from django.forms import ModelForm
import operator
import uuid

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
        
        
#class SubnodeManager(models.Manager):
 #   def get_query_set(self):
 #       return super(SubnodeManager, self).get_query_set().filter(parent_id = self)
    

class Node(models.Model):
    title = models.CharField(max_length = 255)
    slug = models.CharField(max_length = 100)
    breadcrumb = models.CharField(max_length = 160)
    parent_id = models.ForeignKey('self', db_column='parent_id')
    weight = models.IntegerField(default=1)
    lft = models.IntegerField()
    rgt = models.IntegerField()
    
    def offersNum(self):
        if self.parent_id.id == 1:
            return Offer.objects.filter(node_id__in = Node.objects.filter(parent_id = self)).count()
        else:
            return Offer.objects.filter(node_id = self).count()
    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'nodes'
        
        
class UUIDField(models.CharField) :
    value = ''
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64 )
        kwargs['blank'] = True
        models.CharField.__init__(self, *args, **kwargs)
    
    def pre_save(self, model_instance, add):
        if add :
            value = str(uuid.uuid4())
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(models.CharField, self).pre_save(model_instance, add)
            
    def __getitem__(self, *args, **kwargs):
        return self.value
        
class FirmHalfUUIDField(models.CharField) :
    value = ''
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 64 )
        kwargs['blank'] = True
        models.CharField.__init__(self, *args, **kwargs)
    
    def pre_save(self, model_instance, add):
        if add :
            value = model_instance.global_id[0:13]
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(models.CharField, self).pre_save(model_instance, add)
            
    def __getitem__(self, *args, **kwargs):
        return self.value

class Firm(models.Model):
    town_id = models.ForeignKey(Town, db_column='town_id')
    title = models.CharField(max_length = 255)
    short_title = models.CharField(max_length = 160, null=True, blank=True, default=None)
    global_id = UUIDField(editable = False, unique = True)
    slug =  FirmHalfUUIDField(max_length = 255)                         #KIND OF UGLY, maybe refactor later
    slug_name = models.CharField(max_length = 255, unique = True)
    firm_nodes = models.ManyToManyField(Node, db_table='firms_nodes')
    def __unicode__(self):
        return self.title
        

    class Meta:
        db_table = 'firms'
        
class FirmForm(ModelForm):
    class Meta:
        model = Firm
        exclude = {'global_id', 'slug',}

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
        return self.node_id.title + u' - ' + self.firm_id.title

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
    desc = models.CharField(max_length=300)
    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'offers'