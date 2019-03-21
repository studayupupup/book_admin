from django.db import models

class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, null=False, unique=True)

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64,unique=True,null=False)
    # 通过orm建立外键 在python里取出来会是一个对象，转化到数据库会是一个字段
    publisher_id = models.ForeignKey(to="Publisher",on_delete=models.DO_NOTHING)
