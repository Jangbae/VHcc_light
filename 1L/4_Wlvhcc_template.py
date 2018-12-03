from ROOT import *
from array import array
import random
import glob, sys
import VHcc_Weights as weight
gStyle.SetOptStat(0)
gROOT.SetBatch(True)


if len(sys.argv)>1: combo=sys.argv[1]
if len(sys.argv)>1: sd=sys.argv[2]
# combo = 'Comb4_SR'   
# print combo
comb={}

                    # HpT_min  WpT_min H_min H_Max Njets CvsL CvsB
comb['Comb4_SR']    = [150,      150,    50, 200,    4,  0.40,0.15]
comb['Comb4_TTbar'] = [150,      150,    90, 150,    4,  0.40,0.15]
comb['Comb4_HF']    = [150,      150,    90, 150,    2,  0.40,0.15]
comb['Comb4_LF']    = [150,      150,    50, 200,    2,  0.40,0.15]


TAG = '_'+combo
nbins = 25
 
version = 'v2'
sampleList = {}
sampleList['dataSE']='SingleElectron'
sampleList['dataSM']='SingleMuon'

sampleList['WminusH_HToCC']='WminusH_HToCC_WToLNu_M125_13TeV_powheg_pythia8'########## XSEC
sampleList['WplusH_HToCC']='WplusH_HToCC_WToLNu_M125_13TeV_powheg_pythia8'########## XSEC

sampleList['WJetsInc']='WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['WJetsHT100']='WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['WJetsHT200']='WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['WJetsHT400']='WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['WJetsHT600']='WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['WJetsHT800']='WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['WJetsHT1200']='WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['WJetsHT2500']='WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'


sampleList['WW']='WW_TuneCUETP8M1_13TeV-pythia8'
sampleList['WZ']='WZ_TuneCUETP8M1_13TeV-pythia8'

sampleList['TTbar']='TT_TuneCUETP8M2T4_13TeV-powheg-pythia8'
sampleList['ST_s-channel']='ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8'
sampleList['ST_t-channel_antitop']='ST_t-channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin'
sampleList['ST_t-channel_top']='ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1'
sampleList['ST_tW_antitop']='ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4'
sampleList['ST_tW_top']='ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1'

# sampleList['DYJetsInc']='DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT100']='QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT200']='QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT300']='QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT500']='QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT700']='QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT1000']='QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT1500']='QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
# sampleList['QCD_HT2000']='QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'

keyList = list(sampleList.keys())
random.seed(int(combo.split('Comb')[1].split('_')[0])*int(sd))
random.shuffle(keyList)
ckey = combo

file = {}
process = {}

plotDict = {
# 'W_Mass' : [100, 0, 300],
# 'W_Pt' : [60, 0, 600],
# 'E_Pt' : [60, 0, 600],
# 'E_Eta' : [40, -4, 4],
# 'E_Phi' : [40, -4, 4],
# 'M_Pt' : [60, 0, 600],
# 'M_Eta' : [40, -4, 4],
# 'M_Phi' : [40, -4, 4],
# 'jet_Pt' : [60, 0, 600],
# 'jet_Eta' : [40, -4, 4],
# 'jet_Phi' : [40, -4, 4],
# 'jet_CvsL' : [30, 0, 1.5],
# 'jet_CvsB' : [30, 0, 1.5],
'CvsL_CvsLJet1' : [48, 0, 1.2],
# 'CvsL_CvsLJet2' : [48, 0, 1.2],
'CvsB_CvsLJet1' : [48, 0, 1.2],
# 'CvsB_CvsLJet2' : [48, 0, 1.2],
'HIGGS_CvsL_Mass' : [nbins, 50, 200],
# 'HIGGS_CvsL_Mass' : [15, 50, 200],
# 'SoftActivityJetHT' : [60, 0, 600],
# 'SoftActivityJetNjets2' : [10, 0, 10],
# 'SoftActivityJetNjets5' : [10, 0, 10],
# 'SoftActivityJetNjets10' : [10, 0, 10],
# 'DPhi_VH' : [40, -4, 4],
# 'DPhi_METlep' : [40, -4, 4],
# 'DR_cc' : [40, 0, 4],
# 'lepDR_cc' : [40, 0, 4],
# 'W_Tmass' : [60, 0, 600],
# 'top_Mass' : [60, 0, 600],
# 'M_lep_c' : [60, 0, 600],
# 'centrality' : [40, -0.1, 1.1],
# 'avgCvsLpT' : [40, -0.1, 1.1],
# 'FWmoment_1' : [40, -0.1, 1.1],
# 'FWmoment_2' : [40, -0.1, 1.1],
# 'FWmoment_3' : [40, -0.1, 1.1],
# 'FWmoment_4' : [40, -0.1, 1.1],
}

