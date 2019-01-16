from ROOT import *
from array import array

import Wlvhcc_cfg as configurations
import glob, sys, time
import numpy as np
import nuSolutions as nu
import types, math

start_time = time.time()
############### FOR INTERACTIVE RUN ##############
# fileName = "/store/user/lmastrol/VHcc_2016V4_Aug18/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/arizzi-RunIIMoriond17-DeepAndR105/180909_010329/0000/tree_1.root"
# fileName = "/store/user/lmastrol/VHcc_2016V4_Aug18/SingleElectron/arizzi-NanoDeepAndReg2016Run2094/180817_113615/0000/tree_122.root"
# channel  = 'SingleElectron'
# version = 'v2'
##################################################

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

number = fileName.split('/0000/')[1].split('.root')[0].split('_')[1]
temp = fileName.split(channel+'/')[1].split("/0000/")[0]
label = temp.split('/')[0]+"_"+number

oFile = TFile(configurations.outputPath+'WlvHcc/'+version+'/'+channel+'/tree_'+label+'.root','RECREATE')

oFile.cd()
outputTree = TTree("Events","Events")

run              = array('d',[0])
lumiBlock        = array('d',[0])
event            = array('d',[0])
LHE_HT           = array('d',[0])

E_Mass           = std.vector('double')()
E_Pt             = std.vector('double')()
E_Eta            = std.vector('double')()
E_Phi            = std.vector('double')()
E_Charge         = std.vector('double')()

M_Pt             = std.vector('double')()
M_Eta            = std.vector('double')()
M_Phi            = std.vector('double')()
M_Charge         = std.vector('double')()

HT               = array('d',[0])
jet_Pt             = std.vector('double')()
jet_Eta            = std.vector('double')()
jet_Phi            = std.vector('double')()
jet_Mass           = std.vector('double')()
jet_CvsL           = std.vector('double')()
jet_CvsB           = std.vector('double')()
jet_qgl            = std.vector('double')()

if not 'Single' in channel and not 'Double' in channel:
    jet_hadronFlv      = std.vector('double')()
jet_nJet           = array('d',[0])
met_Pt             = array('d',[0])
met_signif         = array('d',[0])
is_E               = array('d',[0])
is_M               = array('d',[0])
# is_H_mass_CR       = array('d',[0])
# is_W_mass_CR       = array('d',[0])

W_Mass           = array('d',[0])
W_Pt             = array('d',[0])
W_Eta            = array('d',[0])
W_Phi            = array('d',[0])

W_Mass_nuSol     = array('d',[0])
W_Pt_nuSol       = array('d',[0])
W_Eta_nuSol      = array('d',[0])
W_Phi_nuSol      = array('d',[0])

numOf_cJet       = array('d',[0])
numOf_bJet       = array('d',[0])
numOf_lJet       = array('d',[0])
pt_Of_cJet       = std.vector('double')()
pt_Of_bJet       = std.vector('double')()
pt_Of_lJet       = std.vector('double')()
eta_Of_cJet       = std.vector('double')()
eta_Of_lJet       = std.vector('double')()
phi_Of_cJet       = std.vector('double')()
phi_Of_lJet       = std.vector('double')()
pt_CvsLJet1       = array('d',[0])
pt_CvsLJet2       = array('d',[0])
eta_CvsLJet1      = array('d',[0])
eta_CvsLJet2      = array('d',[0])
phi_CvsLJet1      = array('d',[0])
phi_CvsLJet2      = array('d',[0])
CvsL_CvsLJet1     = array('d',[0])
CvsL_CvsLJet2     = array('d',[0])
CvsB_CvsLJet1     = array('d',[0])
CvsB_CvsLJet2     = array('d',[0])
if not 'Single' in channel and not 'Double' in channel:
    hadronFlavour_CsvLJet1  = array('d',[0])
    hadronFlavour_CsvLJet2  = array('d',[0])
    is_ZtoCCorBB       = array('d',[0])
HIGGS_Pt         = array('d',[0])
HIGGS_FL         = array('d',[0])
HIGGS_CvsL_Mass  = array('d',[0])
HIGGS_CvsL_Pt    = array('d',[0])
HIGGS_CvsL_Eta   = array('d',[0])
HIGGS_CvsL_Phi   = array('d',[0])
HIGGS_CvsB       = array('d',[0])
HIGGS_CvsB_CvsL  = array('d',[0])
HIGGS_CvsB_CvsL2 = array('d',[0])

cc_HIGGS_Pt         = array('d',[0])
cc_HIGGS_FL         = array('d',[0])
cc_HIGGS_CvsL       = array('d',[0])
cc_HIGGS_CvsB       = array('d',[0])
cc_HIGGS_CvsB_CvsL  = array('d',[0])
cc_HIGGS_CvsB_CvsL2 = array('d',[0])

co_HIGGS_Pt         = array('d',[0])
co_HIGGS_FL         = array('d',[0])
co_HIGGS_CvsL       = array('d',[0])
co_HIGGS_CvsB       = array('d',[0])
co_HIGGS_CvsB_CvsL  = array('d',[0])
co_HIGGS_CvsB_CvsL2 = array('d',[0])

oo_HIGGS_Pt         = array('d',[0])
oo_HIGGS_FL         = array('d',[0])
oo_HIGGS_CvsL       = array('d',[0])
oo_HIGGS_CvsB       = array('d',[0])
oo_HIGGS_CvsB_CvsL  = array('d',[0])
oo_HIGGS_CvsB_CvsL2 = array('d',[0])

M_Mass              = std.vector('double')()
met_Phi             = array('d',[0])
eta_Of_bJet         = std.vector('double')()
phi_Of_bJet         = std.vector('double')()
Flag_W_jet          = array('d',[0])
solver_chi2         = array('d',[0])

