from ssl import SSLSocket
oldinit=SSLSocket.__init__
def newinit(*args,**kwargs):
	kwargs["_context"]=None
	kwargs["ssl_version"]=SSLVERSION
	return oldinit(*args,**kwargs)
SSLSocket.__init__=newinit
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
getsmsqueue=TimedQueue()
def getsmslock():
	getsmsqueue.get()
	getsmsqueue.put(1,5)
def _blocknumber():
    sess=requests.session()
    v={}
    while True:
        while True:
            try:
                yu=BLOCKQUEUE.get_nowait()
                v[yu]=1
                try:
                    sess.post("http://www.getsmscode.com/do.php",data={"action":"addblack","username":GETSMSEMAIL,"token":GETSMSTOKEN,"pid":"462","mobile":yu},timeout=30)
                    print "Blocking {0}\n".format(yu),
                except:
                    pass
            except:
                break
        if len(v)==0:
            yu=BLOCKQUEUE.get()
            v[yu]=1
            try:
                sess.post("http://www.getsmscode.com/do.php",data={"action":"addblack","username":GETSMSEMAIL,"token":GETSMSTOKEN,"pid":"462","mobile":yu},timeout=30)
                print "Blocking {0}\n".format(yu),
            except:
                pass
            continue
        try:
            mobilelist=sess.post("http://www.getsmscode.com/do.php",data={"action":"mobilelist","username":GETSMSEMAIL,"token":GETSMSTOKEN},timeout=30).text
            for p in v.keys():
                if p not in mobilelist:
                    if v[p]>=10:
                        v.pop(p,None)
                    else:
                        v[p]+=1
                else:
                    try:
                        sess.post("http://www.getsmscode.com/do.php",data={"action":"addblack","username":GETSMSEMAIL,"token":GETSMSTOKEN,"pid":"462","mobile":p},timeout=30)
                        print "Blocking {0}\n".format(p),
                    except:
                        pass
        except:
            pass
        time.sleep(1)
BLOCKQUEUE=Queue.Queue()
for i in range(0,20):
    Thread(target=_blocknumber).start()
def blocknumber(num):
    BLOCKQUEUE.put(num)
def verifyinfo():
	m=getsmssession.post("http://www.getsmscode.com/do.php",data={"action":"login","username":GETSMSEMAIL,"token":GETSMSTOKEN})
	n=m.text.split("|")
	if len(n)==2:
		print m.text+"\n",
		print "Invalid info entered for getsmscode.com\n",
		exit()
