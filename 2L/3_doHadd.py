import os, sys, glob

dic_sample = {}

sampleList = [
# 'DoubleEG',
# 'DoubleMuon',
# 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY3JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8',
# 'ggZH_HToCC_ZToLL_M125_13TeV_powheg_pythia8',
# 'TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',
# 'WW_TuneCUETP8M1_13TeV-pythia8',
# 'WZ_TuneCUETP8M1_13TeV-pythia8',
# 'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8',
# 'ZH_HToCC_ZToLL_M125_13TeV_powheg_pythia8',
# 'ZZ_TuneCUETP8M1_13TeV-pythia8',

'DoubleEG',
# 'DoubleMuon',
# 
# 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',
# 'WW_TuneCUETP8M1_13TeV-pythia8',
# 'WZ_TuneCUETP8M1_13TeV-pythia8',
# 'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8',
# 'ZH_HToCC_ZToLL_M125_13TeV_powheg_pythia8',
# 'ZZ_TuneCUETP8M1_13TeV-pythia8',
]
runDir=os.getcwd()
version = 'v10'
nlepton = 'ZllHcc'

if not os.path.exists("/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"_Hadd"): os.system('mkdir '+"/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"_Hadd")
outputPath = "/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"_Hadd/"

for s in sampleList:
    print s
    os.chdir(runDir)
    pathInput = glob.glob("sampleList/Samples_"+s+"_fPath_*.txt")
    num_lines = 0
    for path in pathInput:
        print path
        num_lines += sum(1 for line in open(path))
    os.chdir("/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"/"+s)
    fileList = glob.glob("*.root")    
    Nfile = 0
    haddCommand = "hadd -f "+outputPath+s+"_hadd.root "
    for f in fileList:
        haddCommand = haddCommand + f +" "
        Nfile+=1
    if int(Nfile) != num_lines:
        print "There is some missing ntuples in "+s
        print "number of ntuples created : ", num_lines
        print "number of ntuples used for hadd: ", int(Nfile)
    print haddCommand
    os.system(haddCommand)
