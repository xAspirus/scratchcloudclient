import threading
import websocket
import json


websocket.WebSocket.send_packet = lambda self, x: self.send(json.dumps(x) + '\n')


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



	def set_variable(self, variable_name :str, value :str):
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
