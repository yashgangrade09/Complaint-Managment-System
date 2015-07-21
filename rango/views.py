from django.shortcuts import render
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
import datetime
from rango.forms import ComplaintForm,ViewForm,LoginForm
from rango.models import Complaint,office_staff,offices,status,taluka,comp_type
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from django.utils.translation import ugettext
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

def loginview(request):

    state = "Enter username and password."

    print request
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        form=LoginForm(request.POST)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                return HttpResponseRedirect('/rango/complaints/')
                #return view_complaint(request)
            else:
                state = "Your account is not active, please contact the site admin."

        else:
            state = "Your username and/or password were incorrect."
            form=LoginForm(initial={'username':request.POST.get('username')})
    elif request.GET.get('next')=='loggedout':                                              #from next in logoutview
        state = "Logged out successfully. Enter username and password to login again."
        form=LoginForm(initial={'username':"" ,'password':' '})
    else:                                                                                    #first time login
        form=LoginForm(initial={'username':'','password':' '})

    return render(request,'rango/Login.html',{'state':state, 'form': form})

def logoutview(request):

    logout(request)
    request.GET = request.GET.copy()
    request.GET['next']='loggedout'

    return loginview(request)


def editview(request):
    if request.POST:
        complaint_id = request.POST.get('complaint_id')
        c = Complaint.objects.get(id=complaint_id)
        c.complaint_taker = request.POST.get('complaint_taker')
        c.fname = request.POST.get('fname')
        c.lname = request.POST.get('lname')
        c.address = request.POST.get('address')
        c.village = request.POST.get('village')
        c.taluka = taluka.objects.get(t=request.POST.get('taluka'))
        c.pin = request.POST.get('pin')
        c.email = request.POST.get('email')
        c.mob = request.POST.get('mob')
        c.ph_areacode = request.POST.get('ph_areacode')
        c.ph_no = request.POST.get('ph_no')
        c.complaint_type = comp_type.objects.get(type=request.POST.get('complaint_type'))
        c.descrip = request.POST.get('descrip')
        c.acc_person= office_staff.objects.get(name='acc_person')
        c.status = status.objects.get(complaint_status=request.POST.get('status'))
        c.status_remarks = request.POST.get('status_remarks')
        c.save()
        dict = {'complaint':c}
        return HttpResponseRedirect('/rango/complaints/')