########################## MVA VARIABLES ##########################
SoftActivityJetHT       = array('d',[0])
SoftActivityJetNjets2   = array('d',[0])
SoftActivityJetNjets5   = array('d',[0])
SoftActivityJetNjets10  = array('d',[0])

DPhi_VH             = array('d',[0])
DPhi_METlep         = array('d',[0])
W_Tmass             = array('d',[0])
top_Mass            = array('d',[0])
DR_cc               = array('d',[0])
lepDR_cc            = array('d',[0])
M_lep_c             = array('d',[0])
centrality          = array('d',[0])
avgCvsLpT           = array('d',[0])
FWmoment_1         = array('d',[0])
FWmoment_2         = array('d',[0])
FWmoment_3         = array('d',[0])
FWmoment_4         = array('d',[0])

###################################################################

outputTree.Branch('run'              ,run           ,'run/D'        )
outputTree.Branch('lumiBlock'        ,lumiBlock     ,'lumiBlock/D'  )
outputTree.Branch('event'            ,event         ,'event/D'      )
outputTree.Branch('LHE_HT'           ,LHE_HT        ,'LHE_HT/D'     )

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
outputTree.Branch('jet_CvsL'         ,jet_CvsL      )
outputTree.Branch('jet_CvsB'         ,jet_CvsB      )
outputTree.Branch('jet_qgl'          ,jet_qgl      )


if not 'Single' in channel and not 'Double' in channel:
    outputTree.Branch('jet_hadronFlv'    ,jet_hadronFlv )
outputTree.Branch('met_Pt'           ,met_Pt          ,'met_Pt/D'     )
outputTree.Branch('met_Phi'          ,met_Phi         ,'met_Phi/D')
outputTree.Branch('met_signif'       ,met_signif      ,'met_signif/D')

outputTree.Branch('W_Mass'           ,W_Mass          ,'W_Mass/D'     )
outputTree.Branch('W_Pt'             ,W_Pt            ,'W_Pt/D'     )
outputTree.Branch('W_Eta'            ,W_Eta           ,'W_Eta/D'     )
outputTree.Branch('W_Phi'            ,W_Phi           ,'W_Phi/D'     )

outputTree.Branch('W_Mass_nuSol'     ,W_Mass_nuSol    ,'W_Mass_nuSol/D'     )
outputTree.Branch('W_Pt_nuSol'       ,W_Pt_nuSol      ,'W_Pt_nuSol/D'     )
outputTree.Branch('W_Eta_nuSol'      ,W_Eta_nuSol     ,'W_Eta_nuSol/D'     )
outputTree.Branch('W_Phi_nuSol'      ,W_Phi_nuSol     ,'W_Phi_nuSol/D'     )

outputTree.Branch('is_E'     ,is_E    ,'is_E/D'     )
outputTree.Branch('is_M'     ,is_M    ,'is_M/D'     )

# outputTree.Branch('is_H_mass_CR'     ,is_H_mass_CR    ,'is_H_mass_CR/D'     )
# outputTree.Branch('is_W_mass_CR'     ,is_W_mass_CR    ,'is_W_mass_CR/D'     )

outputTree.Branch('Flag_W_jet'       ,Flag_W_jet      ,'Flag_W_jet/D'     )
outputTree.Branch('solver_chi2'      ,solver_chi2     ,'solver_chi2/D'     )
outputTree.Branch('numOf_cJet'       ,numOf_cJet      ,'numOf_cJet/D'     )
outputTree.Branch('numOf_bJet'       ,numOf_bJet      ,'numOf_bJet/D'     )
outputTree.Branch('numOf_lJet'       ,numOf_lJet      ,'numOf_lJet/D'     )

outputTree.Branch('pt_Of_cJet'       ,pt_Of_cJet    )
outputTree.Branch('pt_Of_bJet'       ,pt_Of_bJet    )
outputTree.Branch('pt_Of_lJet'       ,pt_Of_lJet    )

outputTree.Branch('eta_Of_cJet'       ,eta_Of_cJet  )
outputTree.Branch('eta_Of_bJet'       ,eta_Of_bJet  )
outputTree.Branch('eta_Of_lJet'       ,eta_Of_lJet  )

outputTree.Branch('phi_Of_cJet'       ,phi_Of_cJet  )
outputTree.Branch('phi_Of_bJet'       ,phi_Of_bJet  )
outputTree.Branch('phi_Of_lJet'       ,phi_Of_lJet  )

outputTree.Branch('pt_CvsLJet1'       ,pt_CvsLJet1      ,'pt_CvsLJet1/D'     )
outputTree.Branch('pt_CvsLJet2'       ,pt_CvsLJet2      ,'pt_CvsLJet2/D'     )

outputTree.Branch('eta_CvsLJet1'       ,eta_CvsLJet1      ,'eta_CvsLJet1/D'     )
outputTree.Branch('eta_CvsLJet2'       ,eta_CvsLJet2      ,'eta_CvsLJet2/D'     )

outputTree.Branch('phi_CvsLJet1'       ,phi_CvsLJet1      ,'phi_CvsLJet1/D'     )
outputTree.Branch('phi_CvsLJet2'       ,phi_CvsLJet2      ,'phi_CvsLJet2/D'     )

outputTree.Branch('CvsL_CvsLJet1'       ,CvsL_CvsLJet1      ,'CvsL_CvsLJet1/D'     )
outputTree.Branch('CvsL_CvsLJet2'       ,CvsL_CvsLJet2      ,'CvsL_CvsLJet2/D'     )

outputTree.Branch('CvsB_CvsLJet1'       ,CvsB_CvsLJet1      ,'CvsB_CvsLJet1/D'     )
outputTree.Branch('CvsB_CvsLJet2'       ,CvsB_CvsLJet2      ,'CvsB_CvsLJet2/D'     )
if not 'Single' in channel and not 'Double' in channel:
    outputTree.Branch('hadronFlavour_CsvLJet1' ,hadronFlavour_CsvLJet1 ,'hadronFlavour_CsvLJet1/D'     )
    outputTree.Branch('hadronFlavour_CsvLJet2' ,hadronFlavour_CsvLJet2 ,'hadronFlavour_CsvLJet2/D'     )
    outputTree.Branch('is_ZtoCCorBB'     ,is_ZtoCCorBB    ,'is_ZtoCCorBB/D'     )
