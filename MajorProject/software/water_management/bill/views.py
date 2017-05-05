from django.shortcuts import render
import smtplib
import MySQLdb
# Create your views here.
def bill(request):
	db = MySQLdb.connect("localhost","water_consumer","test1234","watermeter" )
	cursor = db.cursor()


	cursor.execute("SELECT * from bill where username='soham_m1705'");
	msg = cursor.fetchall()
	msg1 = str(msg[0][1])
	msg1 += "ml\n"
	msg1 += str(msg[0][2])
	msg1 += "paise."
	
	db.close()
	smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
	smtpObj.starttls()
	smtpObj.login('sriharsha.g15@iiits.in', 'Sri@CyberEye')

	smtpObj.sendmail('sriharsha.g15@iiits.in', 'soham.m15@iiits.in', str(msg1))
	return render(request,'bill.html')
