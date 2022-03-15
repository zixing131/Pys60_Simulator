# -*- coding: utf-8 -*-
import graphics
import appuifw
import key_codes
from math import cos as cos
from math import sin as sin
from math import pi as pi
from math import sqrt as sqrt
from math import atan2 as atan2
from math import tan as tan
from e32 import ao_sleep as ao_sleep
__version__ = 1.4
class Keyboard(object, ) :


    __module__ = __name__
    def __init__(self, onevent = lambda  : None ):
        self._keyboard_state = {}
        self._downs = {}
        self._onevent = onevent
        self.evt = {'keycode' : None, 'scancode' : None, 'type' : None}




    def handle_event(self, event):
        self.evt = event
        self._downs = {}
        if event['type'] == appuifw.EEventKeyDown : 
            code = event['scancode']
            if  not (self._keyboard_state.get(code, 0)) : 
                self._downs[code] = True
            self._keyboard_state[code] = 1
        elif event['type'] == appuifw.EEventKeyUp : 
            self._keyboard_state[event['scancode']] = 0




    def is_down(self, scancode):
        return self._keyboard_state.get(scancode, 0)




    def pressed(self, scancode):
        return self._downs.get(scancode, False)




    def keycode(self, code):
        if self.evt['keycode'] == code : 
            return True
        return False




    def scancode(self, code):
        if self.evt['scancode'] == code : 
            return True
        return False






keyboard = Keyboard()
def copy_image(img):
    im = graphics.Image.new(img.size)
    if im is not None : 
        im.blit(img)
    return im




def new_image(size, mode = 'RGB16'):
    try :
        return graphics.Image.new(size, mode)
    except Exception, exc : 
        appuifw.note(unicode(exc), 'error')
        return None




def line(can, cr, outline, width):
    can.line([cr[0], cr[1], cr[2], cr[3]], outline = outline, width = width)
    can.point((cr[2], cr[3]), outline = outline, width = width)




def rect(canv, cr, outline = None, fill = None, width = 1, pattern = None):
    if cr[0] != cr[2] and cr[1] != cr[3] : 
        canv.rectangle([min(cr[0], cr[2]), min(cr[1], cr[3]), (max(cr[0], cr[2]) + 1), (max(cr[1], cr[3]) + 1)], outline, fill, width)
    else : 
        line(canv, [cr[0], cr[1], cr[2], cr[3]], outline = outline, width = width)




def softrect(canv,hh, outline = 0, fill = 16777215, width = 1, corner = 1):
    x, y, x1, y1 =hh
    canv.polygon(((x + corner, y), (x, y + corner), (x, (y1 - corner)), (x + corner, y1), ((x1 - corner), y1), (x1, (y1 - corner)), (x1, y + corner), ((x1 - corner), y)), outline = outline, fill = fill, width = width)




def ellps(canv, cr, outline = None, fill = None, width = 1, pattern = None):
    if cr[0] != cr[2] and cr[1] != cr[3] : 
        canv.ellipse([min(cr[0], cr[2]), min(cr[1], cr[3]), max(cr[0], cr[2]), max(cr[1], cr[3])], outline, fill, width)
    else : 
        line(canv, [cr[0], cr[1], cr[2], cr[3]], outline = outline, width = width)




def inttorgb(color):
    b = (color % 256)
    g = ((color / 256) % 256)
    r = (((color / 256) / 256) % 256)
    return (r, g, b)




def _image_cropcolors(aa, ignorecol, descol, callback):
    img, msk = aa
    col = 0
    w = img.size[0]
    h = img.size[1]
    for x in xrange(w):
        for y in xrange(h):
            c = img.getpixel((x, y))[0]
            if c != ignorecol :
                appuifw.note(unicode(c))
                c = descol
                img.point((x, y), c)
        callback(x, w)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (img, msk)




def _image_tomaskwhite(aa, maskcol, callback = None):
    img, msk = aa
    w = img.size[0]
    h = img.size[1]
    getpixel = img.getpixel
    point = img.point
    for x in xrange(w):
        for y in xrange(h):
            c = getpixel((x, y))[0]
            if c == maskcol :
                point((x, y), (0, 0, 0))
            else :
                point((x, y), (255, 255, 255))
        callback(x, w)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (img, msk)




