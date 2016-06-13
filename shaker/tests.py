from execute.models import Modindex
import urllib
import urllib2
import re
import time

req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept':'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Connection':'close',
    'Referer':None,
    }
def getPage(url):
        request = urllib2.Request(url,None,req_header)
        response = urllib2.urlopen(request)
        index = response.read().decode('utf-8')
        pattern = re.compile('(salt.modules.*).html')
        items = re.findall(pattern,index)
        return items

all_fun = []
def getfun():
    salt_modindex = getPage('http://docs.saltstack.com/en/latest/salt-modindex.html')
    for i in salt_modindex[307:]:
        url = 'http://docs.saltstack.com/en/latest/ref/modules/all/'+ i + '.html#module-' + i
        print url
        request = urllib2.Request(url,None,req_header)
        response = urllib2.urlopen(request)
        index = response.read().decode('utf-8')
        #print index
        pattern_name = re.compile('<code class="descname">(.*)</code>')
        pattern_info = re.compile('<dd><p>(.*)</p>')
        pattern_example = re.compile('<pre>(.*)')
        items_name = re.findall(pattern_name,index)
        #items_info = re.findall(pattern_info,index)
        #items_example = re.findall(pattern_example,index)
        i_fun = i.split('.')[2]
        print i_fun
        print items_name
        #print items_info
        #print items_example
        for i in items_name:
            modindex = Modindex()
            name = i_fun + '.' + i
            modindex.module_name = name
            modindex.save()
            time.sleep(1)
            print i_fun + '.' + i
        '''
        modindex = Modindex()
        modindex.module_name = i_fun
        modindex.module_fun = items_name
        modindex.module_des = items_info
        modindex.module_exa = items_example
        modindex.save()
        time.sleep(2)
        #fun_dict = {i_fun:items}
        #all_fun.append(fun_dict)
        #return items


#print salt_modindex
#print len(salt_modindex)
#salt_fun = getfun()
#print salt_fun
        '''
#salt_fun = getfun()
#salt_modindex = getPage('http://docs.saltstack.com/en/latest/salt-modindex.html')
#print salt_modindex[307:]