import win32gui
import win32con
import re
import ctypes
from ctypes import c_int
import ctypes.wintypes
from ctypes.wintypes import HWND, DWORD

class Mouse:
    def __init__(self):
        flags, hcursor, (self.x, self.y) = win32gui.GetCursorInfo()
        pass

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y



##########################################################################
class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None
        self.dwmapi = ctypes.WinDLL("dwmapi")
        self.DWMWA_CLOAKED = 14 
        self.isCloacked = c_int(0)
        self.firstLoop = True
        self.title = ""

    def window_enum_handler(self, hwnd, resultList):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
            self.dwmapi.DwmGetWindowAttribute(HWND(hwnd), DWORD(self.DWMWA_CLOAKED), ctypes.byref(self.isCloacked), ctypes.sizeof(self.isCloacked))
            if(self.isCloacked.value == 0):
                if self.firstLoop:
                    resultList.clear()
                if win32gui.GetWindowText(hwnd) != self.title:
                    resultList.append((hwnd, win32gui.GetWindowText(hwnd)))
                    self.firstLoop = False

    def get_app_list(self, title, handles=[]):
        self.title = title
        mlst=[]
        self.firstLoop = True
        win32gui.EnumWindows(self.window_enum_handler, handles)
        for handle in handles:
            mlst.append(handle)
        return mlst

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self,handle = ""):
        """put the window in the foreground"""
        if handle == "":
            handle = self._handle
        tup = win32gui.GetWindowPlacement(handle)
        if tup[1] == win32con.SW_SHOWMINIMIZED:
            win32gui.ShowWindow(handle,win32con.SW_SHOWMAXIMIZED)
        win32gui.SetForegroundWindow(handle)

    def get_handle(self,classname,title):
        print(9)
        return win32gui.FindWindow(classname,title)

# w = WindowMgr()
# # w.find_window_wildcard(".*Excel.*")
# print(w.get_app_list())
# w.set_foreground(66316)
#########################################################################


##############################################################
# def winEnumHandler( hwnd, ctx ):
#     if win32gui.IsWindowVisible( hwnd ):
#         print (hex(hwnd), win32gui.GetWindowText( hwnd ))

# win32gui.EnumWindows( winEnumHandler, None )
##############################################################

if __name__ == "__main__":
    # print(Mouse().get_y())
    # w = WindowMgr()
    # w.find_window_wildcard("Olho mágico")
    # print(w._handle)
    pass