def _image_tomaskblack(aa, maskcol, callback = None):
    img, msk = aa
    w = img.size[0]
    h = img.size[1]
    getpixel = img.getpixel
    point = img.point
    for x in xrange(w):
        for y in xrange(h):
            c = getpixel((x, y))[0]
            if c == maskcol :
                point((x, y), (255, 255, 255))
            else :
                point((x, y), (0, 0, 0))
        callback(x, w)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (img, msk)




def _image_decolor(aa,hh):
    img, msk = aa
    r, g, b =hh
    tmp = graphics.Image.new(img.size)
    tmp.blit(img)
    tmp = image_tobpp(tmp, 'L')
    msk = graphics.Image.new(img.size, 'L')
    msk.clear((r, g, b))
    img.blit(tmp, mask = msk)
    return (img, msk)




def _image_lightness_slow(aa, val, callback):
    img, msk = aa
    if val == 0 :
        return None
    w = img.size[0]
    h = img.size[1]
    getpxl = img.getpixel
    point = img.point
    for x in xrange(w):
        for y in xrange(h):
            r = g = b = 255
            c = getpxl((x, y))[0]
            c1 = c[0] + val
            if c1 < 255 :
                r = c1
            c1 = c[1] + val
            if c1 < 255 :
                g = c1
            c1 = c[2] + val
            if c1 < 255 :
                b = c1
            point((x, y), (r, g, b))
        callback(x, w)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (img, msk)




def _image_lightness(aa, val):
    img, msk = aa
    if val == 0 :
        return None
    im = graphics.Image.new(img.size)
    mask = graphics.Image.new(img.size, 'L')
    mask.clear((val, val, val))
    img.blit(im, mask = mask)
    return (img, msk)




def _image_invertcolors(aa, callback):
    img, msk = aa
    col = 0
    w = img.size[0]
    h = img.size[1]
    getpxl = img.getpixel
    point = img.point
    for x in xrange(w):
        for y in xrange(h):
            c = getpxl((x, y))[0]
            point((x, y), ((255 - c[0]), (255 - c[1]), (255 - c[2])))
        callback(x, w)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (img, msk)




def _image_invertcolor_channel(aa, callback, ch = 0):
    img, msk = aa
    col = 0
    w = img.size[0]
    h = img.size[1]
    getpxl = img.getpixel
    point = img.point
    for x in xrange(w):
        for y in xrange(h):
            c = getpxl((x, y))[0]
            if ch == 0 :
                point((x, y), ((255 - c[0]), c[1], c[2]))
            elif ch == 1 :
                point((x, y), (c[0], (255 - c[1]), c[2]))
            elif ch == 2 :
                point((x, y), (c[0], c[1], (255 - c[2])))
        callback(x, w)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (img, msk)




def _image_colorbalance(aa,hh, callback):
    img, msk =aa
    rr, gg, bb =hh
    w = img.size[0]
    h = img.size[1]
    getpxl = img.getpixel
    point = img.point
    for x in xrange(w):
        for y in xrange(h):
            c = getpxl((x, y))[0]
            r = c[0] + rr
            g = c[1] + gg
            b = c[2] + bb
            if r > 255 :
                r = 255
            elif r < 0 :
                r = 0
            if g > 255 :
                g = 255
            elif g < 0 :
                g = 0
            if b > 255 :
                b = 255
            elif b < 0 :
                b = 0
            point((x, y), (r, g, b))
        callback(x, w)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (img, msk)




def _image_saturation(aa, v, callback):
    img, msk = aa
    w = img.size[0]
    h = img.size[1]
    getpxl = img.getpixel
    point = img.point
    for x in xrange(w):
        for y in xrange(h):
            c = getpxl((x, y))[0]
            s = (c[0] + c[1] + c[2] / 3)
            r = s + ((v * (c[0] - s)) / 100)
            g = s + ((v * (c[1] - s)) / 100)
            b = s + ((v * (c[2] - s)) / 100)
            if r > 255 :
                r = 255
            elif r < 0 :
                r = 0
            if g > 255 :
                g = 255
            elif g < 0 :
                g = 0
            if b > 255 :
                b = 255
            elif b < 0 :
                b = 0
            point((x, y), (r, g, b))
        callback(x, w)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (img, msk)




