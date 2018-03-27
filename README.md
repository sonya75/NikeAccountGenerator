# NikeAccountGenerator
## Run using python 2.7

Script to generate verified Nike+ accounts using getsmscode.com


## Instructions

  * All info related to the gmail or custom domain to be used in the accounts, account password, getsmscode account email and api token, those will need to be entered in the nikeconfig.json file. You can open the file in any text editor (like Notepad for example) and edit it.
    * First field in nikeconfig.json is **getsmsemail**, which is the email on your account in getsmscode.com.
    * You can get the API token from getsmscode for your account and enter it in the **getsmstoken** field.
    * The field **nikeaccountname** is to specify the name you want on the nike accounts.
    * **nikemainemail** is the main gmail address you want to use(i.e it will generate the emails for the accounts using dot trick and plus trick on the gmail) or if you want to use your own domain, enter @yourdomain.com instead of a gmail address.
    * If you use your own domain, enter true in **useowndomain** field.
    * **nikeaccountpassword** is the password you want on all the nike accounts.
    * **maxaccounts** is how many accounts you want to make.
    * **savetofile** field is to specify the file where all the account info will be saved.
    * **maxthreads** is the maximum number of threads you want to use. (if you are not a programmer and don't understand it, don't bother changing this field).
    * **proxyfilename** is the file where you want the script to load proxies from.
    * You can enter US or EU in the **nikeaccountcountry** field.
    * **minintervalbetweenrequests** is to specify the minimum interval between requests from the same IP, to be safe the default value is set to 1 second, you can change it to 0.5 if you want, but if you get banned, that's on you.

## Proxy File format

The proxies in the proxy file needs to be in the following format.

```http://username:password@ip:port```

That's for http proxy, its similar for socks proxies. Enter one proxy per line.

## Required modules

You will need to install the following modules before running the script:- ``` requests, names, click ```
So, you can run these commands from the command prompt (assuming you have installed python 2.7 and added the proper folders to PATH):-

```
pip install requests names click numpy
```

### Happy Account Generating !!!


The place where it all started: https://twitter.com/JonesUnk

The nike+ account generator in action through a web interface:-

http://serverdestroyers.com/


## A Note About the Bot Detection

In nikesensor.py file, there is a global variable named DEVICESIGNATURE is defined. This signature is not device specific, its actually times taken for different types of calculation like sin, cos, ..... It depends on CPU load as well. The same signature can be easily produced from multiple devices. But still, it will be very easy to block a signature. So I will update it to produce a properly randomized value soon.
