from ROOT import *
from array import array
import glob, sys, os

parent = os.path.join(os.getcwd(), os.pardir)
sys.path.append(parent)

import VHcc_Weights as weight
gStyle.SetOptStat(0)
gROOT.SetBatch(True)

comb={}
comb['Comb0_ZpT_bin1'] = [75,105,50,200,50,150,0.40,0.20]
comb['Comb0_ZpT_bin2'] = [75,105,50,200,0,150, 0.40,0.20]

# comb['Comb0_ZpT_bin1'] = [75,105,50,200,50,150,0.40,0.20]
# TAG = 'SR_WP_Scan_CvsL45_CvsB15'
# TAG = 'CvsB_CvsL_CR2'
TAG = 'SR_bins' 
version = 'v10'
nlepton = 'ZllHcc'

sampleList = {}
sampleList['dataDE']='DoubleEG'
sampleList['dataDM']='DoubleMuon'
sampleList['ZH_HToCC']='ZH_HToCC_ZToLL_M125_13TeV_powheg_pythia8'########## XSEC
sampleList['DYJetsInc']='DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'
sampleList['TTbar']='TT_TuneCUETP8M2T4_13TeV-powheg-pythia8'
sampleList['WZ']='WZ_TuneCUETP8M1_13TeV-pythia8'
sampleList['ZZ']='ZZ_TuneCUETP8M1_13TeV-pythia8'
sampleList['ZH_HToBB']='ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8'

