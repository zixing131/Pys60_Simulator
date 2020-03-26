# -*- coding: utf-8 -*-
import os,sys
path = os.getcwd()
index = path.rfind('\\')
mypath=path[:index]
mypath2=path+"\\ImageDesigner\\"
sys.path.append(mypath)
sys.path.append(mypath2)
'''
import appuifw
import sys
from os import path, remove
__selfmodlist__ = ('main','improc','classes','wt_requester','wt_colormx','wt_ui','iniparser','langimp','SV_TRANS','lloader','conf','batch','mbm', 'kconfig')
tocomp = []
for f in __selfmodlist__:
  if path.exists('C:\\System\\Apps\\ImageDesigner\\palette.dat'):
    drive = 'c:\\'
  else:
    drive = 'e:\\'
  sys.path.append(drive+'System\\Apps\\ImageDesigner')
  file = drive+'System\\Apps\\ImageDesigner\\' + f + '.py'.lower()
  source = drive+'System\\Apps\\ImageDesigner\\source\\' + f + '.py'.lower()
  if path.exists(file) and not path.exists(drive+'System\\Apps\\ImageDesigner\\dontcompile'): tocomp.append((file,source))
if tocomp:
  ans = appuifw.query(u'Source files are not compiled. To compile?','query')
  if ans:
    import py_compile
    import shutil
    appuifw.note(u'Compiling...','conf')
    for f in tocomp:
      py_compile.compile(f[0])
      shutil.copyfile(f[0], f[1])
      remove(f[0])
    appuifw.note(u'Done! Restart the application.','info')
    sys.exit()
  del ans
del __selfmodlist__
del tocomp
del file
del source
'''
import main

#while 1:
#  appuifw.app.Yield()
#  appuifw.app.body.root.update()
