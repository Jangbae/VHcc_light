import os, sys

sample_List = [
####### SIGNAL for WHcc #######
# 'WminusH_HToBB_WToLNu_M125_13TeV_powheg_herwigpp',
# 'WminusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8',
'WminusH_HToCC_WToLNu_M125_13TeV_powheg_pythia8',
# 
# 'WplusH_HToBB_WToLNu_M125_13TeV_powheg_herwigpp',
# 'WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8',
# 'WplusH_HToCC_WToLNu_M125_13TeV_powheg_pythia8',
# 
# 
# ####### BKG for WHcc #######
# 'ST_s-channel_4f_InclusiveDecays_13TeV-amcatnlo-pythia8',
# 'ST_t-channel_antitop_4f_inclusiveDecays_TuneCUETP8M2T4_13TeV-powhegV2-madspin',
# 'ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1',
# 'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4',
# 'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1',
# 
# 'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',
# 
# 'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 
# 'WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 
# 
# 'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY3JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 'DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
# 
# 
# 'WW_TuneCUETP8M1_13TeV-pythia8',
# 'WZ_TuneCUETP8M1_13TeV-pythia8',
# 
# ####### DATA for WHcc #######
# 'SingleElectron',
# 'SingleMuon',

]

nlepton = 'WlvHcc'
dir_sampleList = 'sampleList_WlvHcc'
script = 'Wlvhcc.py'
dic_sample = {}
runDir=os.getcwd()
queue = '8nh'
version = 'v4'
outputPath = '/eos/cms/store/user/jblee/Hcc/'
X509_USER_PROXY = '/afs/cern.ch/user/j/jblee/x509up_u37238'