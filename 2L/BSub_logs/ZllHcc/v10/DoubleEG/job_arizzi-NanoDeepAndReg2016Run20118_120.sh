#!/bin/sh
source /afs/cern.ch/cms/cmsset_default.sh
cd /afs/cern.ch/work/j/jblee/private/Hcc/CMSSW_10_2_0_pre5/src/VHcc/2L
eval `scramv1 runtime -sh`
export X509_USER_PROXY=/afs/cern.ch/user/j/jblee/x509up_u37238
python Zllhcc.py /store/user/lmastrol/VHcc_2016V4_Aug18/DoubleEG/arizzi-NanoDeepAndReg2016Run20118/180817_115303/0000/tree_120.root DoubleEG v10