c1 = TCanvas('c1','c1', 800, 600)
for Key in sampleList:
    print "#####"*10
    print Key
    nTuple = glob.glob("/eos/cms/store/user/jblee/Hcc/WlvHcc/"+version+"_Hadd/"+sampleList[Key]+"_hadd.root")
    print nTuple[0]
    file[Key] = TFile(nTuple[0])        
outfile = TFile("WlvHccPlots/template_"+version+"_"+TAG+".root",'RECREATE')

print "#####"*10
print "#####"*10
print ckey
#  HpT_min WpT_min H_min H_Max Njets CvsL CvsB
HpT_min  =   str(comb[ckey][0])
WpT_min  =   str(comb[ckey][1])
Hmin    =   str(comb[ckey][2])
Hmax    =   str(comb[ckey][3])
Njets   =   str(comb[ckey][4])
CvsL    =   str(comb[ckey][5])
CvsB    =   str(comb[ckey][6])       

wjets_Split = ['cc','cb','cl','bb','bl','ll']

tempHistE = 0
tempHistM = 0
for Key in sampleList:
    print "#####"*10
    print Key
    process[Key] = {}
    for plot in plotDict:
        nbin = plotDict[plot][0]
        xMin = plotDict[plot][1]
        xMax = plotDict[plot][2]
        if 'WJets' not in Key:
            process[Key][plot] = TH1F(plot+'_'+ckey+'__'+Key, plot+'_'+ckey+'__'+Key, nbin, xMin, xMax)
        else:
            for cat in wjets_Split:
                process[Key][plot+'_'+cat] = TH1F(plot+'_'+ckey+'__'+cat+'__'+Key, plot+'_'+ckey+'__'+cat+'__'+Key, nbin, xMin, xMax)
            
    iTree = file[Key].Get("Events")
    if 'SR' in TAG and int(combo.split('Comb')[1].split('_SR')[0])<12:
        cut =  "*(HIGGS_CvsL_Mass<"+Hmax+")"
        cut += "*(HIGGS_CvsL_Mass>"+Hmin+")"
        cut += "*(HIGGS_CvsL_Pt>"+HpT_min+")"
        cut += "*(W_Pt>"+WpT_min+")"
        cut += "*(jet_nJet<"+Njets+")"            
        cut += "*(CvsL_CvsLJet1>"+CvsL+")"
        cut += "*(CvsB_CvsLJet1>"+CvsB+")"            
        cut += "*(abs(DPhi_VH)>2.5)"            
        cut += "*(abs(DPhi_METlep)<2)"            

    elif 'LF' in TAG:
        cut =  "*(HIGGS_CvsL_Mass<"+Hmax+")" 
        cut += "*(HIGGS_CvsL_Pt>"+HpT_min+")"
        cut += "*(W_Pt>"+WpT_min+")"
        cut += "*(CvsL_CvsLJet1<"+CvsL+")"
        cut += "*(CvsB_CvsLJet1>"+CvsB+")"
        cut += "*(abs(DPhi_VH)>2.5)"            
        cut += "*(abs(DPhi_METlep)<2)"            

    elif 'HF' in TAG:
        cut =  "*((HIGGS_CvsL_Mass>"+Hmax+")||(HIGGS_CvsL_Mass<"+Hmin+"))" 
        cut += "*(HIGGS_CvsL_Pt>"+HpT_min+")"
        cut += "*(W_Pt>"+WpT_min+")"
        cut += "*(jet_nJet=="+Njets+")"            
        cut += "*(CvsL_CvsLJet1>"+CvsL+")"
        cut += "*(CvsB_CvsLJet1<"+CvsB+")"
        cut += "*(abs(DPhi_VH)>2.5)"            
        cut += "*(abs(DPhi_METlep)<2)"            

    elif 'TTbar' in TAG:
        cut =  "*((HIGGS_CvsL_Mass>"+Hmax+")||(HIGGS_CvsL_Mass<"+Hmin+"))" 
        cut += "*(HIGGS_CvsL_Pt>"+HpT_min+")"
        cut += "*(W_Pt>"+WpT_min+")"
        cut += "*(jet_nJet>="+Njets+")"            
        cut += "*(CvsL_CvsLJet1>"+CvsL+")"
        cut += "*(CvsB_CvsLJet1<"+CvsB+")"
        cut += "*(abs(DPhi_VH)>2.5)"            
        cut += "*(abs(DPhi_METlep)<2)"            


    
    for plot in plotDict:
        iTree.Project(plot+'_'+ckey+'__'+Key, plot, str(weight.eff_xsec[sampleList[Key]])+cut)
        if 'ST' not in Key and 'data' not in Key and 'HToCC' not in Key and 'WJets' not in Key:
            process[Key][plot].Draw()
            process[Key][plot].Write()
            c1.Clear()
            c1.Update()
        if 'WJets' in Key:
            for index, cat in enumerate(wjets_Split, 1):
                if 'Inc' not in Key:
                    iTree.Project(plot+'_'+ckey+'__'+cat+'__'+Key, plot, str(weight.eff_xsec[sampleList[Key]])+cut+"*(Flag_W_jet=="+str(index)+")")
                elif 'Inc' in Key:            
                    iTree.Project(plot+'_'+ckey+'__'+cat+'__'+Key, plot, str(weight.eff_xsec[sampleList[Key]])+cut+"*(Flag_W_jet=="+str(index)+")"+"*(LHE_HT<100)")                    
                c1.Clear()
                c1.Update()

