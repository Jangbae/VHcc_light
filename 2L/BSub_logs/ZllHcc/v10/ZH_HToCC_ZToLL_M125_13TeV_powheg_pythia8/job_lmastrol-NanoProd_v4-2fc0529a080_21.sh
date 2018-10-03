#!/bin/sh
source /afs/cern.ch/cms/cmsset_default.sh
cd /afs/cern.ch/work/j/jblee/private/Hcc/CMSSW_10_2_0_pre5/src/VHcc/2L
eval `scramv1 runtime -sh`
export X509_USER_PROXY=/afs/cern.ch/user/j/jblee/x509up_u37238
python Zllhcc.py /store/user/lmastrol/VHcc_2016V4_Aug18/ZH_HToCC_ZToLL_M125_13TeV_powheg_pythia8/lmastrol-NanoProd_v4-2fc0529a080/180801_192320/0000/tree_21.root ZH_HToCC_ZToLL_M125_13TeV_powheg_pythia8 v10