def _image_sepia(aa, callback):
    img, msk = aa
    col = 0
    w = img.size[0]
    h = img.size[1]
    getpixel = img.getpixel
    point = img.point
    for x in xrange(w):
        for y in xrange(h):
            c = getpixel((x, y))[0]
            r = (c[0] * 0.393) + (c[1] * 0.769) + (c[2] * 0.189)
            if r > 255 :
                r = 255
            g = (c[0] * 0.349) + (c[1] * 0.686) + (c[2] * 0.168)
            if g > 255 :
                g = 255
            b = (c[0] * 0.272) + (c[1] * 0.534) + (c[2] * 0.131)
            if b > 255 :
                b = 255
            point((x, y), (r, g, b))
        callback(x, w)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (img, msk)




def _image_posterize( aa, callback):
    img, msk= aa
    col = 0
    w = img.size[0]
    h = img.size[1]
    getpixel = img.getpixel
    point = img.point
    dell = 64
    for x in xrange(w):
        for y in xrange(h):
            c = getpixel((x, y))[0]
            r = ((c[0] / dell) * dell)
            if r > 255 :
                r = 255
            g = ((c[1] / dell) * dell)
            if g > 255 :
                g = 255
            b = ((c[2] / dell) * dell)
            if b > 255 :
                b = 255
            point((x, y), (r, g, b))
        callback(x, w)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (img, msk)




def _image_replacecolor( aa, color, dcolor, callback):
    img, msk= aa
    imgw = img.size[0]
    imgh = img.size[1]
    getpix = img.getpixel
    line = img.line
    yr = xrange(imgh)
    for n in xrange(imgw):
        state = 0
        start = []
        stop = []
        for t in yr:
            if getpix((n, t))[0] == color :
                if state == 0 :
                    start.append(t)
                    state = 1
                if t == (imgh - 1) :
                    stop.append((t + 1))
                pass
            elif state == 1 :
                stop.append(t)
                state = 0
        for x in xrange(len(start)):
            line((n, start[x], n, stop[x]), outline = dcolor)
        callback(n, imgw)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (img, msk)




def _image_flip(flag, imwin):
    if imwin.selector.isactive() :
        img, msk = imwin.selector.getimage()
        im = img.transpose(flag)
        ms = msk.transpose(flag)
        imwin.img.blit(im, target = imwin.selector.getcoord(), mask = ms)
    else :
        im = imwin.img.transpose(flag)
        imwin.img.blit(im)
    return (img, msk)




def _image_rotate(flag, imwin, workzone):
    if imwin.selector.isactive() :
        img, msk = imwin.selector.getimage()
        im = img.transpose(flag)
        ms = msk.transpose(flag)
        imwin.img.blit(im, target = imwin.selector.getcoord(), mask = ms)
    else :
        im = imwin.img.transpose(flag)
        image = graphics.Image.new(im.size)
        if image is None :
            return None
        imwin.img = image
        imwin.size((min(im.size[0], workzone[0]), min(im.size[1], workzone[1])))
        imwin.img.blit(im)
    return (img, msk)




def _image_resize( aa,hh, imwin):
    img, msk= aa
    sz, asp, workzone =hh
    im = img.resize(sz, keepaspect = asp)
    imwin.img = copy_image(im)
    imwin.size((min(imwin.img.size[0], workzone[0]), min(imwin.img.size[1], workzone[1])))
    return (img, msk)




def _image_darkness_slow( aa, val, callback):
    img, msk= aa
    if val == 0 :
        return None
    w = img.size[0]
    h = img.size[1]
    getpxl = img.getpixel
    point = img.point
    for x in xrange(w):
        for y in xrange(h):
            r = g = b = 0
            c = getpxl((x, y))[0]
            if c[0] > val :
                r = (c[0] - val)
            if c[1] > val :
                g = (c[1] - val)
            if c[2] > val :
                b = (c[2] - val)
            point((x, y), (r, g, b))
        callback(x, w)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (img, msk)




def _image_darkness( aa, val):
    img, msk= aa
    if val == 0 :
        return None
    im = graphics.Image.new(img.size)
    mask = graphics.Image.new(img.size, 'L')
    im.clear(0)
    mask.clear((val, val, val))
    img.blit(im, mask = mask)
    return (img, msk)




