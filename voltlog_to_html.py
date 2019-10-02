#!/usr/bin/env python3

from pip_ensure_installed import pip_ensure_installed
pip_ensure_installed("xlsxlite")
pip_ensure_installed("xlsxwriter")
pip_ensure_installed("Adafruit_ADS1x15")
pip_ensure_installed("tzlocal")
#from xlsxlite.writer import XLSXBook
import xlsxwriter

import random
import datetime
import tzlocal
import time
import csv
import Adafruit_ADS1x15
import glob
import os

#fakesamples = 2*60*24*10
fakesamples = 0
sample_interval_seconds = 30
backup_interval_seconds = 60*20

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

data = []

def getTimestring():
	return str(datetime.datetime.now(tzlocal.get_localzone()))
	
def readNewSample():
	sample = {}
	#sample['timestring'] = 	str(datetime.datetime.now(tzlocal.get_localzone()))
	sample['timestring'] = 	datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	sample['datetime'] = 	datetime.datetime.now()
	
	values = [] 
	for i in range(4):
		if(fakesamples>0):
			v = random.randint(0,20)
		else:
			v = adc.read_adc(i, gain=GAIN)*4.096/32768.0
		values.append(v)
		
	sample['values'] = values
	return sample

def data_to_csv(filename_to_save, samples_to_save):	
	with open(filename_to_save, mode='w') as myfile:
		writer = csv.writer(myfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for sample_to_save in samples_to_save:
			writer.writerow([
				sample_to_save['values'][0],
				sample_to_save['values'][1],
				sample_to_save['values'][2],
				sample_to_save['values'][3],
				sample_to_save['timestring']
				])
				
				#["value-0"], entry["value-1"], entry["value-2"], entry["value-3"], entry["year"], entry["month"], entry["day"], entry["hour"], entry["minute"]])
def tablevalue(myfile,s):
	myfile.write("<td>")
	myfile.write(str(s))
	myfile.write("</td>")

def data_to_html(filename_to_save, samples_to_save):
	with open(filename_to_save, mode='w') as myfile:
		myfile.write("<!DOCTYPE html>\n<html>\n<head>\n<style>\ntable, th, td {border: 1px solid black;}\n</style>\n</head>\n<body>\n<h1>My First Heading</h1>\n")
		myfile.write('<table style="width:100%">')
		for sample_to_save in samples_to_save:
				myfile.write("<tr>")
				tablevalue(myfile, sample_to_save['timestring'])
				tablevalue(myfile, sample_to_save['values'][0])
				tablevalue(myfile, sample_to_save['values'][1])
				tablevalue(myfile, sample_to_save['values'][2])
				tablevalue(myfile, sample_to_save['values'][3])
				myfile.write("</tr>\n")
		myfile.write("</table>")
		myfile.write("\n</body>\n</html>\n")
	
	
	
def data_to_xlsx(filename_to_save, samples_to_save):
	workbook   = xlsxwriter.Workbook(filename_to_save, {'constant_memory': True})
	worksheet  = workbook.add_worksheet("data")
	r = 0
	worksheet.write(r, 0, 'Zeit')
	worksheet.write(r, 1, 'value1')
	worksheet.write(r, 2, 'value2')
	worksheet.write(r, 3, 'value3')
	worksheet.write(r, 4, 'value4')
	r = 1
	date_format = workbook.add_format({'num_format': 'dd/mm/yy hh:mm:ss','align': 'left'})
	for sample_to_save in samples_to_save:
				worksheet.write_datetime(r, 0, sample_to_save['datetime'], date_format)
				worksheet.write(r, 1, sample_to_save['values'][0])
				worksheet.write(r, 2, sample_to_save['values'][1])
				worksheet.write(r, 3, sample_to_save['values'][2])
				worksheet.write(r, 4, sample_to_save['values'][3])
				r = r +1
	workbook.close()
	
def filename_backup():
    amount = 0
    for i in glob.glob(os.getcwd() + "/logs/backups/*"):
        amount += 1
    p = "./logs/backups/data_" + str(amount + 1) 
    return p
	
filename=getTimestring()
filename = filename[:19]
filename = filename.replace(' ','_')
filename = filename.replace(':','-')
#filename = filename + ".txt"
print(filename)


samples = []
t_backup = time.time()

if(fakesamples>0):
	print('generate fake test data')
	for x in range(fakesamples):
			sample = readNewSample()
			samples.append(sample)

while True:
	print('main loop')
	t_start = time.time()
	try:
		t = time.time()
		print('try')
		sample = readNewSample()
		print('sample')
		print(sample)
		samples.append(sample)
		#print(samples)
		print('sample in {:}s'.format(time.time()-t))
		if((time.time() - t_backup) > backup_interval_seconds):
			print('save csv')
			t = time.time()
			data_to_csv (filename_backup() + ".txt", samples)
			t_backup = time.time()
			print('done in {:}s'.format(time.time() - t))
		print('save html')
		t = time.time()
		data_to_html("./logs/" + filename + ".html", samples)
		print('done in {:}s'.format(time.time() - t))
		#print('save xlsx')
		#t = time.time()
		#data_to_xlsx("./logs/" + filename + ".xlsx", samples)
		#print('done in {:}s'.format(time.time() - t))
		
		seconds_to_sleep = sample_interval_seconds - (time.time() - t_start)
		print('sleep ' + str(seconds_to_sleep))
		time.sleep(seconds_to_sleep)
	except Exception as e:
		print('Exception: '+ str(e))
		#raise 
		print('sleep 3')
		time.sleep(3)
		pass
	
