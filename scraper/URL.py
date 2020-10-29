class URL:
	def __init__(self, url):
		prorocol_link = url.split('://')
		if len(prorocol_link) == 1:
			prorocol_link = ['', url]
		
		protocol, link = prorocol_link
		host, *path = link.split('/')
		path = '/'.join(path)

		path_query = path.split('?')
		if len(path_query) == 1:
			path_query = [path, '']

		path, query = path_query
		domain = '.'.join(host.split('.')[-2:]).split(':')[0]
		
		self.protocol = protocol
		self.path = path
		self.domain = domain
		self.host = host
		self.query = query

		self.params = None
		self.__get_params()

	def __get_params(self):
		query = self.query
		if not query: return

		params = {}
		query = query.split('&')

		for q in query:
			name, val = q.split('=')
			params[name] = val

		self.params = params

