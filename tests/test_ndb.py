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

    class Address(ndb.Model):
        name    = ndb.StringProperty() # E.g., 'home', 'work'
        street  = ndb.StringProperty()
        city    = ndb.StringProperty()

    class Person(ndb.Model):
        name = ndb.StringProperty()
        address = ndb.StructuredProperty(Address)
        
    class AddressFactory(NDBModelFactory):
        class Meta:
            model = Address

        street = factory.Sequence(lambda n: 'street%d' % n)
        city   = factory.Sequence(lambda n: 'city%d' % n)

    class PersonFactory(NDBModelFactory):
        class Meta:
            model = Person

        name = factory.Sequence(lambda n: 'name%d' % n)
        address = factory.SubFactory(AddressFactory)
    
    
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
        p = PersonFactory.build()
        self.assertEqual('name0', p.name)
        self.assertEqual('street0', p.address.street)

    def test_creation(self):
        person = PersonFactory.create()
        self.assertEqual('name1', person.name)
        self.assertEqual('street1', person.address.street)
        self.assertIsNotNone(person.key)    