# -*- coding: utf-8 -*-
import platform

class os:
	def __init__(self):
		platform.system()

	def osWindows(self):
		if platform.system() == 'Linux':
			return False
		else:
			return True

	def changeDir(self,SystemOS):
		import os
		if SystemOS == False:
			path = '/export'
			if os.path.exists(path):
				return path
			else:
				return False
			
		else:
			return 'Jiny OS'

i = os()
zjisti= i.osWindows()
print i.changeDir(zjisti)