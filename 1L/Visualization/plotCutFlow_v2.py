import os, sys, glob
from ROOT import *
from array import array
import random 
import numpy as np
import glob, sys
import matplotlib.pyplot as plt
gStyle.SetOptStat(0)
gROOT.SetBatch(True)


def plotting(sigList, bkgList, ticks, nlep):
    Sig_ratioList = [sig/sigList[0] for sig in sigList]
    Bkg_ratioList = [bkg/bkgList[0] for bkg in bkgList]
    bincuts = [0,1,2,3,4,5,6,7]
    print Sig_ratioList
    print Bkg_ratioList

    if nlep == 0:
        signal = 'ZvvHcc'
        bkg = 'ttbar'
    elif nlep == 1:
        signal = 'WlvHcc'
        bkg = 'ttbar'
        bincuts = [0,1,2,3,4,5,6,7,8]
    elif nlep == 2:
        signal = 'ZllHcc'
        bkg = 'DY'
    plt.plot(bincuts, Sig_ratioList, color='r', marker="o", label=signal)
    plt.plot(bincuts, Bkg_ratioList, color='b', marker="o", label=bkg)
    for i, sig in enumerate(Sig_ratioList):
        plt.annotate(round(sig, 2), (bincuts[i],Sig_ratioList[i]), color='r') 
    for i, bkg in enumerate(Bkg_ratioList):
        plt.annotate(round(bkg, 2), (bincuts[i],Bkg_ratioList[i]), color='b') 
    if nlep == 1:
        plt.xticks(np.arange(9),ticks,fontsize=10,rotation=45)
    else:
        plt.xticks(np.arange(8),ticks,fontsize=10,rotation=45)

    plt.ylabel("Efficiency")
    plt.legend()
    plt.grid(True)
    plt.savefig("Cutflow_"+str(nlep)+"L.png", bbox_inches="tight")
    plt.close()

dic_sample = {}
sampleList_0l = [
'TT_powheg',
'ZH125ToCC_ZNuNu_powheg'
]

sampleList_1l = [
'TT_powheg',
'WplusH125ToCC_WLNu_powheg',
'WminusH125ToCC_WLNu_powheg',
]

sampleList_2l = [
'DYToLL_HT100to200',
'DYToLL_HT200to400',
'DYToLL_HT400to600',
'DYToLL_HT600to800',
'DYToLL_HT800to1200',
'DYToLL_HT1200to2500',
'DYToLL_HT2500toInf',
# 'DYToLL_madgraph',
'ZH125ToCC_ZLL_powheg',
]

sampleList = sampleList_2l

runDir=os.getcwd()
version = 'v2'
nlepton = 'VHbbAnalysisNtuples'
sampleListDir = 'sampleList_WlvHcc'
inputPath = "/eos/cms/store/user/jblee/"+nlepton+"/"+version+"_Hadd/"

plotDict = {
'Pass_nominal' : [2, 0, 2],
}
file = {}
c1 = TCanvas('c1','c1', 800, 600)
for Key in sampleList:
    print "#####"*10
    print Key
    nTuple = glob.glob(inputPath+Key+"_hadd.root")
    print nTuple
    file[Key] = TFile(nTuple[0])        

process = {}
procDicBinCont = {}

if 'NuNu_' in sampleList[-1]:
    cut_0       =  "( Pass_nominal ) * ( controlSample == 0 ) * (isZnn)"
    cut_1       = cut_0   + "* (twoResolvedJets) * ( max(Jet_Pt[hJetInd1],Jet_Pt[hJetInd2]) > 60 ) * ( min(Jet_Pt[hJetInd1],Jet_Pt[hJetInd2]) > 35 ) * ( nJetsCloseToMET==0 )"
    cut_2       = cut_1 + "* ( H_pt>120 )"
    cut_3       = cut_2 + "* ( HVdPhi_noFSR>2.0 )"
    cut_4       = cut_3 + " * ( H_mass>50 ) * ( H_mass<200 )"        
    cut_5       = cut_4 + " * ( dPhi_MET_TkMET < 0.5 )"        
    cut_6       = cut_5 + " * ( MET_Pt>170 )"            
    cut_7       = cut_6 + " * ( Jet_CvsL[hJetInd1]>0.90 ) * ( Jet_CvsB[hJetInd1]>0.20 ) * ( Jet_CvsB[hJetInd2]>0.3 )"

if 'LL_' in sampleList[-1]:
    cut_0       =  "( Pass_nominal ) * ( controlSample == 0 ) * (isZee || isZmm)"
    cut_1       = cut_0 + "* (twoResolvedJets) * (Jet_Pt[hJetInd1]>25) * (Jet_Pt[hJetInd2]>25)"
    cut_2       = cut_1 + "* ( H_pt>50 )"
    cut_3       = cut_2 + "* ( HVdPhi>2.5 )"
    cut_4       = cut_3 + " * ( H_mass>50 ) * ( H_mass<200 )"        
    cut_5       = cut_4 + " * ( V_mass>75) * ( V_mass<105 )"        
    cut_6       = cut_5 + " * ( V_pt>50 ) * ( V_pt<150 )"            
    cut_7       = cut_6 + " * (Jet_CvsL[hJetInd1]>0.85) * (Jet_CvsB[hJetInd1]>0.20) * (Jet_CvsB[hJetInd2]>0.2)"            