outputTree.Branch('HIGGS_Pt'         ,HIGGS_Pt        ,'HIGGS_Pt/D'       )
outputTree.Branch('HIGGS_CvsL_Mass'  ,HIGGS_CvsL_Mass ,'HIGGS_CvsL_Mass/D')
outputTree.Branch('HIGGS_CvsL_Pt'    ,HIGGS_CvsL_Pt   ,'HIGGS_CvsL_Pt/D')
outputTree.Branch('HIGGS_CvsL_Eta'   ,HIGGS_CvsL_Eta  ,'HIGGS_CvsL_Eta/D')
outputTree.Branch('HIGGS_CvsL_Phi'   ,HIGGS_CvsL_Phi  ,'HIGGS_CvsL_Phi/D')
outputTree.Branch('HIGGS_CvsB'       ,HIGGS_CvsB      ,'HIGGS_CvsB/D'     )
outputTree.Branch('HIGGS_CvsB_CvsL'  ,HIGGS_CvsB_CvsL ,'HIGGS_CvsB_CvsL/D')
outputTree.Branch('HIGGS_CvsB_CvsL2' ,HIGGS_CvsB_CvsL2,'HIGGS_CvsB_CvsL2/D')

outputTree.Branch('cc_HIGGS_Pt'         ,cc_HIGGS_Pt        ,'cc_HIGGS_Pt/D'       )
outputTree.Branch('cc_HIGGS_CvsL'       ,cc_HIGGS_CvsL      ,'cc_HIGGS_CvsL/D'     )
outputTree.Branch('cc_HIGGS_CvsB'       ,cc_HIGGS_CvsB      ,'cc_HIGGS_CvsB/D'     )
outputTree.Branch('cc_HIGGS_CvsB_CvsL'  ,cc_HIGGS_CvsB_CvsL ,'cc_HIGGS_CvsB_CvsL/D')
outputTree.Branch('cc_HIGGS_CvsB_CvsL2' ,cc_HIGGS_CvsB_CvsL2,'cc_HIGGS_CvsB_CvsL2/D')

outputTree.Branch('co_HIGGS_Pt'         ,co_HIGGS_Pt        ,'co_HIGGS_Pt/D'       )
outputTree.Branch('co_HIGGS_CvsL'       ,co_HIGGS_CvsL      ,'co_HIGGS_CvsL/D'     )
outputTree.Branch('co_HIGGS_CvsB'       ,co_HIGGS_CvsB      ,'co_HIGGS_CvsB/D'     )
outputTree.Branch('co_HIGGS_CvsB_CvsL'  ,co_HIGGS_CvsB_CvsL ,'co_HIGGS_CvsB_CvsL/D')
outputTree.Branch('co_HIGGS_CvsB_CvsL2' ,co_HIGGS_CvsB_CvsL2,'co_HIGGS_CvsB_CvsL2/D')

outputTree.Branch('oo_HIGGS_Pt'         ,oo_HIGGS_Pt        ,'oo_HIGGS_Pt/D'       )
outputTree.Branch('oo_HIGGS_CvsL'       ,oo_HIGGS_CvsL      ,'oo_HIGGS_CvsL/D'     )
outputTree.Branch('oo_HIGGS_CvsB'       ,oo_HIGGS_CvsB      ,'oo_HIGGS_CvsB/D'     )
outputTree.Branch('oo_HIGGS_CvsB_CvsL'  ,oo_HIGGS_CvsB_CvsL ,'oo_HIGGS_CvsB_CvsL/D')
outputTree.Branch('oo_HIGGS_CvsB_CvsL2' ,oo_HIGGS_CvsB_CvsL2,'oo_HIGGS_CvsB_CvsL2/D')

########################## MVA VARIABLES ##########################
outputTree.Branch('SoftActivityJetHT'                 ,SoftActivityJetHT                  ,'SoftActivityJetHT/D'            )
outputTree.Branch('SoftActivityJetNjets2'             ,SoftActivityJetNjets2              ,'SoftActivityJetNjets2/D'        )
outputTree.Branch('SoftActivityJetNjets5'             ,SoftActivityJetNjets5              ,'SoftActivityJetNjets5/D'        )
outputTree.Branch('SoftActivityJetNjets10'            ,SoftActivityJetNjets10             ,'SoftActivityJetNjets10/D'       )
outputTree.Branch('DPhi_VH'                     ,DPhi_VH          ,'DPhi_VH/D'          )
outputTree.Branch('DPhi_METlep'                 ,DPhi_METlep      ,'DPhi_METlep/D'      )
outputTree.Branch('W_Tmass'                     ,W_Tmass          ,'W_Tmass/D'          )
outputTree.Branch('top_Mass'                    ,top_Mass         ,'top_Mass/D'     )
outputTree.Branch('DR_cc'                       ,DR_cc            ,'DR_cc/D'         )
outputTree.Branch('lepDR_cc'                    ,lepDR_cc         ,'lepDR_cc/D'   )
outputTree.Branch('M_lep_c'                     ,M_lep_c          ,'M_lep_c/D'       )
outputTree.Branch('centrality'                  ,centrality       ,'centrality/D'       )
outputTree.Branch('avgCvsLpT'                   ,avgCvsLpT        ,'avgCvsLpT/D'        )
# outputTree.Branch('FWmoment_0'                 ,FWmoment_0      ,'FWmoment_0/D'      )
outputTree.Branch('FWmoment_1'                 ,FWmoment_1      ,'FWmoment_1/D'      )
outputTree.Branch('FWmoment_2'                 ,FWmoment_2      ,'FWmoment_2/D'      )
outputTree.Branch('FWmoment_3'                 ,FWmoment_3      ,'FWmoment_3/D'      )
outputTree.Branch('FWmoment_4'                 ,FWmoment_4      ,'FWmoment_4/D'      )
###################################################################


