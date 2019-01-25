from ROOT import *
from array import array

import glob, sys, time
import numpy as np
import nuSolutions as nu
import types, math

start_time = time.time()

############### FOR INTERACTIVE RUN ##############
# fileName = "/store/user/lmastrol/VHcc_2016V4bis_Nov18/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/arizzi-RunIIMoriond17-DeepAndR139/181118_101427/0000/tree_1.root"
# channel  = 'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8'
# version = 'vJ'
# oFile = TFile('TestAgain.root','RECREATE')
##################################################

############### FOR NON INTERACTIVE RUN ##############
start_time = time.time()
fileName = str(sys.argv[1])
channel  = str(sys.argv[2])
version = str(sys.argv[3]) 
print "#########"*10
print "start_time : ",time.ctime()
print "processing on : ",fileName

debug = False

iFile = TFile.Open("root://xrootd-cms.infn.it//"+fileName)
inputTree = iFile.Get("Events")
inputTree.SetBranchStatus("*",1)

print fileName
number = fileName.split('/0000/')[1].split('.root')[0].split('_')[1]
print number
temp = fileName.split(channel+'/')[1].split("/0000/")[0]
print temp
label = temp.split('/')[0]+"_"+number
print label

#oFile = TFile('/afs/cern.ch/work/x/xcoubez/private/SFttbar/'+version+'/'+channel+'/tree_'+label+'.root','RECREATE')
oFile = TFile('/afs/cern.ch/work/x/xcoubez/private/SFttbar/'+version+'/'+channel+'/tree_'+label+'.root','RECREATE')
print "output file in : '/afs/cern.ch/work/x/xcoubez/private/SFttbar/",version,"'/",channel,"/tree_",label,".root"
############### FOR INTERACTIVE RUN ##############

oFile.cd()
outputTree = TTree("Events","Events")


run                = array('d',[0])
lumiBlock          = array('d',[0])
event              = array('d',[0])
puWeight           = array('d',[0])
puWeightUp         = array('d',[0])
puWeightDn         = array('d',[0])
LHE_HT             = array('d',[0])
LHEScaleWeight     = std.vector('double')()
nLHEScaleWeight    = std.vector('double')()

E_Mass             = std.vector('double')()
E_Pt               = std.vector('double')()
E_Eta              = std.vector('double')()
E_Phi              = std.vector('double')()
E_Charge           = std.vector('double')()


M_Pt               = std.vector('double')()
M_Eta              = std.vector('double')()
M_Phi              = std.vector('double')()
M_Charge           = std.vector('double')()

HT                 = array('d',[0])
jet_Pt             = std.vector('double')()
jet_Eta            = std.vector('double')()
jet_Phi            = std.vector('double')()
jet_Mass           = std.vector('double')()
jet_Pb             = std.vector('double')()
jet_CvsL           = std.vector('double')()
jet_CvsB           = std.vector('double')()
jet_qgl            = std.vector('double')()

if not 'Single' in channel and not 'Double' in channel:
    jet_hadronFlv      = std.vector('double')()

jet_nJet           = array('d',[0])

met_Pt             = array('d',[0])
met_Phi            = array('d',[0])
met_signif         = array('d',[0])

is_E               = array('d',[0])
is_M               = array('d',[0])

W_Mass             = array('d',[0])
W_Pt               = array('d',[0])
W_Eta              = array('d',[0])
W_Phi              = array('d',[0])

W_Mass_nuSol       = array('d',[0])
W_Pt_nuSol         = array('d',[0])
W_Eta_nuSol        = array('d',[0])
W_Phi_nuSol        = array('d',[0])

nJetsB             = array('d',[0])
nJetsC             = array('d',[0])
nJetsL             = array('d',[0])

JetB_Pt            = std.vector('double')()
JetB_Eta           = std.vector('double')()
JetB_Phi           = std.vector('double')()

JetC_Pt            = std.vector('double')()
JetC_Eta           = std.vector('double')()
JetC_Phi           = std.vector('double')()

JetL_Pt            = std.vector('double')()
JetL_Eta           = std.vector('double')()
JetL_Phi           = std.vector('double')()

Jet0_pt            = array('d',[0])
Jet0_eta           = array('d',[0])
Jet0_phi           = array('d',[0])
Jet0_Pb            = array('d',[0])
Jet0_CvsL          = array('d',[0])
Jet0_CvsB          = array('d',[0])

AddJet1_pt         = array('d',[0])
AddJet1_eta        = array('d',[0])
AddJet1_phi        = array('d',[0])
AddJet1_Pb         = array('d',[0])
AddJet1_CvsL       = array('d',[0])
AddJet1_CvsB       = array('d',[0])

AddJet2_pt         = array('d',[0])
AddJet2_eta        = array('d',[0])
AddJet2_phi        = array('d',[0])
AddJet2_Pb         = array('d',[0])
AddJet2_CvsL       = array('d',[0])
AddJet2_CvsB       = array('d',[0])

AddJet3_pt         = array('d',[0])
AddJet3_eta        = array('d',[0])
AddJet3_phi        = array('d',[0])
AddJet3_Pb         = array('d',[0])
AddJet3_CvsL       = array('d',[0])
AddJet3_CvsB       = array('d',[0])

JER                = std.vector('double')()
JERup              = std.vector('double')()
JERdn              = std.vector('double')()

