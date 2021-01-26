# -*- coding: utf-8 -*-
# wc.py
#   by Pixel
from tkinter import *
from subprocess import Popen as run
from time import ctime
from time import sleep
from socket import gethostname, gethostbyname
from datetime import datetime
import sys
import random
import os
import platform

DELAY = True
SAFE = False
DIE = False
TINY = False
if len(sys.argv) > 1:
  if '--no-delay' in sys.argv:
    DELAY = False
  if '-n' in sys.argv:
    DELAY = False
  if '--tiny' in sys.argv:
    TINY = True
  if '-t' in sys.argv:
    TINY = True
  if '--safe' in sys.argv:
    SAFE = True
  if '-s' in sys.argv:
    SAFE = True
  if '--die' in sys.argv:
    DIE = True
  if '-d' in sys.argv:
    DIE = True

LIST = ( # List of questions
  #   Software
  "Target administrator account name",#1
  "New administrator password",#2
  "Confirm new administrator password",#3
  "Current user account name",#4
  "Computer Name",#5
  "Windows version",#6
  "Creation time of folder \"System32\" (HH:MM:SS)",#7
  "Last Windows Update actualisation date (YYYY-MM-DD)",#8
  "Build number of last Windows Update actualisation",#9
  #   Hardware
  "Total size of installed RAM (GB)",#10
  "Number of installed RAM modules",#11
  "Hard drive serial number",#12
  "Motherboard vendor",#13
  "Motherboard serial number",#14
  "GPU vendor",#15
  "GPU serial number",#16
  "Keyboard vendor",#17
  "Mouse vendor",#18
  "Mouse serial number",#19
  #   Net
  "Computer IP address",#20
  "Computer MAC address",#21
  #   BIOS
  "Bios vendor",#22
  "Current date (YYYY-MM-DD)",#23
  "Current time (HH:MM:SS)",#24
)
def convert(list):
  out = []
  for question in list:
    question += ": "
    out.append(question)
  return out
class Root(Tk):
  """ Tk root object class """
  def __init__(self, title = 'Window'):
    super(Root, self).__init__()
    self.title(str(title))

class App(Frame):
  """ Main frame of app """
  def __init__(self, master):
    super(App, self).__init__(master)
    self.list = convert(LIST)
    self.number = 0 # Current question number from LIST
    if TINY:
      self.number = len(self.list) - 3 # DEBUG: last 3 questions
    self.grid()
    self.main()
    Label(self, # Podpis
      text = "Writen by Pixel",
      bg = 'lightgrey'
      ).grid(row = 0, column = 0, columnspan = 3, sticky = W)
  def main(self):
    self.row = 0
    self.column = 0
    self.setup()
  def setup(self):
    Label(self,
          text = "Please enter provided variables"
          ).grid(row = self.row, column = self.column, columnspan = 3)
    self.newRow()
    Label(self,
      text = "!!! WARNING !!!"
      ).grid(row = self.row, column = self.column, columnspan = 3)
    self.newRow()
    Label(self,
      text = "Incorrect data will cause the need to repeat the whole process"
      ).grid(row = self.row, column = self.column, columnspan = 3)
    self.newRow()
    Label(self,
      text = ""
      ).grid(row = self.row, column = self.column)
    self.newRow()
    self.firstQuestion()
  def firstQuestion(self, number = None):
    if number is None:
      number = self.number
    Label(self,
      text = self.list[self.number]
      ).grid(row = self.row, column = self.column, sticky = E)
    self.newColumn()
    self.ent = Entry(self)
    self.ent.grid(row = self.row, column = self.column)
    self.newColumn()
    self.bttn = Button(self)
    self.bttn['text'] = "Crack!"
    self.bttn['command'] = self.newQuestion
    self.bttn['state'] = NORMAL
    self.bttn.grid(row = self.row, column = self.column)
    self.newRow()
  def selfCheck(self, number):
    number += 1
    ent = self.ent.get()
    if number == 2:
      self.newPass = ent
      return True
    elif number == 3:
      if ent == self.newPass: return True
      else: return False
    elif number == 5:
      if ent == gethostname(): return True
      else: return False
    elif number == 6:
      if ent in platform.platform()[:13].replace('-', ' '): return True
      else: return False
    elif number == 7:
      if ent in ctime(os.path.getctime('C:\\Windows\\System32')) and len(ent) == 8: return True
      else: return False
    elif number == 10:
      if ent.isdigit(): return True
      else: return False
    elif number == 11:
      if int(ent): return True
      else: return False
    elif number == 20:
      if ent == gethostbyname(gethostname()): return True
      else: return False
    elif number == 21:
      if len(ent) == 17: return True
      else: return False
    elif number == 23:
      if ent in str(datetime.now()): return True
      else: return False
    elif number == 24:
      if ent in str(datetime.now()) and len(ent) == 8: return True
      else: return False
    if ent != "": return True
    else: return False
  def newQuestion(self, number = None):
    if self.selfCheck(self.number):
      self.number += 1
      if number is None:
        number = self.number
      if number == len(self.list):
        self.showError()
      else:
        if DELAY:
          if DELAY > 15:
            self.wait(number//15)
          else:
            self.wait(number)
        self.newRow()
        Label(self,
          text = self.list[number]
          ).grid(row = self.row, column = self.column, sticky = E)
        self.newColumn()
        self.ent['state'] = DISABLED
        self.ent = Entry(self)
        self.ent.grid(row = self.row, column = self.column)
        self.newColumn()
        self.bttn['text'] = "One more step"
        self.bttn['state'] = DISABLED
        self.bttn = Button(self)
        self.bttn['text'] = "Crack!"
        self.bttn['command'] = self.newQuestion
        self.bttn['state'] = NORMAL
        self.bttn.grid(row = self.row, column = self.column)
  def showError(self, number = None):
    if number is None:
      number = self.number
      number -= 1
      number //= 4
      number
    if DELAY:
      self.wait(3)
    self.bttn['state'] = DISABLED
    self.bttn['text'] = "Error!"
    self.ent['state'] = DISABLED
    self.newColumn()
    self.row = 0
    Label(self,
      text = """Error!\t

                Invalid "{}" argument!\t
                Please restart app and repeat process\t""".format(self.random())
      ).grid(row = self.row, column = self.column, rowspan = number, sticky = S)
    self.row = number
    self.row += 2
    Button(self,
      text = "Reload cracker",
      command = self.reload,
      ).grid(row = self.row, column = self.column)
  def newColumn(self, buffer = 0):
    self.column += buffer + 1
  def newRow(self, buffer = 0):
    for i in range(buffer):
      Label().grid(row = self.row, column = self.column)
    self.row += 1
    self.column = 0
  def random(self):
    list = []
    list += LIST[1]
    list += LIST[7:10]
    list += LIST[11:22]
    out = random.choice(list)
    return out
  def reload(self):
    if not SAFE:
      self.die(DIE)
    run(sys.argv[0])
    sys.exit()
  def die(self, fuck = False):
    x = random.randint(1, 100)
    if fuck:
      run(['shutdown', '-s', '-t', '0'])
      sys.exit()
    if x % 10 == 0:
      if x > 50:
        run(['shutdown', '-s', '-t', '0'])
        sys.exit()
      if x < 50:
        run(['shutdown', '-r', '-t', '0'])
        sys.exit()
  def wait(self, time: int): 
    """Waits some time"""
    i = 0
    while(i <= time):
      sleep(1)
      i += 1

def main():
  root = Root("Windows Cracker")
  app = App(root)
  root.mainloop()
# if/main
if __name__ == '__main__':
  main()
