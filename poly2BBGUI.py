#!/usr/bin/python

import wx
import os

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.dirname = ''
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Poly2BB')
        
        # Add a panel so it looks correct on all platforms
        self.panel = wx.Panel(self, wx.ID_ANY)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        imageSizer = wx.GridSizer(rows=2, cols=2, hgap=5, vgap=5)
        
        # Add a Statusbar in the bottom of the window
        self.CreateStatusBar() 
         
        # Input directory section
        self.panel.inputBtn = wx.Button(self.panel, wx.ID_ANY, "XML Dir", \
                        size = (75, -1))
        self.panel.inputTxtCtrl = wx.TextCtrl(self.panel, id = wx.ID_ANY, \
                        value="", style=wx.TE_READONLY, size = (600,-1))
        self.panel.Bind(wx.EVT_BUTTON, self.OnInputBtn, self.panel.inputBtn)
        self.panel.inputBox = wx.StaticBox(self.panel, wx.ID_ANY, \
                        "Directory Containing LabelMe XML Files")
        inputSizer = wx.StaticBoxSizer(self.panel.inputBox, wx.HORIZONTAL)
        inputSizer.Add(self.panel.inputBtn, 0, wx.EXPAND)
        inputSizer.Add(self.panel.inputTxtCtrl, 1, wx.EXPAND)
        mainSizer.Add(inputSizer, 0, wx.LEFT)
        
         # Output directory section
        self.panel.outputBtn = wx.Button(self.panel, wx.ID_ANY, "KITTI Dir", \
                        size = (75, -1))
        self.panel.outputTxtCtrl = wx.TextCtrl(self.panel, id = wx.ID_ANY, \
                        value="", size = (600,-1))

        self.panel.Bind(wx.EVT_BUTTON, self.OnOutputBtn, self.panel.outputBtn)
        self.panel.outputBox = wx.StaticBox(self.panel, wx.ID_ANY, \
                        "Output Directory for KITTI txt Files")
        outputSizer = wx.StaticBoxSizer(self.panel.outputBox, wx.HORIZONTAL)
        outputSizer.Add(self.panel.outputBtn, 0, wx.EXPAND)
        outputSizer.Add(self.panel.outputTxtCtrl, 1, wx.EXPAND)
        mainSizer.Add(outputSizer, 0, wx.LEFT)

                
        # Progress Section
        self.panel.goBtn = wx.Button(self.panel, wx.ID_ANY, "CONVERT")       
        mainSizer.Add(self.panel.goBtn, 0, wx.EXPAND)
        self.panel.Bind(wx.EVT_BUTTON, self.OnGoBtn, self.panel.goBtn)
        self.panel.guage = wx.Gauge(self.panel, range=100, \
                        style=wx.GA_HORIZONTAL)
        self.panel.log = wx.TextCtrl(self.panel, id = wx.ID_ANY, \
                        value="", style=wx.TE_READONLY | wx.TE_MULTILINE, size = (600, 100))
        self.panel.statusBox = wx.StaticBox(self.panel, wx.ID_ANY, \
                        "Output Progress")
        statusSizer = wx.StaticBoxSizer(self.panel.statusBox, wx.VERTICAL)
        statusSizer.Add(self.panel.guage, 0, wx.EXPAND)
        statusSizer.Add(self.panel.log, 1, wx.EXPAND)
        mainSizer.Add(statusSizer, 0, wx.EXPAND) 
        
        
        
        
        
        
        self.panel.SetSizer(mainSizer)
        mainSizer.Fit(self)
        
        self.Show()

        
    def OnInputBtn(self, event):
        dlg = wx.DirDialog(None, "Choose input directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            path = (dlg.GetPath())
            self.panel.inputTxtCtrl.ChangeValue(path)
        dlg.Destroy()
        
        
    def OnOutputBtn(self, event):
        dlg = wx.DirDialog(None, "Choose input directory", "", wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            path = (dlg.GetPath())
            self.panel.outputTxtCtrl.ChangeValue(path)
        dlg.Destroy()
        
        
        
    def OnGoBtn(self, event):
        # Check if directory exists and prompt if it doesn't
        outputDir = self.panel.outputTxtCtrl.GetValue()
        if len(outputDir):
            if outputDir[-1] == '/':
                outputDir = outputDir[0:-1]
            self.panel.log.AppendText("Output Dir: " + outputDir +"\n")
            if not os.path.exists(outputDir):
                dlg = wx.MessageDialog(self, \
                    "Directory does not exist: \n" + outputDir + "\nCreate?", \
                    caption = "Output Directory", style=wx.YES_NO | wx.ICON_QUESTION)
                if(dlg.ShowModal() == wx.ID_YES):
                    print(os.makedirs(outputDir))
                    #if os.makedirs(outputDir):
                    #    self.panel.log.WriteText("Created Directory: " + outputDir + "\n")
                    #else: 
                    #    self.panel.log.WriteText("Directory creation failed. \
                    #        Do you have the correct permissions?\n")
        #else: 
        #    self.panel.log.WriteText("No Output Directory Specified \n")
        #    return False
        # Count files to be processed
        # Print number of files to be processed and initiate %tracker
        
        # Call processing subroutine / update progress bar
        
        # Output summary of process
        
        pass
        
        
app = wx.App(False)
frame = MainWindow(None, "Poly2BB")
app.MainLoop()
