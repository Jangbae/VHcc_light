import os, sys, glob
print "Check voms-proxy-init -voms cms"
os.system("cp /tmp/x509up_u37238 /afs/cern.ch/user/j/jblee/")


sampleList_ZllHcc = [
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

nlepton = 'ZllHcc'
sample_List = sampleList_ZllHcc
dir_sampleList = 'sampleList_ZllHcc'
script = 'Zllhcc.py'

dic_sample = {}
runDir=os.getcwd()
queue = '8nh'
version = 'v10'

if not os.path.exists(dir_sampleList): os.system('mkdir '+dir_sampleList)
if not os.path.exists("BSub_logs/"): os.system('mkdir '+"BSub_logs/")

for s in sample_List:
    os.system("rm "+dir_sampleList+"/Samples_"+str(s)+"_0.txt")
    os.system("gfal-ls srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/lmastrol/VHcc_2016V4_Aug18/"+s+"/ > "+dir_sampleList+"/Samples_"+str(s)+"_0.txt")
    os.system("rm "+dir_sampleList+"/Samples_"+str(s)+"_1.txt")
    print s
    list_0 = open(dir_sampleList+"/Samples_"+str(s)+"_0.txt")
    num_lines = sum(1 for line in list_0)
    i = 0
    dic_sample[s] = []
    for ff in open(dir_sampleList+"/Samples_"+str(s)+"_0.txt"):
        i+=1
        num = str(i)
        if num_lines>1:
            os.system("rm "+dir_sampleList+"/Samples_"+str(s)+"_1_"+num+".txt")
            os.system("gfal-ls srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/lmastrol/VHcc_2016V4_Aug18/"+s+"/"+ff[:-1]+" >> "+dir_sampleList+"/Samples_"+str(s)+"_1_"+num+".txt")
            f2 = open(dir_sampleList+"/Samples_"+str(s)+"_1_"+num+".txt")
            for y in f2:
                path = ff.strip()+"/"+y.strip()+"/0000/"
                os.system("gfal-ls srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/lmastrol/VHcc_2016V4_Aug18/"+s+"/"+path+"/ > "+dir_sampleList+"/Samples_"+str(s)+"_2_"+num+".txt" )

                os.system("rm "+dir_sampleList+"/Samples_"+str(s)+"_fPath_"+num+".txt")
                for f in open(dir_sampleList+"/Samples_"+str(s)+"_2_"+num+".txt"):
                    if ".root" in f:
                        fullpath = "/store/user/lmastrol/VHcc_2016V4_Aug18/"+s+"/"+path+f[:-1]
                        os.system("echo srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2"+fullpath+" >>"+dir_sampleList+"/Samples_"+str(s)+"_fPath_"+num+".txt")
                        dic_sample[s].append(fullpath)


        else:
            os.system("gfal-ls srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/lmastrol/VHcc_2016V4_Aug18/"+s+"/"+ff[:-1]+" >> "+dir_sampleList+"/Samples_"+str(s)+"_1.txt")
            f1 = open(dir_sampleList+"/Samples_"+str(s)+"_0.txt")
            f2 = open(dir_sampleList+"/Samples_"+str(s)+"_1.txt")
            for x, y in zip(f1, f2):
                path = x.strip()+"/"+y.strip()+"/0000/"
                os.system("gfal-ls srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/lmastrol/VHcc_2016V4_Aug18/"+s+"/"+path+"/ > "+dir_sampleList+"/Samples_"+str(s)+"_2.txt" )
                dic_sample[s] = []
                os.system("rm "+dir_sampleList+"/Samples_"+str(s)+"_fPath.txt")
                for f in open(dir_sampleList+"/Samples_"+str(s)+"_2.txt"):
                    if ".root" in f:
                        fullpath = "/store/user/lmastrol/VHcc_2016V4_Aug18/"+s+"/"+path+f[:-1]
                        os.system("echo srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2"+fullpath+" >>"+dir_sampleList+"/Samples_"+str(s)+"_fPath_1.txt")
                        dic_sample[s].append(fullpath)

# sys.exit()
total = 0
os.system("cp "+script+" doBSubSubmit.py "+runDir+"/BSub_logs/"+nlepton+"/"+version+"/")
os.system("cp "+dir_sampleList+"/Samples_*.txt "+runDir+"/BSub_logs/"+nlepton+"/"+version+"/")
if not os.path.exists("BSub_logs/"+nlepton): os.system('mkdir '+"BSub_logs/"+nlepton)
if not os.path.exists("BSub_logs/"+nlepton+"/"+version): os.system('mkdir '+"BSub_logs/"+nlepton+"/"+version)
if not os.path.exists("/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version): os.system('mkdir '+"/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version)

for d in sorted(dic_sample):
    print d
    count = 0
    fileList=dic_sample[d]
    channel = d
    if not os.path.exists("BSub_logs/"+nlepton+"/"+version+"/"+channel): os.system('mkdir '+"BSub_logs/"+nlepton+"/"+version+"/"+channel)
    if not os.path.exists("/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"/"+channel): os.system('mkdir '+"/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"/"+channel)
    
    for file in fileList:
        print file
        log = file.split('/0000/')[1].split('.root')[0]        
        number = log.split('_')[1]        
        temp = file.split(d+'/')[1].split("/0000/")[0]
        label = temp.split('/')[0]+"_"+number
        count+=1    
        total+=1
        dict={'RUNDIR':runDir,'FILENAME':file,'log':log}

        with open('BSub_logs/'+nlepton+'/'+version+'/'+channel+'/job_'+label+'.sh', 'w') as fout:
            fout.write("#!/bin/sh\n")
            fout.write("source /afs/cern.ch/cms/cmsset_default.sh\n")
            fout.write("cd "+runDir+"\n")
            fout.write("eval `scramv1 runtime -sh`\n")
            fout.write("export X509_USER_PROXY=/afs/cern.ch/user/j/jblee/x509up_u37238\n")
            fout.write("python "+script+" "+file+" "+d+" "+version+"\n")
        os.system("chmod 755 BSub_logs/"+nlepton+"/"+version+"/"+channel+"/job_"+label+".sh")
        os.system("bsub -q "+queue+" -o "+runDir+"/BSub_logs/"+nlepton+"/"+version+"/"+channel+"/logs_"+label+".log "+runDir+"/BSub_logs/"+nlepton+"/"+version+"/"+channel+"/job_"+label+".sh")
    print count, "jobs submitted!!!"
print total, "jobs in total submitted!!!"