from django import forms
from django.db import models
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from rango.models import Complaint,ComplaintView,office_staff,offices,comp_type,status,taluka,village
import datetime

class ComplaintForm(ModelForm):
    #address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Address Line','size':'40'}),required=False)
    office = forms.ModelChoiceField(queryset=offices.objects.all().exclude(office_name__icontains='Admin'),empty_label=' Choose Office',widget=forms.Select(attrs={'style':'width:160px'}))
    acc_person = forms.ModelChoiceField(queryset=office_staff.objects.all(),empty_label=' Choose Concerned person',widget=forms.Select(attrs={'style':'width:160px'}))
    complaint_type = forms.ModelChoiceField(queryset=comp_type.objects.all(),empty_label='Choose Complaint type',widget=forms.Select(attrs={'style':'width:161px'}))
    village = forms.ModelChoiceField(queryset=village.objects.all(),empty_label='Choose Village',widget=forms.Select(attrs={'style':'width:160px'}))
    taluka = forms.ModelChoiceField(queryset=taluka.objects.all(),empty_label=' Choose Taluka',widget=forms.Select(attrs={'style':'width:160px'}))
    #pin= forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Pin Code','size':'7'}),required=False)
    #lname = forms.CharField(required=False)
    #ph_areacode = forms.IntegerField(widget=forms.TextInput(attrs={'size': '4'}),required=False)
    #ph_no=forms.IntegerField(required=False)
    docfile = forms.FileField(label='Select a File',help_text='(max. 30MB)',required=False)
    status=forms.ModelChoiceField(queryset=status.objects.all(),widget=forms.RadioSelect,required=True)
    descrip = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'cols':'40','rows':'5'}),required=True)
    status_remarks = forms.CharField(max_length=300,widget=forms.Textarea(attrs={'cols':'32','rows':'3'}),required=False)
    YEAR_CHOICES = ('2015','2014','2013','2012','2011','2010',
                    '2009','2008','2007','2006','2005','2004','2003','2002','2001','2000',
                    '1999','1998','1997','1996','1995','1994','1993','1992','1991','1990',
                    '1999','1988','1987','1986','1985','1984','1983','1982','1981','1980',
                    '1999','1978','1977','1976','1975','1974','1973','1972','1971','1970',
                    '1999','1968','1967','1966','1965','1964','1963','1962','1961','1960',
                    '1999','1958','1957','1956','1955','1954','1953','1952','1951','1950',
                    '1999','1948','1947','1946','1945','1944','1943','1942','1941','1940',
                    )
    birth_date = forms.DateField(
    widget=SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),years=YEAR_CHOICES
    ),
)
    class Meta:
        model = Complaint
        #fields= ('complaint_date','complaint_taker','office','salutation','fname','lname','birth_date','gender',
         #       'email','mob','ph_areacode','ph_no','complaint_type','descrip','acc_person','status',)
        exclude = ('complaint_date',)

class LoginForm(forms.Form):
    username=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Ex. Baramati'}))
    password=forms.CharField(widget=forms.PasswordInput(render_value=False))

class ViewForm(ModelForm):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Search','size':'24px'}),required=False)
    office= forms.ModelChoiceField(queryset=offices.objects.all(),empty_label='Any',required=False,)
    acc_person = forms.ModelChoiceField(queryset=office_staff.objects.all(),empty_label='Concerned Person',required=False,widget=forms.Select(attrs={'style':'width:200px'}))
    complaint_type = forms.ModelChoiceField(queryset=comp_type.objects.all(),empty_label='Complaint Type',required=False,widget=forms.Select(attrs={'style':'width:200px'}))
    status = forms.ModelChoiceField(queryset=status.objects.all(),empty_label='Complaint Status',required=False,widget=forms.Select(attrs={'style':'width:200px'}))
    taluka = forms.ModelChoiceField(queryset=taluka.objects.all(),empty_label='Taluka',required=False,widget=forms.Select(attrs={'style':'width:200px'}))
    YEAR_CHOICES = ('2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015',
                    '2016','2017','2018','2019','2020','2021','2022','2023','2024','2025','2026','2027','2028','2029','2030',
                    '2031','2032','2033','2034','2035','2036','2037','2038','2039','2040')
    start_date = forms.DateField(required=False,widget=SelectDateWidget(
        empty_label=("Year", "Month", "Day"),years=YEAR_CHOICES,
    ),
)
    end_date = forms.DateField(required=False,
    widget=SelectDateWidget(
        empty_label=("Year", "Month", "Day"),years=YEAR_CHOICES
    ),
)
    class Meta:
        model = ComplaintView
        exclude = ()