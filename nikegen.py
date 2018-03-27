import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import random
from threading import Thread,Lock
import json
import time
import re
import names
import math
import Queue
import click
from timedqueue import TimedQueue
from nikesensor import *
from nikereqpatch import *
import uuid
globallock=Lock()
class NumberException(Exception):
	pass
allLocks={}
MAINLOCKS={}
getsmssession=requests.session()
def getLock(prox):
    global MININTERVAL
    allLocks[prox].get()
    allLocks[prox].put(1,MININTERVAL)
def blocknumber(num):
    try:
        getsmssession.post("http://www.getsmscode.com/do.php",data={"action":"addblack","username":GETSMSEMAIL,"token":GETSMSTOKEN,"pid":"462","mobile":num})
    except Exception as e:
        print "{0}\n".format(e),
def blockall():
	print "Blocking all current numbers"
	m=getsmssession.post("http://www.getsmscode.com/do.php",data={"action":"mobilelist","username":GETSMSEMAIL,"token":GETSMSTOKEN})
	n=m.text.split(',')
	for p in n:
		print "Blocking {0}\n".format(p),
		blocknumber(p.split("|")[0])
def verifyinfo():
	m=getsmssession.post("http://www.getsmscode.com/do.php",data={"action":"login","username":GETSMSEMAIL,"token":GETSMSTOKEN})
	n=m.text.split("|")
	if len(n)==2:
		print m.text+"\n",
		print "Invalid info entered for getsmscode.com\n",
		exit()
def getsession(prox):
    sess=requests.session()
    print "Trying to get abck cookie"
    allLocks[prox].get()
    try:
        bot=BotDetector()
        payload="{\"sensor_data\":\""+bot.generatesensordata()+"\"}"
        d=sess.post("https://www.nike.com/_bm/_data",headers={"Connection":"keep-alive","X-NewRelic-ID":"VQYGVF5SCBAJVlFaAQIH","Origin":"https://www.nike.com","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36","Content-Type":"application/json","Accept":"*/*","Referer":"https://www.nike.com/us/en_us","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"},proxies={"https":prox},data=payload,verify=False,timeout=15)
        bot.cookie=sess.cookies["_abck"]
        payload="{\"sensor_data\":\""+bot.generatesensordata1()+"\"}"
        d=sess.post("https://www.nike.com/_bm/_data",headers={"Connection":"keep-alive","X-NewRelic-ID":"VQYGVF5SCBAJVlFaAQIH","Origin":"https://www.nike.com","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36","Content-Type":"application/json","Accept":"*/*","Referer":"https://www.nike.com/us/en_us","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"},proxies={"https":prox},data=payload,verify=False,timeout=15)
        if "~0~" in sess.cookies["_abck"]:
            print sess.cookies["_abck"]
            allLocks[prox].put(1,MININTERVAL)
            return sess
    except Exception as e:
        print e
    allLocks[prox].put(1,MININTERVAL)
    return sess
def generateemail(email,maxval=1,usedom=False):
    if email[0]=="@":
        return names.get_first_name()+str(random.randint(1,999999))+email
    em=email.split("@")
    em1=em[0][:-1]
    vt=2**len(em1)
    gt=0
    if vt<(maxval*100):
        wt=float(maxval*100)/vt
        gt=int(math.ceil(math.log(wt,36)))
    a=""
    for p in em1:
        a+=p
        a+=random.choice(["","."])
    a+=em[0][-1]
    if gt>0:
        a+="+"+("".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for i in range(0,gt)]))
    a+="@"+em[-1]
    return a
def getnumber():
    d=getsmssession.post("http://www.getsmscode.com/do.php",data={"action":"getmobile","username":GETSMSEMAIL,"token":GETSMSTOKEN,"pid":"462"})
    return d.text
def getcode(number):
    for i in range(0,20):
        d=requests.post("http://www.getsmscode.com/do.php",data={"action":"getsms","username":GETSMSEMAIL,"token":GETSMSTOKEN,"pid":"462","mobile":("86"+number)})
        if "NIKE" in d.text:
            return d.text
        print "Not received sms yet on {0}\n".format(number),
        time.sleep(5)
    blocknumber("86"+number)
    raise Exception("Not received sms in time")
