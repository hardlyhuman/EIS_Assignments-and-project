from django.shortcuts import render
from forms import SignInForm
from django.http import HttpResponseRedirect
import mysql.connector


def signin(request):
     signin_form = SignInForm
     form = signin_form(data=request.POST or None)
     if request.method == 'POST':
          form = SignInForm(request.POST)
          if form.is_valid():
               data = form.cleaned_data
               username = data['username']
               password = data['password']
               #print username
               #print password
               cnx = mysql.connector.connect(user='water_consumer', password='test1234', database='watermeter')
               cursor = cnx.cursor()
               print "SELECT password FROM logins WHERE username = '" + username + "';"
               query = ("SELECT password FROM logins WHERE username = '" + username + "';")
               cursor.execute(query)
               result=cursor.fetchall()
               print cursor
               success = 0
              #print result[0] + '...' + result[1]
               for passw in result:
                    print "Entered loop..."
                    print passw,password
                    if(password=='password'):
                        success = 1
                        break
               cnx.commit()
               cursor.close()
               cnx.close()
               if(success==1):
                    return HttpResponseRedirect('/profilepage')
               else:
                    return HttpResponseRedirect('/signin')
     else:
          return render(request, 'signin.html', {'form': form})

