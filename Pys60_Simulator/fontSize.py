from fonts import fonts

def getFontSize(str,size):
    #print(str)
    if(fonts.has_key(str)==False):
        return [-1,-1]
    basesize = 15
    sizeof15 = fonts[str]
    x = int( round( ((float)(size)/(float)(basesize)) * sizeof15[0],0))
    y= int(round(((float)(size)/(float)(basesize)) * sizeof15[1],0))
    sizeofsize = (x,y)
    return sizeofsize
def getStrSize(str,size):
    count = 0
    max = 0
    for i in str: 
        msize = getFontSize(i,size)
        count+=msize[0]
        if(max<msize[1]):
            max = msize[1]
    return [count,max]
