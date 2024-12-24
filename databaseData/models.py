from django.db import models

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name

class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=100)
    class_type = models.CharField(max_length=50)
    department_id = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        
        related_name='classes'
    )
    def __str__(self):
        return f"{self.class_name} ({self.class_type})"

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    department_id = models.OneToOneField(
        Department,
        on_delete=models.CASCADE,
        related_name='user'
    )

    def __str__(self):
        return self.user_name

class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department_id = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='teachers'
    )
    def __str__(self):
        return self.teacher_name
    #changes made from here ---------------------------------------------
class Subject(models.Model):
    subject_id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=100)
    theory=models.IntegerField()
    lab =models.IntegerField()
    semester = models.CharField(max_length=100)
    course_module = models.CharField(max_length=100)
    teacher_id=models.ForeignKey(Teacher , on_delete=models.SET_NULL, null=True , blank=True)
    department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.subject_name } ({self.semester})'
    
#--------------------------------------------------------------------------------

class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)

class FreeClassSlot(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
   
    id = models.AutoField(primary_key=True)
    class_id=models.ForeignKey(Class,on_delete=models.CASCADE , related_name='free_slots')
    free_slots = models.CharField(max_length=100)
    department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    def __str__(self):
        return f'{self.class_id} {self.free_slots} , {self.day_of_week}'
    

# =================================================================================================
class Scheduler(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    slot = models.CharField(max_length=10)
    semester = models.CharField(max_length=100)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.class_id} {self.subject_id} {self.teacher_id} {self.day_of_week} {self.slot} {self.semester}'