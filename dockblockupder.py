
import sublime
import sublime_plugin
import os
import datetime
import random
import getpass
import re
import sys


'''
   Doc Block Updater
'''

class DocBlockUpdater(sublime_plugin.EventListener):
   def console_write(self, string):
      if sys.version_info < (3,):
          if isinstance(string, unicode):
              string = string.encode('UTF-8')
      sys.stdout.write('DocBlockUpdater: ')
      print(string)
   
   def on_pre_save(self, view):
      l_DateTime = datetime.datetime.utcnow()
      l_Enabled = view.settings().get("update_version_in_docblock_on_save")
      
      if (True == l_Enabled) and (True == view.is_dirty()):
         l_RandNumb = str(random.randrange(0000, 9999)).zfill(4)
         l_DTString = l_DateTime.strftime("%Y-%m-%d %H:%M:%S UTC")
         l_User     = getpass.getuser()
         l_FilePath = view.file_name()
         l_FileName = os.path.basename(l_FilePath)
         self.console_write("Looking for Doc Blocks in: %s" %(l_FileName))
         
         
         '''
   /*
    *        @version   $Id: file.py 123 121212 $                                       
    */
         '''
         l_TypeString = "Type 1 - Version Stamp"
         l_Region = view.find(' \* @version *\$Id: .* \$', 0, sublime.IGNORECASE)
         if None == l_Region:
            self.console_write(l_TypeString + " was not found.")
         else:
            self.console_write(l_TypeString + " was found.")
            l_NewText = (" * %s   $Id: %s %s %s %s $" % ("@version", l_FileName, l_RandNumb, l_DTString, l_User))
            l_Edit   = view.begin_edit()
            self.console_write("      Updating version in docblock: " + l_NewText)
            view.replace(l_Edit, l_Region, l_NewText)
            view.end_edit(l_Edit)
         
         '''
   //  |     LAST MODIFY DATE:  Fri Jul 23 17:49:40 EDT 2004             |
         '''
         l_TypeString = "ype 2 - Timestamp"
         l_DTString = l_DateTime.strftime("%a %b %d %H:%M:%S %Z %Y")
         l_VersionCore = (
            'LAST MODIFY DATE:\s*((Mon)|(Tue)|(Wed)|(Thu)|(Fri)|(Sat)|(Sun)) ((Jan)|(Feb)|(Mar)|(Apr)|(May)|(Jun)|(Jul)|(Aug)|(Sep)|(Oct)|(Nov)|(Dec)) [0-3][0-9] [0-2][0-9]:[0-6][0-9]:[0-6][0-9] [A-Z]{3} [1-2][0-9]{3}'
         )
         l_VersionLine_Regex  = ('^\s*//\s*\|\s*' + l_VersionCore + '\s*\|\s*$' )
         l_Region = view.find(l_VersionLine_Regex, 0, sublime.IGNORECASE)
         if None == l_Region:
            self.console_write(l_TypeString + " was not found.")
         else:
            self.console_write(l_TypeString + " was found.")
            l_OldText = view.substr(l_Region)
            l_VersionUpdateCore = ("LAST MODIFY DATE:  %s" % ( l_DTString))
            l_NewText = re.sub(r'\(.*\)'+ l_VersionCore + r'\(.*\)', r'\1'+ l_VersionUpdateCore + r'\2', l_OldText)
            l_Edit    = view.begin_edit()
            self.console_write("      Updating version in docblock: " + l_NewText)
            view.replace(l_Edit, l_Region, l_NewText)
            view.end_edit(l_Edit)
         
         '''
   //   |     LAST MODIFY DATE:  03/18/2004                                     |
         '''
         l_TypeString = "Type 3 - Timestamp"
         l_DTString = l_DateTime.strftime("%m/%d/%Y")
         l_VersionLine_Regex  = (
            '^\s*//\s*\|\s*LAST MODIFY DATE:\s*[0-1][0-9]/[0-3][0-9]/[1-2][0-9]{3}\s*\|.*$'
         )
         l_Region = view.find(l_VersionLine_Regex, 0, sublime.IGNORECASE)
         if None == l_Region:
            self.console_write(l_TypeString + " was not found.")
         else:
            self.console_write(l_TypeString + " was found.")
            l_OldText = view.substr(l_Region)
            l_VersionUpdateCore = ("LAST MODIFY DATE:  %s" % ( l_DTString))
            l_NewText = re.sub(r'^\(.*LAST MODIFY DATE:\s*\).*\(.*\)', r'\1'+ l_DTString + r'\2', l_OldText)
            l_Edit    = view.begin_edit()
            self.console_write("      Updating version in docblock: " + l_NewText)
            view.replace(l_Edit, l_Region, l_NewText)
            view.end_edit(l_Edit)
            
            
      else:
         self.console_write("update_version_in_docblock_on_save:%s" % (l_Enabled))
      
   