def _image_blur_bysizing(img):
    sz = img.size
    im = img.resize(((sz[0] * 4), (sz[1] * 4)), keepaspect = 1)
    imwin.img.blit(im, scale = 1)
    return (img, msk)




def _image_fractal( aa, col, callback):
    image, msk= aa
    c = (0.5 + 0.2j)
    widthlist = xrange(image.size[0])
    w = image.size[0]
    h = image.size[1]
    for x in xrange(w):
        for y in xrange(h):
            re = (((x * 2.0) / image.size[0]) - 1.0)
            im = (((y * 2.0) / image.size[1]) - 1.0)
            z = re + (im * 1j)
            for i in widthlist:
                if abs(z) > 2.0 :
                    break
                z = (z * z) + c
            image.point((x, y), outline = (i * (col[0] * 65536) + (col[1] * 256) + col[2]), width = 1)
        callback(x, w)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (image, msk)




def _image_fractal_mandelbrot( aa, iterations = 25, scale = 60, callback = lambda  : None ):
    image, msk= aa
    width, height = image.size
    xaxis = (width / 2)
    yaxis = (height / 1.5)
    scale = 60
    for y in xrange(height):
        for x in xrange(width):
            magnitude = 0
            z = (0 + 0j)
            c = complex((float((y - yaxis)) / scale), (float((x - xaxis)) / scale))
            for i in xrange(iterations):
                z = (z ** 2) + c
                if abs(z) > 2 :
                    v = ((765 * i) / iterations)
                    if v > 510 :
                        color = (255, 255, (v % 255))
                    elif v > 255 :
                        color = (255, (v % 255), 0)
                    else :
                        color = ((v % 255), 0, 0)
                    break
            else :
                color = (0, 0, 0)
            image.point((x, y), color)
        callback(y, height)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    return (image, msk)




def _image_blur( aa, val):
    img, msk= aa
    if val == 0 :
        return None
    im = graphics.Image.new(img.size)
    if im is None :
        return None
    im.blit(img)
    mask = graphics.Image.new(img.size, 'L')
    if mask is None :
        return None
    mask.clear((val, val, val))
    if msk is not None :
        mask0 = graphics.Image.new(img.size, 'L')
        if mask0 is None :
            return None
        mask0.clear(0)
        mask0.blit(mask, mask = msk)
        mask = mask0
    img.blit(im, target = (1, 0), mask = mask)
    img.blit(im, target = (0, 1), mask = mask)
    img.blit(im, target = (-1, 0), mask = mask)
    img.blit(im, target = (0, -1), mask = mask)
    return (img, msk)




def _image_rotateangle( aa, ang, bgcolor, callback, mode = 0):
    img, msk= aa
    ang = (( - ang / 180.0) * pi)
    imw, imh = img.size
    imnew = copy_image(img)
    imnew.clear(bgcolor)
    mask = new_image(imnew.size, 'L')
    xc = (imw / 2)
    yc = (imh / 2)
    sn = sin(ang)
    cs = cos(ang)
    tar = img.getpixel((xc, yc))[0]
    a = ang
    for y in xrange(imh):
        for x in xrange(imw):
            r = sqrt(((x - xc) * (x - xc)) + ((y - yc) * (y - yc)))
            if (x - xc) != 0 :
                ann = a + atan2((y - yc), (x - xc))
            else :
                ann = a + atan2((y - yc), 1E-05)
            imnew.point((x, y), img.getpixel((round(xc + (r * cos(ann))), round(yc + (r * sin(ann)))))[0])
        callback(y, imh)
        if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
            return False
        ao_sleep(0.001)
    imnew.point((xc, yc), tar)
    return (imnew, msk)




