import importlib
from ..exceptions import WebEngineAbsent


def get_adapter_for_webengine(webengine):

    try:
        module = importlib.import_module('.' + webengine, package=__package__)
        return module.HttpEngineAdapter
    except ImportError:
        raise WebEngineAbsent('{} webengine is absent'.format(webengine))
