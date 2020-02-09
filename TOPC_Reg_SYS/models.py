from django.db import models

# Create your models here.
class ALLStudents(models.Model):
    sID = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    regby = models.CharField(max_length=100)
    regtiem = models.DateTimeField()
    status = models.CharField(max_length=100,default="Not_Registered")

    class Mate:
        db_table = "all_students"



class RegStudents(models.Model):
    sID = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    pc_no = models.CharField(max_length=100)
    rank = models.IntegerField(default=0)
    solve = models.IntegerField(default=99)
    penalty = models.IntegerField(default=99)
    advance_camp = models.CharField(max_length=100,default="Pending")
    regby = models.CharField(max_length=100)
    regtiem = models.DateTimeField()
    reg_status = models.CharField(max_length=100,default="Not_Registered")

    class Mate:
        db_table = "reg_students"