def getsession(prox,p,q,r):
    sess=requests.session()
    print "Trying to get abck cookie"
    allLocks[prox].get()
    try:
        bot=BotDetector()
        bot.url=q
        payload="{\"sensor_data\":\""+bot.generatesensordata()+"\"}"
        d=sess.post(p,headers={"Connection":"keep-alive","X-NewRelic-ID":"VQYGVF5SCBAJVlFaAQIH","Origin":r,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36","Content-Type":"text/plain;charset=UTF-8","Accept":"*/*","Referer":q,"Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"},proxies={"https":prox},data=payload,verify=False,timeout=15)
        bot.cookie=sess.cookies["_abck"]
        payload="{\"sensor_data\":\""+bot.generatesensordata1()+"\"}"
        d=sess.post(p,headers={"Connection":"keep-alive","X-NewRelic-ID":"VQYGVF5SCBAJVlFaAQIH","Origin":r,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36","Content-Type":"text/plain;charset=UTF-8","Accept":"*/*","Referer":q,"Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"},proxies={"https":prox},data=payload,verify=False,timeout=15)
        if "~0~" in sess.cookies["_abck"]:
            print sess.cookies["_abck"]
            allLocks[prox].put(1,MININTERVAL)
            return sess
    except Exception as e:
        print e
    allLocks[prox].put(1,MININTERVAL)
    raise Exception("Error getting cookie")
def reverify(sess,prox,p,q,r):
    allLocks[prox].get()
    try:
        bot=BotDetector()
        bot.cookie=sess.cookies["_abck"]
        payload="{\"sensor_data\":\""+bot.generatesensordata1()+"\"}"
        d=sess.post(p,headers={"Connection":"keep-alive","X-NewRelic-ID":"VQYGVF5SCBAJVlFaAQIH","Origin":r,"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36","Content-type":"text/plain;charset=UTF-8","Accept":"*/*","Referer":q,"Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"},proxies={"https":prox},data=payload,verify=False,timeout=15)
        if "~0~" in sess.cookies["_abck"]:
            print repr(sess.cookies["_abck"])
            allLocks[prox].put(1,MININTERVAL)
            return sess
    except:
        pass
    try:
        sess.close()
    except:
        pass
    allLocks[prox].put(1,MININTERVAL)
    raise Exception("Error getting abck cookie")
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
    getsmslock()
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
        sess=getsession(prox,"https://s3.nikecdn.com/_bm/_data","https://s3.nikecdn.com/unite/mobile.html","https://s3.nikecdn.com")
        sess.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"})
        getLock(prox)
        sess.cookies["CONSUMERCHOICE"]="cn/zh_cn"
        sess.cookies["NIKE_COMMERCE_COUNTRY"]="CN"
        sess.cookies["NIKE_COMMERCE_LANG_LOCALE"]="zh_CN"
        sess.cookies["nike_locale"]="cn/zh_cn"
        dob="{0}-{1:02d}-{2:02d}".format(random.randint(1990,1998),random.randint(1,12),random.randint(1,28))
        if country=="US":
            locale="en_US" 
        else:
            country="GB"
            locale="en_GB"
        payload={"country":country,"emailOnly":False,"firstName":nam[0],"gender":random.choice(["F","M"]),"lastName":nam[1],"locale":locale,"password":password,"receiveEmail":False,"registrationSiteId":"nikedotcom","welcomeEmailTemplate":"TSD_PROF_MS_WELC_T0_GENERIC_V1.0","emailAddress":email,"dateOfBirth":dob,"username":email,"account":{"email":email,"passwordSettings":{"password":password,"passwordConfirm":password}}}
        getLock(prox)
        print "Signing up with email {0}\n".format(email),
        r=sess.post("https://s3.nikecdn.com/access/users/v1?appVersion=447&experienceVersion=374&uxid=com.nike.unite&locale=en_US&backendEnvironment=&browser=&os=undefined&mobile=true&native=true&visit=&visitor=&language=en-US",json=payload,verify=False,proxies={"https":prox},headers={"Referer":"https://www.nike.com/"+country.lower()+"/"+locale.lower(),"Origin":"https://www.nike.com","Content-Type":"application/json"},timeout=30)
        if r.status_code!=400:
            r.raise_for_status()
        getLock(prox)
        m_login_data = {'keepMeLoggedIn':True, 'client_id':'PbCREuPr3iaFANEDjtiEzXooFl7mXGQ7','ux_id':'com.nike.commerce.snkrs.droid','grant_type':'password','username':email,'password':password}
        e=sess.post('https://api.nike.com/idn/shim/oauth/2.0/token',json=m_login_data,verify=False,proxies={"https":prox},timeout=30)
        TOKEN=json.loads(e.text)['access_token']
        sess.close()
    sess=getsession(prox,"https://www.nike.com/_bm/_data","https://www.nike.com/us/en_us","https://www.nike.com")
    sess1=getsession(prox,"https://www.nike.com/_bm/_data","https://www.nike.com/us/en_us","https://www.nike.com")
    sess.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"})
    sess1.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"})
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
        time.sleep(2)
    if not ok:
        sess.close()
        sess1.close()
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
        sess.close()
        sess1.close()
        if NUMBER!=None:
            blocknumber("86"+NUMBER)
        raise e
    sess.close()
    sess1.close()
    blocknumber("86"+NUMBER)
    return password
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
	global GETSMSEMAIL,GETSMSTOKEN,NAME,MAINEMAIL,PASSWORD,MAX,SAVETOFILE,MAXTHREADS,MININTERVAL,PROXYLIST,COUNTRY,USEDOMAIN,GETSMSTHREADLIMIT,SSLVERSION
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
		GETSMSTHREADLIMIT=int(x["getsmsthreadlimit"])
		if GETSMSTHREADLIMIT<=0:
			raise Exception
	except:
		print "Enter a proper value for the getsmscode thread limit"
		exit()
	try:
		SSLVERSION=int(x["sslversion"])
		if SSLVERSION not in [3,4]:
			raise Exception
	except:
		print "Enter proper value for SSL Version, 3 for TLS v1 and 4 for TLS v1.1"
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
	print "Getsmscode thread limit: {0}".format(GETSMSTHREADLIMIT)
	print "SSL version: {0}".format(["TLS v1","TLS v1.1"][SSLVERSION-3])
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
	for i in range(0,int(GETSMSTHREADLIMIT/2)):
		getsmsqueue.put(1)
	mainfunc(SAVETOFILE,NAME,MAINEMAIL,MAX,PASSWORD,COUNTRY)