Dic_JECsys = {}
JES_cfg_file = 'JES_cfg.txt'
for line in open(JES_cfg_file).readlines():
    if not 'nominal' in line:
        JES_source = line[:-1].split('scaleVar=')[1].split(',')[0]
        Dic_JECsys[JES_source] = std.vector('double')()
        outputTree.Branch(JES_source         ,Dic_JECsys[JES_source] )        
        
        Dic_JECsys[JES_source+'_Entry'] = 0


if not 'Single' in channel and not 'Double' in channel:
    Jet0_hadronFlavour     = array('d',[0])
    AddJet1_hadronFlavour  = array('d',[0])
    AddJet2_hadronFlavour  = array('d',[0])
    AddJet3_hadronFlavour  = array('d',[0])

########################## MVA VARIABLES ##########################
W_Tmass            = array('d',[0])
top_Mass           = array('d',[0])
M_Mass             = std.vector('double')()
###################################################################

outputTree.Branch('run'              ,run           ,'run/D'        )
outputTree.Branch('lumiBlock'        ,lumiBlock     ,'lumiBlock/D'  )
outputTree.Branch('event'            ,event         ,'event/D'      )
outputTree.Branch('LHE_HT'           ,LHE_HT        ,'LHE_HT/D'     )
outputTree.Branch('LHEScaleWeight'           ,LHEScaleWeight)
outputTree.Branch('nLHEScaleWeight'          ,nLHEScaleWeight)


outputTree.Branch('puWeight'                ,puWeight           ,'puWeight/D'      )
outputTree.Branch('puWeightUp'              ,puWeightUp         ,'puWeightUp/D'    )
outputTree.Branch('puWeightDown'            ,puWeightDn         ,'puWeightDown/D'  )

outputTree.Branch('E_Mass'           ,E_Mass        )
outputTree.Branch('E_Pt'             ,E_Pt          )
outputTree.Branch('E_Eta'            ,E_Eta         )
outputTree.Branch('E_Phi'            ,E_Phi         )
outputTree.Branch('E_Charge'         ,E_Charge      )

outputTree.Branch('M_Mass'           ,M_Mass        )
outputTree.Branch('M_Pt'             ,M_Pt          )
outputTree.Branch('M_Eta'            ,M_Eta         )
outputTree.Branch('M_Phi'            ,M_Phi         )
outputTree.Branch('M_Charge'         ,M_Charge      )

outputTree.Branch('HT'               ,HT            ,'HT/D'     )

outputTree.Branch('jet_Pt'           ,jet_Pt        )
outputTree.Branch('jet_Eta'          ,jet_Eta       )
outputTree.Branch('jet_Phi'          ,jet_Phi       )
outputTree.Branch('jet_Mass'         ,jet_Mass      )
outputTree.Branch('jet_nJet'         ,jet_nJet      ,'jet_nJet/D')
outputTree.Branch('jet_Pb'           ,jet_Pb        )
outputTree.Branch('jet_CvsL'         ,jet_CvsL      )
outputTree.Branch('jet_CvsB'         ,jet_CvsB      )
outputTree.Branch('jet_qgl'          ,jet_qgl       )


if not 'Single' in channel and not 'Double' in channel:
    outputTree.Branch('jet_hadronFlv'    ,jet_hadronFlv )

outputTree.Branch('met_Pt'           ,met_Pt          ,'met_Pt/D'     )
outputTree.Branch('met_signif'       ,met_signif      ,'met_signif/D' )

outputTree.Branch('W_Mass'           ,W_Mass          ,'W_Mass/D'     )
outputTree.Branch('W_Pt'             ,W_Pt            ,'W_Pt/D'       )
outputTree.Branch('W_Eta'            ,W_Eta           ,'W_Eta/D'      )
outputTree.Branch('W_Phi'            ,W_Phi           ,'W_Phi/D'      )

outputTree.Branch('W_Mass_nuSol'     ,W_Mass_nuSol    ,'W_Mass_nuSol/D'   )
outputTree.Branch('W_Pt_nuSol'       ,W_Pt_nuSol      ,'W_Pt_nuSol/D'     )
outputTree.Branch('W_Eta_nuSol'      ,W_Eta_nuSol     ,'W_Eta_nuSol/D'    )
outputTree.Branch('W_Phi_nuSol'      ,W_Phi_nuSol     ,'W_Phi_nuSol/D'    )

outputTree.Branch('is_E'     ,is_E    ,'is_E/D'     )
outputTree.Branch('is_M'     ,is_M    ,'is_M/D'     )

outputTree.Branch('nJetsB'       ,nJetsB      ,'nJetsB/D'     )
outputTree.Branch('nJetsC'       ,nJetsC      ,'nJetsC/D'     )
outputTree.Branch('nJetsL'       ,nJetsL      ,'nJetsL/D'     )

outputTree.Branch('JetB_Pt'      ,JetB_Pt     )
outputTree.Branch('JetB_Eta'     ,JetB_Eta    )
outputTree.Branch('JetB_Phi'     ,JetB_Phi    )

outputTree.Branch('JetC_Pt'      ,JetC_Pt     )
outputTree.Branch('JetC_Eta'     ,JetC_Eta    )
outputTree.Branch('JetC_Phi'     ,JetC_Phi    )

outputTree.Branch('JetL_Pt'      ,JetL_Pt     )
outputTree.Branch('JetL_Eta'     ,JetL_Eta    )
outputTree.Branch('JetL_Phi'     ,JetL_Phi    )

