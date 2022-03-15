# -*- coding: utf-8 -*-
import json,os
import e32db

class db(object):

    def __setitem__(self,item,value):
        self.data[item] = value
    def __getitem__(self,item):
        return str(self.data[int(item)])
    def __init__(self,filename,mode,data={}):
        self.filename=filename
        self.data = data
    def items(self):
        return self.data
        ret = []
        for i in self.data:
            ret.append((i,self.data[i]))
        return ret
    def close(self):
        data=json.dumps(self.data)
        if(self.filename!=''):
            e32db.open(self.filename, 'wb').write(data)

def open(name, flags = 'r', mode = 0666):
    """Open the specified database, flags is one of c to create
    it, if it does not exist, n to create a new one (will destroy
    old contents), r to open it read-only and w to open it read-
    write. Appending 'f' to the flags opens the database in fast
    mode, where updates are not written to the database
    immediately. Use the sync() method to force a write."""
    create = 0
    if name.endswith('.e32dbm'):
        filename=unicode(name)
    else:
        filename=unicode(name+'.e32dbm')
    
    if flags[0] not in 'cnrw':
        raise TypeError, "First flag must be one of c, n, r, w."
    if flags[0] == 'c' and not os.path.exists(filename):
        create = 1
    if flags[0] == 'n':
        create = 1
    if create:
        return db(filename,flags)
    else:
        file1 = e32db.open(filename, 'rb').read()
        if(file1!=''):
            return db(filename,flags,eval(file1))
        else:
            return db(filename,flags)
    

if __name__=='__main__':
    db1=open("data","c")
    db1["score"]='0'
    db1.close()

    db2=open("data","r")
    tdb=db2.items()
    db2.close()
    print(tdb[0][1])
    
