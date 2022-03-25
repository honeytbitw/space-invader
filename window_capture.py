import win32gui, win32con, win32ui
import numpy as np

class WindowCapture :
    w=800
    h=600
    hwnd = None
    cropped_x =0
    cropped_y =0

    def __init__(self,window_name) : 

        self.hwnd = win32gui.FindWindow(None, window_name)

        # if not self.hwnd :
        #     raise Exception('Window not Found')

        # window_rect = win32gui.GetWindowRect(self.hwnd)
        # self.w = window_rect[2] - window_rect[0] #window_rect[0] & [1] are x & y coordinate of upper left corner of window
        # self.h = window_rect[3] - window_rect[1] #window_rect[2] & [3] are x & y coordinate of lower right corner of window
        border_pixels = 8
        titlebar_pixels = 30
        self.w -= 2*border_pixels
        self.h -= (titlebar_pixels+border_pixels)
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

    def take_screenshot(self) :
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (self.cropped_x,self.cropped_y), win32con.SRCCOPY)
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')

        img.shape = (1,self.h,self.w,4)
        img = img[... ,:3 ]  #Numpy slicing to get rid of alpha channel

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        return img