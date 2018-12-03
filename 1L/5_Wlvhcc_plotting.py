from ROOT import *
from array import array
import glob
import sys
import VHcc_Weights as weight
import utils
gStyle.SetOptStat(0)
gROOT.SetBatch(True)
# template_V4_SC_R.root template_v8_CR_minZmass50.root
# Region = 'CR_Zmass_CvsB'
Region = 'CR_preliminary'
# Region = 'CR_minZmass50'
TAG = 'check_'+Region#+'_log'


Rfile = TFile("WlvHccPlots/template_v2_"+Region+"_Comb5.root",'READ')
can = TCanvas("can", "can", 800, 800) 

SIG_List = [
  {
    'component' : 'WHToCC',
    'fillcolor' : 600+1,
    'fillstyle' : 1001,
    'linewidth' : 2,
    'linestyle' : 1,
    'label'     : 'WlvHcc',
  },
  {
    'component' : 'WminusH_HToCC',
    'fillcolor' : 600+1,
    'fillstyle' : 1001,
    'linewidth' : 2,
    'linestyle' : 1,
    'label'     : 'WlvHcc',
  },
  {
    'component' : 'WplusH_HToCC',
    'fillcolor' : 600+1,
    'fillstyle' : 1001,
    'linewidth' : 2,
    'linestyle' : 1,
    'label'     : 'WlvHcc',
  },

]
BKG_List = [  
  {
    'component' : 'WJetsInc',
    'fillcolor' : 800-2,
    'fillstyle' : 1001,
    'linewidth' : 2,
    'linestyle' : 1,
    'label'     : 'WJets',
  },
#   {
#     'component' : 'TTbar',
#     'fillcolor' : 632+1,
#     'fillstyle' : 1001,
#     'linewidth' : 2,
#     'linestyle' : 1,
#     'label'     : 'ttbar',
#   },
#   {
#     'component' : 'WW',
#     'fillcolor' : 416+3,
#     'fillstyle' : 1001,
#     'linewidth' : 2,
#     'linestyle' : 1,
#     'label'     : 'WW',
#   },
#   {
#     'component' : 'WZ',
#     'fillcolor' : 860+7,
#     'fillstyle' : 1001,
#     'linewidth' : 2,
#     'linestyle' : 1,
#     'label'     : 'WZ',
#   },
#   {
#     'component' : 'ST',
#     'fillcolor' : 632-9,
#     'fillstyle' : 1001,
#     'linewidth' : 2,
#     'linestyle' : 1,
#     'label'     : 'ST',
#   },  
]

# sampleList['QCD_HT100']='QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT200']='QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT300']='QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT500']='QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT700']='QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT1000']='QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT1500']='QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT2000']='QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'


    
comb = 'Comb4'
hist={}
variable_List = [
'W_Pt_'+comb+'_bin1',
'W_Mass_'+comb+'_bin1', 
'jet_CvsL_'+comb+'_bin1',
'jet_CvsB_'+comb+'_bin1',
'jet_Pt_'+comb+'_bin1',
'jet_Eta_'+comb+'_bin1',
'jet_Phi_'+comb+'_bin1',
'M_Pt_'+comb+'_bin1',
'M_Eta_'+comb+'_bin1',
'E_Pt_'+comb+'_bin1',
'E_Eta_'+comb+'_bin1',
'HIGGS_CvsL_Mass_'+comb+'_bin1',
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

#     for index, BKG in enumerate(BKG_List_ST, 1):
#         b = BKG['component']        
#         temp = Rfile.Get(variable+'__'+b)
#         if index == 1:
#             hist['ST'] = temp
#         hist['ST'].Add(temp)
#     hist['ST'].SetFillColor(632-9)
#     hist['ST'].SetLineColor(632-9)
#     hist['ST'].SetLineStyle(1001)

    ## BKG SUM (FROM POSTFIT BKG-ONLY)
    bkg = THStack("Bkg", " ")
    for BKG in BKG_List: 
        b = BKG['component']
        bkg.Add(hist[b])
#     bkg.Add(hist['ST'])
    bkg.SetMaximum(int(1.3*bkg.GetMaximum()))
#     bkg.GetXaxis().SetTitle(xTitle)
    bkg.Draw('HIST')

    hist['signal'] = Rfile.Get(variable+'__WHToCC')
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
    leg.AddEntry(hist['signal'], 'WlvHcc (#times1000)', "l")
    leg.Draw()
    if doRatio:
        utils.drawRatio(hist['data'],bkg, can, Title,TAG, unit)
    can.SaveAs(Title+'__'+TAG+'.png')
    can.Clear()
    can.Update()
    





