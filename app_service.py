import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time
from app import app  # Import your Flask app from app.py

class AppService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Amazebot"
    _svc_display_name_ = "Amazebot-Amazon tracker"
    _svc_description_ = "Script to track the price of amazon products"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        self.main()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def main(self):
        app.run(host='0.0.0.0', port=5000)  # Run your Flask app here

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppService)