count = 0
for entry in inputTree:
    if count%100 ==0:
        print "Number of events processed : ", count
#     if count>1000: break
    count+=1
    TriggerPass = False
    elec                = []
    muon                = []

    el_List             = []
    mu_List             = []
    jetList             = []
    jet_FL_List         = []
    jet_Pt_List         = []
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
    j_CvsL_List              = []
    j_CvsB_List              = []
    j_qgl_List               = []
    if not 'Single' in channel and not 'Double' in channel:
        j_hadronFlv_List         = []
        is_ZtoCCorBB[0]     = -100
    isElec              = True
    isMuon              = True
#     is_H_mass_CR[0]     = 0
#     is_W_mass_CR[0]     = 0
 
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
                
    HIGGS_CvsL_Mass[0]  = -1000
    HIGGS_CvsL_Pt[0]    = -1000
    HIGGS_CvsL_Eta[0]   = -1000
    HIGGS_CvsL_Phi[0]   = -1000

    pt_Of_cJet.clear()
    pt_Of_bJet.clear()
    pt_Of_lJet.clear()

    eta_Of_cJet.clear()
    eta_Of_bJet.clear()
    eta_Of_lJet.clear()
    
    phi_Of_cJet.clear()
    phi_Of_bJet.clear()
    phi_Of_lJet.clear()

    jet_nJet[0]            = -1
    Flag_W_jet[0]          = -1000
    solver_chi2[0]         = -1000
    numOf_cJet[0]          = -1
    numOf_bJet[0]          = -1
    numOf_lJet[0]          = -1
    
    cc_HIGGS_Pt[0]         = -1
    cc_HIGGS_CvsL[0]       = -1
    cc_HIGGS_CvsB[0]       = -1
    cc_HIGGS_CvsB_CvsL[0]  = -1
    cc_HIGGS_CvsB_CvsL2[0] = -1
    
    co_HIGGS_Pt[0]         = -1
    co_HIGGS_CvsL[0]       = -1
    co_HIGGS_CvsB[0]       = -1
    co_HIGGS_CvsB_CvsL[0]  = -1
    co_HIGGS_CvsB_CvsL2[0] = -1

    oo_HIGGS_Pt[0]         = -1
    oo_HIGGS_CvsL[0]       = -1
    oo_HIGGS_CvsB[0]       = -1
    oo_HIGGS_CvsB_CvsL[0]  = -1
    oo_HIGGS_CvsB_CvsL2[0] = -1

    pt_CvsLJet1[0]       = -1
    pt_CvsLJet2[0]       = -1
    eta_CvsLJet1[0]      = -1000
    eta_CvsLJet2[0]      = -1000
    phi_CvsLJet1[0]      = -1000
    phi_CvsLJet2[0]      = -1000
    CvsL_CvsLJet1[0]     = -1
    CvsL_CvsLJet2[0]     = -1
    CvsB_CvsLJet1[0]     = -1
    CvsB_CvsLJet2[0]     = -1

    SoftActivityJetHT[0]       = -1000.0
    SoftActivityJetNjets2[0]   = -1000
    SoftActivityJetNjets5[0]   = -1000
    SoftActivityJetNjets10[0]  = -1000
    DPhi_VH[0]                 = -1000.0
    DPhi_METlep[0]             = -1000.0
    W_Tmass[0]                 = -1000.0
    top_Mass[0]                = -1000.0
    DR_cc[0]                   = -1000.0
    lepDR_cc[0]                = -1000.0
    M_lep_c[0]                 = -1000
    centrality[0]              = -1000.0
    avgCvsLpT[0]               = -1000.0
    
    if not 'Single' in channel and not 'Double' in channel:
        hadronFlavour_CsvLJet1[0] = -100
        hadronFlavour_CsvLJet2[0] = -100
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
    jet_CvsL.clear()
    jet_CvsB.clear()
    jet_qgl.clear()
    if not 'Single' in channel and not 'Double' in channel:
        jet_hadronFlv.clear()

    met_Pt[0]             = -1
    met_Phi[0]            = -1000
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
        jet =  TLorentzVector()
        jet.SetPtEtaPhiM(entry.Jet_pt[i],entry.Jet_eta[i],entry.Jet_phi[i],entry.Jet_mass[i])
        jetList.append(jet)

        if not 'Single' in channel and not 'Double' in channel:
            jet_FL_List.append(entry.Jet_hadronFlavour[i])
        jet_Pt_List.append(entry.Jet_pt[i])
        jet_CvsL_List.append(entry.Jet_CvsL[i])
        jet_CvsB_List.append(entry.Jet_CvsB[i])
        jet_CvsB_CvsL_List.append((entry.Jet_CvsB[i])+(entry.Jet_CvsL[i]))
        jet_CvsB_CvsL_List2.append((entry.Jet_CvsB[i])**2+(entry.Jet_CvsL[i])**2)

        HT_temp         += entry.Jet_pt[i]
        totalJetEnergy  += jet.E()
        if entry.Jet_CvsL[i]>0:
            totalJetCvsLpt  += entry.Jet_CvsL[i]*entry.Jet_pt[i]

        j_Pt_List.append(entry.Jet_pt[i])
        j_Eta_List.append(entry.Jet_eta[i])
        j_Phi_List.append(entry.Jet_phi[i])
        j_Mass_List.append(entry.Jet_mass[i])
        j_CvsL_List.append(entry.Jet_CvsL[i])
        j_CvsB_List.append(entry.Jet_CvsB[i])
        j_qgl_List.append(entry.Jet_qgl[i])
        if not 'Single' in channel and not 'Double' in channel:
            j_hadronFlv_List.append(entry.Jet_hadronFlavour[i])
    HT[0]                  = HT_temp
    if totalJetEnergy!=0:
        centrality[0]          = HT_temp/totalJetEnergy
    if HT_temp!=0:
        avgCvsLpT[0]           = (totalJetCvsLpt+1)/HT_temp

    met_Pt[0]              = entry.MET_Pt
    met_Phi[0]             = entry.MET_Phi
    met_signif[0]          = entry.MET_significance
    
    mW = 80.38
    mH = 125 + mW    
    MET = TLorentzVector()
    MET.SetPtEtaPhiM(entry.MET_Pt, 0., entry.MET_Phi, 0.)
    sigma2 = np.array([((MET.Px()*.1)**2,0),(0,(MET.Py()*.1)**2)])    
    
    
    if debug == True:
        print "Preselection 2 : at least two jets with jet_pt > 20 and jet_eta < 2.4"    
    if len(jetList)<2: continue
    if not 'Single' in channel and not 'Double' in channel:
        for i in range(0,len(j_hadronFlv_List)):
            if j_hadronFlv_List[i] == 4:
                eta_Of_cJet.push_back(j_Eta_List[i])
                pt_Of_cJet.push_back(j_Pt_List[i])
                phi_Of_cJet.push_back(j_Phi_List[i])
            elif j_hadronFlv_List[i] == 5:
                eta_Of_bJet.push_back(j_Eta_List[i])
                pt_Of_bJet.push_back(j_Pt_List[i])
                phi_Of_bJet.push_back(j_Phi_List[i])
            elif j_hadronFlv_List[i] == 0:
                eta_Of_lJet.push_back(j_Eta_List[i])
                pt_Of_lJet.push_back(j_Pt_List[i])
                phi_Of_lJet.push_back(j_Phi_List[i])
    VBoson = 0
    if not isElec and len(m_Pt_List)==1:
        for i in range(0, len(m_Pt_List)):
            mu =  TLorentzVector()
            mu.SetPtEtaPhiM(m_Pt_List[i],m_Eta_List[i],m_Phi_List[i],m_Mass_List[i])
            muon.append(mu)
        VBoson      = (muon[0]+MET)
        DPhi_METlep[0] = (muon[0]).DeltaPhi(MET)
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
        DPhi_METlep[0] = (elec[0]).DeltaPhi(MET)
        W_Mass[0]   = (elec[0]+MET).M()
        W_Tmass[0]  = (elec[0]+MET).Mt()
        W_Pt[0]     = (elec[0]+MET).Pt()
        W_Eta[0]    = (elec[0]+MET).Eta()                    
        W_Phi[0]    = (elec[0]+MET).Phi()                               
    if debug == True:
        print "Preselection 3 : W_pt > 50"    
    if W_Pt[0]<50: continue    

    if debug == True:
        print "Preselection 4 : TRIGGERS" 
        print "HLT_IsoMu24"
        print "HLT_IsoTkMu24"         
        print "HLT_Ele27_WPTight_Gsf"
    if ( entry.HLT_IsoMu24 == 0 ) and ( entry.HLT_IsoTkMu24 == 0 ) and (entry.HLT_Ele27_WPTight_Gsf == 0 )  : continue
    TriggerPass = True    

    if not 'Single' in channel and not 'Double' in channel:
        hJets_Pt         = sorted(zip(jetList,jet_Pt_List,         jet_FL_List                ), key = lambda pair : pair[1], reverse=True)[0:3]
        hJets_CvsL       = sorted(zip(jetList,jet_CvsL_List,       jet_FL_List, jet_CvsB_List ), key = lambda pair : pair[1], reverse=True)[0:4]
        hJets_CvsB       = sorted(zip(jetList,jet_CvsB_List,       jet_FL_List                ), key = lambda pair : pair[1], reverse=True)[0:3]
        hJets_CvsB_CvsL  = sorted(zip(jetList,jet_CvsB_CvsL_List,  jet_FL_List                ), key = lambda pair : pair[1], reverse=True)[0:3]
        hJets_CvsB_CvsL2 = sorted(zip(jetList,jet_CvsB_CvsL_List2, jet_FL_List                ), key = lambda pair : pair[1], reverse=True)[0:3]

        numOf_cJet[0] = jet_FL_List.count(4)
        numOf_bJet[0] = jet_FL_List.count(5)
        numOf_lJet[0] = jet_FL_List.count(0)

