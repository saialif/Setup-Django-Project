import logging


def get_logger(name=__name__):
    """Get a logger instance with the specified name.
    By default, it uses the logger name based on the module's __name__."""
    return logging.getLogger(name)


def make_key_prefix(key, key_prefix, version):
    return "ARC:%s:%s:%s" % (key_prefix, version, key)


def bytes_to_mb(size_in_bytes):
    """Convert file size from bytes to megabytes (MB), rounded to 2 decimal places."""
    size_in_mb = size_in_bytes / (1024 * 1024)
    return f"{round(size_in_mb, 2)} MB"
