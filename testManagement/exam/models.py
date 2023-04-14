from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
import os
from django.conf import settings

class UserAccountManager(BaseUserManager):
	def create_user(self , email , password = None):
		if not email or len(email) <= 0 :
			raise ValueError("Email field is required !")
		if not password :
			raise ValueError("Password is must !")
		
		user = self.model(
			email = self.normalize_email(email) ,
		)
		user.set_password(password)
		user.save(using = self._db)
		return user
	
	def create_superuser(self , email , password):
		user = self.create_user(
			email = self.normalize_email(email) ,
			password = password
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using = self._db)
		return user
	
class UserAccount(AbstractBaseUser):
	class Types(models.TextChoices):
		ADMIN = "ADMIN" , "admin"
		STUDENT = "STUDENT" , "student"
		TEACHER = "TEACHER" , "teacher"
		
	type = models.CharField(max_length = 8 , choices = Types.choices ,
							# Default is user is teacher
							default = Types.ADMIN)
	email = models.EmailField(max_length = 200 , unique = True)
	fname = models.CharField(max_length=100)
	lname = models.CharField(max_length=100)
	is_active = models.BooleanField(default = True)
	is_admin = models.BooleanField(default = False)
	is_staff = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)
	
	# special permission which define that
	# the new user is teacher or student
	is_student = models.BooleanField(default = False)
	is_teacher = models.BooleanField(default = False)
	
	USERNAME_FIELD = "email"
	
	# defining the manager for the UserAccount model
	objects = UserAccountManager()
	
	def __str__(self):
		return str(self.email)
	
	def has_perm(self , perm, obj = None):
		return self.is_admin
	
	def has_module_perms(self , app_label):
		return True
	
	def save(self , *args , **kwargs):
		if not self.type or self.type == None :
			self.type = UserAccount.Types.TEACHER
		return super().save(*args , **kwargs)
	
class StudentManager(models.Manager):
	def create_user(self , fname, lname, email , password = None):
		if not email or len(email) <= 0 :
			raise ValueError("Email field is required !")
		if not password :
			raise ValueError("Password is must !")
		email = email.lower()
		user = self.model(
			email = email
		)
		user.set_password(password)
		user.fname = fname
		user.lname = lname
		user.save(using = self._db)
		return user
	
	def get_queryset(self , *args, **kwargs):
		queryset = super().get_queryset(*args , **kwargs)
		queryset = queryset.filter(type = UserAccount.Types.STUDENT)
		return queryset	
	
	


		
class Student(UserAccount):
	class Meta :
		proxy = True
	objects = StudentManager()
	
	def save(self , *args , **kwargs):
		self.type = UserAccount.Types.STUDENT
		self.is_student = True
		return super().save(*args , **kwargs)
	
	@property
	def showprofile(self):
		return self.studentprofile
	
class StudentProfile(models.Model):
	user = models.OneToOneField(UserAccount,on_delete=models.CASCADE)
	standard = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(12)],default=1)

# @receiver(post_save, sender=Student)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.type == "STUDENT":
#         StudentProfile.objects.create(user=instance)
	
class TeacherManager(models.Manager):
	def create_user(self , fname, lname, email , password = None):
		if not email or len(email) <= 0 :
			raise ValueError("Email field is required !")
		if not password :
			raise ValueError("Password is must !")
		email = email.lower()
		user = self.model(
			email = email
		)
		user.fname = fname
		user.lname = lname
		user.set_password(password)
		user.save(using = self._db)
		return user
		
	def get_queryset(self , *args , **kwargs):
		queryset = super().get_queryset(*args , **kwargs)
		queryset = queryset.filter(type = UserAccount.Types.TEACHER)
		return queryset
	
class Teacher(UserAccount):
	class Meta :
		proxy = True
	objects = TeacherManager()
	
	def save(self , *args , **kwargs):
		self.type = UserAccount.Types.TEACHER
		self.is_teacher = True
		return super().save(*args , **kwargs)
	
	@property
	def showprofile(self):
		return self.teacherprofile

class TeacherProfile(models.Model):
	user = models.OneToOneField(UserAccount,on_delete=models.CASCADE)
	subject = models.CharField(max_length=20)

# @receiver(post_save, sender=Teacher)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.type == "TEACHER":
#         TeacherProfile.objects.create(user=instance)


class Test(models.Model):
	title = models.CharField(max_length=100)
	pdf = models.FileField(upload_to="tests/pdfs/",unique=True) #also have upload to parameter

	def __str__(self):
		return self.title
	
	def delete(self, *args, **kwargs):
		os.remove(os.path.join(settings.MEDIA_ROOT, self.pdf.name))
		super().delete(*args, **kwargs) 