######################### FLAGS for splitting W + jets #######################
    if 'WJetsToLNu' in channel:
        if jet_FL_List.count(4) >= 2:
            Flag_W_jet[0] = 1
        elif jet_FL_List.count(4) == 1 and jet_FL_List.count(5) == 1:
            Flag_W_jet[0] = 2
        elif jet_FL_List.count(4) == 1 and jet_FL_List.count(0) == 1:
            Flag_W_jet[0] = 3
        elif jet_FL_List.count(5) >= 2:
            Flag_W_jet[0] = 4
        elif jet_FL_List.count(5) == 1 and jet_FL_List.count(0) == 1:
            Flag_W_jet[0] = 5
        else:
            Flag_W_jet[0] = 6            

#     if 'WJetsToLNu' in channel:
#         if jet_FL_List.count(5) >= 2:
#             Flag_W_jet[0] = 1
#         elif jet_FL_List.count(4) == 1 and jet_FL_List.count(5) == 1:
#             Flag_W_jet[0] = 2
#         elif jet_FL_List.count(4) >= 2:
#             Flag_W_jet[0] = 3
#         elif jet_FL_List.count(5) == 1 and jet_FL_List.count(0) == 1:
#             Flag_W_jet[0] = 4
#         elif jet_FL_List.count(4) == 1 and jet_FL_List.count(0) == 1:
#             Flag_W_jet[0] = 5
#         else:
#             Flag_W_jet[0] = 6            


