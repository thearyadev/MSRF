import logging
import warnings
import functools


def deprecated(func):
    @functools.wraps(func)
    def deprecation_wrapper(*args, **kwargs):
        logger: logging.Logger = logging.getLogger("msrf")
        logger.critical(f"Usage of deprecated module: {func.__name__} has been detected.")
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn(f"Call to deprecated function {func.__name__}.",
                      category=DeprecationWarning,
                      stacklevel=2
                      )
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return deprecation_wrapper