Sig_List    = ['WminusH_HToCC','WplusH_HToCC']
ST_List     = ['ST_s-channel','ST_t-channel_antitop','ST_t-channel_top','ST_tW_antitop','ST_tW_top']
WJets_List  = ['WJetsInc','WJetsHT100','WJetsHT200','WJetsHT400','WJetsHT600','WJetsHT800','WJetsHT1200','WJetsHT2500']
Data_List   = ['dataSE','dataSM']

for plot in plotDict:
    sig_Template = process[Sig_List[0]][plot].Clone(plot+'_'+ckey+'__'+'WHToCC')
    sig_Template.SetTitle(plot+'_'+ckey+'__'+'WHToCC')
    for sig in Sig_List:
        if sig==Sig_List[0]: continue
        sig_Template.Add(process[sig][plot])
    sig_Template.Draw()
    sig_Template.Write()        
    c1.Clear()
    c1.Update()
    
    for cat in wjets_Split:
        wjet_Template = process[WJets_List[0]][plot+'_'+cat].Clone(plot+'_'+ckey+'__'+cat+'__'+'WJets')
        wjet_Template.SetTitle(plot+'_'+ckey+'__'+'WJets')
        for wjet in WJets_List:
            if wjet==WJets_List[0]: continue
            wjet_Template.Add(process[wjet][plot+'_'+cat])
        wjet_Template.Draw()
        wjet_Template.Write()        
        c1.Clear()
        c1.Update()
    
    ST_Template = process[ST_List[0]][plot].Clone(plot+'_'+ckey+'__'+'ST')    
    ST_Template.SetTitle(plot+'_'+ckey+'__'+'ST')
    for st in ST_List:
        if st==ST_List[0]: continue
        ST_Template.Add(process[st][plot])
    ST_Template.Draw()
    ST_Template.Write()        
    c1.Clear()
    c1.Update()

    Data_Template = process[Data_List[0]][plot].Clone(plot+'_'+ckey+'__'+'data_obs')            
    Data_Template.SetTitle(plot+'_'+ckey+'__'+'data_obs')
    for data in Data_List:
        if data==Data_List[0]: continue
        Data_Template.Add(process[data][plot])
    Data_Template.Draw()
    Data_Template.Write()        
    c1.Clear()
    c1.Update()

        