###########################################################################
    if 'Single' in channel or 'Double' in channel:
        hJets_Pt         = sorted(zip(jetList,jet_Pt_List,                         ), key = lambda pair : pair[1], reverse=True)[0:3]
        hJets_CvsL       = sorted(zip(jetList,jet_CvsL_List,       jet_CvsB_List   ), key = lambda pair : pair[1], reverse=True)[0:4]
        hJets_CvsB       = sorted(zip(jetList,jet_CvsB_List,                       ), key = lambda pair : pair[1], reverse=True)[0:3]
        hJets_CvsB_CvsL  = sorted(zip(jetList,jet_CvsB_CvsL_List,                  ), key = lambda pair : pair[1], reverse=True)[0:3]
        hJets_CvsB_CvsL2 = sorted(zip(jetList,jet_CvsB_CvsL_List2,                 ), key = lambda pair : pair[1], reverse=True)[0:3]
    
    sum_hJets_Pt         = hJets_Pt[0][0]         +   hJets_Pt[1][0]
    sum_hJets_CvsL       = hJets_CvsL[0][0]       +   hJets_CvsL[1][0]
    sum_hJets_CvsB       = hJets_CvsB[0][0]       +   hJets_CvsB[1][0]
    sum_hJets_CvsB_CvsL  = hJets_CvsB_CvsL[0][0]  +   hJets_CvsB_CvsL[1][0]
    sum_hJets_CvsB_CvsL2 = hJets_CvsB_CvsL2[0][0] +   hJets_CvsB_CvsL2[1][0]
        
    HIGGS_Pt[0]         = sum_hJets_Pt.M()
    HIGGS_CvsL_Mass[0]  = sum_hJets_CvsL.M()
    HIGGS_CvsL_Pt[0]    = sum_hJets_CvsL.Pt()
    HIGGS_CvsL_Eta[0]   = sum_hJets_CvsL.Eta()
    HIGGS_CvsL_Phi[0]   = sum_hJets_CvsL.Phi()
    HIGGS_CvsB[0]       = sum_hJets_CvsB.M()

    DPhi_VH[0]          = (sum_hJets_CvsL).DeltaPhi(VBoson)
    DR_cc[0]            = (hJets_CvsL[0][0]).DeltaR(hJets_CvsL[1][0])

    top_Mass[0] = (VBoson+hJets_CvsB[-1][0]).M()


    if not isMuon and len(e_Pt_List)==1:
        lepDR_cc[0]         = (elec[0]).DeltaR(sum_hJets_CvsL)
        M_lep_c[0]          = (elec[0]+hJets_CvsL[0][0]).M()
    if not isElec and len(m_Pt_List)==1:
        lepDR_cc[0]         = (muon[0]).DeltaR(sum_hJets_CvsL)
        M_lep_c[0]          = (muon[0]+hJets_CvsL[0][0]).M()
    HIGGS_CvsB_CvsL[0]  = sum_hJets_CvsB_CvsL.M()
    HIGGS_CvsB_CvsL2[0] = sum_hJets_CvsB_CvsL2.M()

    pt_CvsLJet1[0]       = hJets_CvsL[0][0].Pt()
    pt_CvsLJet2[0]       = hJets_CvsL[1][0].Pt()
    eta_CvsLJet1[0]      = hJets_CvsL[0][0].Eta()
    eta_CvsLJet2[0]      = hJets_CvsL[1][0].Eta()
    phi_CvsLJet1[0]      = hJets_CvsL[0][0].Phi()
    phi_CvsLJet2[0]      = hJets_CvsL[1][0].Phi()
    CvsL_CvsLJet1[0]     = hJets_CvsL[0][1]
    CvsL_CvsLJet2[0]     = hJets_CvsL[1][1]
    if not 'Single' in channel and not 'Double' in channel:
        CvsB_CvsLJet1[0]     = hJets_CvsL[0][3]
        CvsB_CvsLJet2[0]     = hJets_CvsL[1][3]
        hadronFlavour_CsvLJet1[0] = hJets_CvsL[0][2]
        hadronFlavour_CsvLJet2[0] = hJets_CvsL[1][2]
    if 'Single' in channel or 'Double' in channel:
        CvsB_CvsLJet1[0]     = hJets_CvsL[0][2]
        CvsB_CvsLJet2[0]     = hJets_CvsL[1][2]
    
    if not 'Single' in channel and not 'Double' in channel:
        if hJets_Pt[0][2] == 4 and hJets_Pt[1][2] == 4:
            cc_sum_hJets_Pt         = hJets_Pt[0][0]         +   hJets_Pt[1][0]
            cc_HIGGS_Pt[0]          = cc_sum_hJets_Pt.M()
        if hJets_CvsL[0][2] == 4 and hJets_CvsL[1][2] == 4:
            cc_sum_hJets_CvsL       = hJets_CvsL[0][0]       +   hJets_CvsL[1][0]
            cc_HIGGS_CvsL[0]        = cc_sum_hJets_CvsL.M()
        
        if hJets_CvsB[0][2] == 4 and hJets_CvsB[1][2] == 4:
            cc_sum_hJets_CvsB       = hJets_CvsB[0][0]       +   hJets_CvsB[1][0]
            cc_HIGGS_CvsB[0]        = cc_sum_hJets_CvsB.M()
        if hJets_CvsB_CvsL[0][2] == 4 and hJets_CvsB_CvsL[1][2] == 4:
            cc_sum_hJets_CvsB_CvsL  = hJets_CvsB_CvsL[0][0]  +   hJets_CvsB_CvsL[1][0]
            cc_HIGGS_CvsB_CvsL[0]   = cc_sum_hJets_CvsB_CvsL.M()
        if hJets_CvsB_CvsL2[0][2] == 4 and hJets_CvsB_CvsL2[1][2] == 4:
            cc_sum_hJets_CvsB_CvsL2 = hJets_CvsB_CvsL2[0][0] +   hJets_CvsB_CvsL2[1][0]
            cc_HIGGS_CvsB_CvsL2[0]  = cc_sum_hJets_CvsB_CvsL2.M()    


        if (hJets_Pt[0][2] == 4 and hJets_Pt[1][2] != 4) or (hJets_Pt[0][2] != 4 and hJets_Pt[1][2] == 4):
            co_sum_hJets_Pt         = hJets_Pt[0][0]         +   hJets_Pt[1][0]
            co_HIGGS_Pt[0]          = co_sum_hJets_Pt.M()
        if (hJets_CvsL[0][2] == 4 and hJets_CvsL[1][2] != 4) or (hJets_CvsL[0][2] != 4 and hJets_CvsL[1][2] == 4):
            co_sum_hJets_CvsL       = hJets_CvsL[0][0]       +   hJets_CvsL[1][0]
            co_HIGGS_CvsL[0]        = co_sum_hJets_CvsL.M()

        if (hJets_CvsB[0][2] == 4 and hJets_CvsB[1][2] != 4) or (hJets_CvsB[0][2] != 4 and hJets_CvsB[1][2] == 4):
            co_sum_hJets_CvsB       = hJets_CvsB[0][0]       +   hJets_CvsB[1][0]
            co_HIGGS_CvsB[0]        = co_sum_hJets_CvsB.M()
        if (hJets_CvsB_CvsL[0][2] == 4 and hJets_CvsB_CvsL[1][2] != 4) or (hJets_CvsB_CvsL[0][2] != 4 and hJets_CvsB_CvsL[1][2] == 4):
            co_sum_hJets_CvsB_CvsL  = hJets_CvsB_CvsL[0][0]  +   hJets_CvsB_CvsL[1][0]
            co_HIGGS_CvsB_CvsL[0]   = co_sum_hJets_CvsB_CvsL.M()
        if (hJets_CvsB_CvsL2[0][2] == 4 and hJets_CvsB_CvsL2[1][2] != 4) or (hJets_CvsB_CvsL2[0][2] != 4 and hJets_CvsB_CvsL2[1][2] == 4):
            co_sum_hJets_CvsB_CvsL2 = hJets_CvsB_CvsL2[0][0] +   hJets_CvsB_CvsL2[1][0]
            co_HIGGS_CvsB_CvsL2[0]  = co_sum_hJets_CvsB_CvsL2.M()    

        
        if (hJets_Pt[0][2] != 4 and hJets_Pt[1][2] != 4):
            oo_sum_hJets_Pt         = hJets_Pt[0][0]         +   hJets_Pt[1][0]
            oo_HIGGS_Pt[0]          = oo_sum_hJets_Pt.M()
        if (hJets_CvsL[0][2] != 4 and hJets_CvsL[1][2] != 4):
            oo_sum_hJets_CvsL       = hJets_CvsL[0][0]       +   hJets_CvsL[1][0]
            oo_HIGGS_CvsL[0]        = oo_sum_hJets_CvsL.M()
        if (hJets_CvsB[0][2] != 4 and hJets_CvsB[1][2] != 4):
            oo_sum_hJets_CvsB       = hJets_CvsB[0][0]       +   hJets_CvsB[1][0]
            oo_HIGGS_CvsB[0]        = oo_sum_hJets_CvsB.M()
        if (hJets_CvsB_CvsL[0][2] != 4 and hJets_CvsB_CvsL[1][2] != 4):
            oo_sum_hJets_CvsB_CvsL  = hJets_CvsB_CvsL[0][0]  +   hJets_CvsB_CvsL[1][0]
            oo_HIGGS_CvsB_CvsL[0]   = oo_sum_hJets_CvsB_CvsL.M()
        if (hJets_CvsB_CvsL2[0][2] != 4 and hJets_CvsB_CvsL2[1][2] != 4):
            oo_sum_hJets_CvsB_CvsL2 = hJets_CvsB_CvsL2[0][0] +   hJets_CvsB_CvsL2[1][0]
            oo_HIGGS_CvsB_CvsL2[0]  = oo_sum_hJets_CvsB_CvsL2.M()    


    if isElec:
        is_E[0] = isElec
        for i, ePt in enumerate(e_Pt_List):
            E_Mass.push_back(e_Mass_List[i])
            E_Pt.push_back(ePt)
            E_Eta.push_back(e_Eta_List[i])
            E_Phi.push_back(e_Phi_List[i])
            E_Charge.push_back(e_Charge_List[i])
        Nu = TLorentzVector()
        solver_CvsL = nu.singleNeutrinoSolution((hJets_CvsL[0][0]+hJets_CvsL[1][0]),elec[0],(MET.Px(),MET.Py()),sigma2,mW**2,mH**2)
        Neutrino = solver_CvsL.nu
        if type(Neutrino) is not types.BooleanType:
            Nu.SetXYZM(Neutrino[0],Neutrino[1],Neutrino[2],0)
            W_Mass_nuSol[0] = (Nu + elec[0]).M()
            W_Pt_nuSol[0]   = (Nu + elec[0]).Pt()
            W_Eta_nuSol[0]  = (Nu + elec[0]).Eta()
            W_Phi_nuSol[0]  = (Nu + elec[0]).Phi()                
            solver_chi2[0] = solver_CvsL.chi2
    if isMuon:
        is_M[0] = isMuon
        for i, mPt in enumerate(m_Pt_List):
            M_Mass.push_back(m_Mass_List[i])
            M_Pt.push_back(mPt)
            M_Eta.push_back(m_Eta_List[i])
            M_Phi.push_back(m_Phi_List[i])
            M_Charge.push_back(m_Charge_List[i])
        Nu = TLorentzVector()
        solver_CvsL = nu.singleNeutrinoSolution((hJets_CvsL[0][0]+hJets_CvsL[1][0]),muon[0],(MET.Px(),MET.Py()),sigma2,mW**2,mH**2)
        Neutrino = solver_CvsL.nu
        if type(Neutrino) is not types.BooleanType:
            Nu.SetXYZM(Neutrino[0],Neutrino[1],Neutrino[2],0)
            W_Mass_nuSol[0] = (Nu + muon[0]).M()
            W_Pt_nuSol[0]   = (Nu + muon[0]).Pt()
            W_Eta_nuSol[0]  = (Nu + muon[0]).Eta()
            W_Phi_nuSol[0]  = (Nu + muon[0]).Phi()                
            solver_chi2[0] = solver_CvsL.chi2

        
    for i, jPt in enumerate(j_Pt_List):
        jet_Mass.push_back(j_Mass_List[i])
        jet_Pt.push_back(jPt)
        jet_Eta.push_back(j_Eta_List[i])
        jet_Phi.push_back(j_Phi_List[i])
        jet_CvsL.push_back(j_CvsL_List[i])
        jet_CvsB.push_back(j_CvsB_List[i])
        jet_qgl.push_back(j_qgl_List[i])
        if not 'Single' in channel and not 'Double' in channel:
            jet_hadronFlv.push_back(j_hadronFlv_List[i])
    jet_nJet[0]            = len(j_Pt_List)

