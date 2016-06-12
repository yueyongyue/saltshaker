from execute.models import Modindex
import urllib2
import re
import time

req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept':'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Connection':'close',
    'Referer':None,
    }

def get_modindex(url):
        request = urllib2.Request(url, None, req_header)
        response = urllib2.urlopen(request)
        index = response.read().decode('utf-8')
        pattern = re.compile('(salt.modules.*).html')
        items = re.findall(pattern, index)
        return items

all_fun = []
def get_module():
    modindex = Modindex.objects.all()
    modindex.delete()
    salt_modindex = get_modindex('http://docs.saltstack.com/en/latest/salt-modindex.html')
    print salt_modindex
    for mod in salt_modindex:
        url = 'http://docs.saltstack.com/en/latest/ref/modules/all/' + mod + '.html#module-' + mod
        print url
        request = urllib2.Request(url, None, req_header)
        try:
            response = urllib2.urlopen(request)
        except:
            time.sleep(10)
            response = urllib2.urlopen(request)
        index = response.read().decode('utf-8')
        pattern_name = re.compile('<code class="descname">(.*)</code>')
        #pattern_info = re.compile('<dd><p>(.*)</p>')
        #pattern_example = re.compile('<pre>(.*)')
        items_name = re.findall(pattern_name, index)
        #items_info = re.findall(pattern_info,index)
        #items_example = re.findall(pattern_example,index)
        mod_fun = mod.split('.')[2]
        print mod_fun
        print items_name
        #print items_info
        #print items_example
        for i in items_name:
            modindex = Modindex()
            if mod_fun == 'sysmod':
                mod_fun = 'sys'
            name = mod_fun + '.' + i
            modindex.module_name = name
            modindex.save()
            time.sleep(1)
            print name
