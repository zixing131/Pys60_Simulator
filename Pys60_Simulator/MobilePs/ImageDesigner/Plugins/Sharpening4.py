# -*- coding: utf-8 -*-
import graphics
__version_info__ = (u'internal', '锐化效果4'.decode('utf8'), u'1.0', u'1.0')
def Execute(.0, ProgressCallback):
    sourceim, MASK = .0
    image = graphics.Image.new(sourceim.size)
    a, b, c = (-1, -1, -1)
    d, e, f = (-1, 9, -1)
    gg, h, k = (-1, -1, -1)
    width, height = sourceim.size
    for i in range(width):
        for j in range(height):
            g = sourceim.getpixel((((i - 1), (j - 1)), (i, (j - 1)), ((i + 1), (j - 1)), ((i - 1), j), (i, j), ((i + 1), j), ((i - 1), (j + 1)), (i, (j + 1)), ((i + 1), (j + 1))))
            red = ((a * g[0][0]) + (b * g[1][0]) + (c * g[2][0]) + (d * g[3][0]) + (e * g[4][0]) + (f * g[5][0]) + (gg * g[6][0]) + (h * g[7][0]) + (k * g[8][0]) / a + b + c + d + e + f + gg + h + k)
            bl = ((a * g[0][1]) + (b * g[1][1]) + (c * g[2][1]) + (d * g[3][1]) + (e * g[4][1]) + (f * g[5][1]) + (gg * g[6][1]) + (h * g[7][1]) + (k * g[8][1]) / a + b + c + d + e + f + gg + h + k)
            gr = ((a * g[0][2]) + (b * g[1][2]) + (c * g[2][2]) + (d * g[3][2]) + (e * g[4][2]) + (f * g[5][2]) + (gg * g[6][2]) + (h * g[7][2]) + (k * g[8][2]) / a + b + c + d + e + f + gg + h + k)
            if red > 254 : 
                red = 255
            if bl > 254 : 
                bl = 255
            if gr > 254 : 
                gr = 255
            if red < 0 : 
                red = 0
            if bl < 0 : 
                bl = 0
            if gr < 0 : 
                gr = 0
            image.point((i, j), outline = (red, bl, gr), width = 1)
        ProgressCallback(i, width)
    return (image, MASK)