def signup(email,name,password,country):
    prox=random.choice(PROXYLIST)
    with MAINLOCKS[prox]:
        nam=name.split(' ')
        sess=getsession(prox)
        sess.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"})
        getLock(prox)
        sess.cookies["CONSUMERCHOICE"]="cn/zh_cn"
        sess.cookies["NIKE_COMMERCE_COUNTRY"]="CN"
        sess.cookies["NIKE_COMMERCE_LANG_LOCALE"]="zh_CN"
        sess.cookies["nike_locale"]="cn/zh_cn"
        dob=str(random.randint(1990,1995))+"-"+str(random.randint(10,12))+"-"+str(random.randint(10,28))
        if country=="US":
            payload={"account":{"email":email,"passwordSettings":{"password":password,"passwordConfirm":password}},"locale":"en_US","welcomeEmailTemplate":"TSD_PROF_MS_WELC_T0_GENERIC_V1.0","registrationSiteId":"nikedotcom","username":email,"firstName":nam[0],"lastName":nam[1],"dateOfBirth":dob,"country":"US","gender":"F","receiveEmail":True}
        else:
            payload={"account":{"email":email,"passwordSettings":{"password":password,"passwordConfirm":password}},"locale":"en_US","welcomeEmailTemplate":"TSD_PROF_MS_WELC_T0_GENERIC_V1.0","registrationSiteId":"nikedotcom","username":email,"firstName":nam[0],"lastName":nam[1],"dateOfBirth":dob,"country":"GB","gender":"F","receiveEmail":True}
        getLock(prox)
        print "Signing up with email {0}\n".format(email),
        uid=str(uuid.uuid4())
        r=sess.post("https://unite.nike.com/join?appVersion=389&experienceVersion=325&uxid=com.nike.commerce.nikedotcom.web&locale=en_US&backendEnvironment=identity&browser=Google%20Inc.&os=undefined&mobile=false&native=false&visit=1&visitor="+uid,json=payload,verify=False,proxies={"https":prox},headers={"Referer":"https://www.nike.com/us/en_us","Origin":"https://www.nike.com","Content-Type":"text/plain"},timeout=30)
        r.raise_for_status()
        getLock(prox)
        m_login_data = {'keepMeLoggedIn':True, 'client_id':'PbCREuPr3iaFANEDjtiEzXooFl7mXGQ7','ux_id':'com.nike.commerce.snkrs.droid','grant_type':'password','username':email,'password':password}
        e=sess.post('https://api.nike.com/idn/shim/oauth/2.0/token',json=m_login_data,verify=False,proxies={"https":prox},timeout=30)
        TOKEN=json.loads(e.text)['access_token']
        sess1=sess
    ok=False
    NUMBER=None
    for i in range(0,60):
        try:
            NUMBER=getnumber()
            if len(NUMBER)!=13:
                print "{0}\n".format(NUMBER)
            else:
                ok=True
                NUMBER=NUMBER[2:]
                break
        except Exception as e:
            try:
                print e
            except:
                pass
        time.sleep(5)
    if not ok:
        raise Exception("Didn't receive number in time")
    try:
        getLock(prox)
        print "Using number: {0}\n".format(NUMBER),
        f=sess1.put("https://idn.nike.com/idn/phone/+86"+NUMBER,headers={"Authorization":"Bearer "+TOKEN,"Referer":"https://www.nike.com/cn/zh_cn/p/settings","Origin":"https://www.nike.com","Content-Locale":"zh_CN"},verify=False,proxies={"https":prox},timeout=30)
        f.raise_for_status()
        TOKEN=json.loads(e.text)['access_token']
        code=getcode(NUMBER)[-6:]
        print "Submitting code\n",
        getLock(prox)
        d=sess.post("https://idn.nike.com/idn/phone/{0}".format(code),headers={"Authorization":"Bearer "+TOKEN},verify=False,proxies={"https":prox},timeout=30)
        try:
            getLock(prox)
            if COUNTRY=="US":
                url="https://secure-store.nike.com/us/services/profileService"
            else:
                url="https://secure-store.nike.com/gb/services/profileService"
            e=sess.post(url,data={"action":"getprofile","rt":"JSON"},headers={"X-Requested-With":"XMLHttpRequest"},verify=False,proxies={"https":prox},timeout=30)
        except:
            pass
    except Exception as e:
        if NUMBER!=None:
            blocknumber("86"+NUMBER)
        raise e
    return password
import traceback
def dosignup(id,name,email,maxq,password,maxal,country):
    while maxq.qsize()>0:
        emr=generateemail(email,maxal)
        try:
            try:
                maxq.get_nowait()
            except:
                return
            password=signup(emr,name,password,country)
            globallock.acquire()
            v=open(id,'ab')
            v.write(emr+":"+password+"\r\n")
            v.close()
            globallock.release()
        except NumberException:
            time.sleep(5)
            continue
        except Exception as e:
            traceback.print_exc()
            print e
            maxq.put(1)
            print "Error creating account\n",
            print "{0}\n".format(e),
def mainfunc(id,name,email,maxval,password,country="US"):
    q=Queue.Queue()
    for i in range(0,maxval):
        q.put(1)
    for i in range(0,MAXTHREADS):
        Thread(target=dosignup,args=(id,name,email,q,password,maxval,country)).start()
def verifyName(nam):
	nam=nam.strip()
	if nam.count(" ")!=1:
		raise Exception
	if re.search("[^a-z|A-Z| ]",nam):
		raise Exception
