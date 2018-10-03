from ROOT import *
from array import array
import glob
import sys

parent = os.path.join(os.getcwd(), os.pardir)
sys.path.append(parent)
import VHcc_Weights as weight
import utils
gStyle.SetOptStat(0)
gROOT.SetBatch(True)

Region = 'CR_minZmass50'
TAG = 'checkV10_'+Region#+'_log'


Rfile = TFile("templates/template_v10_"+Region+".root",'READ')
can = TCanvas("can", "can", 800, 800) 

SIG_List = [
  {
    'component' : 'ZH_HToCC',
    'fillcolor' : 600+1,
    'fillstyle' : 1001,
    'linewidth' : 2,
    'linestyle' : 1,
    'label'     : 'ZllHcc',
  },
]
BKG_List = [

  {
    'component' : 'TTbar',
    'fillcolor' : 632+1,
    'fillstyle' : 1001,
    'linewidth' : 2,
    'linestyle' : 1,
    'label'     : 'ttbar',
  },
  
  {
    'component' : 'DYJetsInc',
    'fillcolor' : 800-2,
    'fillstyle' : 1001,
    'linewidth' : 2,
    'linestyle' : 1,
    'label'     : 'DY',
  },

  {
    'component' : 'ZZ',
    'fillcolor' : 416+3,
    'fillstyle' : 1001,
    'linewidth' : 2,
    'linestyle' : 1,
    'label'     : 'ZZ',
  },
  {
    'component' : 'WZ',
    'fillcolor' : 860+7,
    'fillstyle' : 1001,
    'linewidth' : 2,
    'linestyle' : 1,
    'label'     : 'WZ',
  },
  
]    
comb = 'Comb0'
hist={}
variable_List = [
'Z_Pt_'+comb+'_ZpT_bin1',
'Z_Mass_'+comb+'_ZpT_bin1', 
'jet_CvsL_'+comb+'_ZpT_bin1',
'jet_CvsB_'+comb+'_ZpT_bin1',
'jet_Pt_'+comb+'_ZpT_bin1',
'jet_Eta_'+comb+'_ZpT_bin1',
'jet_Phi_'+comb+'_ZpT_bin1',
'M_Pt_'+comb+'_ZpT_bin1',
'M_Eta_'+comb+'_ZpT_bin1',
'E_Pt_'+comb+'_ZpT_bin1',
'E_Eta_'+comb+'_ZpT_bin1',
'HIGGS_CvsL_Mass_'+comb+'_ZpT_bin1',
 
'Z_Mass_'+comb+'_ZpT_bin2', 
'Z_Pt_'+comb+'_ZpT_bin2',
'jet_CvsL_'+comb+'_ZpT_bin2',
'jet_CvsB_'+comb+'_ZpT_bin2',
'jet_Pt_'+comb+'_ZpT_bin2',
'jet_Eta_'+comb+'_ZpT_bin2',
'jet_Phi_'+comb+'_ZpT_bin2',
'M_Pt_'+comb+'_ZpT_bin2',
'M_Eta_'+comb+'_ZpT_bin2',
'E_Pt_'+comb+'_ZpT_bin2',
'E_Eta_'+comb+'_ZpT_bin2',
'HIGGS_CvsL_Mass_'+comb+'_ZpT_bin2',
]

for variable in variable_List:
    can.Divide(1, 2)        
    can.GetPad(1).SetPad('Top', '', 0., 0.25, 1.0, 1.0, 0, -1, 0)
    can.GetPad(1).SetTopMargin(0.069)
    can.GetPad(1).SetBottomMargin(0.0004)
    can.GetPad(1).SetRightMargin(0.046)
    can.GetPad(1).SetLeftMargin(0.138)
    can.GetPad(1).SetTicks(1, 1)        
    can.GetPad(2).SetPad("Bottom", '', 0., 0.0, 1.0, 0.25, 0, -1, 0)
    can.GetPad(2).SetBottomMargin(0.358)
    can.GetPad(2).SetRightMargin(0.046)
    can.GetPad(2).SetLeftMargin(0.138)
    can.cd(1)
    if 'log' in TAG:
        gPad.SetLogy()   

    print variable
    if 'Mass' in variable or 'Pt' in variable:
        unit = 'GeV'
    elif 'Eta' in variable:
        unit = 'Eta'
    elif 'Phi' in variable:
        unit = 'Phi'
    elif 'CvsL' in variable:
        unit = 'CvsL'
    elif 'CvsB' in variable:
        unit = 'CvsB'

    Title = variable
    ## BKG HISTOGRAMS
    for BKG in BKG_List:
        b = BKG['component']        
        hist[b] = Rfile.Get(variable+'__'+b)
        hist[b].SetFillColor(BKG['fillcolor'])
        hist[b].SetLineColor(BKG['fillcolor'])
        hist[b].SetLineStyle(BKG['linestyle'])

    ## BKG SUM (FROM POSTFIT BKG-ONLY)
    bkg = THStack("Bkg", " ")
    for BKG in BKG_List: 
        b = BKG['component']
        bkg.Add(hist[b])
    bkg.SetMaximum(int(1.3*bkg.GetMaximum()))
#     bkg.GetXaxis().SetTitle(xTitle)
    bkg.Draw('HIST')

    hist['signal'] = Rfile.Get(variable+'__ZH_HToCC')
    hist['signal'].SetLineWidth(5)
    hist['signal'].Scale(1000)
    hist['signal'].Draw('HIST SAME')

    hist['data'] = Rfile.Get(variable+'__data_obs')
    hist['data'].SetLineColor(1)
    hist['data'].SetLineWidth(2)
    hist['data'].SetMarkerStyle(20)
    hist['data'].SetMarkerSize(0.8)
    hist['data'].Draw('SAME PE')

    leg = TLegend(0.65,0.65,0.9,0.9)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0) #1001
    leg.SetFillColor(0)
    leg.SetNColumns(2)
    leg.AddEntry(hist['data'], 'Data', "PL")
    for BKG in BKG_List: 
        b = BKG['component']
        leg.AddEntry(hist[b], BKG['label'], "f")
    leg.AddEntry(hist['signal'], 'ZllHcc (#times1000)', "l")
    leg.Draw()
    utils.drawRatio(hist['data'],bkg, can, Title,TAG, unit)
    