def deleteview(request,complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    complaint.delete()
    return HttpResponseRedirect('/rango/complaints/')

def index(request):
    output = ugettext('abc')
    return render(request, 'rango/w3.html')

def view_complaint(request):
    if  request.user.is_authenticated():
        complaints=Complaint.objects.all().order_by('-complaint_date','-id')
        complaints=complaints.exclude(id__lt=91)
        if request.user.is_superuser==True:
            user_office=offices.objects.get(office_name='Admin account')
        else:
            user_office=offices.objects.get(office_name=request.user.username)
            complaints= complaints.filter(office=user_office)

        if request.method == 'POST':
            if request.POST.get('sort_form')=='true':           #validates that post method is coming from sort_form

                form=ViewForm(request.POST)
                if form.is_valid():

                    if request.POST.get('search'):
                        search=request.POST.get('search')
                        complaints = complaints.filter(Q(id__icontains=search)|Q(fname__icontains=search)|Q(taluka__t__icontains=search)|Q(email__icontains=search)|Q(office__office_name__icontains=search)|
                                                               Q(mob__icontains=search)|Q(complaint_type__type__icontains=search)|Q(fname__icontains=search)|Q(descrip__icontains=search)
                                                               |Q(acc_person__name__icontains=search)|Q(village__village_name__icontains=search)|Q(status__complaint_status__icontains=search)|
                                                               Q(status_remarks__icontains=search))

                    else:
                        pass
                    if request.POST.get('start_date_year')==u'0' or request.POST.get('start_date_month')==u'0' or request.POST.get(                                            'start_date_day')==u'0':
                        pass
                    else:
                        first_date = datetime.date(int(request.POST.get('start_date_year')),int(request.POST.get('start_date_month')),
                                                   int(request.POST.get('start_date_day')))
                        complaints = complaints.filter(complaint_date__gte=first_date)
                    if request.POST.get('end_date_year')==u'0' or request.POST.get('end_date_month')==u'0' or request.POST.get('end_date_day')==u'0':
                        pass
                    else:
                        last_date = datetime.date(int(request.POST.get('end_date_year')),int(request.POST.get('end_date_month')),
                                                   int(request.POST.get('end_date_day')))
                        complaints = complaints.filter(complaint_date__lte=last_date)

                    if request.POST.get('status')=='':
                        pass
                    else:
                        complaints = complaints.filter(status=request.POST.get('status'))
                    if request.POST.get('complaint_type')=='':
                        pass
                    else:
                        complaints = complaints.filter(complaint_type=request.POST.get('complaint_type'))
                    if request.POST.get('taluka')=='':
                        pass
                    else:
                        complaints = complaints.filter(taluka=request.POST.get('taluka'))
                    if request.POST.get('acc_person')=='':
                        pass
                    else:
                        complaints = complaints.filter(acc_person=request.POST.get('acc_person'))
                    print request.POST
                    count=complaints.count()
                    dict = {'complaints':complaints,'form':form,'user_office':user_office,'count':count}
                    return  render(request,'rango/homepage.html',dict)
                else:
                    error =  form.errors
                    print error
                    form=ViewForm()
                    count=complaints.count()
                    dict = {'complaints':complaints,'form':form,'user_office':user_office,'count':count}
                    return render(request,'rango/homepage.html',dict)
            else:
                form= ViewForm()
                count=complaints.count()
                dict = {'complaints':complaints,'form':form,'user_office':user_office,'count':count}
                return render(request,'rango/homepage.html',dict)
        else:                                       #next=login, request has a POST method
            form= ViewForm()
            count=complaints.count()
            dict = {'complaints':complaints,'form':form,'user_office':user_office,'count':count}
            return render(request,'rango/homepage.html',dict)
    else:
        print 'You must be logged in first'
        return HttpResponse('not logged in')

def add_complaint(request):
     # A HTTP POST?
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = ComplaintForm(request.POST,request.FILES)

            # Have we been provided with a valid form?
            if form.is_valid():
                # Save the new category to the database.
                return confirmview(request)

                # Now call the index() view.
                # The user will be shown the homepage.

            else:
                # The supplied form contained errors - just print them to the terminal.
                print form.errors
        else:
            # If the request was not a POST, display the form to enter details.
            form = ComplaintForm()

        # Bad form (or form details), no form supplied...
        # Render the form with error messages (if any).
        return render(request, 'add_form/add_form.html',{'form':form} )
    else:
     render_to_response("Not logged in.")
def confirmview(request):

    form=ComplaintForm(request.POST,request.FILES)
    if form.is_valid():     #unnecessary validation
        fname = form.cleaned_data['fname']
        #lname = form.cleaned_data['lname']
        office = form.cleaned_data['office']
        birth_date = form.cleaned_data['birth_date']
        #address = form.cleaned_data['address']
        village = form.cleaned_data['village']
        taluka = form.cleaned_data['taluka']
        #pin = form.cleaned_data['pin']
        email = form.cleaned_data['email']
        mob = form.cleaned_data['mob']
        #ph_areacode = form.cleaned_data['ph_areacode']
        #ph_no = form.cleaned_data['ph_no']
        complaint_type = form.cleaned_data['complaint_type']
        descrip = form.cleaned_data['descrip']
        acc_person = form.cleaned_data['acc_person']
        status = form.cleaned_data['status']
        status_remarks = form.cleaned_data['status_remarks']
        filename = request.FILES.getlist('docfile')
        dict = {
            'fname':fname,
         #   'lname' : lname,
            'office' : office,
            'birth_date' :birth_date,
          #  'address' :address,
            'village' :village,
            'taluka' :taluka,
           # 'pin' :pin,
            'email' :email,
            'mob' :mob,
            #'ph_areacode' :ph_areacode,
            #'ph_no' :ph_no,
            'complaint_type' :complaint_type,
            'descrip' :descrip,
            'acc_person' :acc_person,
            'status' :status,
            'status_remarks' :status_remarks,
            'filename': filename
        }

        form.save()
        return render(request, 'rango/confirmation.html',dict)
    else:
        pass





