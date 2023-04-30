import logging

class Logger:
    def __init__(self, name, level=logging.DEBUG, filename='app.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.handler = logging.FileHandler(filename)
        self.handler.setLevel(level)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
    
    def __getattr__(self, name):
        if name in ('debug', 'info', 'warning', 'error', 'critical'):
            return getattr(self.logger, name)
        raise AttributeError(f"'Logger' object has no attribute '{name}'")