outputTree.Branch('Jet0_pt'         ,Jet0_pt         ,'Jet0_pt/D'        )
outputTree.Branch('Jet0_eta'        ,Jet0_eta        ,'Jet0_eta/D'       )
outputTree.Branch('Jet0_phi'        ,Jet0_phi        ,'Jet0_phi/D'       )
outputTree.Branch('Jet0_Pb'         ,Jet0_Pb         ,'Jet0_Pb/D'        )
outputTree.Branch('Jet0_CvsL'       ,Jet0_CvsL       ,'Jet0_CvsL/D'      )
outputTree.Branch('Jet0_CvsB'       ,Jet0_CvsB       ,'Jet0_CvsB/D'      )

outputTree.Branch('AddJet1_pt'      ,AddJet1_pt      ,'AddJet1_pt/D'     )
outputTree.Branch('AddJet1_eta'     ,AddJet1_eta     ,'AddJet1_eta/D'    )
outputTree.Branch('AddJet1_phi'     ,AddJet1_phi     ,'AddJet1_phi/D'    )
outputTree.Branch('AddJet1_Pb'      ,AddJet1_Pb      ,'AddJet1_Pb/D'     )
outputTree.Branch('AddJet1_CvsL'    ,AddJet1_CvsL    ,'AddJet1_CvsL/D'   )
outputTree.Branch('AddJet1_CvsB'    ,AddJet1_CvsB    ,'AddJet1_CvsB/D'   )

outputTree.Branch('AddJet2_pt'      ,AddJet2_pt      ,'AddJet2_pt/D'     )
outputTree.Branch('AddJet2_eta'     ,AddJet2_eta     ,'AddJet2_eta/D'    )
outputTree.Branch('AddJet2_phi'     ,AddJet2_phi     ,'AddJet2_phi/D'    )
outputTree.Branch('AddJet2_Pb'      ,AddJet2_Pb      ,'AddJet2_Pb/D'     )
outputTree.Branch('AddJet2_CvsL'    ,AddJet2_CvsL    ,'AddJet2_CvsL/D'   )
outputTree.Branch('AddJet2_CvsB'    ,AddJet2_CvsB    ,'AddJet2_CvsB/D'   )

outputTree.Branch('AddJet3_pt'      ,AddJet3_pt      ,'AddJet3_pt/D'     )
outputTree.Branch('AddJet3_eta'     ,AddJet3_eta     ,'AddJet3_eta/D'    )
outputTree.Branch('AddJet3_phi'     ,AddJet3_phi     ,'AddJet3_phi/D'    )
outputTree.Branch('AddJet3_Pb'      ,AddJet3_Pb      ,'AddJet3_Pb/D'     )
outputTree.Branch('AddJet3_CvsL'    ,AddJet3_CvsL    ,'AddJet3_CvsL/D'   )
outputTree.Branch('AddJet3_CvsB'    ,AddJet3_CvsB    ,'AddJet3_CvsB/D'   )

outputTree.Branch('JERup'           ,JERup )
outputTree.Branch('JERdn'           ,JERdn )


if not 'Single' in channel and not 'Double' in channel:
    outputTree.Branch('Jet0_hadronFlavour' ,      Jet0_hadronFlavour ,      'Jet0_hadronFlavour/D'     )
    outputTree.Branch('AddJet1_hadronFlavour' ,   AddJet1_hadronFlavour ,   'AddJet1_hadronFlavour/D'  )
    outputTree.Branch('AddJet2_hadronFlavour' ,   AddJet2_hadronFlavour ,   'AddJet2_hadronFlavour/D'  )
    outputTree.Branch('AddJet3_hadronFlavour' ,   AddJet3_hadronFlavour ,   'AddJet3_hadronFlavour/D'  )

########################## MVA VARIABLES ##########################
outputTree.Branch('W_Tmass'                     ,W_Tmass          ,'W_Tmass/D'          )
outputTree.Branch('top_Mass'                    ,top_Mass         ,'top_Mass/D'     )
###################################################################