file = {
}
for Key in sampleList:
    fileList = []
    print "#####"*10
    print Key
    nTuple = glob.glob("/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"_Hadd/"+sampleList[Key]+"_hadd.root")
    print nTuple[0]
    file[Key] = TFile(nTuple[0])

if not os.path.exists("templates/"): os.system('mkdir '+"templates/")
outfile = TFile("templates/template_"+version+"_"+TAG+".root",'RECREATE')

for ckey in comb:
    print "#####"*10
    print "#####"*10
    print ckey
    Zmin    =   str(comb[ckey][0])
    Zmax    =   str(comb[ckey][1])
    Hmin    =   str(comb[ckey][2])
    Hmax    =   str(comb[ckey][3])
    ZpTmin  =   str(comb[ckey][4])
    ZpTmax  =   str(comb[ckey][5])
    CvsL    =   str(comb[ckey][6])
    CvsB    =   str(comb[ckey][7])       
    
    tempHistE = 0
    tempHistM = 0
    for Key in sampleList:
        fileList = []
        print "#####"*10
        print Key
        iTree = file[Key].Get("Events")

        c1 = TCanvas('c1','c1', 800, 600)

        Z_Mass = TH1F('Z_Mass_'+ckey+'__'+Key,'Z_Mass_'+ckey+'__'+Key, 100, 0, 300)
        Z_Pt   = TH1F('Z_Pt_'+ckey+'__'+Key,'Z_Pt_'+ckey+'__'+Key, 60, 0, 600)
        E_Pt   = TH1F('E_Pt_'+ckey+'__'+Key,'E_Pt_'+ckey+'__'+Key, 60, 0, 600)
        E_Eta  = TH1F('E_Eta_'+ckey+'__'+Key,'E_Eta_'+ckey+'__'+Key, 40, -4, 4)
        E_Phi  = TH1F('E_Phi_'+ckey+'__'+Key,'E_Phi_'+ckey+'__'+Key, 40, -4, 4)
        M_Pt   = TH1F('M_Pt_'+ckey+'__'+Key,'M_Pt_'+ckey+'__'+Key, 60, 0, 600)
        M_Eta  = TH1F('M_Eta_'+ckey+'__'+Key,'M_Eta_'+ckey+'__'+Key, 40, -4, 4)
        M_Phi  = TH1F('M_Phi_'+ckey+'__'+Key,'M_Phi_'+ckey+'__'+Key, 40, -4, 4)
        jet_Pt  = TH1F('jet_Pt_'+ckey+'__'+Key,'jet_Pt_'+ckey+'__'+Key, 60, 0, 600)
        jet_Eta  = TH1F('jet_Eta_'+ckey+'__'+Key,'jet_Eta_'+ckey+'__'+Key, 40, -4, 4)
        jet_Phi  = TH1F('jet_Phi_'+ckey+'__'+Key,'jet_Phi_'+ckey+'__'+Key, 40, -4, 4)
        jet_CvsL  = TH1F('jet_CvsL_'+ckey+'__'+Key,'jet_CvsL_'+ckey+'__'+Key, 30, 0, 1.5)
        jet_CvsB  = TH1F('jet_CvsB_'+ckey+'__'+Key,'jet_CvsB_'+ckey+'__'+Key, 30, 0, 1.5)   
        HIGGS_CvsL_Mass =  TH1F('HIGGS_CvsL_Mass_'+ckey+'__'+Key,'HIGGS_CvsL_Mass_'+ckey+'__'+Key, 16, comb[ckey][2], comb[ckey][3])   
    
        print str(weight.eff_xsec[sampleList[Key]])
        
        if 'SR_' in TAG:
            cut =  "*(Z_Mass>"+Zmin+")*(Z_Mass<"+Zmax+")"
            cut += "*(HIGGS_CvsL_Mass>"+Hmin+")*(HIGGS_CvsL_Mass<"+Hmax+")"
            if 'bin1' in ckey:
                cut += "*(Z_Pt>"+ZpTmin+")*(Z_Pt<"+ZpTmax+")"
            elif 'bin2' in ckey:
                cut += "*(Z_Pt>"+ZpTmax+")" 
            cut += "*(CvsL_CvsLJet1>"+CvsL+")"
            cut += "*(CvsB_CvsLJet1>"+CvsB+")"
        elif 'CR_' in TAG:
            cut =  "*((50<Z_Mass)*(Z_Mass<"+Zmin+")||(Z_Mass>"+Zmax+"))"
            cut += "*(CvsL_CvsLJet1>"+CvsL+")"
            cut += "*(CvsB_CvsLJet1<"+CvsB+")"
#             cut += "*is_M"
        elif 'CvsB_CvsL_CR1' in TAG:
            cut = "*(CvsL_CvsLJet1<"+CvsL+")"
            cut += "*(CvsB_CvsLJet1>"+CvsB+")"
        elif 'CvsB_CvsL_CR2' in TAG:
            cut = "*(CvsL_CvsLJet1>"+CvsL+")"
            cut += "*(CvsB_CvsLJet1<"+CvsB+")"


    
        print "cut : ", cut
    
        iTree.Project('Z_Mass_'+ckey+'__'+Key, 'Z_Mass',str(weight.eff_xsec[sampleList[Key]])+cut)
        iTree.Project('Z_Pt_'+ckey+'__'+Key, 'Z_Pt',str(weight.eff_xsec[sampleList[Key]])+cut)

        iTree.Project('E_Pt_'+ckey+'__'+Key, 'E_Pt',str(weight.eff_xsec[sampleList[Key]])+cut)
        iTree.Project('E_Eta_'+ckey+'__'+Key, 'E_Eta',str(weight.eff_xsec[sampleList[Key]])+cut)
        iTree.Project('E_Phi_'+ckey+'__'+Key, 'E_Phi',str(weight.eff_xsec[sampleList[Key]])+cut)

        iTree.Project('M_Pt_'+ckey+'__'+Key, 'M_Pt',str(weight.eff_xsec[sampleList[Key]])+cut)
        iTree.Project('M_Eta_'+ckey+'__'+Key, 'M_Eta',str(weight.eff_xsec[sampleList[Key]])+cut)
        iTree.Project('M_Phi_'+ckey+'__'+Key, 'M_Phi',str(weight.eff_xsec[sampleList[Key]])+cut)

        iTree.Project('jet_CvsL_'+ckey+'__'+Key, 'jet_CvsL',str(weight.eff_xsec[sampleList[Key]])+cut)
        iTree.Project('jet_CvsB_'+ckey+'__'+Key, 'jet_CvsB',str(weight.eff_xsec[sampleList[Key]])+cut)
        iTree.Project('jet_Pt_'+ckey+'__'+Key, 'jet_Pt',str(weight.eff_xsec[sampleList[Key]])+cut)
        iTree.Project('jet_Eta_'+ckey+'__'+Key, 'jet_Eta',str(weight.eff_xsec[sampleList[Key]])+cut)
        iTree.Project('jet_Phi_'+ckey+'__'+Key, 'jet_Phi',str(weight.eff_xsec[sampleList[Key]])+cut)
        
        iTree.Project('HIGGS_CvsL_Mass_'+ckey+'__'+Key, 'HIGGS_CvsL_Mass',str(weight.eff_xsec[sampleList[Key]])+cut)
        
        if 'dataDE' in Key:
            tempHistDE           = HIGGS_CvsL_Mass.Clone('HIGGS_CvsL_Mass_'+ckey+'__data_obs')
            tempHistDE_ZZ        = Z_Mass.Clone('Z_Mass_'+ckey+'__data_obs')
            tempHistDE_Z_PT      = Z_Pt.Clone('Z_Pt_'+ckey+'__data_obs')            
            tempHistDE_E_Pt      = E_Pt.Clone('E_Pt_'+ckey+'__data_obs')
            tempHistDE_E_Eta     = E_Eta.Clone('E_Eta_'+ckey+'__data_obs')    
            tempHistDE_M_Pt      = M_Pt.Clone('M_Pt_'+ckey+'__data_obs')
            tempHistDE_M_Eta     = M_Eta.Clone('M_Eta_'+ckey+'__data_obs')    
            tempHistDE_jet_Pt    = jet_Pt.Clone('jet_Pt_'+ckey+'__data_obs')    
            tempHistDE_jet_Phi   = jet_Phi.Clone('jet_Phi_'+ckey+'__data_obs')    
            tempHistDE_jet_Eta   = jet_Eta.Clone('jet_Eta_'+ckey+'__data_obs')    
            tempHistDE_jet_CvsL  = jet_CvsL.Clone('jet_CvsL_'+ckey+'__data_obs')    
            tempHistDE_jet_CvsB  = jet_CvsB.Clone('jet_CvsB_'+ckey+'__data_obs')    
        if 'dataDM' in Key:
            tempHistDM           = HIGGS_CvsL_Mass.Clone('HIGGS_CvsL_Mass_'+ckey+'__data_obs')
            tempHistDM_ZZ        = Z_Mass.Clone('Z_Mass_'+ckey+'__data_obs')
            tempHistDM_Z_PT      = Z_Pt.Clone('Z_Pt_'+ckey+'__data_obs')
            tempHistDM_E_Pt      = E_Pt.Clone('E_Pt_'+ckey+'__data_obs')
            tempHistDM_E_Eta     = E_Eta.Clone('E_Eta_'+ckey+'__data_obs')            
            tempHistDM_M_Pt      = M_Pt.Clone('M_Pt_'+ckey+'__data_obs')
            tempHistDM_M_Eta     = M_Eta.Clone('M_Eta_'+ckey+'__data_obs')            
            tempHistDM_jet_Pt    = jet_Pt.Clone('jet_Pt_'+ckey+'__data_obs')    
            tempHistDM_jet_Phi   = jet_Phi.Clone('jet_Phi_'+ckey+'__data_obs')    
            tempHistDM_jet_Eta   = jet_Eta.Clone('jet_Eta_'+ckey+'__data_obs')    
            tempHistDM_jet_CvsL  = jet_CvsL.Clone('jet_CvsL_'+ckey+'__data_obs')    
            tempHistDM_jet_CvsB  = jet_CvsB.Clone('jet_CvsB_'+ckey+'__data_obs')    

        Z_Mass.Draw()
        Z_Mass.Write()        
        c1.Clear()
        c1.Update()

        Z_Pt.Draw()
        Z_Pt.Write()
        c1.Clear()
        c1.Update()

        E_Pt.Draw()
        E_Pt.Write()
        c1.Clear()
        c1.Update()

        E_Eta.Draw()
        E_Eta.Write()
        c1.Clear()
        c1.Update()

        E_Phi.Draw()
        E_Phi.Write()
        c1.Clear()
        c1.Update()

        M_Pt.Draw()
        M_Pt.Write()
        c1.Clear()
        c1.Update()

        M_Eta.Draw()
        M_Eta.Write()
        c1.Clear()
        c1.Update()
    
        M_Phi.Draw()
        M_Phi.Write()
        c1.Clear()
        c1.Update()

        jet_Pt.Draw()
        jet_Pt.Write()
        c1.Clear()
        c1.Update()

        jet_Phi.Draw()
        jet_Phi.Write()
        c1.Clear()
        c1.Update()

        jet_Eta.Draw()
        jet_Eta.Write()
        c1.Clear()
        c1.Update()

        jet_CvsL.Draw()
        jet_CvsL.Write()
        c1.Clear()
        c1.Update()
    
        jet_CvsB.Draw()
        jet_CvsB.Write()
        c1.Clear()
        c1.Update()
    
        HIGGS_CvsL_Mass.Draw()
        HIGGS_CvsL_Mass.Write()
        c1.Clear()
        c1.Update()
    
    tempHistDE.Add(tempHistDM)
    tempHistDE.Draw()
    tempHistDE.Write()


    tempHistDE_ZZ.Add(tempHistDM_ZZ)
    tempHistDE_ZZ.Draw()
    tempHistDE_ZZ.Write()

    tempHistDE_Z_PT.Add(tempHistDM_Z_PT)
    tempHistDE_Z_PT.Draw()
    tempHistDE_Z_PT.Write()

    tempHistDE_E_Pt.Add(tempHistDM_E_Pt)
    tempHistDE_E_Pt.Draw()
    tempHistDE_E_Pt.Write()

    tempHistDE_E_Eta.Add(tempHistDM_E_Eta)
    tempHistDE_E_Eta.Draw()
    tempHistDE_E_Eta.Write()

    tempHistDE_M_Pt.Add(tempHistDM_M_Pt)
    tempHistDE_M_Pt.Draw()
    tempHistDE_M_Pt.Write()

    tempHistDE_M_Eta.Add(tempHistDM_M_Eta)
    tempHistDE_M_Eta.Draw()
    tempHistDE_M_Eta.Write()

    tempHistDE_jet_Pt.Add(tempHistDM_jet_Pt)
    tempHistDE_jet_Pt.Draw()
    tempHistDE_jet_Pt.Write()    

    tempHistDE_jet_Phi.Add(tempHistDM_jet_Phi)
    tempHistDE_jet_Phi.Draw()
    tempHistDE_jet_Phi.Write()    

    tempHistDE_jet_Eta.Add(tempHistDM_jet_Eta)
    tempHistDE_jet_Eta.Draw()
    tempHistDE_jet_Eta.Write()    

    tempHistDE_jet_CvsL.Add(tempHistDM_jet_CvsL)
    tempHistDE_jet_CvsL.Draw()
    tempHistDE_jet_CvsL.Write()

    tempHistDE_jet_CvsB.Add(tempHistDM_jet_CvsB)
    tempHistDE_jet_CvsB.Draw()
    tempHistDE_jet_CvsB.Write()


    c1.Clear()
    c1.Update()

        