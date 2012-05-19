import braille
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
    self.SetSizerAndFit(vSizer)

  def onTyping(self, event):
    self.outText.SetValue(braille.convert(self.inText.GetValue()))

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

app = wx.App(False)
MyFrame()
app.MainLoop()
