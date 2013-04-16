import logging
import logging.handlers

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('MyLogger')
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(module)s -%(message)s')
        self.handler = logging.handlers.SysLogHandler(("localhost",514),'local0')
        self.handler.setFormatter(formatter);
        self.logger.addHandler(self.handler)
    def trace_back(self,tb):
         tb_out = StringIO.StringIO()
         traceback.print_tb(tb,None,tb_out);
         self.logger.error(tb_out.getvalue());
         tb_out.close();


def main():         
    L = Logger()
    L.logger.warn("fdsafsd\n\n")