if 'WLNu_' in sampleList[-1]:
    cut_0       =  "( Pass_nominal ) * ( controlSample == 0 ) * (isWenu)"
    cut_1       = cut_0 + "* (twoResolvedJets) * (Jet_Pt[hJetInd1]>25) * (Jet_Pt[hJetInd2]>25)"
    cut_2       = cut_1 + "* ( MET_pt>60 )"
    cut_3       = cut_2 + "* ( HVdPhi>2.5 )"
    cut_4       = cut_3 + " * ( H_mass>50 ) * ( H_mass<200 )"        
    cut_5       = cut_4 + " * ( SA5<4)"        
    cut_6       = cut_5 + " * ( V_pt>100 )"            
    cut_7       = cut_6 + " * ( H_pt>100 )"                
    cut_8       = cut_7 + " * (Jet_CvsL[hJetInd1]>0.90) * (Jet_CvsB[hJetInd1]>0.20) * (Jet_CvsL[hJetInd2]>0.15) * (Jet_CvsB[hJetInd2]>0.15)"            

for Key in sampleList:
    print "#####"*10
    print Key
    for plot in plotDict:
        nbin = plotDict[plot][0]
        xMin = plotDict[plot][1]
        xMax = plotDict[plot][2]
        process[Key+'cut0'] = TH1F(plot+'__'+Key+'__cut0', plot+'__'+Key+'__cut0', nbin, xMin, xMax)
        process[Key+'cut1'] = TH1F(plot+'__'+Key+'__cut1', plot+'__'+Key+'__cut1', nbin, xMin, xMax)
        process[Key+'cut2'] = TH1F(plot+'__'+Key+'__cut2', plot+'__'+Key+'__cut2', nbin, xMin, xMax)
        process[Key+'cut3'] = TH1F(plot+'__'+Key+'__cut3', plot+'__'+Key+'__cut3', nbin, xMin, xMax)
        process[Key+'cut4'] = TH1F(plot+'__'+Key+'__cut4', plot+'__'+Key+'__cut4', nbin, xMin, xMax)
        process[Key+'cut5'] = TH1F(plot+'__'+Key+'__cut5', plot+'__'+Key+'__cut5', nbin, xMin, xMax)
        process[Key+'cut6'] = TH1F(plot+'__'+Key+'__cut6', plot+'__'+Key+'__cut6', nbin, xMin, xMax)
        process[Key+'cut7'] = TH1F(plot+'__'+Key+'__cut7', plot+'__'+Key+'__cut7', nbin, xMin, xMax)
        if 'WLNu_' in sampleList[-1]:
            process[Key+'cut8'] = TH1F(plot+'__'+Key+'__cut8', plot+'__'+Key+'__cut8', nbin, xMin, xMax)                                                                                
    iTree = file[Key].Get("Events")
        
    procDicBinCont[Key+'cut0'] = []
    procDicBinCont[Key+'cut1'] = []
    procDicBinCont[Key+'cut2'] = []
    procDicBinCont[Key+'cut3'] = []
    procDicBinCont[Key+'cut4'] = []
    procDicBinCont[Key+'cut5'] = []
    procDicBinCont[Key+'cut6'] = []
    procDicBinCont[Key+'cut7'] = []
    if 'WLNu_' in sampleList[-1]:
        procDicBinCont[Key+'cut8'] = []                    
        
    for plot in plotDict:
        iTree.Project(plot+'__'+Key+'__cut0', plot, cut_0)
        iTree.Project(plot+'__'+Key+'__cut1', plot, cut_1)
        iTree.Project(plot+'__'+Key+'__cut2', plot, cut_2)
        iTree.Project(plot+'__'+Key+'__cut3', plot, cut_3)
        iTree.Project(plot+'__'+Key+'__cut4', plot, cut_4)
        iTree.Project(plot+'__'+Key+'__cut5', plot, cut_5)
        iTree.Project(plot+'__'+Key+'__cut6', plot, cut_6)
        iTree.Project(plot+'__'+Key+'__cut7', plot, cut_7)                        
        if 'WLNu_' in sampleList[-1]:
            iTree.Project(plot+'__'+Key+'__cut8', plot, cut_8)                                        
        if 'DYToLL' not in Key and 'WLNu' not in Key:
            for i in range(2,process[Key+'cut7'].GetNbinsX()+1):
                procDicBinCont[Key+'cut0'].append(process[Key+'cut0'].GetBinContent(i))
                procDicBinCont[Key+'cut1'].append(process[Key+'cut1'].GetBinContent(i))
                procDicBinCont[Key+'cut2'].append(process[Key+'cut2'].GetBinContent(i))
                procDicBinCont[Key+'cut3'].append(process[Key+'cut3'].GetBinContent(i))
                procDicBinCont[Key+'cut4'].append(process[Key+'cut4'].GetBinContent(i))
                procDicBinCont[Key+'cut5'].append(process[Key+'cut5'].GetBinContent(i))
                procDicBinCont[Key+'cut6'].append(process[Key+'cut6'].GetBinContent(i))
                procDicBinCont[Key+'cut7'].append(process[Key+'cut7'].GetBinContent(i))                                                                                
                if 'WLNu_' in sampleList[-1]:
                    procDicBinCont[Key+'cut8'].append(process[Key+'cut8'].GetBinContent(i))                                                                                

