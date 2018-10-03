#!/bin/sh
source /afs/cern.ch/cms/cmsset_default.sh
cd /afs/cern.ch/work/j/jblee/private/Hcc/CMSSW_10_2_0_pre5/src/VHcc/2L
eval `scramv1 runtime -sh`
export X509_USER_PROXY=/afs/cern.ch/user/j/jblee/x509up_u37238
python Zllhcc.py /store/user/lmastrol/VHcc_2016V4_Aug18/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/arizzi-RunIIMoriond17-DeepAndR81/180904_144655/0000/tree_4.root DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 v10
