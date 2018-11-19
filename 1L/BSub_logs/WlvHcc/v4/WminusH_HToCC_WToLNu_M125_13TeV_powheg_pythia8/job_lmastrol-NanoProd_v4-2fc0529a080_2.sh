#!/bin/sh
source /afs/cern.ch/cms/cmsset_default.sh
cd /afs/cern.ch/work/j/jblee/private/Hcc/CMSSW_10_2_0_pre5/src/VHcc/1L
eval `scramv1 runtime -sh`
export X509_USER_PROXY=/afs/cern.ch/user/j/jblee/x509up_u37238
python Wlvhcc.py /store/user/lmastrol/VHcc_2016V4_Aug18/WminusH_HToCC_WToLNu_M125_13TeV_powheg_pythia8/lmastrol-NanoProd_v4-2fc0529a080/180802_104152/0000/tree_2.root WminusH_HToCC_WToLNu_M125_13TeV_powheg_pythia8 v4
