"""Basic exceptions for pyVBox."""

import sys

######################################################################
# Constants from IDL file. I can't find a way to programmatically
# get at these through the python API.

# Object corresponding to the supplied arguments does not exist.
VBOX_E_OBJECT_NOT_FOUND = 0x80BB0001

# Current virtual machine state prevents the operation.
VBOX_E_INVALID_VM_STATE = 0x80BB0002

# Virtual machine error occurred attempting the operation.
VBOX_E_VM_ERROR = 0x80BB0003

# File not accessible or erroneous file contents.
VBOX_E_FILE_ERROR = 0x80BB0004

# Runtime subsystem error.
VBOX_E_IPRT_ERROR = 0x80BB0005

# Pluggable Device Manager error.
VBOX_E_PDM_ERROR = 0x80BB0006

# Current object state prohibits operation.
VBOX_E_INVALID_OBJECT_STATE = 0x80BB0007

# Host operating system related error.
VBOX_E_HOST_ERROR = 0x80BB0008

# Requested operation is not supported.
VBOX_E_NOT_SUPPORTED = 0x80BB0009

# Invalid XML found.
VBOX_E_XML_ERROR = 0x80BB000A

# Current session state prohibits operation.
VBOX_E_INVALID_SESSION_STATE = 0x80BB000B

# Object being in use prohibits operation. 
VBOX_E_OBJECT_IN_USE = 0x80BB000C

######################################################################
# Constants I've found experimentally. Names are of my own creation.

# Returned from Progress.waitForCompletion()
VBOX_E_ERROR_ABORT = 0x80004004 

# Returned when VirtualMachine.open() method doesn't find a file
VBOX_E_FILE_NOT_FOUND = 0x80004005

# Returned if VirtualMachine.memorySize is set out of range
XPCOM_E_INVALID_ARGUMENT = 0x80070057

# Returned when getting machine attribute from closed session
VBOX_E_SESSION_CLOSED = 0x8000ffff

######################################################################

class VirtualBoxException(Exception):
    """Base exception for pyVBox exceptions."""
    pass

class VirtualBoxObjectNotFoundException(VirtualBoxException):
    """Object corresponding to the supplied arguments does not exist."""
    errno = VBOX_E_OBJECT_NOT_FOUND

class VirtualBoxInvalidVMStateException(VirtualBoxException):
    """Current virtual machine state prevents the operation."""
    errno = VBOX_E_INVALID_VM_STATE

class VirtualBoxVMError(VirtualBoxException):
    """Virtual machine error occurred attempting the operation."""
    errno = VBOX_E_VM_ERROR

class VirtualBoxFileError(VirtualBoxException):
    """File not accessible or erroneous file contents."""
    errno = VBOX_E_FILE_ERROR

class VirtualBoxRuntimeSubsystemError(VirtualBoxException):
    """Runtime subsystem error."""
    errno = VBOX_E_IPRT_ERROR

class VirtualBoxPluggableDeviceManagerError(VirtualBoxException):
    """Pluggable Device Manager error."""
    errno = VBOX_E_PDM_ERROR

class VirtualBoxInvalidObjectState(VirtualBoxException):
    """Current object state prohibits operation."""
    errno = VBOX_E_INVALID_OBJECT_STATE

class VirtualBoxHostError(VirtualBoxException):
    """Host operating system related error."""
    errno = VBOX_E_HOST_ERROR

class VirtualBoxNotSupportException(VirtualBoxException):
    """Requested operation is not supported."""
    errno = VBOX_E_NOT_SUPPORTED

class VirtualBoxInvalidXMLError(VirtualBoxException):
    """Invalid XML found."""
    errno = VBOX_E_XML_ERROR

class VirtualBoxInvalidSessionStateException(VirtualBoxException):
    """Current session state prohibits operation."""
    errno = VBOX_E_INVALID_SESSION_STATE

class VirtualBoxObjectInUseException(VirtualBoxException):
    """Object being in use prohibits operation."""
    errno = VBOX_E_OBJECT_IN_USE

class VirtualBoxFileNotFoundException(VirtualBoxException):
    """File not found."""
    errno = VBOX_E_FILE_NOT_FOUND

class VirtualBoxInvalidArgument(VirtualBoxException):
    """Invalid argument."""
    errno = XPCOM_E_INVALID_ARGUMENT

class VirtualBoxOperationAborted(VirtualBoxException):
    """Operation aborted."""
    errno = VBOX_E_ERROR_ABORT

# Mappings from VirtualBox error numbers to pyVBox classes
EXCEPTION_MAPPINGS = {
    VBOX_E_OBJECT_NOT_FOUND      : VirtualBoxObjectNotFoundException,
    VBOX_E_INVALID_VM_STATE      : VirtualBoxInvalidVMStateException,
    VBOX_E_VM_ERROR              : VirtualBoxVMError,
    VBOX_E_FILE_ERROR            : VirtualBoxFileError,
    VBOX_E_IPRT_ERROR            : VirtualBoxRuntimeSubsystemError,
    VBOX_E_PDM_ERROR             : VirtualBoxPluggableDeviceManagerError,
    VBOX_E_INVALID_OBJECT_STATE  : VirtualBoxInvalidObjectState,
    VBOX_E_HOST_ERROR            : VirtualBoxHostError,
    VBOX_E_NOT_SUPPORTED         : VirtualBoxNotSupportException,
    VBOX_E_XML_ERROR             : VirtualBoxInvalidXMLError,
    VBOX_E_INVALID_SESSION_STATE : VirtualBoxInvalidSessionStateException,
    VBOX_E_OBJECT_IN_USE         : VirtualBoxObjectInUseException,
    VBOX_E_ERROR_ABORT           : VirtualBoxOperationAborted,
    VBOX_E_FILE_NOT_FOUND        : VirtualBoxFileNotFoundException,
    XPCOM_E_INVALID_ARGUMENT     : VirtualBoxInvalidArgument,
    VBOX_E_SESSION_CLOSED        : VirtualBoxInvalidVMStateException,
    }

def handle_exception(ex):
    """Handle an exception from virtualbox code.

Since the VirtualBox Python API raises normal exceptions, this
function determines if an exception is related to VirtualBox and, if
so, raises its pyVBox equivalent.

Otherwise, it returns without doing anything. The intention being the
caller can raise the original exception. This allows python to know
the catch block ends with a raise and is not a valid flow of control
to the code past the try/catch block, which can lead to errors about
values being used before they are set.

The function should be used as follows:

    try:
        # Some VirtualBox code here
    catch Exception, e:
        VirtualBoxException.handle_exception(e)
        raise
"""
    if hasattr(ex, 'errno'):
        # Convert errno from exception to constant value from IDL file.
        # I don't understand why this is needed, determined experimentally.
        # ex.errno is a negative value (e.g. -0x7f44ffff), this effectively
        # takes its aboslute value and subtracts it from 0x100000000.
        errno = 0x100000000 + ex.errno
        if EXCEPTION_MAPPINGS.has_key(errno):
            # Reraise with original stacktrace and instance
            # information, but with new class.
            cls = EXCEPTION_MAPPINGS[errno]
            exc_info = sys.exc_info()
            raise cls, ex.msg, exc_info[2]
    # Else we don't have or don't recognize the errno, return and allow
    # original code to re-raise exception.

