# -*- coding: utf-8 -*-

import graphics
__version_info__ = (u'internal', '90度浮雕'.decode('utf8'), u'1.3', u'1.0')
cc = 0
def Execute(_0, ProgressCallback):


    sourceim, MASK = _0
    cc = 0
    image = graphics.Image.new(sourceim.size)
    a, b, c = (0, 1, 0)
    d, e, f = (0, 0, 0)
    g, h, k = (0, -1, 0)
    width, height = sourceim.size
    width += 1
    height += 1
    dc = (a + b + c + d + e + f + g + h + k + 1)
    lst = ([height] * width)
    def do(jj):
        i = cc
        drw = image.point
        gtp = sourceim.getpixel
        for j in xrange(jj):
            p = gtp((((i - 1), (j - 1)), (i, (j - 1)), ((i + 1), (j - 1)), ((i - 1), j), (i, j), ((i + 1), j), ((i - 1), (j + 1)), (i, (j + 1)), ((i + 1), (j + 1))))
            rr = ((a * p[0][0]) + (b * p[1][0]) + (c * p[2][0]) + (d * p[3][0]) + (e * p[4][0]) + (f * p[5][0]) + (g * p[6][0]) + (h * p[7][0]) + (k * p[8][0]) / dc)
            bb = ((a * p[0][1]) + (b * p[1][1]) + (c * p[2][1]) + (d * p[3][1]) + (e * p[4][1]) + (f * p[5][1]) + (g * p[6][1]) + (h * p[7][1]) + (k * p[8][1]) / dc)
            gg = ((a * p[0][2]) + (b * p[1][2]) + (c * p[2][2]) + (d * p[3][2]) + (e * p[4][2]) + (f * p[5][2]) + (g * p[6][2]) + (h * p[7][2]) + (k * p[8][2]) / dc)
            if rr > 255 : 
                rr = 255
            elif rr < 0 : 
                rr = 0
            if gg > 255 : 
                gg = 255
            elif gg < 0 : 
                gg = 0
            if bb > 255 : 
                bb = 255
            elif bb < 0 : 
                bb = 0
            drw((i, j), outline = (rr, gg, bb))
        cc += 1
        ProgressCallback(i, width)


    map(do, lst)
    return (image, MASK)
    global cc