count = 0
for entry in inputTree:
    if count > 2000 : break
    if count%100 ==0:
        print "Number of events processed : ", count
    #if count>1000: break
    count+=1
    TriggerPass = False
    elec                = []
    muon                = []

    el_List             = []
    mu_List             = []
    jetList             = []
    jet_FL_List         = []
    jet_Pt_List         = []
    jet_Pb_List         = []
    jet_CvsL_List       = []
    jet_CvsB_List       = []
    jet_CvsB_CvsL_List  = []
    jet_CvsB_CvsL_List2 = []

    e_Pt_List                = []
    e_Eta_List               = []
    e_Phi_List               = []
    e_Charge_List            = []
    e_Mass_List              = []

    m_Pt_List                = []
    m_Eta_List               = []
    m_Phi_List               = []
    m_Charge_List            = []
    m_Mass_List              = []

    j_Pt_List                = []
    j_Eta_List               = []
    j_Phi_List               = []
    j_Mass_List              = []
    j_Pb_List                = []
    j_CvsL_List              = []
    j_CvsB_List              = []
    j_qgl_List               = []
    if not 'Single' in channel and not 'Double' in channel:
        j_hadronFlv_List         = []

    isElec              = True
    isMuon              = True
 
    is_E[0]             = False
    is_M[0]             = False

    run[0]              = -1000
    lumiBlock[0]        = -1000
    event[0]            = -1000

    LHE_HT[0]           = -1000
    HT[0]               = -1000

    W_Mass[0]           = -1000
    W_Pt[0]             = -1000
    W_Eta[0]            = -1000
    W_Phi[0]            = -1000

    W_Mass_nuSol[0]     = -1000
    W_Pt_nuSol[0]       = -1000
    W_Eta_nuSol[0]      = -1000
    W_Phi_nuSol[0]      = -1000

    LHEScaleWeight.clear()
    nLHEScaleWeight.clear()

    puWeight[0]           =1
    puWeightUp[0]         =1
    puWeightDn[0]         =1

    JetB_Pt.clear()
    JetB_Eta.clear()
    JetB_Phi.clear()
    
    JetC_Pt.clear()
    JetC_Eta.clear()
    JetC_Phi.clear()

    JetL_Pt.clear()
    JetL_Eta.clear()
    JetL_Phi.clear()

    jet_nJet[0]            = -1
    nJetsB[0]              = -1
    nJetsC[0]              = -1
    nJetsL[0]              = -1
    
    Jet0_pt[0]           = -10
    Jet0_eta[0]          = -10
    Jet0_phi[0]          = -10
    Jet0_Pb[0]           = -10
    Jet0_CvsL[0]         = -10
    Jet0_CvsB[0]         = -10

    AddJet1_pt[0]        = -10
    AddJet1_eta[0]       = -10
    AddJet1_phi[0]       = -10
    AddJet1_Pb[0]        = -10
    AddJet1_CvsL[0]      = -10
    AddJet1_CvsB[0]      = -10

    AddJet2_pt[0]        = -10
    AddJet2_eta[0]       = -10
    AddJet2_phi[0]       = -10
    AddJet2_Pb[0]        = -10
    AddJet2_CvsL[0]      = -10
    AddJet2_CvsB[0]      = -10

    AddJet3_pt[0]        = -10
    AddJet3_eta[0]       = -10
    AddJet3_phi[0]       = -10
    AddJet3_Pb[0]        = -10
    AddJet3_CvsL[0]      = -10
    AddJet3_CvsB[0]      = -10
    
    JERup.clear()
    JERdn.clear()

    W_Tmass[0]           = -1000.0
    top_Mass[0]          = -1000.0
    
    if not 'Single' in channel and not 'Double' in channel:
        Jet0_hadronFlavour[0]    = -10
        AddJet1_hadronFlavour[0] = -10
        AddJet2_hadronFlavour[0] = -10
        AddJet3_hadronFlavour[0] = -10

    E_Mass.clear()
    E_Pt.clear()
    E_Eta.clear()
    E_Phi.clear()
    E_Charge.clear()

    M_Mass.clear()
    M_Pt.clear()
    M_Eta.clear()
    M_Phi.clear()
    M_Charge.clear()

    jet_Pt.clear()
    jet_Eta.clear()
    jet_Phi.clear()
    jet_Mass.clear()
    jet_Pb.clear()
    jet_CvsL.clear()
    jet_CvsB.clear()
    jet_qgl.clear()

    if not 'Single' in channel and not 'Double' in channel:
        jet_hadronFlv.clear()
        for JECkey in Dic_JECsys.keys():
            if 'Entry' in JECkey: continue
            Dic_JECsys[JECkey].clear()

    met_Pt[0]             = -1
    #met_Phi[0]            = -1000
    met_signif[0]         = -1000

    if debug == True:
        print "Preselection 1 : Single Lepton"
        print "                 electron selection : pt > 30 and eta<2.5"
        print "                 electron selection : Electron_mvaSpring16GP_WP80 > 0"
        print "                 electron selection : Electron_pfRelIso03_all <= 0.06"
        print "                 muon selection : pt > 20 and eta<2.4"
        print "                 muon selection : Muon_tightId > 0"
        print "                 muon selection : Muon_pfRelIso04_all <= 0.06"

    for i in range(0, len(entry.Electron_pt)):
        if entry.Electron_pt[i]<30 or abs(entry.Electron_eta[i])>2.5: continue
        if entry.Electron_mvaSpring16GP_WP80[i]<=0: continue
        if entry.Electron_pfRelIso03_all[i]>0.06: continue
        e_Pt_List.append(entry.Electron_pt[i])
        e_Eta_List.append(entry.Electron_eta[i])
        e_Phi_List.append(entry.Electron_phi[i])
        e_Charge_List.append(entry.Electron_charge[i])
        e_Mass_List.append(entry.Electron_mass[i])

    for i in range(0, len(entry.Muon_pt)):
        if entry.Muon_pt[i]<30 or abs(entry.Muon_eta[i])>2.4: continue
        if entry.Muon_tightId[i]<=0: continue
        if entry.Muon_pfRelIso04_all[i]>0.06: continue        
        m_Pt_List.append(entry.Muon_pt[i])
        m_Eta_List.append(entry.Muon_eta[i])
        m_Phi_List.append(entry.Muon_phi[i])
        m_Charge_List.append(entry.Muon_charge[i])
        m_Mass_List.append(entry.Muon_mass[i])
    
    if len(e_Pt_List) + len(m_Pt_List) != 1: continue
        
    if len(e_Pt_List) == 1:
        isMuon = False
        el_List = sorted(zip(e_Pt_List,e_Charge_List), key = lambda pair : pair[0], reverse=True)[0:2]
        
    if len(m_Pt_List) == 1:
        isElec = False
        mu_List = sorted(zip(m_Pt_List,m_Charge_List), key = lambda pair : pair[0], reverse=True)[0:2]


    if debug == True:
        print "                 Jet selection : jet_pt > 25 and jet_eta < 2.5"    
        print "                 Jet selection : Jet_lepFilter == True"    
        print "                 Jet selection : Jet_puId >= 0"    
    HT_temp = 0
    totalJetEnergy = 0
    totalJetCvsL = 0
    totalJetCvsLpt = 0

    for i in range(0, len(entry.Jet_pt)):
        if entry.Jet_pt[i]<25 or abs(entry.Jet_eta[i])>2.5: continue
        if entry.Jet_lepFilter[i] == False: continue
        if entry.Jet_puId[i] < 0: continue
        if entry.Jet_CvsL[i] < 0 or entry.Jet_CvsB[i] < 0: continue

        jet =  TLorentzVector()
        jet.SetPtEtaPhiM(entry.Jet_pt[i],entry.Jet_eta[i],entry.Jet_phi[i],entry.Jet_mass[i])
        jetList.append(jet)

        jet_Pt_List.append(entry.Jet_pt[i])
        jet_Pb_List.append(entry.Jet_btagDeepB[i])
        jet_CvsL_List.append(entry.Jet_CvsL[i])
        jet_CvsB_List.append(entry.Jet_CvsB[i])

        if not 'Single' in channel and not 'Double' in channel:
            jet_FL_List.append(entry.Jet_hadronFlavour[i])

        HT_temp         += entry.Jet_pt[i]
        totalJetEnergy  += jet.E()

        j_Pt_List.append(entry.Jet_pt[i])
        j_Eta_List.append(entry.Jet_eta[i])
        j_Phi_List.append(entry.Jet_phi[i])
        j_Mass_List.append(entry.Jet_mass[i])
        j_Pb_List.append(entry.Jet_btagDeepB[i])
        j_CvsL_List.append(entry.Jet_CvsL[i])
        j_CvsB_List.append(entry.Jet_CvsB[i])
        j_qgl_List.append(entry.Jet_qgl[i])
        if not 'Single' in channel and not 'Double' in channel:
            j_hadronFlv_List.append(entry.Jet_hadronFlavour[i])

    HT[0]                  = HT_temp

    met_Pt[0]              = entry.MET_Pt
    #met_Phi[0]             = entry.MET_Phi
    met_signif[0]          = entry.MET_significance
    
    mW = 80.38
    mH = 125 + mW    
    MET = TLorentzVector()
    MET.SetPtEtaPhiM(entry.MET_Pt, 0., entry.MET_Phi, 0.)
    sigma2 = np.array([((MET.Px()*.1)**2,0),(0,(MET.Py()*.1)**2)])    
    
    if debug == True:
        print "Preselection 2 : at least two jets with jet_pt > 20 and jet_eta < 2.4"    

    if len(jetList)<4: continue

    #print "More than 4 jets, entering filling of stuff"

    if not 'Single' in channel and not 'Double' in channel:
        for i in range(0,len(j_hadronFlv_List)):
            if j_hadronFlv_List[i] == 5:
                JetB_Pt.push_back(j_Pt_List[i])
                JetB_Eta.push_back(j_Eta_List[i])
                JetB_Phi.push_back(j_Phi_List[i])
            elif j_hadronFlv_List[i] == 4:
                JetC_Pt.push_back(j_Pt_List[i])
                JetC_Eta.push_back(j_Eta_List[i])
                JetC_Phi.push_back(j_Phi_List[i])
            elif j_hadronFlv_List[i] == 0:
                JetL_Pt.push_back(j_Pt_List[i])
                JetL_Eta.push_back(j_Eta_List[i])
                JetL_Phi.push_back(j_Phi_List[i])

    VBoson = 0
    if not isElec and len(m_Pt_List)==1:
        for i in range(0, len(m_Pt_List)):
            mu =  TLorentzVector()
            mu.SetPtEtaPhiM(m_Pt_List[i],m_Eta_List[i],m_Phi_List[i],m_Mass_List[i])
            muon.append(mu)
        VBoson      = (muon[0]+MET)
        W_Mass[0]   = (muon[0]+MET).M()
        W_Tmass[0]  = (muon[0]+MET).Mt()
        W_Pt[0]     = (muon[0]+MET).Pt()                    
        W_Eta[0]    = (muon[0]+MET).Eta()                    
        W_Phi[0]    = (muon[0]+MET).Phi()                    

    if not isMuon and len(e_Pt_List)==1:
        for i in range(0, len(e_Pt_List)):
            el =  TLorentzVector()
            el.SetPtEtaPhiM(e_Pt_List[i],e_Eta_List[i],e_Phi_List[i],e_Mass_List[i])
            elec.append(el)
        VBoson      = (elec[0]+MET)
        W_Mass[0]   = (elec[0]+MET).M()
        W_Tmass[0]  = (elec[0]+MET).Mt()
        W_Pt[0]     = (elec[0]+MET).Pt()
        W_Eta[0]    = (elec[0]+MET).Eta()                    
        W_Phi[0]    = (elec[0]+MET).Phi()                               


    if isElec:
        is_E[0] = isElec
        for i, ePt in enumerate(e_Pt_List):
            E_Mass.push_back(e_Mass_List[i])
            E_Pt.push_back(ePt)
            E_Eta.push_back(e_Eta_List[i])
            E_Phi.push_back(e_Phi_List[i])
            E_Charge.push_back(e_Charge_List[i])
    if isMuon:
        is_M[0] = isMuon
        for i, mPt in enumerate(m_Pt_List):
            M_Mass.push_back(m_Mass_List[i])
            M_Pt.push_back(mPt)
            M_Eta.push_back(m_Eta_List[i])
            M_Phi.push_back(m_Phi_List[i])
            M_Charge.push_back(m_Charge_List[i])

    if debug == True:
        print "Preselection 4 : TRIGGERS" 
        print "HLT_IsoMu24"
        print "HLT_IsoTkMu24"         
        print "HLT_Ele27_WPTight_Gsf"
    if ( entry.HLT_IsoMu24 == 0 ) and ( entry.HLT_IsoTkMu24 == 0 ) and (entry.HLT_Ele27_WPTight_Gsf == 0 )  : continue
    TriggerPass = True    

    if not 'Single' in channel and not 'Double' in channel:
        hJets_CvsB       = sorted(zip( jetList, jet_Pb_List, jet_CvsB_List, jet_CvsL_List, jet_FL_List ), key = lambda pair : pair[2], reverse=False)[0:4]

        nJetsB[0] = jet_FL_List.count(5)
        nJetsC[0] = jet_FL_List.count(4)
        nJetsL[0] = jet_FL_List.count(0)

