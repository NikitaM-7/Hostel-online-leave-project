from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.user.username

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.user.username
   

class StudentLeaveApp(models.Model):

    user = models.ForeignKey(Student,on_delete=models.CASCADE)
    to_teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    status = models.CharField(max_length=100,null=True)

class LeaveApplication(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    hostel = models.IntegerField()
    room = models.IntegerField()
    department = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    parents_no = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # The scanned document field (can be an image or any other file)
    supporting_document = models.FileField(upload_to='supporting_documents/', null=True, blank=True)

    def __str__(self):
        return f'{self.student.username} Leave Application'



class AppStatus(models.Model):

    leaveApp = models.ForeignKey(StudentLeaveApp,on_delete=models.CASCADE)
    leaveApp = models.ForeignKey(StudentLeaveApp,on_delete=models.CASCADE)
    status = models.CharField(max_length=100,null=True)


class TeachLeaveApp(models.Model):

    user = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    to_admin = models.ForeignKey(Admin,on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    status = models.CharField(max_length=100,null=True)

