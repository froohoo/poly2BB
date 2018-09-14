#!/usr/bin/python

import wx
import os
import xml.etree.ElementTree as ET
import glob
from threading import Thread

EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class gaugeEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

class converter(Thread):
    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.inDir  = notify_window.panel.inputTxtCtrl.GetValue()
        self.outDir = notify_window.panel.outputTxtCtrl.GetValue()
        self.start()
       
        
    def about(self):
        pass
        
    def run(self):
        filelist = glob.glob(self.inDir + '/*.xml')
        numFiles = len(filelist)
        
        #TODO: POST THIS TO LOG WINDOW SUBSCRIBER 
        self._notify_window.panel.log.AppendText("Processing " + str(numFiles))
        self._notify_window.panel.log.AppendText(" files from: " + self.inDir +"\n")

        KITTI = {}
        processedFiles = 0
        for infile in filelist:
            tree = ET.parse(infile)
            root = tree.getroot()
            imgname = root.find('filename').text
            outfile = open(os.path.join(self.outDir, imgname.split('.')[0].strip() + ".txt"), 'w')
            for obj in root.findall('object'):
                # labelme retains delted objects
                if obj.find('deleted').text == '1': continue
                poly = obj.find('polygon')
                xcoords =[]
                ycoords =[]
                for pt in poly.findall('pt'):
                    xcoords.append(int(pt.find('x').text))
                    ycoords.append(int(pt.find('y').text))
                
                if obj.find('occluded').text == 'yes':
                    KITTI['occluded'] = '1'
                else: 
                    KITTI['occluded'] = '0'
                
                KITTI['type']         =  obj.find('name').text
                KITTI['truncated']    =  '0.0'                   
                KITTI['alpha']        =  '0.0'
                KITTI['left']         = min(xcoords)
                KITTI['right']        = max(xcoords)
                KITTI['top']          = min(ycoords)
                KITTI['bottom']       = max(ycoords)
                KITTI['height']       = '0.0'
                KITTI['width']        = '0.0'
                KITTI['length']       = '0.0'
                KITTI['locx']         = '0.0'
                KITTI['locy']         = '0.0'
                KITTI['locz']         = '0.0'
                KITTI['roty']         = '0.0'
                
                KITTIString = ""
                for key in ['type', 'truncated','occluded', 'alpha', 'left', 'top', 'right', 'bottom', 'height', 'width', 'length', 'locx', 'locy', 'locz', 'roty']:
                    KITTIString += str(KITTI[key]) + " "
                outfile.write(KITTIString + "\n")
            outfile.close()
            processedFiles += 1
            if processedFiles % 10 == 0: 
                wx.PostEvent(self._notify_window, gaugeEvent(int(100*processedFiles/numFiles)))
            if processedFiles == numFiles:
                wx.PostEvent(self._notify_window, gaugeEvent(100))
            
        self._notify_window.panel.log.AppendText("Processing complete. KITTI txt files written to: ")
        self._notify_window.panel.log.AppendText(self.outDir +"\n")

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
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
        self.panel.gauge = wx.Gauge(self.panel, range=100, \
                        style=wx.GA_HORIZONTAL)
        self.panel.log = wx.TextCtrl(self.panel, id = wx.ID_ANY, \
                        value="", style=wx.TE_READONLY | wx.TE_MULTILINE, size = (600, 100))
        self.panel.statusBox = wx.StaticBox(self.panel, wx.ID_ANY, \
                        "Output Progress")
        statusSizer = wx.StaticBoxSizer(self.panel.statusBox, wx.VERTICAL)
        statusSizer.Add(self.panel.gauge, 0, wx.EXPAND)
        statusSizer.Add(self.panel.log, 1, wx.EXPAND)
        mainSizer.Add(statusSizer, 0, wx.EXPAND)
        EVT_RESULT(self, self.OnResult)
        self.worker = None
        
        
        
        
        self.panel.SetSizer(mainSizer)
        mainSizer.Fit(self)
        
        self.Show()
        
    def OnResult(self, event):
        if event.data is None:
            pass
        else:
            self.panel.gauge.SetValue(event.data)

        
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
                self.panel.outputTxtCtrl.SetValue(outputDir)
            #self.panel.log.AppendText("Output Dir: " + outputDir +"\n")
            if not os.path.exists(outputDir):
                dlg = wx.MessageDialog(self, \
                    "Directory does not exist: \n" + outputDir + "\nCreate?", \
                    caption = "Output Directory", style=wx.YES_NO | wx.ICON_QUESTION)
                if(dlg.ShowModal() == wx.ID_YES):
                    os.makedirs(outputDir)
                    #TODO Needs some error handling to validate this worked.
            self.worker = converter(self)
        pass
        
class MainApp(wx.App):
    def OnInit(self):
        self.frame = MainWindow(None, "Poly2BB")
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True
#app = wx.App(False)
#frame = MainWindow(None, "Poly2BB")
#app.MainLoop()


if __name__ == '__main__':
    app = MainApp(0)
    app.MainLoop()