#     if HIGGS_CvsL_Mass[0]<90 or HIGGS_CvsL_Mass[0]>150:
#         is_H_mass_CR[0] = 1
#     if W_Mass[0]<65 or W_Mass[0]>95:
#         is_W_mass_CR[0] = 1    


######################### FLAGS for W to cc or bb #######################
    if not 'Single' in channel and not 'Double' in channel:
        dau1c_index   = -1
        dau2c_index   = -1
        dau1b_index   = -1
        dau2b_index   = -1
        num_Z         = 0
        genpart_List  = []

        for genpart in range(entry.nGenPart):
            if entry.GenPart_pdgId[genpart] == 23 and ( entry.GenPart_statusFlags[genpart] & 8192 ) == 8192 :
                genpart_List.append(genpart)
                num_Z += 1
        if len(genpart_List) == 2:
            for mother_index in genpart_List:
               for genpart in range(entry.nGenPart):
                   if abs(entry.GenPart_pdgId[genpart]) == 4 and entry.GenPart_genPartIdxMother[genpart] == mother_index:
                       if dau1c_index > -1 and dau2c_index > -1: continue
                       elif dau1c_index > -1 :
                           dau2c_index = genpart
                       else :
                           dau1c_index = genpart
               for genpart in range(entry.nGenPart):
                   if abs(entry.GenPart_pdgId[genpart]) == 5 and entry.GenPart_genPartIdxMother[genpart] == mother_index:
                       if dau1b_index > -1 and dau2b_index > -1: continue
                       elif dau1b_index > -1 :
                           dau2b_index = genpart
                       else :
                           dau1b_index = genpart
            if dau1c_index > -1 and dau2c_index > -1:
                if  abs(entry.GenPart_pdgId[dau1c_index]) == 4 and abs(entry.GenPart_pdgId[dau2c_index]) == 4: is_ZtoCCorBB[0] = 1
            elif dau1b_index > -1 and dau2b_index > -1:
                if  abs(entry.GenPart_pdgId[dau1b_index]) == 5 and abs(entry.GenPart_pdgId[dau2b_index]) == 5: is_ZtoCCorBB[0] = 2
            else: is_ZtoCCorBB[0] = 0
        
    if (isMuon or isElec) and len(j_Pt_List) >= 2 and W_Pt[0]>=50 and TriggerPass:
        run[0]              = entry.run
        lumiBlock[0]        = entry.luminosityBlock
        event[0]            = entry.event
        if not 'Single' in channel and not 'Double' in channel and not 'WW' in channel and not 'WZ' in channel:
            LHE_HT[0]           = entry.LHE_HT

        SoftActivityJetHT[0]       = entry.SoftActivityJetHT
        SoftActivityJetNjets2[0]   = entry.SoftActivityJetNjets2
        SoftActivityJetNjets5[0]   = entry.SoftActivityJetNjets5
        SoftActivityJetNjets10[0]  = entry.SoftActivityJetNjets10
        outputTree.Fill()
    else: continue

    ETSum = 0
