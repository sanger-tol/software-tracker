import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from api import *


class TestingCursorIterator:
	__test__ = False

	def __init__(self, cursor):
		self._cursor = cursor
		self._index = 0

	def __next__(self):
		if self._index < len(self._cursor.results):
			result = self._cursor.results[self._index]
			self._index += 1
			return result
		raise StopIteration

class TestingCursor:
	__test__ = False

	data = {
		'logging_event#foo' : [ {'id':123} ],
	}

	def __init__(self,db):
		self._db = db
		self._rows = []

	def __iter__(self):
		return TestingCursorIterator(self)

	def execute(self,query,args):
		self.results = []
		self.lastrowid = 0
		
		if query=="""INSERT IGNORE INTO `logging_event` (`uuid`,`user`,`timestamp`,`image`,`executable`,`path`,`parameters`) VALUES (uuid(),%s,%s,%s,%s,%s,%s)""":
			if args == ('xyz9', '2020-03-02 11:22:33', 'the_image.sif', 'run_me', '/nfs/foo/bar', 'the_first "the last" \'eternity\''):
				self.lastrowid = 12345
			else:
				self.lastrowid = 0

		else:
			print ("TestingCursor::execute UNRECOGNIZED")
			print (query)
			print (args)

class TestingDB:
	__test__ = False

	def __init__(self):
		return

	def cursor(self,buffered=False,dictionary=False):
		return TestingCursor(self)

	def commit(self):
		return


@pytest.fixture
def client():
    global app
    app.config['TESTING'] = True
    app.test_db = TestingDB()
    return app.test_client()