def _image_gradient( aa,hh):
    img, msk= aa
    color, dcolor, gor =hh
    imgw = img.size[0]
    imgh = img.size[1]
    line = img.line
    tri = (0, 1, 2)
    col1 = inttorgb(color)
    col2 = inttorgb(dcolor)
    col = [0, 0, 0]
    if gor == 1 :
        for t in xrange(imgw):
            col[0] = col1[0] + ((t * (col2[0] - col1[0])) / imgw)
            col[1] = col1[1] + ((t * (col2[1] - col1[1])) / imgw)
            col[2] = col1[2] + ((t * (col2[2] - col1[2])) / imgw)
            line((t, 0, t, imgh), outline = (col[0], col[1], col[2]))
        pass
    elif gor == 0 :
        for t in xrange(imgh):
            col[0] = col1[0] + ((t * (col2[0] - col1[0])) / imgh)
            col[1] = col1[1] + ((t * (col2[1] - col1[1])) / imgh)
            col[2] = col1[2] + ((t * (col2[2] - col1[2])) / imgh)
            line((0, t, imgw, t), outline = (col[0], col[1], col[2]))
        pass
    elif gor == 2 :
        mx = max(imgw, imgh)
        mn = min(imgw, imgh)
        ext = (float(mn) / mx)
        for t in xrange((mx / 2)):
            col[0] = col1[0] + (((t * (col2[0] - col1[0])) / mx) * 2)
            col[1] = col1[1] + (((t * (col2[1] - col1[1])) / mx) * 2)
            col[2] = col1[2] + (((t * (col2[2] - col1[2])) / mx) * 2)
            if mx == imgw :
                ellps(img, (((imgw / 2) - t), ((imgh / 2) - (t * ext)), (imgw / 2) + t, (imgh / 2) + (t * ext)), width = 2, outline = (col[0], col[1], col[2]), fill = None)
            else :
                ellps(img, (((imgw / 2) - (t * ext)), ((imgh / 2) - t), (imgw / 2) + (t * ext), (imgh / 2) + t), width = 2, outline = (col[0], col[1], col[2]), fill = None)
        pass
    elif gor == 3 :
        mx = max(imgw, imgh)
        mn = min(imgw, imgh)
        ext = (float(mn) / mx)
        for t in xrange((mx / 2)):
            col[0] = col1[0] + (((t * (col2[0] - col1[0])) / mx) * 2)
            col[1] = col1[1] + (((t * (col2[1] - col1[1])) / mx) * 2)
            col[2] = col1[2] + (((t * (col2[2] - col1[2])) / mx) * 2)
            if mx == imgw :
                rect(img, (((imgw / 2) - t), ((imgh / 2) - (t * ext)), (imgw / 2) + t, (imgh / 2) + (t * ext)), width = 1, outline = (col[0], col[1], col[2]), fill = None)
            else :
                rect(img, (((imgw / 2) - (t * ext)), ((imgh / 2) - t), (imgw / 2) + (t * ext), (imgh / 2) + t), width = 1, outline = (col[0], col[1], col[2]), fill = None)
        pass
    elif gor == 4 :
        minl = min((imgh / 2), (imgw / 2))
        for t in xrange((imgh / 2)):
            col[0] = col1[0] + (((t * (col2[0] - col1[0])) / imgh) * 2)
            col[1] = col1[1] + (((t * (col2[1] - col1[1])) / imgh) * 2)
            col[2] = col1[2] + (((t * (col2[2] - col1[2])) / imgh) * 2)
            ellps(img, (((imgw / 2) - t), ((imgh / 2) - t), (imgw / 2) + t, (imgh / 2) + t), width = 2, outline = (col[0], col[1], col[2]), fill = None)
        pass
    return (img, msk)




def _image_displacement( aa, angle, vert, bgcolor, callback):
    img, msk= aa
    imgw = img.size[0]
    imgh = img.size[1]
    ang = ((angle / 180.0) * pi)
    if vert == 0 :
        image = new_image((imgw + (imgh * tan(ang)), imgh))
    else :
        image = new_image((imgw, imgh + (imgw * tan(ang))))
    image.clear(bgcolor)
    mask = new_image(image.size, 'L')
    if vert == 0 :
        for y in xrange(imgh):
            linepix = img.getpixel([(x, y) for x in xrange(imgw)])
            val = ((imgh - y) * tan(ang))
            for x in xrange(imgw):
                image.point((x + val, y), outline = linepix[x])
            callback(y, imgh)
            if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
                return False
            ao_sleep(0.001)
        pass
    else :
        for x in xrange(imgw):
            linepix = img.getpixel([(x, y) for y in xrange(imgh)])
            val = (x * tan(ang))
            for y in xrange(imgh):
                image.point((x, y + val), outline = linepix[y])
            callback(x, imgw)
            if keyboard.is_down(key_codes.EScancodeRightSoftkey) :
                return False
            ao_sleep(0.001)
        pass
    return (image, mask)

