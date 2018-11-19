from ROOT import *
from array import array
import random
import glob, sys, os
parent = os.path.join(os.getcwd(), os.pardir)
sys.path.append(parent)

import VHcc_Weights as weight
gStyle.SetOptStat(0)
gROOT.SetBatch(True)


if len(sys.argv)>1: combo=sys.argv[1]
if len(sys.argv)>1: sd=sys.argv[2]
# combo = 'Comb4_SR'   
# print combo
comb={}

                       # Z_min     Z_max  H_min H_Max ZpTmin  ZpTmax    CvsL CvsB
comb['Comb0_ZpT_bin1'] = [75,       105,    50, 200,    50,     150,    0.40,0.20]
comb['Comb0_ZpT_bin2'] = [75,       105,    50, 200,    0,      150,    0.40,0.20]


TAG = '_SR_'
nbins = 25
 
version = 'v10'
sampleList = {}
sampleList['dataDE']='DoubleEG'
sampleList['dataDM']='DoubleMuon'
sampleList['ZH_HToCC']='ZH_HToCC_ZToLL_M125_13TeV_powheg_pythia8'########## XSEC
sampleList['DYJetsInc']='DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['DYJetsHT100']='DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['DYJetsHT200']='DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['DYJetsHT400']='DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['DYJetsHT600']='DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['DYJetsHT800']='DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['DYJetsHT1200']='DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['DYJetsHT2500']='DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'

sampleList['TTbar']='TT_TuneCUETP8M2T4_13TeV-powheg-pythia8'
sampleList['WZ']='WZ_TuneCUETP8M1_13TeV-pythia8'
sampleList['ZZ']='ZZ_TuneCUETP8M1_13TeV-pythia8'
sampleList['ZH_HToBB']='ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8'


# keyList = list(sampleList.keys())
# random.seed(int(combo.split('Comb')[1].split('_')[0])*int(sd))
# random.shuffle(keyList)
# ckey = combo

# print "ckey : ",ckey
file = {}
process = {}


plotDict = {
'HIGGS_CvsL_Mass' : [15, 50, 200],
'jet_CvsL' : [15, 0, 1.5],
'jet_CvsB' : [15, 0, 1.5],
'CvsL_CvsLJet1' : [48, 0, 1.2],
'CvsL_CvsLJet2' : [48, 0, 1.2],
'CvsB_CvsLJet1' : [48, 0, 1.2],
'CvsB_CvsLJet2' : [48, 0, 1.2],
}

c1 = TCanvas('c1','c1', 800, 600)
for Key in sampleList:
    print "#####"*10
    print Key
    nTuple = glob.glob("/eos/cms/store/user/jblee/Hcc/ZllHcc/"+version+"_Hadd/"+sampleList[Key]+"_hadd.root")
    print nTuple[0]
    file[Key] = TFile(nTuple[0])        
outfile = TFile("templates/template_"+version+"_"+TAG+".root",'RECREATE')