WH_List    = ['WminusH125ToCC_WLNu_powheg','WplusH125ToCC_WLNu_powheg']
DY_List     = ['DYToLL_HT100to200','DYToLL_HT200to400','DYToLL_HT400to600','DYToLL_HT600to800','DYToLL_HT800to1200','DYToLL_HT1200to2500','DYToLL_HT2500toInf']#,'DYToLL_madgraph']

cuts = ['cut0','cut1', 'cut2','cut3','cut4','cut5', 'cut6','cut7']
if 'WLNu_' in sampleList[-1]:
    cuts = ['cut0','cut1', 'cut2','cut3','cut4','cut5', 'cut6','cut7','cut8']
    
WHBinCont_List = []
DYBinCont_List = []
# for plot in plotDict:
#     if 'LL_' in sampleList[-1]:
#         DY_Template = process[DY_List[0]].Clone(plot+'__'+'DY')    
#         DY_Template.SetTitle(plot+'__'+'DY')
#         for st in DY_List:
#             if st==DY_List[0]: continue
#             DY_Template.Add(process[st])
#         Nbin = DY_Template.GetNbinsX()
#         for i in range(2,Nbin+1):
#             DYBinCont_List.append(DY_Template.GetBinContent(i))        

DY_Template_dic = {}
WH_Template_dic = {}
DYBinCont_dic = {}
WHBinCont_dic = {}

for cut in cuts:
    for plot in plotDict:
        if 'LL_' in sampleList[-1]:
            DY_Template_dic[cut] = process[DY_List[0]+cut].Clone(plot+'__'+'DY')    
            for st in DY_List:
                if st==DY_List[0]: continue
                DY_Template_dic[cut].Add(process[st+cut])
            Nbin = DY_Template_dic[cut].GetNbinsX()
            DYBinCont_dic[cut]=[]
            for i in range(2,Nbin+1):
                DYBinCont_dic[cut].append(DY_Template_dic[cut].GetBinContent(i))        

        if 'WLNu_' in sampleList[-1]:
            WH_Template_dic[cut] = process[WH_List[0]+cut].Clone(plot+'__'+'DY')    
            for st in WH_List:
                if st==WH_List[0]: continue
                WH_Template_dic[cut].Add(process[st+cut])
            Nbin = WH_Template_dic[cut].GetNbinsX()
            WHBinCont_dic[cut]=[]
            for i in range(2,Nbin+1):
                WHBinCont_dic[cut].append(WH_Template_dic[cut].GetBinContent(i))        


print "procDicBinCont : ",procDicBinCont

if 'NuNu_' in sampleList[-1]:
    Sig_0L_List = procDicBinCont['ZH125ToCC_ZNuNu_powheg']
    Bkg_0L_List = procDicBinCont['TT_powheg']
    for cut in cuts:
        Sig_0L_List += procDicBinCont['ZH125ToCC_ZNuNu_powheg'+cut]
        Bkg_0L_List += procDicBinCont['TT_powheg'+cut]
    tickList=['Pass_nominal','twoResolvedJets','H_pt>120','HVdPhi_noFSR>2.0','50<H_mass<200','dPhi_MET_TkMET < 0.5','MET_Pt>170','JetCvsL/B']
    plotting(Sig_0L_List, Bkg_0L_List, tickList, 0)


if 'LL_' in sampleList[-1]:
    Sig_2L_List = []#procDicBinCont['ZH125ToCC_ZLL_powheg']
    Bkg_2L_List = []
    for cut in cuts:
        Sig_2L_List += procDicBinCont['ZH125ToCC_ZLL_powheg'+cut]
        Bkg_2L_List += DYBinCont_dic[cut]
    tickList=['Pass_nominal','twoResolvedJets','H_pt>50','HVdPhi>2.5','50<H_mass<200','75<V_mass<105','50<V_pt<150','JetCvsL/B']
    plotting(Sig_2L_List, Bkg_2L_List, tickList, 2)


if 'WLNu_' in sampleList[-1]:
    Sig_1L_List = WHBinCont_List
    Bkg_1L_List = []
    for cut in cuts:
        Sig_1L_List += WHBinCont_dic[cut]
        Bkg_1L_List += procDicBinCont['TT_powheg'+cut]
    tickList=['Pass_nominal','twoResolvedJets','MET_pt>60','HVdPhi>2.5','50<H_mass<200','SA5<4','V_pt>100','H_pt>100','JetCvsL/B']
    plotting(Sig_1L_List, Bkg_1L_List, tickList, 1)


    
