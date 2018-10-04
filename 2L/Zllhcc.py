from ROOT import *
from array import array

import glob, sys, time

start_time = time.time()
fileName = str(sys.argv[1])
channel  = str(sys.argv[2])
version = str(sys.argv[3]) 

print "start_time : ",time.ctime()
print "processing on : ",fileName

debug = False
iFile = TFile.Open("root://xrootd-cms.infn.it//"+fileName)
inputTree = iFile.Get("Events")
inputTree.SetBranchStatus("*",1)

number = fileName.split('/0000/')[1].split('.root')[0].split('_')[1]
temp = fileName.split(channel+'/')[1].split("/0000/")[0]
label = temp.split('/')[0]+"_"+number

oFile = TFile('/eos/cms/store/user/jblee/Hcc/ZllHcc/'+version+'/'+channel+'/tree_'+label+'.root','RECREATE')

oFile.cd()
outputTree = TTree("Events","Events")

run              = array('d',[0])
lumiBlock        = array('d',[0])
event            = array('d',[0])

E_Mass           = std.vector('double')()
E_Pt             = std.vector('double')()
E_Eta            = std.vector('double')()
E_Phi            = std.vector('double')()
E_Charge         = std.vector('double')()

M_Pt             = std.vector('double')()
M_Eta            = std.vector('double')()
M_Phi            = std.vector('double')()
M_Charge         = std.vector('double')()

jet_Pt             = std.vector('double')()
jet_Eta            = std.vector('double')()
jet_Phi            = std.vector('double')()
jet_Mass           = std.vector('double')()
jet_CvsL           = std.vector('double')()
jet_CvsB           = std.vector('double')()
if not 'Single' in channel and not 'Double' in channel:
    jet_hadronFlv      = std.vector('double')()
jet_nJet           = array('d',[0])
met_Pt             = array('d',[0])

is_E               = array('d',[0])
is_M               = array('d',[0])
is_H_mass_CR       = array('d',[0])
is_Z_mass_CR       = array('d',[0])


Z_Mass           = array('d',[0])
Z_Pt             = array('d',[0])
Z_Eta            = array('d',[0])
Z_Phi            = array('d',[0])

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

outputTree.Branch('run'              ,run           ,'run/D'        )
outputTree.Branch('lumiBlock'        ,lumiBlock     ,'lumiBlock/D'  )
outputTree.Branch('event'            ,event         ,'event/D'      )

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

outputTree.Branch('jet_Pt'           ,jet_Pt        )
outputTree.Branch('jet_Eta'          ,jet_Eta       )
outputTree.Branch('jet_Phi'          ,jet_Phi       )
outputTree.Branch('jet_Mass'         ,jet_Mass      )
outputTree.Branch('jet_nJet'         ,jet_nJet      ,'jet_nJet/D')
outputTree.Branch('jet_CvsL'         ,jet_CvsL      )
outputTree.Branch('jet_CvsB'         ,jet_CvsB      )
if not 'Single' in channel and not 'Double' in channel:
    outputTree.Branch('jet_hadronFlv'    ,jet_hadronFlv )
outputTree.Branch('met_Pt'           ,met_Pt          ,'met_Pt/D'     )
outputTree.Branch('met_Phi'          ,met_Phi         ,'met_Phi/D')
outputTree.Branch('Z_Mass'           ,Z_Mass          ,'Z_Mass/D'     )
outputTree.Branch('Z_Pt'             ,Z_Pt            ,'Z_Pt/D'     )
outputTree.Branch('Z_Eta'            ,Z_Eta           ,'Z_Eta/D'     )
outputTree.Branch('Z_Phi'            ,Z_Phi           ,'Z_Phi/D'     )

outputTree.Branch('is_E'     ,is_E    ,'is_E/D'     )
outputTree.Branch('is_M'     ,is_M    ,'is_M/D'     )

outputTree.Branch('is_H_mass_CR'     ,is_H_mass_CR    ,'is_H_mass_CR/D'     )
outputTree.Branch('is_Z_mass_CR'     ,is_Z_mass_CR    ,'is_Z_mass_CR/D'     )


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