for ckey in comb:
    Zmin    =   str(comb[ckey][0])
    Zmax    =   str(comb[ckey][1])
    Hmin    =   str(comb[ckey][2])
    Hmax    =   str(comb[ckey][3])
    ZpTmin  =   str(comb[ckey][4])
    ZpTmax  =   str(comb[ckey][5])
    CvsL    =   str(comb[ckey][6])
    CvsB    =   str(comb[ckey][7])       

    print "#####"*10
    print "#####"*10
    print ckey
    #  HpT_min WpT_min H_min H_Max Njets CvsL CvsB

    flavour_Split = ['cc','cb','cl','bb','bl','ll']
    Bool_DYSplit = True

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
            if Bool_DYSplit:
                if 'DYJets' not in Key:
                    process[Key][plot] = TH1F(plot+'_'+ckey+'__'+Key, plot+'_'+ckey+'__'+Key, nbin, xMin, xMax)
                else:
                    for cat in flavour_Split:
                        process[Key][plot+'_'+cat] = TH1F(plot+'_'+ckey+'__'+cat+'__'+Key, plot+'_'+ckey+'__'+cat+'__'+Key, nbin, xMin, xMax)
            else:
                process[Key][plot] = TH1F(plot+'_'+ckey+'__'+Key, plot+'_'+ckey+'__'+Key, nbin, xMin, xMax)
            
        iTree = file[Key].Get("Events")

        if 'SR_' in TAG:
            cut =  "*(Z_Mass>"+Zmin+")*(Z_Mass<"+Zmax+")"
            cut += "*(HIGGS_CvsL_Mass>"+Hmin+")*(HIGGS_CvsL_Mass<"+Hmax+")"
            if 'bin1' in ckey:
                cut += "*(Z_Pt>"+ZpTmin+")*(Z_Pt<"+ZpTmax+")"
            elif 'bin2' in ckey:
                cut += "*(Z_Pt>"+ZpTmax+")" 
            cut += "*(CvsL_CvsLJet1>"+CvsL+")"
            cut += "*(CvsB_CvsLJet1>"+CvsB+")"
        elif 'CR_LF' in TAG:
            cut =  "*((50<Z_Mass)*(Z_Mass<"+Zmin+")||(Z_Mass>"+Zmax+"))"
            cut += "*(HIGGS_CvsL_Mass>"+Hmin+")*(HIGGS_CvsL_Mass<"+Hmax+")"
            cut += "*(CvsL_CvsLJet1<"+CvsL+")"
            cut += "*(CvsB_CvsLJet1>"+CvsB+")"        
    
        for plot in plotDict:
            iTree.Project(plot+'_'+ckey+'__'+Key, plot, str(weight.eff_xsec[sampleList[Key]])+cut)
            if 'data' not in Key and 'DYJets' not in Key:
                process[Key][plot].Draw()
                process[Key][plot].Write()
                c1.Clear()
                c1.Update()
            if Bool_DYSplit:
                if 'DYJets' in Key:
                    for index, cat in enumerate(flavour_Split, 1):
                        if 'Inc' not in Key:
                            iTree.Project(plot+'_'+ckey+'__'+cat+'__'+Key, plot, str(weight.eff_xsec[sampleList[Key]])+cut+"*(Flag_Z_jet=="+str(index)+")")
                        elif 'Inc' in Key:            
                            iTree.Project(plot+'_'+ckey+'__'+cat+'__'+Key, plot, str(weight.eff_xsec[sampleList[Key]])+cut+"*(Flag_Z_jet=="+str(index)+")"+"*(LHE_HT<100)")                    
                        c1.Clear()
                        c1.Update()
            else:
                if 'Inc' not in Key:
                    iTree.Project(plot+'_'+ckey+'__'+Key, plot, str(weight.eff_xsec[sampleList[Key]])+cut)
                elif 'Inc' in Key:            
                    iTree.Project(plot+'_'+ckey+'__'+Key, plot, str(weight.eff_xsec[sampleList[Key]])+cut+"*(LHE_HT<100)")                    
                c1.Clear()
                c1.Update()
        
    Sig_List    = ['ZH_HToCC']
    DYJets_List  = ['DYJetsInc','DYJetsHT100','DYJetsHT200','DYJetsHT400','DYJetsHT600','DYJetsHT800','DYJetsHT1200','DYJetsHT2500']
    Data_List   = ['dataDM', 'dataDE']



    for plot in plotDict:
        sig_Template = process[Sig_List[0]][plot].Clone(plot+'_'+ckey+'__'+'ZllHToCC')
        sig_Template.SetTitle(plot+'_'+ckey+'__'+'ZllHToCC')
        for sig in Sig_List:
            if sig==Sig_List[0]: continue
            sig_Template.Add(process[sig][plot])
        sig_Template.Draw()
        sig_Template.Write()        
        c1.Clear()
        c1.Update()

        if Bool_DYSplit:    
            for cat in flavour_Split:
                DYjet_Template = process[DYJets_List[0]][plot+'_'+cat].Clone(plot+'_'+ckey+'__'+cat+'__'+'DYJets')
                DYjet_Template.SetTitle(plot+'_'+ckey+'__'+'DYJets')
                for dyjet in DYJets_List:
                    if dyjet==DYJets_List[0]: continue
                    DYjet_Template.Add(process[dyjet][plot+'_'+cat])
                DYjet_Template.Draw()
                DYjet_Template.Write()        
                c1.Clear()
                c1.Update()
        else:
            DYjet_Template = process[DYJets_List[0]][plot].Clone(plot+'_'+ckey+'__'+'DYJets')
            DYjet_Template.SetTitle(plot+'_'+ckey+'__'+'DYJets')
            for dyjet in DYJets_List:
                if dyjet==DYJets_List[0]: continue
                DYjet_Template.Add(process[dyjet][plot])
            DYjet_Template.Draw()
            DYjet_Template.Write()        
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

        