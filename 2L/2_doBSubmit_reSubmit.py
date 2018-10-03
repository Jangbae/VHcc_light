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
'WZ_TuneCUETP8M1_13TeV-pythia8',
# 'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8',
# 'ZH_HToCC_ZToLL_M125_13TeV_powheg_pythia8',
# 'ZZ_TuneCUETP8M1_13TeV-pythia8',
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
                if "Total events" in contentl[LN]:
                    Nevent+=int(contentl[LN].split(" :")[1][:-1].split("  ")[1])
            if Error:
                print "Resubmit ", f.split("logs_")[0]+bashScript 
                label=bashScript[:-3].split('job_')[1]
                os.system("rm /eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"/"+s+"/tree_"+label+".root")
                os.system("bsub -q "+queue+" -o "+runDir+"/"+f+" "+runDir+"/"+f.split("logs_")[0]+bashScript )
        else:
            for LN in range(0, len(contentl)):
                if "Job <" in contentl[LN]:
                    bashScript = contentl[LN].split(s+"/")[1].split("> was submitted")[0]
                if "Total events" in contentl[LN]:
                    Nevent+=int(contentl[LN].split(" :")[1][:-1].split("  ")[1])
            if "Error" in content:
                number = f.split("logs_")[1][:-4]
                print "Resubmit ", f.split("logs_")[0]+bashScript
                label=bashScript[:-3].split('job_')[1]                
                os.system("rm /eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"/"+s+"/tree_"+label+".root")
                os.system("bsub -q "+queue+" -o "+runDir+"/"+f+" "+runDir+"/"+f.split("logs_")[0]+bashScript )
    print int(Nevent)