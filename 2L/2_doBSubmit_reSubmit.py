import os, sys, glob


print "Did you do 'voms-proxy-init -voms cms' ?"
os.system("cp /tmp/x509up_u37238 /afs/cern.ch/user/j/jblee/")

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
'DoubleMuon',

'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8',
'WW_TuneCUETP8M1_13TeV-pythia8',
'WZ_TuneCUETP8M1_13TeV-pythia8',
'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8',
'ZH_HToCC_ZToLL_M125_13TeV_powheg_pythia8',
'ZZ_TuneCUETP8M1_13TeV-pythia8',

]
os.system("cp /tmp/x509up_u37238 /afs/cern.ch/user/j/jblee/")
runDir=os.getcwd()
queue = '8nh'
version = 'v10'
nlepton = 'ZllHcc'

for s in sampleList:
    print s
    fileList = glob.glob("BSub_logs/"+nlepton+"/"+version+"/"+s+"/*.log")
    Nevent = 0
    for f in fileList:
        bashScript = ' '
        content = open(f).read()
        contentl = open(f).readlines()
        index = [x for x in range(len(contentl)) if 'CERN statistics' in contentl[x]]
        if len(index)>1:
            startLine = index[-2]
            Error = False
            for LN in range(startLine, len(contentl)):
                if "Error" in contentl[LN]:
                    Error = True
                if "Job <" in contentl[LN]:
                    bashScript = contentl[LN].split(s+"/")[1].split("> was submitted")[0]
                if "Total event processed" in contentl[LN]:
                    Nevent+=int(contentl[LN].split(" :")[1][:-1].split("  ")[1])
            if Error:
                print "Resubmit ", f.split("logs_")[0]+bashScript 
                label=bashScript[:-3].split('job_')[1]
#                 os.system("rm /eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"/"+s+"/tree_"+label+".root")
#                 os.system("bsub -q "+queue+" -o "+runDir+"/"+f+" "+runDir+"/"+f.split("logs_")[0]+bashScript )
        else:
            for LN in range(0, len(contentl)):
                if "Job <" in contentl[LN]:
                    bashScript = contentl[LN].split(s+"/")[1].split("> was submitted")[0]
                if "Total event processed" in contentl[LN]:
                    Nevent+=int(contentl[LN].split(" :")[1][:-1].split("  ")[1])
            if "Error" in content:
                number = f.split("logs_")[1][:-4]
                print "Resubmit ", f.split("logs_")[0]+bashScript
                label=bashScript[:-3].split('job_')[1]                
#                 os.system("rm /eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"/"+s+"/tree_"+label+".root")
#                 os.system("bsub -q "+queue+" -o "+runDir+"/"+f+" "+runDir+"/"+f.split("logs_")[0]+bashScript )
    print int(Nevent)
# sys.exit()
##### Check if there is missing log #####
sampleListDir = 'sampleList_ZllHcc'    
print "################## Check if there is missing log ######################"
for s in sampleList:
    logList = []
    sampleL = []
    print s
    fileList = glob.glob("BSub_logs/"+nlepton+"/"+version+"/"+s+"/*.log")
    for log in fileList:
        logList.append(int(log.split('_')[-1].split('.log')[0]))
    pathInput = glob.glob(sampleListDir+"/Samples_"+s+"_fPath*.txt")
    for sample in pathInput:
        for line in open(sample).readlines(): 
            sampleL.append(int(line.split("tree_")[-1].split('.root')[0]))
    missingLog = list(set(sampleL)-set(logList))
    toResubmit = []
    
    for missing in missingLog:
        toResubmit.append(glob.glob("BSub_logs/"+nlepton+"/"+version+"/"+s+"/*_"+str(missing)+".sh"))
    toResubmit = sum(toResubmit, [])
    for resub in toResubmit:
        print "Missing log for ", resub
        print "resumbitting"
#         print "bsub -q "+queue+" -o "+runDir+"/"+resub.replace('sh','log').replace('job','logs')+" "+runDir+"/"+resub
#         os.system("bsub -q "+queue+" -o "+runDir+"/"+resub.replace('sh','log').replace('job','logs')+" "+runDir+"/"+resub)
##### Check if there is missing output while the log exits #####    
print "################### Check if there is missing output while the log exits ###############"
for s in sampleList:
    logList = []
    ntupleL = []
    print s
    ntupleList = glob.glob("/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"/"+s+"/*.root")
    fileList = glob.glob("BSub_logs/"+nlepton+"/"+version+"/"+s+"/*.log")
    for ntuple in ntupleList:
#         print ntuple
        temp = ntuple.split('arizzi-')[-1]
        num = temp.split('.root')[0]
        ntupleL.append(num)
    for log in fileList:
        logList.append(log.split('arizzi-')[-1].split('.log')[0])
    missingNtuple = list(set(logList)-set(ntupleL))
    toResubmit = []
    for missing in missingNtuple:
        toResubmit.append(glob.glob("BSub_logs/"+nlepton+"/"+version+"/"+s+"/*"+missing+".sh"))
    toResubmit = sum(toResubmit, [])
    for resub in toResubmit:
        print "missing Ntuple : ", resub
        print "resumbitting"
        print "bsub -q "+queue+" -o "+runDir+"/"+resub.replace('sh','log').replace('job','logs')+" "+runDir+"/"+resub
#         os.system("bsub -q "+queue+" -o "+runDir+"/"+resub.replace('sh','log').replace('job','logs')+" "+runDir+"/"+resub)    
sys.exit()    