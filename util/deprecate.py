import logging
import warnings
import functools
import custom_logging


def deprecated(func):
    @functools.wraps(func)
    def deprecation_wrapper(*args, **kwargs):
        logger: custom_logging.FileStreamLogger = custom_logging.FileStreamLogger(console=True, colors=True)
        logger.critical(f"Usage of deprecated module: {func.__name__} has been detected.")
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn(f"Call to deprecated function {func.__name__}.",
                      category=DeprecationWarning,
                      stacklevel=2
                      )
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)

    return deprecation_wrapper
