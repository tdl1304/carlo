import sys

def log(*args, **kwargs):
    file = kwargs.pop('file', sys.stderr)
    print(*args, **kwargs, file=file)

def debug(*args, **kwargs):
    log('[debug]', *args, **kwargs)

def info(*args, **kwargs):
    log('[info] ', *args, **kwargs)
