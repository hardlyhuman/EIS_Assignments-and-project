from django.shortcuts import render
from forms import SignUpForm
from django.http import HttpResponseRedirect
import mysql.connector


def signup(request):
     signup_form = SignUpForm
     form = signup_form(data=request.POST or None)
     if request.method == 'POST':
          form = SignUpForm(request.POST)
          if form.is_valid():
               data = form.cleaned_data
               fname =  data['fname']
               lname = data['lname']
               phone = data['phone']
               email = data['email']
               address = data['address']
               username = data['username']
               password = data['password']

               print fname
               print lname
               print phone
               print email
               print address
               print username
               print password


               cnx = mysql.connector.connect(user='water_consumer', password='test1234', database='watermeter')
               cursor = cnx.cursor()

               add_login = ("INSERT INTO logins "
                               "(username, password) "
                               "VALUES (%s, %s)")
               data_login = (username,password)
               add_user_profile = ("INSERT INTO profile "
                               "(username,fname, lname, phone, email, address) "
                               "VALUES (%s, %s, %s, %s, %s, %s)")
               data_user_profile = (username, fname,lname,phone,email, address)

               cursor.execute(add_login,data_login)
               cursor.execute(add_user_profile, data_user_profile)
               cnx.commit()

               cursor.close()
               cnx.close()
               return HttpResponseRedirect('/signin')
     else:
          return render(request, 'signup.html', {'form': form})

