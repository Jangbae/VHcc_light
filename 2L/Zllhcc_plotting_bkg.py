from ROOT import *
from array import array
import glob
import sys
# import utils
gStyle.SetOptStat(0)
gROOT.SetBatch(True)
# template_V4_SC_R.root template_v8_CR_minZmass50.root
# Region = 'CR_Zmass_CvsB'
Region = 'SR_'
comb = 'Comb0_ZpT_bin2'
TAG = 'check_'+Region+'_'+comb
# WlvHccPlots/template_v2_CR_LF_preliminary_Comb4.root
Rfile = TFile("templates/template_v10__"+Region+".root",'READ')

SIG_List = [
  {
    'component' : 'ZHToCC',
    'fillcolor' : 600+1,
    'fillstyle' : 1001,
    'linewidth' : 2,
    'linestyle' : 1,
    'label'     : 'ZllHcc',
  },
]
BKG_List = [  
  {
    'component' : 'DYJetsInc',
    'fillcolor' : 800-2,
    'fillstyle' : 1001,
    'linewidth' : 2,
    'linestyle' : 1,
    'label'     : 'DYJets',
  },
]

hist={}
variable_List = [
'HIGGS_CvsL_Mass_'+comb,
'jet_CvsL_'+comb,
'jet_CvsB_'+comb,
'CvsL_CvsLJet1_'+comb,
'CvsL_CvsLJet2_'+comb,
'CvsB_CvsLJet1_'+comb,
'CvsB_CvsLJet2_'+comb,

]

List_split = ['ll','cc','cl','cb','bb','bl']

for variable in variable_List:
    can = TCanvas("can", "can", 800, 800) 
    if 'log' in TAG:
        gPad.SetLogy()   
    print variable
    if 'Mass' in variable or 'Pt' in variable:
        unit = 'GeV'
    elif 'Eta' in variable:
        unit = 'Eta'
    elif 'Phi' in variable:
        unit = 'Phi'
    elif 'CvsL' in variable and 'CvsB' not in variable:
        unit = 'CvsL'
    elif 'CvsB' in variable:
        unit = 'CvsB'

    Title = variable
    ## BKG HISTOGRAMS
    count = 1
    histSig = Rfile.Get(variable+'__ZllHToCC')
    histSig.Scale(1/histSig.Integral())
    histSig.SetLineColor(600)

    for split in List_split:
        print variable+'__'+split+'__DYJets'         
        hist[split] = Rfile.Get(variable+'__'+split+'__DYJets')
        hist[split].Scale(1/hist[split].Integral())
        if 'll' in split:
            hist[split].GetYaxis().SetRangeUser(0.0,hist[split].GetMaximum()+0.15)
            hist[split].SetTitle("DYJets splitting in SR bin2;"+unit)
        hist[split].SetLineColor(800+count)
        hist[split].SetLineStyle(1)
        hist[split].SetLineWidth(4)

        hist[split].Draw('HIST SAME')
        count+=3
    histSig.SetLineWidth(4)
    histSig.SetLineStyle(2)
    histSig.Draw('HIST SAME')
    
    leg = TLegend(0.65,0.65,0.9,0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    leg.SetNColumns(2)
    leg.AddEntry(histSig, "ZllHcc" , "f")
    for split in List_split:        
        leg.AddEntry(hist[split], split, "f")
    leg.Draw()
    can.SaveAs(Title+'__'+TAG+'_'+'.png')
    can.Clear()
    can.Update()
    





