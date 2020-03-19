import datetime
import sys,os
import time
import pytz
import ntplib


utc=pytz.utc

print("hora y fecha actual antes de pedir al NPT----> "+str(datetime.datetime.now()))

####Formato para la conversion a UTC
fmt = '%Y-%m-%d %H:%M:%S'
fmtt = '%Y-%m-%d %H:%M:%S.%f'
mexico = pytz.timezone('America/Mexico_City')

####Pide tiempo al servidor ntp
client=ntplib.NTPClient()
print("pidiendo hora a servidor --------------------> ntp.cais.rnp.br...")
tiempo_salida_peticion=datetime.datetime.now()
response=client.request('ntp.cais.rnp.br')#('europe.pool.ntp.org')
tiempo_llegada_peticion=datetime.datetime.now()


tiempo_respuesta_peticion=(tiempo_llegada_peticion-tiempo_salida_peticion)/2
print(f"tiempo de respuesta de peticion -------------> {tiempo_respuesta_peticion}")
hora_servidor=time.localtime(response.tx_time)
#hora_servidor=time.gmtime(response.tx_time)
print(f"hora de servidor NTP ------------------------> {hora_servidor}")


####Cambia al formato para la conversion a UTC
date_time=str(hora_servidor[0])+"-"+str(hora_servidor[1])+"-"+str(hora_servidor[2])+" "+str(hora_servidor[3])+":"+str(hora_servidor[4])+":"+str(hora_servidor[5])


####Cambia hora a UTC
dt = datetime.datetime.strptime(date_time, fmt)
am_dt = mexico.localize(dt)
print(am_dt)
#hora_utc=am_dt.astimezone(utc).strftime(fmt)+",00"
hora_utc=am_dt.strftime(fmt)+".00"

print(f"hora sin la suma el retraso {hora_utc}")

#hora_servidor=time.strftime(fmt,hora_servidor)+".00"

tiempo_en_ejecucion=datetime.datetime.now()-tiempo_llegada_peticion
print(f"tiempo de retraso de ejecucion --------------> {tiempo_en_ejecucion}")
hora_ntp=(datetime.datetime.strptime(hora_utc, fmtt)+tiempo_respuesta_peticion+tiempo_en_ejecucion).strftime(fmtt)

####Aplica la hora al sistema (year,month,dayOfWeek,day,hour,minute,second,millisecond)
if sys.platform=='linux':
	os.system(f"sudo date --set \"{hora_ntp}\"")
elif sys.platform=='win32': 
	# agregar_peticiones("07",ip,datetime.datetime.now())
	import win32api
	win32api.SetSystemTime(int(hora_ntp[:4]),int(hora_ntp[5:7]),int(hora_servidor[6]),int(hora_ntp[8:10]),int(hora_ntp[11:13]),int(hora_ntp[14:16]),int(hora_ntp[17:19]),int(hora_ntp[20:23]))
	agregar_peticiones("07",ip,datetime.datetime.now())
print("hora y fecha actual con servidor NTP --------> "+str(datetime.datetime.now()))



































