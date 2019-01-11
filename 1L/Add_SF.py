from ROOT import *
from array import array
import glob, sys, time, json


SF_SingleElTrigger         = array('d',[0])
SF_SingleElIdIso           = array('d',[0])
SF_egammaEffi_tracker      = array('d',[0])
SF_EleVeto                 = array('d',[0])

SF_MuIDTightBCDEF          = array('d',[0])
SF_MuIDTightGH             = array('d',[0])
SF_MuIsoTightBCDEF         = array('d',[0])
SF_MuIsoTightGH            = array('d',[0])
SF_MuTriggerBCDEF          = array('d',[0])
SF_MuTriggerGH             = array('d',[0])
SF_MuTrackerBCDEF          = array('d',[0])
SF_MuTrackerGH             = array('d',[0])

def readTxtFile(SF_txt, lepPt, lepEta):
    textFile = open(SF_txt,'r')
    Line_Dic = {}
    for l in textFile.read().splitlines():
        Line_Dic[l[:-1].split()[4].split('branchname=')[1]] = l[:-1].split()
    for key in Line_Dic:
        JsonFile    = Line_Dic[key][0].split('json=')[1]
        Name        = Line_Dic[key][1].split('name=')[1]
        binning     = Line_Dic[key][2].split('binning=')[1]
        branches    = Line_Dic[key][3].split('branches=')[1]
        BranchName  = Line_Dic[key][4].split('branchname=')[1]
        if "SF_SingleElTrigger" in BranchName:
            SF_SingleElTrigger[0] = readJSONFile(JsonFile, Name, binning, branches, BranchName, lepPt, lepEta)
        elif "SF_SingleElIdIso" in BranchName:
            SF_SingleElIdIso[0] = readJSONFile(JsonFile, Name, binning, branches, BranchName, lepPt, lepEta)
        elif "SF_egammaEffi_tracker" in BranchName:
            SF_egammaEffi_tracker[0] = readJSONFile(JsonFile, Name, binning, branches, BranchName, lepPt, lepEta)
        elif "SF_EleVeto" in BranchName:
            SF_EleVeto[0] = readJSONFile(JsonFile, Name, binning, branches, BranchName, lepPt, lepEta)        

        if "SF_MuIDTightBCDEF" in BranchName:
            SF_MuIDTightBCDEF[0] = readJSONFile(JsonFile, Name, binning, branches, BranchName, lepPt, lepEta)
        elif "SF_MuIDTightGH" in BranchName:
            SF_MuIDTightGH[0] = readJSONFile(JsonFile, Name, binning, branches, BranchName, lepPt, lepEta)
        elif "SF_MuIsoTightBCDEF" in BranchName:
            SF_MuIsoTightBCDEF[0] = readJSONFile(JsonFile, Name, binning, branches, BranchName, lepPt, lepEta)
        elif "SF_MuIsoTightGH" in BranchName:
            SF_MuIsoTightGH[0] = readJSONFile(JsonFile, Name, binning, branches, BranchName, lepPt, lepEta)        
        elif "SF_MuTriggerBCDEF" in BranchName:
            SF_MuTriggerBCDEF[0] = readJSONFile(JsonFile, Name, binning, branches, BranchName, lepPt, lepEta)
        elif "SF_MuTriggerGH" in BranchName:
            SF_MuTriggerGH[0] = readJSONFile(JsonFile, Name, binning, branches, BranchName, lepPt, lepEta)        
        elif "SF_MuTrackerBCDEF" in BranchName:
            SF_MuTrackerBCDEF[0] = readJSONFile(JsonFile, Name, binning, branches, BranchName, lepPt, lepEta)
        elif "SF_MuTrackerGH" in BranchName:
            SF_MuTrackerGH[0] = readJSONFile(JsonFile, Name, binning, branches, BranchName, lepPt, lepEta)        
    textFile.close()

