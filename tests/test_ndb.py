import sys

import factory
from .compat import unittest

sys.path.append('/usr/local/google_appengine/')

try:
    from google.appengine.ext import ndb
    from google.appengine.ext import testbed
except ImportError:
    ndb = False
    testbed = False

if ndb:
    from factory.ndb import NDBModelFactory

    class Person(ndb.Model):
        name = ndb.StringProperty()

    class PersonFactory(NDBModelFactory):
        class Meta:
            model = Person

        name = factory.Sequence(lambda n: 'name%d' % n)
    
    
@unittest.skipIf(ndb is None, "Google AppEngine is not installed.")
class NDBTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        

    def test_build(self):
        m = PersonFactory.build()
        self.assertIsNotNone(m.name)

    def test_creation(self):
        person = PersonFactory.create()
        self.assertEqual('name1', person.name)
        self.assertIsNotNone(person.key)    