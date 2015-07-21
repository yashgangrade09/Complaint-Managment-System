from django.db import models
import datetime
import django

# Create your models here.

class status(models.Model):
    complaint_status = models.CharField(max_length=10)
    def __unicode__(self):
        return self.complaint_status

class offices(models.Model):
    office_name = models.CharField(max_length=20,unique=True)
    def __unicode__(self):
        return self.office_name

class comp_type(models.Model):
    type = models.CharField(max_length=30)
    def __unicode__(self):
        return self.type

class office_staff(models.Model):
    name = models.CharField(max_length=40,unique=True)
    office = models.ForeignKey('offices')
    def __unicode__(self):
        return self.name

class taluka(models.Model):
    t = models.CharField(max_length=100)
    def __unicode__(self):
        return self.t

class village(models.Model):
   village_name= models.CharField(max_length=100)
   def __unicode__(self):
        return self.village_name

class ComplaintView(models.Model):
    search = models.CharField(max_length=50,blank=True,null=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    office = models.ForeignKey('offices',null=True,blank=True  )
    acc_person = models.ForeignKey('office_staff',to_field='name',null=True)
    complaint_type = models.ForeignKey('comp_type',null=True)
    status = models.ForeignKey('status',null=True)
    taluka = models.ForeignKey('taluka',null=True)
    def __unicode__(self):
        return u'%s,%s,%s,%s,%s'%(self.acc_person,self.office,self.taluka,self.complaint_type,self.status)

class Complaint(models.Model):
    index = models.AutoField
    complaint_date = models.DateTimeField(auto_now_add=True,blank=True)
    complaint_taker = models.CharField(max_length=30)
    office = models.ForeignKey('offices')
    fname= models.CharField(max_length=60)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=2,choices=(('M','Male'),('F','Female'),),default='M')
    village = models.ForeignKey('village',null=True)
    taluka = models.ForeignKey('taluka')
    email = models.EmailField(blank=True)
    mob = models.IntegerField(null=True)
    complaint_type  = models.ForeignKey('comp_type')
    descrip = models.CharField(max_length=500)
    acc_person = models.ForeignKey('office_staff',to_field='name')
    status = models.ForeignKey('status')
    status_remarks= models.CharField(max_length=150,null=True)
    docfile = models.FileField(upload_to='documents',null=True,blank=True)

    def __unicode__(self):
        return '#%s  %s  %s  %s-%s-%s  %s  %s  %s %s %s  %s  %s  %s  %s  %s  %s'%(self.id,self.office,self.acc_person,self.complaint_date.day,self.complaint_date.month,
                                                                         self.complaint_date.year,self.village,self.taluka,self.complaint_type,
                                                            self.descrip,self.status,self.status_remarks,self.fname,self.birth_date,self.gender,
                                                            self.email,self.mob)


    def save(self, *args, **kwargs):
         #On save, update timestamps
        if not self.id:
            self.complaint_date = datetime.date.today()
        return super(Complaint, self).save(*args, **kwargs)
