import logging

logger = logging.getLogger('factory.generate')

from . import base, declarations, utils


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


class KeyPropertyFactory(declarations.ParameteredAttribute):
    """A factory that is somehwat similar to SubFactory only it returns the key for the created model instance.
    Due to the nature of ndb.KeyProperty, we also always have to use create strategy
    """

    EXTEND_CONTAINERS = True

    def __init__(self, factory, **kwargs):
        super(KeyPropertyFactory, self).__init__(**kwargs)
        self.factory_wrapper = declarations._FactoryWrapper(factory)

    def get_factory(self):
        """Retrieve the wrapped factory.Factory subclass."""
        return self.factory_wrapper.get()

    def generate(self, step, params):
        """Evaluate the current definition and fill its attributes."""
        subfactory = self.get_factory()
        create = True
        logger.debug("SubFactory: Instantiating %s.%s(%s), create=%r",
                     subfactory.__module__, subfactory.__name__,
                     utils.log_pprint(kwargs=params),
                     create,
                     )
        return subfactory.simple_generate(create, **params).key


class StructuredPropertyFactory(declarations.ParameteredAttribute):
    """A factory that is somehwat similar to SubFactory only it returns the key for the created model instance.
    Due to the nature of ndb.KeyProperty, we also always have to use create strategy
    """

    EXTEND_CONTAINERS = True

    def __init__(self, factory, **kwargs):
        super(StructuredPropertyFactory, self).__init__(**kwargs)
        self.factory_wrapper = declarations._FactoryWrapper(factory)

    def get_factory(self):
        """Retrieve the wrapped factory.Factory subclass."""
        return self.factory_wrapper.get()

    def generate(self, step, params):
        """Evaluate the current definition and fill its attributes."""
        subfactory = self.get_factory()
        create = True
        logger.debug("SubFactory: Instantiating %s.%s(%s), create=%r",
                     subfactory.__module__, subfactory.__name__,
                     utils.log_pprint(kwargs=params),
                     create,
                     )
        return subfactory.simple_generate(False, **params)
