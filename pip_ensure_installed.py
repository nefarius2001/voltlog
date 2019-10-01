# https://stackoverflow.com/questions/12332975/installing-python-module-within-code
import sys 
import subprocess


def pip_ensure_installed(package_name_import, package_name_install = ''):
	print(sys.executable)
	if(len(package_name_install)==0):
		package_name_install = package_name_import
	import importlib
	try:
		#print 'test import_module now'
		importlib.import_module(package_name_import)
		#print 'test import_module ok'
	except ImportError:
		#print 'ImportError'
		subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name_install])
		#print 'pip install done'


