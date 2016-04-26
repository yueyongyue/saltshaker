# -*- coding: utf-8  -*-
#!/bin/env python
'''
record main url customer accessed with post parameters

Created on 2016-03-31
'''
import  time
import urlparse
import urllib2
import logging

from datetime import datetime
from django.conf import settings




LOG_URL = (
    '/static',
    '/index.html',
    '/minions',
    '/execute',
    '/jobs',
    '/states_config',
    '/code_update',
    '/groups',
    '/system_setup',
         
)

EXCLUDE_URL = (
	"admin",
)

EXCLUDE_POST_URL = ( 
        "account",
        "login",
        
)

def custom_logger_constructor(_logger_name):
	_custom_logger = logging.getLogger(_logger_name)
	return _custom_logger

CUSTOM_LOGGER = custom_logger_constructor(
	"access", 
)
CUSTOM_ERROR_LOGGER = custom_logger_constructor(
	"error", 
)

def pretty_string(content):
	try:
		if not isinstance(content, basestring):
			content = str(content)
		if not isinstance(content, unicode):
			content = content.decode("utf-8")
		content = content.replace("\n", "").replace("\r", "")
	except:
		content = "fail_to_pretty_string"
	return content

class CustomerLogMiddleware(object):
	'''
	class to log access info include post parameters
	'''
	def __init__(self):
		self.start_time = 0
		self.end_time = 0
	
	def process_request(self, request):
		self.start_time = time.time()
	
	def url_need_log(self, _url):
		_flag = False
		_exclude = False
		for _item in LOG_URL:
			if _url.startswith(_item):
				for _ex_item in EXCLUDE_URL:
					if _url.startswith(_ex_item):
						_exclude = True
						break
				_flag = not _exclude
				break
		return _flag
	
	def url_need_log_post(self, _url):
		_flag = True
		for _item in EXCLUDE_POST_URL:
			if _url.startswith(_item):
				_flag = False
				break
		return _flag
	
	def _response(self, request, response=None, exception=None):
		'''
		@param request:
                '''
		_url =_host = _time = ""
		#try:
                if True:
			self.end_time = time.time()
			if not settings.CUSTOM_ACCESS_LOG_OPEN:
				return None

			_url = request.get_full_path()
			if not self.url_need_log(_url):
				return None
			_host = request.META.get("REMOTE_ADDR", "-")
			_time = datetime.now()
			_sp = request.META.get("SERVER_PROTOCOL", "-")
			_http_refer = request.META.get("HTTP_REFERER", "-")
			_agent = request.META.get("HTTP_USER_AGENT", "-")
			_method = request.method
			_post_param = ""
			if _method.upper()=="POST" and self.url_need_log_post(_url):
				try:
					_post_param = request.body
					if str(_post_param):
						_post_param = pretty_string(_post_param)
						#param sorted
						_param_list = _post_param.split("&")
						_param_list.sort()
						_post_param = '&'.join(_param_list)
					else:
						_post_param = "streaming"
				except Exception, e:
					_post_param = "post-except"
				
			#url param  error
			if _method.upper()=="GET":
				urlobject = urlparse.urlparse(_url)
				_url = urlobject.path
				_param_list = urlobject.query.split("&")
				_param_list.sort()
				_post_param = '&'.join(_param_list) 

			_full_url = urlparse.urlunparse(('', '', _url, '', _post_param, ''))
			try:
				_full_url = urllib2.unquote(str(_full_url)).decode('utf-8')
				_agent = urllib2.unquote(str(_agent)).decode("utf-8")
			except:
				pass
			if _full_url.endswith("&"): _full_url = _full_url[:-1]
			_status_code = "500"
			_content_length = "-"
			_result    = True
			if response:
				try:
					_content_length = len(response.content)
					_result = response.get("result", 'True').lower()
					_status_code = response.status_code
				except:
					pass
			_time_delta = self.end_time - self.start_time
			#LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
			_message = '%s - - [%s] "%s %s %s" %s %s "%s" "%s" "%s" %sms' %\
				(   pretty_string(_host),
					pretty_string(_time),
					pretty_string(_method),
					_full_url,
					pretty_string(_sp),
					pretty_string(_status_code),
					pretty_string(_content_length),
					pretty_string(_result),
					pretty_string(_http_refer),
					pretty_string(_agent),
					pretty_string(round(_time_delta*1000)) 
				)
			CUSTOM_LOGGER.info(_message)
		#except Exception, exp:
                else:
			try:
				CUSTOM_ERROR_LOGGER.error("[%s] access logging error...==>" % pretty_string(_time))
				CUSTOM_ERROR_LOGGER.error(_url)
				CUSTOM_ERROR_LOGGER.exception(exp)
			except:
				pass

		return None
            
	def process_response(self, request, response):
		self._response(request, response)
		return response
