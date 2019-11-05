# -*- coding: utf-8 -*-
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########


import time
def today():
    t = time.localtime()
    return str((t[0] % 100)) + str(t[1] > 9 and t[1] or '0' + str(t[1])) + str(t[2] > 9 and t[2] or '0' + str(t[2])) + str(t[3] > 9 and t[3] or '0' + str(t[3])) + str(t[4] > 9 and t[4] or '0' + str(t[4]))


print today(),
print