

class ExtensionLoadError(Exception):
    """Error of loading pollster plugin.

    PollsterBase provides a hook, setup_environment, called in pollster loading
    to setup required HW/SW dependency. Any exception from it would be
    propagated as ExtensionLoadError, then skip loading this pollster.
    """
    pass