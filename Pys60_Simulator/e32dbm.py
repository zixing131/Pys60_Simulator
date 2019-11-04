# -*- coding: utf-8 -*-
import json,os
import e32db

class db(dict):
    def __init__(self,file1,mode,data={}):
        self.file1=file1
        for i in data:
            self[i]=data[i]
    def items(self):
        ret = []
        for i in self:
            ret.append((i,self[i]))
        return ret
    def close(self):
        data=json.dumps(self)
        self.file1.write(data)
        self.file1.close()


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
        file1 = e32db.open(filename,'wb')
        return db(file1,flags)
    else:
        file1 = e32db.open(filename,'rb').read()
        file2 = e32db.open(filename,'wb')
        if(file1!=''):
            return db(file2,flags,json.loads(file1))
        else:
            return db(file2,flags)
    

if __name__=='__main__':
    db1=open("data","c")
    db1["score"]='0'
    db1.close()

    db2=open("data","r")
    tdb=db2.items()
    db2.close()
    print(tdb[0][1])
    
