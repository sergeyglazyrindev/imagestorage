import importlib
from ..exceptions import WebEngineAbsent


def get_adapter_for_webengine(webengine):

    try:
        return importlib.import_module('.' + webengine + '.HttpEngineAdapter', package=__package__)
    except ImportError:
        raise WebEngineAbsent('{} webengine is absent'.format(webengine))
