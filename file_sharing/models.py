# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from mptt.fields import TreeForeignKey
from django.db.models.signals import post_save
from mptt.models import MPTTModel

DEFAULT_FOLDERS = ['Music', 'Picture', 'Images', 'Documents']

class Folders(MPTTModel):    
    name = models.CharField(max_length=250)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    user = models.ForeignKey(User)
    
    @models.permalink
    def get_absolute_url(self):
        return ('home', [self.id])
    
    @classmethod
    def create_user_folders(cls, sender, instance, *args, **kwargs):
        user = User.objects.get(username=instance)
        if kwargs['created']:
            root_folder = Folders(name='root',user=user)
            root_folder.save()
            for folder in DEFAULT_FOLDERS:
                f = Folders(name=folder, user=user, parent=root_folder)
                f.save()
        

class File(models.Model):
    name = models.CharField(max_length=500)
    target = models.CharField(max_length=1000)
    file_type = models.CharField(max_length=250)
    size = models.IntegerField()
    
    folder = models.ForeignKey(Folders)


post_save.connect(Folders.create_user_folders, sender=User, dispatch_uid="create_user_folders")