def verifyEmail(email,usedom=False):
	try:
		if usedom:
			if email[0]!="@":
				raise Exception("If you want to use your own domain, enter @domain in nikemainemail\nFor example, @nike.com if you want to use emails from domain nike.com")
			return
	except TypeError:
		raise Exception("Invalid entry for nikemainemail")
	try:
		if email[-10:]!="@gmail.com":
			raise Exception("You need to enter a gmail address")
		if len(email)==10:
			raise TypeError
		if re.search("[^a-z|0-9|A-Z]",email[:-10]):
			raise Exception("You need a gmail username with only letters and numbers in it")
	except TypeError:
		raise Exception("Enter your gmail address properly")
def verifyPassword(password):
	try:
		if len(password)<8:
			raise Exception("The password needs to be of at least length 8")
		if re.search("[a-z]",password)==None:
			raise Exception("There needs to be at least one small letter in the password")
		if re.search("[A-Z]",password)==None:
			raise Exception("There needs to be at least one capital letter in the password")
		if re.search("[0-9]",password)==None:
			raise Exception("There needs to be at least one number in the password")
	except TypeError:
		raise Exception("Enter a proper password")
def getData(x):
	global GETSMSEMAIL,GETSMSTOKEN,NAME,MAINEMAIL,PASSWORD,MAX,SAVETOFILE,MAXTHREADS,MININTERVAL,PROXYLIST,COUNTRY,USEDOMAIN
	try:
		GETSMSEMAIL=x["getsmsemail"]
	except:
		print "You need to enter the email of your getsmscode account"
		exit()
	try:
		GETSMSTOKEN=x["getsmstoken"]
	except:
		print "You need to enter your api token from getsmscode.com"
		exit()
	try:
		NAME=x["nikeaccountname"]
		verifyName(NAME)
	except:
		print "You need to enter the name you want in your nike+ accounts properly"
		exit()
	try:
		USEDOMAIN=(x["useowndomain"]==True)
	except:
		USEDOMAIN=False
	try:
		MAINEMAIL=x["nikemainemail"]
		verifyEmail(MAINEMAIL,USEDOMAIN)
	except Exception as e:
		print e
		exit()
	try:
		PASSWORD=x["nikeaccountpassword"]
		verifyPassword(PASSWORD)
	except Exception as e:
		print e
		exit()
	try:
		MAX=int(x["maxaccounts"])
	except:
		print "Enter a proper value for the maximum number of accounts you want to generate"
		exit()
	try:
		SAVETOFILE=x["savetofile"]
		if len(SAVETOFILE)>50:
			raise Exception
		if re.search("[^\.|a-z|A-Z|0-9]",SAVETOFILE):
			raise Exception
	except:
		print "Enter a proper filename to save the accounts to, the name can have max 50 letters"
		exit()
	try:
		MAXTHREADS=int(x["maxthreads"])
		if MAXTHREADS<=0:
			raise Exception
	except:
		print "Enter a proper value for the maximum number of threads to use"
		exit()
	try:
		MININTERVAL=float(x["minintervalbetweenrequests"])
		if MININTERVAL<=0:
			raise Exception
	except:
		print "Enter a proper value for the minimum number of seconds between two requests from same IP, recommended value: 1"
		exit()
	try:
		PROXYFILENAME=x["proxyfilename"]
		PROXS=open(PROXYFILENAME,'r').read().split('\n')
		PROXYLIST=[p.strip() for p in PROXS if p.strip()!='']
		PROXYLIST.append(None)
	except:
		PROXYFILENAME=None
		PROXYLIST=[None]
	for p in PROXYLIST:
		allLocks[p]=TimedQueue()
		allLocks[p].put(1)
		MAINLOCKS[p]=Lock()
	try:
		COUNTRY=x["nikeaccountcountry"].upper()
		if COUNTRY not in ["US","EU"]:
			raise Exception
	except:
		print "Enter a proper country for the nike+ accounts, US or EU"
		exit()
	print "You have entered:\n\n"
	print "Your getsmscode email address: {0}".format(GETSMSEMAIL)
	print "Your getsmscode token: {0}".format(GETSMSTOKEN)
	print "The name you want on your nike accounts: {0}".format(NAME)
	if USEDOMAIN:
		print "The emails you want to use for the nike accounts: *******{0}".format(MAINEMAIL)
	else:
		print "Your main gmail account to use for the nike accounts: {0}".format(MAINEMAIL)
	print "The passwords for the nike+ accounts: {0}".format(PASSWORD)
	print "The country for the Nike+ accounts: {0}".format(COUNTRY)
	print "Maximum number of accounts you want to generate: {0}".format(MAX)
	print "The file you want to save the accounts to: {0}".format(SAVETOFILE)
	print "Maximum number of threads: {0}".format(MAXTHREADS)
	print "Minimum interval between two requests from same IP(in seconds): {0}".format(MININTERVAL)
	print "Loading proxylist from: {0}".format(PROXYFILENAME)
	return click.confirm("Do you want to continue? ")
if __name__=="__main__":
	try:
		config=json.loads(open("nikeconfig.json",'r').read())
	except:
		print "Error loading config file"
		exit()
	if not getData(config):
		exit()
	verifyinfo()
	blockall()
	mainfunc(SAVETOFILE,NAME,MAINEMAIL,MAX,PASSWORD,COUNTRY)
