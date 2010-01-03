"""Wrapper around vboxapi.VirtualBoxManager"""

import vboxapi
import VirtualBoxException

class VirtualBoxManager(vboxapi.VirtualBoxManager):

    def __init__(self, style=None, params=None):
        try:
            vboxapi.VirtualBoxManager.__init__(self, style, params)
        except Exception, e:
            VirtualBoxException.handle_exception(e)
            raise

    def waitForEvents(self, timeout=None):
        """Wait for an event.

        Timeout is in miliseconds (I think)."""
        if timeout is None:
            # No timeout
            timeout = 0
        try:
            vboxapi.VirtualBoxManager.waitForEvents(self, timeout)
        except Exception, e:
            VirtualBoxException.handle_exception(e)
            raise


    def getIVirtualBox(self):
        return self.vbox

    def isMSCOM(self):
        """This this a MSCOM manager?"""
        return (self.type == 'MSCOM')

class Constants:
    _manager = VirtualBoxManager()
    
    # Pass any request for unrecognized method or attribute on to
    # XPCOM object. We do this since I don't know how to inherit the
    # XPCOM class directly.
    class __metaclass__(type):
        def __getattr__(cls, name):
            return eval("cls._manager.constants." + name)
