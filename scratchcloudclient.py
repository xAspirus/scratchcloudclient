from rich import print
import threading
import requests
import websocket
import json
import re
from getpass import *


websocket.WebSocket.send_packet = lambda self, x: self.send(json.dumps(x) + '\n')


class ScratchSession:
	def __init__(
	             self,
	             username :str,
	             password :str = None,
	             user_agent :str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
	            ):
		""" Leave password to prompt for password """
		self.username = username
		self.token = None
		self.csrf_token = None
		self.session_id = None
		self.user_agent = user_agent

		if password is None: password = getpass()
		
		self.login(password)

	def login(self, password):
		request = requests.post(
			'https://scratch.mit.edu/login/', 
			data = json.dumps({'username': self.username, 'password': password}),
			headers = {
				'x-csrftoken': 'a',
				'x-requested-with': 'XMLHttpRequest',
				'Cookie': 'scratchcsrftoken=a;scratchlanguage=en;',
				'referer': 'https://scratch.mit.edu',
				'user-agent': self.user_agent
			}
		)
		
		request_json = request.json()[0]

		if request_json['success'] == 0:
			if request_json['msg'] == '':
				raise Exception('Login time-out')
			
			raise Exception('Incorrect username or password.')
		
		self.token = request_json['token']
		self.session_id = re.search(r'"(.*)"', request.headers['Set-Cookie']).group(0)

		request = requests.get(
			'https://scratch.mit.edu/csrf_token/',
			headers = {
				'x-requested-with': 'XMLHttpRequest',
				'Cookie': 'scratchlanguage=en;permissions=%7B%7D;',
				'referer': 'https://scratch.mit.edu',
				'user-agent': self.user_agent
			}
		)

		self.csrf_token = re.search(
			r'scratchcsrftoken=(.*?);', request.headers['Set-Cookie']
		).group(1)
	
	def create_cloud_session(self, project_id :str):
		return CloudConnection(project_id, self)


class CloudConnection:
	def __init__(self, project_id, session):
		self.session = session
		self.project_id = project_id
		self.variables = {}
		self.ws = websocket.WebSocket()
		self.connect()
		threading.Thread()

	def connect(self):
		self.ws.connect(
			'wss://clouddata.scratch.mit.edu',
			cookie=f'scratchsessionsid={self.session.session_id};',
			origin='https://scratch.mit.edu'
		)

		self.ws.send_packet({
			'method': 'handshake',
			'user': self.session.username,
			'project_id': self.project_id
		})

		response = self.ws.recv().split('\n')
		for variable in response:
			if variable == '': continue
			variable = json.loads(variable)
			self.variables[variable['name'][2:]] = variable['value']



	def set_variable(self, variable_name :str, value :int):
		"""
		variable_name should not start with cloud emoji
		"""
		self.ws.send_packet({
			'method': 'set',
			'user': self.session.username,
			'project_id': self.project_id,
			'name': f'☁️ {variable_name}',
			'value': value
		})

	
	def update(self):
		""" Waits for variable updates for self.variables """
		response = json.loads(self.ws.recv())
		if response['method'] == 'set':
			self.variables[response['name'][2:]] = response['value']

	def on_cloud_update(self, func):
		""" Calls func when cloud variables are updated in a thread """
		def loop(self):
			while True:
				self.update()
				func(self)
		
		threading.Thread(target=loop, args=(self,)).start()