def readJSONFile(JSON, Name, binning, branches, BranchName, lepPt, lepEta):
    JSON_File = open("/afs/cern.ch/work/j/jblee/private/Hcc/CMSSW_10_2_0_pre5/src/VHcc/"+JSON)
    JData = json.load(JSON_File)
    if "eta_pt_ratio" in binning:
        for key in JData[Name][binning]:
            etaL = key.split("eta:[")[1].split("]")[0].split(',')[0]
            etaH = key.split("eta:[")[1].split("]")[0].split(',')[1]
            if check(lepEta[0], float(etaL),float(etaH)):
                for E_key in JData[Name][binning]['eta:['+etaL+','+etaH+']']:
                    ptL = E_key.split("pt:[")[1].split("]")[0].split(',')[0]
                    ptH = E_key.split("pt:[")[1].split("]")[0].split(',')[1]
                    if check(lepPt[0], float(ptL),float(ptH)):
                        SF = JData[Name][binning]['eta:['+etaL+','+etaH+']']['pt:['+ptL+','+ptH+']']['value']                    
                    else: SF = 1.0
            else: SF = 1.0                                            
    elif "pt_abseta_ratio" in binning:
        for key in JData[Name][binning]:
            ptL = key.split("pt:[")[1].split("]")[0].split(',')[0]
            ptH = key.split("pt:[")[1].split("]")[0].split(',')[1]
            if check(lepPt[0], float(ptL),float(ptH)):
                for E_key in JData[Name][binning]['pt:['+ptL+','+ptH+']']:
                    etaL = E_key.split("abseta:[")[1].split("]")[0].split(',')[0]
                    etaH = E_key.split("abseta:[")[1].split("]")[0].split(',')[1]
                    if check(abs(lepEta[0]), float(etaL),float(etaH)):
                        SF = JData[Name][binning]['pt:['+ptL+','+ptH+']']['abseta:['+etaL+','+etaH+']']['value']                    
                    else: SF = 1.0
            else: SF = 1.0                        
    elif "pt_eta_ratio" in binning:
        for key in JData[Name][binning]:
            ptL = key.split("pt:[")[1].split("]")[0].split(',')[0]
            ptH = key.split("pt:[")[1].split("]")[0].split(',')[1]
            if check(lepPt[0], float(ptL),float(ptH)):
                for E_key in JData[Name][binning]['pt:['+ptL+','+ptH+']']:
                    etaL = E_key.split("eta:[")[1].split("]")[0].split(',')[0]
                    etaH = E_key.split("eta:[")[1].split("]")[0].split(',')[1]
                    if check(lepEta[0], float(etaL),float(etaH)):
                        SF = JData[Name][binning]['pt:['+ptL+','+ptH+']']['eta:['+etaL+','+etaH+']']['value']                    
                    else: SF = 1.0
            else: SF = 1.0                                            
    JSON_File.close()
    return SF

                    
def check(value, low, high):
    if low <= value <= high:
        return True
    return False    


Elec_SF_txt = "/afs/cern.ch/work/j/jblee/private/Hcc/CMSSW_10_2_0_pre5/src/VHcc/1L/Elec_SF_cfg.txt"
Muon_SF_txt = "/afs/cern.ch/work/j/jblee/private/Hcc/CMSSW_10_2_0_pre5/src/VHcc/1L/Muon_SF_cfg.txt"

rootFileName = str(sys.argv[1])

fileName = "/eos/cms/store/user/jblee/Hcc/WlvHcc/v2_Hadd/"+rootFileName
iFile = TFile.Open(fileName)
inputTree = iFile.Get("Events")
inputTree.SetBranchStatus("*",1)

oFile = TFile('/eos/cms/store/user/jblee/Hcc/WlvHcc/v2_Hadd_SFadded/'+rootFileName,'RECREATE')
oFile.cd()
outputTree = inputTree.CloneTree(0)
outputTree.Branch('SF_SingleElTrigger',         SF_SingleElTrigger,         'SF_SingleElTrigger/D')
outputTree.Branch('SF_SingleElIdIso',           SF_SingleElIdIso,           'SF_SingleElIdIso/D')
outputTree.Branch('SF_egammaEffi_tracker',      SF_egammaEffi_tracker,      'SF_egammaEffi_tracker/D')
outputTree.Branch('SF_EleVeto',                 SF_EleVeto,                 'SF_EleVeto/D')

outputTree.Branch('SF_MuIDTightBCDEF',          SF_MuIDTightBCDEF,          'SF_MuIDTightBCDEF/D')
outputTree.Branch('SF_MuIDTightGH',             SF_MuIDTightGH,             'SF_MuIDTightGH/D')
outputTree.Branch('SF_MuIsoTightBCDEF',         SF_MuIsoTightBCDEF,         'SF_MuIsoTightBCDEF/D')
outputTree.Branch('SF_MuIsoTightGH',            SF_MuIsoTightGH,            'SF_MuIsoTightGH/D')
outputTree.Branch('SF_MuTriggerBCDEF',          SF_MuTriggerBCDEF,          'SF_MuTriggerBCDEF/D')
outputTree.Branch('SF_MuTriggerGH',             SF_MuTriggerGH,             'SF_MuTriggerGH/D')
outputTree.Branch('SF_MuTrackerBCDEF',          SF_MuTrackerBCDEF,          'SF_MuTrackerBCDEF/D')
outputTree.Branch('SF_MuTrackerGH',             SF_MuTrackerGH,             'SF_MuTrackerGH/D')

i = 0
for entry in inputTree:
    SF_SingleElTrigger[0]          = 1
    SF_SingleElIdIso[0]            = 1
    SF_egammaEffi_tracker[0]       = 1
    SF_EleVeto[0]                  = 1

    SF_MuIDTightBCDEF[0]           = 1
    SF_MuIDTightGH[0]              = 1
    SF_MuIsoTightBCDEF[0]          = 1
    SF_MuIsoTightGH[0]             = 1
    SF_MuTriggerBCDEF[0]           = 1
    SF_MuTriggerGH[0]              = 1
    SF_MuTrackerBCDEF[0]           = 1
    SF_MuTrackerGH[0]              = 1
    if entry.is_M: 
        readTxtFile(Muon_SF_txt, entry.M_Pt, entry.M_Eta)
    if entry.is_E: 
        readTxtFile(Elec_SF_txt, entry.E_Pt, entry.E_Eta)
    outputTree.Fill()
outputTree.Write()
