import sys

sys.path.append('/usr/local/google_appengine/')

import factory
from factory import ndb as factory_ndb
import unittest

try:
    from google.appengine.ext import ndb
    from google.appengine.ext import testbed

except ImportError:
    ndb = None
    testbed = None

if ndb:
    from factory.ndb import NDBModelFactory


    class Color(ndb.Model):
        name = ndb.StringProperty()


    class Address(ndb.Model):
        name = ndb.StringProperty()  # E.g., 'home', 'work'
        street = ndb.StringProperty()
        city = ndb.StringProperty()


    class Person(ndb.Model):
        name = ndb.StringProperty()
        address = ndb.StructuredProperty(Address)
        color = ndb.KeyProperty(Color)


    class ColorFactory(NDBModelFactory):
        class Meta:
            model = Color

        name = factory.Sequence(lambda n: 'color%d' % n)


    class AddressFactory(NDBModelFactory):
        class Meta:
            model = Address

        street = factory.Sequence(lambda n: 'street%d' % n)
        city = factory.Sequence(lambda n: 'city%d' % n)


    class PersonFactory(NDBModelFactory):
        class Meta:
            model = Person

        name = factory.Sequence(lambda n: 'name%d' % n)
        # address = factory.SubFactory(AddressFactory)
        address = factory_ndb.StructuredPropertyFactory(AddressFactory)
        color = factory_ndb.KeyPropertyFactory(ColorFactory)


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
        self.assertEqual('color0', p.color.get().name)

    def test_creation(self):
        person = PersonFactory.create()
        self.assertEqual('name1', person.name)
        self.assertEqual('street1', person.address.street)
        self.assertIsNotNone(person.key)