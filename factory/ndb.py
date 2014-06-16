from __future__ import unicode_literals

from google.appengine.ext import ndb

from . import base

class NDBModelFactory(base.Factory):
    """Factory for Google AppEngine NDB models. """

    class Meta:
        abstract = True
        
    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        return model_class(*args, **kwargs)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        obj = model_class(*args, **kwargs)
        obj.put()
        return obj