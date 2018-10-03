#!/bin/sh
source /afs/cern.ch/cms/cmsset_default.sh
cd /afs/cern.ch/work/j/jblee/private/Hcc/CMSSW_10_2_0_pre5/src/VHcc/2L
eval `scramv1 runtime -sh`
export X509_USER_PROXY=/afs/cern.ch/user/j/jblee/x509up_u37238
python Zllhcc.py /store/user/lmastrol/VHcc_2016V4_Aug18/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/arizzi-RunIIMoriond17-DeepAndR94/180806_234029/0000/tree_105.root TT_TuneCUETP8M2T4_13TeV-powheg-pythia8 v10
