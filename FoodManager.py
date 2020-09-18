from stuff import *
import openpyxl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage                   
from email.mime.audio import MIMEAudio 
import smtplib

def send_msg(post, filename):
	msg = MIMEMultipart() #создание объекта сообщения
	message = "заказ:" #сообщение которое отправялется
	password = "kingking2281337" # пароль от почты с которой идет отправление
	msg['From'] = "testtesttesttest9990@gmail.com" #почта с которой отправляется
	msg['To'] = post # почта куда отправляется
	msg['Subject'] = "Поставки" # тема сообщения

	msg.attach(MIMEText(message, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com: 587') # подключение к серверу отправки сообщений

	server.starttls() # хз точно, но как понял делает подключение к почте безопасным

	server.login(msg['From'], password) #логин в почту с которой будет отправляться сообщение

	'''filepath = new_output         # если файл в той же папке то не менять если в другой то прописыаать весь путь
	filename = os.path.basename(filepath)                     # Только имя файла
	'''
	if os.path.isfile(filename):
		ctype, encoding = mimetypes.guess_type(filename)
		maintype, subtype = ctype.split('/', 1)
		with open(filename, 'rb') as fp:
			file = MIMEBase(maintype, subtype)
			file.set_payload(fp.read())
			fp.close()
		encoders.encode_base64(file)
		file.add_header('Content-Disposition', 'attachment', filename=filename)
		msg.attach(file)    
	server.sendmail(msg['From'], msg['To'], msg.as_string()) # отправка сообщения
	server.quit()
	print ("successfully sent email to %s:" % (msg['To'])) # вывод того что сообщение отправилось

path_post = r'C:\Users\nekry\Desktop\PYTHON PROJECTS\Foodmanager\some\post.xlsx'#пусть к таблице с поставщиками
path_prod = r'C:\Users\nekry\Desktop\PYTHON PROJECTS\Foodmanager' #в какой папке искать файл с отчетом
path_output = r'C:\Users\nekry\Desktop\PYTHON PROJECTS\Foodmanager\output\\'

wb = openpyxl.load_workbook(filename=path_post) #открытие файла для чтения с поставщиками
wb.active = 0 #установка рабочего листа на первый
sheet = wb.active

post_dict = {} #словарь с ключами - почта поставщики, значения - продукты
post_list = [] #список только с почтой поставщиков 
for i in range(2, 4):
	post_dict[sheet['A'+str(i)].value] = sheet['B'+str(i)].value#формирование словаря
	
wb.save(path_post) #закрытие файла из которго читали
post_list = [key for key in post_dict]# формирование списка поставщиков

files = [i for i in os.listdir(path_prod) if i.endswith('.xlsx')]#выбираются только файлы с расщирение xlsx

new = max(files, key=os.path.getctime)#самый новый файл среди них
files = [os.path.join(path_prod, file) for file in files] #добавление полного пути к файлам
new_path = max(files, key=os.path.getctime) #самый новый файл с путем к нему

wb = openpyxl.load_workbook(filename=new_path) #открытие файла для чтения с продуктами
wb.active = 0 #установка рабочего листа на первый
sheet = wb.active

for post in post_list:
	i = 2
	p = 1
	wb_output = openpyxl.Workbook() #создание и открытие файла для записи
	wb_output.active = 0 #установка рабочего листа на первый
	sheet_output = wb_output.active
	while sheet['A'+str(i)].value:
		print('\n i = ', i)
		if sheet['A' + str(i)].value in post_dict.get(post):
			print('\np = ', p)
			sheet_output['A'+str(p)].value = sheet['A'+str(i)].value
			sheet_output['B' + str(p)] = sheet['B'+str(i)].value - sheet['C'+str(i)].value #заносится в столбец A разница между заказом и остатком
			p += 1
		i += 1
	filename = path_output + post + '.xlsx'
	wb_output.save(filename)
	send_msg(post, filename)
wb.save(new)
