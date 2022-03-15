# -*- coding: utf-8 -*-
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########


def cn(x):
    return x.decode('u8')




def en(x):
    return x.decode('u16')




def lrc(path, number = 0):
    try :
        a = open(path)
    except :
        a = open('c' + path[1 : ])
    if number == 1 : 
        try :
            b = cn(a.read()).split(cn('\\n'))
        except :
            b = a.read().split(cn('\\n'))
        pass
    elif number == 0 : 
        try :
            b = en(a.read()).split(cn('\\n'))
        except :
            b = a.read().split(cn('\\n'))
        pass


    a.close()
    del a
    WIN.list = []
    def re(t):
        t = t.replace(cn('['), '').replace('\\n', '').replace('\\r', '').split(cn(']'))
        for a in t[ : (len(t) - 1)]:
            try :
                a = a.split(cn(':'))
                b = float((int(a[0]) * 60) + float(a[1][ : 4]))
                WIN.list.append([b, t[(len(t) - 1)]])
                del a
                del b
            except :
                pass


    for t in b:
        try :
            t = cn(t)
        except :
            pass
        re(t)
    del t
    del b
    if number == 0 and WIN.list == [] : 
        lrc(path, 1)
    for i in xrange((len(WIN.list) - 1)):
        for i1 in xrange(((len(WIN.list) - 1) - i)):
            if float(WIN.list[i1][0]) > float(WIN.list[(i1 + 1)][0]) : 
                WIN.list[(i1 + 1)], WIN.list[i1] = (WIN.list[i1], WIN.list[(i1 + 1)])
            del i1
        del i




class WIN :
    __module__ = __name__




def Lr(time):
    for i in WIN.list:
        if i[0] == time : 
            return i[1]




def Return(t, number = 0):
    dur = (t / 100000)
    dur = (str((dur / 600)) + ':' + ('%02d' % ((dur % 600) / 10)) + '.' + str((dur % 600))[-1]).split(':')
    time = float((int(dur[0]) * 60) + float(dur[1][ : 4]))
    if number != 0 : 
        return time
    else : 
        return Lr(time)


if __name__ == '__main__' : 
    import audio
    import e32
    m = audio.Sound.open(cn('e:\\Attachments\\贝多芬的悲伤-郑毅.aac'))
    m.play()
    lrc('e:\\TTPod\\Lyrics\\贝多芬的悲伤-郑毅.lrc')
    WIN.true = ''
    while True : 
        true = Return(m.current_position())
        if true != None : 
            if WIN.true != true : 
                WIN.true = true
                print WIN.true,
                print
                del true
            pass
        if m.state() != 2 : 
            break
        e32.ao_yield()
    m.close()
    del m
    del audio
    del e32