######################### FLAGS for splitting W + jets #######################
#    if 'WJetsToLNu' in channel:
#        if jet_FL_List.count(4) >= 2:
#            Flag_W_jet[0] = 1
#        elif jet_FL_List.count(4) == 1 and jet_FL_List.count(5) == 1:
#            Flag_W_jet[0] = 2
#        elif jet_FL_List.count(4) == 1 and jet_FL_List.count(0) == 1:
#            Flag_W_jet[0] = 3
#        elif jet_FL_List.count(5) >= 2:
#            Flag_W_jet[0] = 4
#        elif jet_FL_List.count(5) == 1 and jet_FL_List.count(0) == 1:
#            Flag_W_jet[0] = 5
#        else:
#            Flag_W_jet[0] = 6            

###########################################################################
    if 'Single' in channel or 'Double' in channel:
        hJets_CvsB       = sorted(zip( jetList, jet_Pb_List, jet_CvsB_List, jet_CvsL_List              ), key = lambda pair : pair[2], reverse=False)[0:4]
    # was reverse = True
    
    sum_hJets_CvsB       = hJets_CvsB[0][0]       +   hJets_CvsB[1][0]
        
    top_Mass[0] = (VBoson+hJets_CvsB[-1][0]).M()

    #print "N jets = ", len(jetList)
    #print "N jets = ", len(hJets_CvsB)

    #print "Jet 1 - Pt: ", hJets_CvsB[0][0].Pt(), "  Eta: ", hJets_CvsB[0][0].Eta(), "  Phi: ", hJets_CvsB[0][0].Phi(), "  CvsL: ", hJets_CvsB[0][1], "  CvsB: ", hJets_CvsB[0][2]
    Jet0_pt[0]           = hJets_CvsB[0][0].Pt()
    Jet0_eta[0]          = hJets_CvsB[0][0].Eta()
    Jet0_phi[0]          = hJets_CvsB[0][0].Phi()
    Jet0_Pb[0]           = hJets_CvsB[0][1]
    Jet0_CvsL[0]         = hJets_CvsB[0][2]
    Jet0_CvsB[0]         = hJets_CvsB[0][3]

    #print "Jet 2 - Pt: ", hJets_CvsB[1][0].Pt(), "  Eta: ", hJets_CvsB[1][0].Eta(), "  Phi: ", hJets_CvsB[1][0].Phi(), "  CvsL: ", hJets_CvsB[1][1], "  CvsB: ", hJets_CvsB[1][2]
    AddJet1_pt[0]        = hJets_CvsB[1][0].Pt()
    AddJet1_eta[0]       = hJets_CvsB[1][0].Eta()
    AddJet1_phi[0]       = hJets_CvsB[1][0].Phi()
    AddJet1_Pb[0]        = hJets_CvsB[1][1]
    AddJet1_CvsL[0]      = hJets_CvsB[1][2]
    AddJet1_CvsB[0]      = hJets_CvsB[1][3]

    #print "Jet 3 - Pt: ", hJets_CvsB[2][0].Pt(), "  Eta: ", hJets_CvsB[2][0].Eta(), "  Phi: ", hJets_CvsB[2][0].Phi(), "  CvsL: ", hJets_CvsB[2][1], "  CvsB: ", hJets_CvsB[2][2]
    AddJet2_pt[0]        = hJets_CvsB[2][0].Pt()
    AddJet2_eta[0]       = hJets_CvsB[2][0].Eta()
    AddJet2_phi[0]       = hJets_CvsB[2][0].Phi()
    AddJet2_Pb[0]        = hJets_CvsB[2][1]
    AddJet2_CvsL[0]      = hJets_CvsB[2][2]
    AddJet2_CvsB[0]      = hJets_CvsB[2][3]

    #print "Jet 4 - Pt: ", hJets_CvsB[3][0].Pt(), "  Eta: ", hJets_CvsB[3][0].Eta(), "  Phi: ", hJets_CvsB[3][0].Phi(), "  CvsL: ", hJets_CvsB[3][1], "  CvsB: ", hJets_CvsB[3][2]
    AddJet3_pt[0]        = hJets_CvsB[3][0].Pt()
    AddJet3_eta[0]       = hJets_CvsB[3][0].Eta()
    AddJet3_phi[0]       = hJets_CvsB[3][0].Phi()
    AddJet3_Pb[0]        = hJets_CvsB[3][1]
    AddJet3_CvsL[0]      = hJets_CvsB[3][2]
    AddJet3_CvsB[0]      = hJets_CvsB[3][3]

    if not 'Single' in channel and not 'Double' in channel:
        #print "Jet 1 - hadronFLavour: ", hJets_CvsB[0][3], "  CvsL: ", hJets_CvsB[0][1], "  CvsB: ", hJets_CvsB[0][2]
        #print "Jet 2 - hadronFLavour: ", hJets_CvsB[1][3], "  CvsL: ", hJets_CvsB[1][1], "  CvsB: ", hJets_CvsB[1][2]
        #print "Jet 3 - hadronFLavour: ", hJets_CvsB[2][3], "  CvsL: ", hJets_CvsB[2][1], "  CvsB: ", hJets_CvsB[2][2]
        #print "Jet 4 - hadronFLavour: ", hJets_CvsB[3][3], "  CvsL: ", hJets_CvsB[3][1], "  CvsB: ", hJets_CvsB[3][2]
        Jet0_hadronFlavour[0]    = hJets_CvsB[0][4]
        AddJet1_hadronFlavour[0] = hJets_CvsB[1][4]
        AddJet2_hadronFlavour[0] = hJets_CvsB[2][4]
        AddJet3_hadronFlavour[0] = hJets_CvsB[3][4]
        
        puWeight[0]   = entry.puWeight
        puWeightUp[0] = entry.puWeightUp
        puWeightDn[0] = entry.puWeightDown

        Dic_JECsys['Jet_pt_jesAbsoluteStatUp_Entry']       = entry.Jet_pt_jesAbsoluteStatUp
        Dic_JECsys['Jet_pt_jesAbsoluteStatDown_Entry']     = entry.Jet_pt_jesAbsoluteStatDown
        Dic_JECsys['Jet_pt_jesAbsoluteScaleUp_Entry']      = entry.Jet_pt_jesAbsoluteScaleUp
        Dic_JECsys['Jet_pt_jesAbsoluteScaleDown_Entry']    = entry.Jet_pt_jesAbsoluteScaleDown
        Dic_JECsys['Jet_pt_jesAbsoluteMPFBiasUp_Entry']    = entry.Jet_pt_jesAbsoluteMPFBiasUp
        Dic_JECsys['Jet_pt_jesAbsoluteMPFBiasDown_Entry']  = entry.Jet_pt_jesAbsoluteMPFBiasDown
        Dic_JECsys['Jet_pt_jesFragmentationUp_Entry']      = entry.Jet_pt_jesFragmentationUp
        Dic_JECsys['Jet_pt_jesFragmentationDown_Entry']    = entry.Jet_pt_jesFragmentationDown
        Dic_JECsys['Jet_pt_jesSinglePionECALUp_Entry']     = entry.Jet_pt_jesSinglePionECALUp
        Dic_JECsys['Jet_pt_jesSinglePionECALDown_Entry']   = entry.Jet_pt_jesSinglePionECALDown
        Dic_JECsys['Jet_pt_jesSinglePionHCALUp_Entry']     = entry.Jet_pt_jesSinglePionHCALUp
        Dic_JECsys['Jet_pt_jesSinglePionHCALDown_Entry']   = entry.Jet_pt_jesSinglePionHCALDown
        Dic_JECsys['Jet_pt_jesFlavorQCDUp_Entry']          = entry.Jet_pt_jesFlavorQCDUp
        Dic_JECsys['Jet_pt_jesFlavorQCDDown_Entry']        = entry.Jet_pt_jesFlavorQCDDown
        Dic_JECsys['Jet_pt_jesRelativeJEREC1Up_Entry']     = entry.Jet_pt_jesRelativeJEREC1Up
        Dic_JECsys['Jet_pt_jesRelativeJEREC1Down_Entry']   = entry.Jet_pt_jesRelativeJEREC1Down
        Dic_JECsys['Jet_pt_jesRelativeJEREC2Up_Entry']     = entry.Jet_pt_jesRelativeJEREC2Up
        Dic_JECsys['Jet_pt_jesRelativeJEREC2Down_Entry']   = entry.Jet_pt_jesRelativeJEREC2Down
        Dic_JECsys['Jet_pt_jesRelativeJERHFUp_Entry']      = entry.Jet_pt_jesRelativeJERHFUp
        Dic_JECsys['Jet_pt_jesRelativeJERHFDown_Entry']    = entry.Jet_pt_jesRelativeJERHFDown
        Dic_JECsys['Jet_pt_jesRelativePtBBUp_Entry']       = entry.Jet_pt_jesRelativePtBBUp
        Dic_JECsys['Jet_pt_jesRelativePtBBDown_Entry']     = entry.Jet_pt_jesRelativePtBBDown
        Dic_JECsys['Jet_pt_jesRelativePtEC1Up_Entry']      = entry.Jet_pt_jesRelativePtEC1Up
        Dic_JECsys['Jet_pt_jesRelativePtEC1Down_Entry']    = entry.Jet_pt_jesRelativePtEC1Down
        Dic_JECsys['Jet_pt_jesRelativePtEC2Up_Entry']      = entry.Jet_pt_jesRelativePtEC2Up
        Dic_JECsys['Jet_pt_jesRelativePtEC2Down_Entry']    = entry.Jet_pt_jesRelativePtEC2Down
        Dic_JECsys['Jet_pt_jesRelativePtHFUp_Entry']       = entry.Jet_pt_jesRelativePtHFUp
        Dic_JECsys['Jet_pt_jesRelativePtHFDown_Entry']     = entry.Jet_pt_jesRelativePtHFDown
        Dic_JECsys['Jet_pt_jesRelativeFSRUp_Entry']        = entry.Jet_pt_jesRelativeFSRUp
        Dic_JECsys['Jet_pt_jesRelativeFSRDown_Entry']      = entry.Jet_pt_jesRelativeFSRDown
        Dic_JECsys['Jet_pt_jesRelativeStatFSRUp_Entry']    = entry.Jet_pt_jesRelativeStatFSRUp
        Dic_JECsys['Jet_pt_jesRelativeStatFSRDown_Entry']  = entry.Jet_pt_jesRelativeStatFSRDown
        Dic_JECsys['Jet_pt_jesRelativeStatECUp_Entry']     = entry.Jet_pt_jesRelativeStatECUp
        Dic_JECsys['Jet_pt_jesRelativeStatECDown_Entry']   = entry.Jet_pt_jesRelativeStatECDown
        Dic_JECsys['Jet_pt_jesRelativeStatHFUp_Entry']     = entry.Jet_pt_jesRelativeStatHFUp
        Dic_JECsys['Jet_pt_jesRelativeStatHFDown_Entry']   = entry.Jet_pt_jesRelativeStatHFDown
        Dic_JECsys['Jet_pt_jesPileUpDataMCUp_Entry']       = entry.Jet_pt_jesPileUpDataMCUp
        Dic_JECsys['Jet_pt_jesPileUpDataMCDown_Entry']     = entry.Jet_pt_jesPileUpDataMCDown
        Dic_JECsys['Jet_pt_jesPileUpPtRefUp_Entry']        = entry.Jet_pt_jesPileUpPtRefUp
        Dic_JECsys['Jet_pt_jesPileUpPtRefDown_Entry']      = entry.Jet_pt_jesPileUpPtRefDown
        Dic_JECsys['Jet_pt_jesPileUpPtBBUp_Entry']         = entry.Jet_pt_jesPileUpPtBBUp
        Dic_JECsys['Jet_pt_jesPileUpPtBBDown_Entry']       = entry.Jet_pt_jesPileUpPtBBDown
        Dic_JECsys['Jet_pt_jesPileUpPtEC1Up_Entry']        = entry.Jet_pt_jesPileUpPtEC1Up
        Dic_JECsys['Jet_pt_jesPileUpPtEC1Down_Entry']      = entry.Jet_pt_jesPileUpPtEC1Down
        Dic_JECsys['Jet_pt_jesPileUpPtEC2Up_Entry']        = entry.Jet_pt_jesPileUpPtEC2Up
        Dic_JECsys['Jet_pt_jesPileUpPtEC2Down_Entry']      = entry.Jet_pt_jesPileUpPtEC2Down
        Dic_JECsys['Jet_pt_jesPileUpPtHFUp_Entry']         = entry.Jet_pt_jesPileUpPtHFUp
        Dic_JECsys['Jet_pt_jesPileUpPtHFDown_Entry']       = entry.Jet_pt_jesPileUpPtHFDown
        Dic_JECsys['Jet_pt_jesRelativeBalUp_Entry']        = entry.Jet_pt_jesRelativeBalUp
        Dic_JECsys['Jet_pt_jesRelativeBalDown_Entry']      = entry.Jet_pt_jesRelativeBalDown
        Dic_JECsys['Jet_pt_jesTimePtEtaUp_Entry']          = entry.Jet_pt_jesTimePtEtaUp
        Dic_JECsys['Jet_pt_jesTimePtEtaDown_Entry']        = entry.Jet_pt_jesTimePtEtaDown


        for i in range(0, len(entry.Jet_pt_jerUp)):
            JERup.push_back(entry.Jet_pt_jerUp[i])
            JERdn.push_back(entry.Jet_pt_jerDown[i])            
            for JECkey in Dic_JECsys.keys():
                if 'Entry' in JECkey: continue
                print JECkey
                Dic_JECsys[JECkey].push_back(Dic_JECsys[JECkey+'_Entry'][i])
            
        for i in range(0, len(entry.LHEScaleWeight)):
            LHEScaleWeight.push_back(entry.LHEScaleWeight[i])


    outputTree.Fill()

outputTree.Write()

nEventTree = iFile.Get("Runs")
nEventCount = 0
if not 'Single' in channel and not 'Double' in channel:
    for entry in nEventTree:
        nEventCount += entry.genEventCount
    print "Total event processed by Nano AOD post processor : ", nEventCount
print "Total events processed : ",count    
print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))
    