#     FWM_0 = 0
    FWM_1 = 0
    FWM_2 = 0
    FWM_3 = 0
    FWM_4 = 0
    for jet in jetList:
        ETSum += jet.Et()
    for jet1 in jetList:
        for jet2 in jetList:
            EToverETSum2 = jet1.Et()*jet2.Et()/ETSum**2
            cosTheta_ij = (jet1.Px()*jet2.Px() + jet1.Py()*jet2.Py() + jet1.Pz()*jet2.Pz())/(jet1.Rho()*jet2.Rho())
#             FWM_0 += EToverETSum2
            FWM_1 += EToverETSum2*cosTheta_ij
            FWM_2 += EToverETSum2*0.5   * (  3*pow(cosTheta_ij,2)- 1)
            FWM_3 += EToverETSum2*0.5   * (  5*pow(cosTheta_ij,3)- 3*cosTheta_ij)
            FWM_4 += EToverETSum2*0.125 * ( 35*pow(cosTheta_ij,4)- 30*pow(cosTheta_ij,2)+3)
#     FWmoment_0[0] = FWM_0
    FWmoment_1[0] = FWM_1
    FWmoment_2[0] = FWM_2
    FWmoment_3[0] = FWM_3
    FWmoment_4[0] = FWM_4

outputTree.Write()

nEventTree = iFile.Get("Runs")
nEventCount = 0
if not 'Single' in channel and not 'Double' in channel:
    for entry in nEventTree:
        nEventCount += entry.genEventCount
    print "Total event processed by Nano AOD post processor : ", nEventCount
print "Total events processed : ",count    
print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))
    