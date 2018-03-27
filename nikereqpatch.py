from requests.adapters import HTTPAdapter
import user_agents
import urlparse
from collections import OrderedDict
def modifyheaders(headers):
    headerorder=["Host","Connection","Content-Length","X-NewRelic-ID","Origin","User-Agent","Content-Type","Accept","Referer","Accept-Encoding","Accept-Language","Cookie"]
    finalheader=OrderedDict()
    for q in headerorder:
        if q in headers:
            finalheader[q]=headers[q]
    for q in headers:
        finalheader[q]=headers[q]
    return finalheader
def modded_add_headers(adapter,req,**kwargs):
    req.headers=modifyheaders(req.headers)
HTTPAdapter.add_headers=modded_add_headers