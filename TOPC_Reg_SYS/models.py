from django.db import models


# Create your models here.
class ALLStudents(models.Model):
    token = models.IntegerField(default=99999)
    sID = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    gender= models.CharField(max_length=100, default="none")
    campus = models.CharField(max_length=100)
    shift = models.CharField(max_length=100, default="none")
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    t_shirt = models.CharField(max_length=100, default="none")
    rank = models.IntegerField(default=0)
    solve = models.IntegerField(default=99)
    penalty = models.IntegerField(default=99999)
    regby = models.CharField(max_length=100)
    regtiem = models.DateTimeField()
    status = models.CharField(max_length=100, default="Not_Registered")

    class Mate:
        db_table = "all_students"


class RegStudents(models.Model):
    token = models.IntegerField(default=99999)
    sID = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    shift = models.CharField(max_length=100, default="Pending")
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    gender= models.CharField(max_length=100, default="none")
    t_shirt = models.CharField(max_length=100, default="none")
    room = models.CharField(max_length=100)
    pc_no = models.CharField(max_length=100)
    userid = models.CharField(max_length=100, default="none")
    password = models.CharField(max_length=100, default="none")
    rank = models.IntegerField(default=0)
    solve = models.IntegerField(default=99)
    penalty = models.IntegerField(default=99999)
    advance_camp = models.CharField(max_length=100, default="Pending")
    regby = models.CharField(max_length=100)
    regtiem = models.DateTimeField()
    reg_status = models.CharField(max_length=100, default="Not_Registered")

    class Mate:
        db_table = "reg_students"
