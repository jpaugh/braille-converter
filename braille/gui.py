# Copyright 2012 Jonathan Paugh
# See COPYING for license details
'''   coding=utf8
Graphical interface to braille converter
'''
from . import util, opt, convert, import_ruleset
import wx
import  wx.lib.filebrowsebutton as filebrowse

class MyFrame(wx.Frame):
  def __init__(self, **kwargs):
    super(MyFrame, self).__init__(parent=None,
	title='Braille Converter', size=(500,500), **kwargs)
    nb = wx.Notebook(self)
    nb.AddPage(InteractiveInput(nb), 'Interactive')
    #nb.AddPage(FileInput(nb), 'From file')
    self.Show(True)

class InteractiveInput(wx.Panel):
  '''
  in/out text boxes conversion is instant
  '''
  def __init__(self, parent):
    super(self.__class__, self).__init__(parent)
    self.inText = InputText(self)
    self.outText = OutputText(self)
    self.Bind(wx.EVT_TEXT, self.onTyping, self.inText)

    #Sizers
    vSizer = wx.BoxSizer(wx.VERTICAL)

    vSizer.Add(wx.StaticText(self, label='Type plain text here:'),
	0, wx.ALIGN_LEFT|wx.ALL)
    vSizer.Add(self.inText, 1, wx.GROW|wx.SOUTH)

    vSizer.Add(wx.StaticText(self, label='Braille output:'),
	0, wx.ALIGN_LEFT|wx.ALL)
    vSizer.Add(self.outText, 1, wx.GROW|wx.NORTH)

    if opt('debug'):
      #Add a logging window
      self.logger = OutputText(self)
      self.logger.write = lambda s: self.logger.AppendText(s)
      self.logger.flush = lambda : None
      self.logger.resetText = lambda : self.logger.SetValue('')
      util.log.replaceHandlerStream(self.logger)

      #Add debug panel
      self.dpanel = DebugPanel(self)

      vSizer.Add(wx.StaticText(self, label='Log output:'),
	  0, wx.ALIGN_LEFT|wx.ALL)
      vSizer.Add(self.logger, 1, wx.GROW|wx.NORTH)
      vSizer.Add(self.dpanel, 0)

    self.SetSizerAndFit(vSizer)

  def onTyping(self, event):
    if opt('debug'):
      self.logger.resetText()
    self.outText.SetValue(convert(self.inText.GetValue()))

class InputText(wx.TextCtrl):
  def __init__(self, *args, **kwargs):
    defargs = {'style': wx.TE_MULTILINE|wx.TE_PROCESS_TAB}
    defargs.update(kwargs)
    super(self.__class__, self).__init__(*args, **defargs)

class OutputText(wx.TextCtrl):
  def __init__(self, *args, **kwargs):
    defargs = {'style': wx.TE_MULTILINE|wx.TE_READONLY}
    defargs.update(kwargs)
    super(self.__class__, self).__init__(*args, **defargs)

class DebugPanel(wx.Panel):
  def __init__(self, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)

    shRuleset = wx.Button(self, wx.ID_ANY, label='Show &Ruleset')
    self.Bind(wx.EVT_BUTTON, self.show_ruleset, shRuleset)

    hSizer = wx.BoxSizer(wx.HORIZONTAL)
    hSizer.Add(shRuleset, 1, wx.GROW)
    self.SetSizerAndFit(hSizer)
    return

  def show_ruleset(self, event):
    '''
    Shows a listing of the current ruleset in another window.
    '''
    def format_ruleset(ruleset):
      res = []
      for i in xrange(len(ruleset)):
	r=ruleset[i]
	res.append('%d { prn: %s, brl %s, type: %s, pri: %d }' %
	  (i, repr(r['prn']), repr(r['brl']), r['type'], r['priority']))
      return '\n'.join(res)

    diag = wx.Frame(parent=topLevel, size=(500,800),
	title='Ruleset amer-2')
    diag.text = OutputText(diag)
    diag.text.SetValue(format_ruleset(import_ruleset('amer-2')))
    diag.vSizer = wx.BoxSizer(wx.VERTICAL)
    diag.vSizer.Add(diag.text, 1, wx.GROW)
    diag.SetSizerAndFit(diag.vSizer)
    diag.Show()


#TODO: Get this to work, too.
# It will need a better parser to support it, though
class FileInput(wx.Panel):
  '''
  in/out file name. Batch conversioun
  '''
  def __init__(self, parent):
    super(self.__class__, self).__init__(parent)
    inFile = filebrowse.FileBrowseButton(self, -1,
	changeCallback=self.OnInFile)

    outFile = filebrowse.FileBrowseButton(self, -1,
	changeCallback=self.OnOutFile)

    submit = wx.Button(self, label='Convert')
    self.Bind(wx.EVT_BUTTON, self.OnClick, submit)
    

    #Sizer
    vSizer = wx.BoxSizer(wx.VERTICAL)

    vSizer.Add(inFile, 1, wx.GROW)
    vSizer.Add(outFile, 1, wx.GROW)
    vSizer.Add(submit, 1, wx.GROW)




  def OnInFile(self, event):
    print 'self: %s\nevent: %s\nid: %d' % (self, event, event.GetId())

  def OnOutFile(self,event):
    print 'stuff'

  def OnClick(self, event):
    print 'Clicked on %s, event: %s' % (event.GetId(), event)
    pass
topLevel = None
def __main__():
  app = wx.App(False)
  topLevel = MyFrame()
  app.MainLoop()

if __name__ == '__main__':
  __main__()