count = 0
for entry in inputTree:
    if count%100 ==0:
        print "Number of events processed : ", count
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
    if not 'Single' in channel and not 'Double' in channel:
        j_hadronFlv_List         = []
        is_ZtoCCorBB[0]     = -100
    isElec              = True
    isMuon              = True
    is_H_mass_CR[0]     = 0
    is_Z_mass_CR[0]     = 0

    is_E[0]             = False
    is_M[0]             = False

    run[0]              = -1000
    lumiBlock[0]        = -1000
    event[0]            = -1000

    Z_Mass[0]           = -1000
    Z_Pt[0]             = -1000
    Z_Eta[0]            = -1000
    Z_Phi[0]            = -1000

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
    if not 'Single' in channel and not 'Double' in channel:
        jet_hadronFlv.clear()

    met_Pt[0]             = -1
    met_Phi[0]            = -1000

    if debug == True:
        print "Preselection 1 : OSSF Lepton"
        print "                 electron selection : pt1 > 20 and eta<2.5"
        print "                 electron selection : pt2 > 20 and eta<2.5"
        print "                 electron selection : Electron_mvaSpring16GP_WP80 > 0"
        print "                 electron selection : Electron_pfRelIso03_all <= 0.15"
        print "                 muon selection : pt > 20 and eta<2.4"
        print "                 muon selection : pt > 20 and eta<2.4"
        print "                 muon selection : Muon_mediumId > 0"
        print "                 muon selection : Muon_pfRelIso03_all<0.25"

    for i in range(0, len(entry.Electron_pt)):
        if entry.Electron_pt[i]<20 or abs(entry.Electron_eta[i])>2.5: continue
        if entry.Electron_mvaSpring16GP_WP80[i]<=0: continue
        if entry.Electron_pfRelIso03_all[i]>0.15: continue
        e_Pt_List.append(entry.Electron_pt[i])
        e_Eta_List.append(entry.Electron_eta[i])
        e_Phi_List.append(entry.Electron_phi[i])
        e_Charge_List.append(entry.Electron_charge[i])
        e_Mass_List.append(entry.Electron_mass[i])

    for i in range(0, len(entry.Muon_pt)):
        if entry.Muon_pt[i]<20 or abs(entry.Muon_eta[i])>2.4: continue
        if entry.Muon_mediumId[i]<=0: continue
        if entry.Muon_pfRelIso03_all[i]>0.25: continue        
        m_Pt_List.append(entry.Muon_pt[i])
        m_Eta_List.append(entry.Muon_eta[i])
        m_Phi_List.append(entry.Muon_phi[i])
        m_Charge_List.append(entry.Muon_charge[i])
        m_Mass_List.append(entry.Muon_mass[i])
    
    if len(e_Pt_List) + len(m_Pt_List) != 2: continue
    if len(e_Pt_List) == 2 and (e_Pt_List[0]<20 or e_Pt_List[1]<20): continue
    if len(m_Pt_List) == 2 and (m_Pt_List[0]<20 or m_Pt_List[1]<20): continue
        
    if len(e_Pt_List) == 2:
        isMuon = False
        el_List = sorted(zip(e_Pt_List,e_Charge_List), key = lambda pair : pair[0], reverse=True)[0:2]
    if not isMuon and el_List[0][1]*el_List[1][1] > 0: continue

        
    if len(m_Pt_List) == 2:
        isElec = False
        mu_List = sorted(zip(m_Pt_List,m_Charge_List), key = lambda pair : pair[0], reverse=True)[0:2]
    if not isElec and mu_List[0][1]*mu_List[1][1] > 0: continue


    if debug == True:
        print "                 Jet selection : jet_pt > 25 and jet_eta < 2.5"    
        print "                 Jet selection : Jet_lepFilter == True"    
        print "                 Jet selection : Jet_puId >= 0"    

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

        j_Pt_List.append(entry.Jet_pt[i])
        j_Eta_List.append(entry.Jet_eta[i])
        j_Phi_List.append(entry.Jet_phi[i])
        j_Mass_List.append(entry.Jet_mass[i])
        j_CvsL_List.append(entry.Jet_CvsL[i])
        j_CvsB_List.append(entry.Jet_CvsB[i])
        if not 'Single' in channel and not 'Double' in channel:
            j_hadronFlv_List.append(entry.Jet_hadronFlavour[i])

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
    if not isElec and len(m_Pt_List)==2:
        for i in range(0, len(m_Pt_List)):
            mu =  TLorentzVector()
            mu.SetPtEtaPhiM(m_Pt_List[i],m_Eta_List[i],m_Phi_List[i],m_Mass_List[i])
            muon.append(mu)
        Z_Mass[0] = (muon[0]+muon[1]).M()
        Z_Pt[0] = (muon[0]+muon[1]).Pt()                    
        Z_Eta[0] = (muon[0]+muon[1]).Eta()                    
        Z_Phi[0] = (muon[0]+muon[1]).Phi()                    
    if not isMuon and len(e_Pt_List)==2:
        for i in range(0, len(e_Pt_List)):
            el =  TLorentzVector()
            el.SetPtEtaPhiM(e_Pt_List[i],e_Eta_List[i],e_Phi_List[i],e_Mass_List[i])
            elec.append(el)
        Z_Mass[0] = (elec[0]+elec[1]).M()
        Z_Pt[0] = (elec[0]+elec[1]).Pt()
        Z_Eta[0] = (elec[0]+elec[1]).Eta()                    
        Z_Phi[0] = (elec[0]+elec[1]).Phi()                    

    if debug == True:
        print "Preselection 3 : Z_pt > 50"    
    if Z_Pt[0]<50: continue    

    if debug == True:
        print "Preselection 4 : TRIGGERS" 
        print "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ"
        print "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ"         
        print "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"
    if (entry.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL == 0) and (entry.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ == 0    ) and (entry.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL == 0   ) and (entry.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ == 0  ) and (entry.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ == 0) : continue
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
    if isMuon:
        is_M[0] = isMuon
        for i, mPt in enumerate(m_Pt_List):
            M_Mass.push_back(m_Mass_List[i])
            M_Pt.push_back(mPt)
            M_Eta.push_back(m_Eta_List[i])
            M_Phi.push_back(m_Phi_List[i])
            M_Charge.push_back(m_Charge_List[i])

    for i, jPt in enumerate(j_Pt_List):
        jet_Mass.push_back(j_Mass_List[i])
        jet_Pt.push_back(jPt)
        jet_Eta.push_back(j_Eta_List[i])
        jet_Phi.push_back(j_Phi_List[i])
        jet_CvsL.push_back(j_CvsL_List[i])
        jet_CvsB.push_back(j_CvsB_List[i])
        if not 'Single' in channel and not 'Double' in channel:
            jet_hadronFlv.push_back(j_hadronFlv_List[i])
    met_Pt[0]              = entry.MET_Pt
    met_Phi[0]             = entry.MET_Phi
    jet_nJet[0]            = len(j_Pt_List)

    if HIGGS_CvsL_Mass[0]<100 or HIGGS_CvsL_Mass[0]>140:
        is_H_mass_CR[0] = 1
    if Z_Mass[0]<81 or Z_Mass[0]>101:
        is_Z_mass_CR[0] = 1    


######################### FLAGS for Z to cc or bb #######################
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
        
    if (isMuon or isElec) and len(j_Pt_List) >= 2 and Z_Pt[0]>=50 and TriggerPass:
        run[0]              = entry.run
        lumiBlock[0]        = entry.luminosityBlock
        event[0]            = entry.event
        outputTree.Fill()
    else: continue

outputTree.Write()

nEventTree = iFile.Get("Runs")
nEventCount = 0
if not 'Single' in channel and not 'Double' in channel:
    for entry in nEventTree:
        nEventCount += entry.genEventCount
    print "Total event processed by Nano AOD post processor : ", nEventCount
print "Total events processed : ",count    
print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))