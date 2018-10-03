#!/bin/sh
source /afs/cern.ch/cms/cmsset_default.sh
cd /afs/cern.ch/work/j/jblee/private/Hcc/CMSSW_10_2_0_pre5/src/VHcc/2L
eval `scramv1 runtime -sh`
export X509_USER_PROXY=/afs/cern.ch/user/j/jblee/x509up_u37238
python Zllhcc.py /store/user/lmastrol/VHcc_2016V4_Aug18/ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/arizzi-RunIIMoriond17-DeepAndR99/180806_234234/0000/tree_3.root ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8 v10
