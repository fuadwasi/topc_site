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
    sec_email = models.CharField(max_length=100, default="none")
    phone = models.CharField(max_length=100)
    sec_phone = models.CharField(max_length=100, default="none")

    status = models.CharField(max_length=100, default="Not_Registered")

    class Mate:
        db_table = "all_students"


class RegStudents(models.Model):
    token = models.IntegerField(default=99999)
    sID = models.CharField(max_length=30)
    t_shirt = models.CharField(max_length=100, default="none")
    room = models.CharField(max_length=100)
    pc_no = models.CharField(max_length=100)
    userid = models.CharField(max_length=100, default="none")
    password = models.CharField(max_length=100, default="none")
    rank = models.IntegerField(default=0)
    solve = models.IntegerField(default=99)
    penalty = models.IntegerField(default=99999)
    advance_camp = models.CharField(max_length=100, default="Pending")
    viva_date = models.CharField(max_length=100, default="Pending")
    regby = models.CharField(max_length=100)
    regtiem = models.DateTimeField(auto_now_add=True)
    basic_info = models.OneToOneField(ALLStudents, on_delete=models.CASCADE)

    def pr_data(self):
        return self.basic_info.name+' '+self.sID

    class Mate:
        db_table = "reg_students"




class Req_queuey(models.Model):
    token = models.IntegerField(default=99999)
    req_info = models.OneToOneField(RegStudents, on_delete=models.CASCADE)
    req_by=models.CharField(max_length=100, default="none")
    req_time = models.DateTimeField(auto_now_add=True)
    class Mate:
        db_table = "req_queue"





class Teacher_Info(models.Model):
    tID = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    shift = models.CharField(max_length=100, default="none")
    email = models.CharField(max_length=100, default="none")
    phone = models.CharField(max_length=100, default="none")

    class Mate:
        db_table = "teacher_info"

class Cancel_log(models.Model):

    token = models.IntegerField(default=99999)
    sID = models.CharField(max_length=30)
    email = models.CharField(max_length=100, default="none")
    phone = models.CharField(max_length=100, default="none")
    cancel_by = models.CharField(max_length=100, default="none")
    cancel_time = models.DateTimeField(auto_now_add=True)
    req_by = models.CharField(max_length=100, default="none")
    req_time = models.DateTimeField()


    class Mate:
        db_table = "cancel_log"

class Room_data(models.Model):
    roon_no = models.CharField(max_length=30)
    token_starts = models.IntegerField(default=99999)
    token_ends = models.IntegerField(default=99999)
    total_pcs = models.IntegerField(default=99999)
    generated_by = models.CharField(max_length=100, default="none")
    M_count = models.IntegerField(default=0)
    L_count = models.IntegerField(default=0)
    XL_count = models.IntegerField(default=0)
    XXL_count = models.IntegerField(default=0)
    XXXL_count = models.IntegerField(default=0)


    class Mate:
        db_table = "room_data"




