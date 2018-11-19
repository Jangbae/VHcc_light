import os, sys, glob


print "Check voms-proxy-init -voms cms"
os.system("cp /tmp/x509up_u37238 /afs/cern.ch/user/j/jblee/")

sampleList_WlvHcc = [
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
sample_List = sampleList_WlvHcc
dir_sampleList = 'sampleList_WlvHcc'
script = 'Wlvhcc.py'
dic_sample = {}
runDir=os.getcwd()
queue = '8nh'
version = 'v4'

if not os.path.exists(dir_sampleList): os.system('mkdir '+dir_sampleList)
if not os.path.exists("BSub_logs/"): os.system('mkdir '+"BSub_logs/")
if not os.path.exists("BSub_logs/"+nlepton): os.system('mkdir '+"BSub_logs/"+nlepton)
if not os.path.exists(runDir+"/condorJDF"): os.system('mkdir '+runDir+"/condorJDF")

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
            num_lines_1 = sum(1 for line in f2)
            f2.seek(0)
            if num_lines_1 == 1:
                dic_sample[s] = []
                for x, y in zip(f1, f2):
                    path = x.strip()+"/"+y.strip()+"/0000/"
                    os.system("gfal-ls srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/lmastrol/VHcc_2016V4_Aug18/"+s+"/"+path+"/ > "+dir_sampleList+"/Samples_"+str(s)+"_2.txt" )
                    os.system("rm "+dir_sampleList+"/Samples_"+str(s)+"_fPath.txt")
                    for f in open(dir_sampleList+"/Samples_"+str(s)+"_2.txt"):
                        if ".root" in f:
                            fullpath = "/store/user/lmastrol/VHcc_2016V4_Aug18/"+s+"/"+path+f[:-1]
                            os.system("echo srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2"+fullpath+" >>"+dir_sampleList+"/Samples_"+str(s)+"_fPath.txt")
                            dic_sample[s].append(fullpath)
            elif num_lines_1 > 1:
                x_f1 = f1.readline().strip()
                inx = 0
                os.system("rm "+dir_sampleList+"/Samples_"+str(s)+"_fPath.txt")
                dic_sample[s] = []
                for y in open(dir_sampleList+"/Samples_"+str(s)+"_1.txt"):
                    inx+=1
                    path = x_f1+"/"+y.strip()+"/0000/"
                    os.system("gfal-ls srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2/store/user/lmastrol/VHcc_2016V4_Aug18/"+s+"/"+path+"/ > "+dir_sampleList+"/Samples_"+str(s)+"_2_"+str(inx)+".txt" )
                    for f in open(dir_sampleList+"/Samples_"+str(s)+"_2_"+str(inx)+".txt"):
                        if ".root" in f:
                            fullpath = "/store/user/lmastrol/VHcc_2016V4_Aug18/"+s+"/"+path+f[:-1]
                            os.system("echo srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/pnfs/desy.de/cms/tier2"+fullpath+" >>"+dir_sampleList+"/Samples_"+str(s)+"_fPath.txt")
                            dic_sample[s].append(fullpath)

total = 0
os.system("cp "+script+" 1_doBSubmit.py "+runDir+"/BSub_logs/"+nlepton+"/"+version+"/")
os.system("cp "+dir_sampleList+"/Samples_*.txt "+runDir+"/BSub_logs/"+nlepton+"/"+version+"/")


for d in sorted(dic_sample):
    print d
    count = 0

    fileList=dic_sample[d]
    channel = d

    if not os.path.exists("BSub_logs/"+nlepton+"/"+version): os.system('mkdir '+"BSub_logs/"+nlepton+"/"+version)
    if not os.path.exists("BSub_logs/"+nlepton+"/"+version+"/"+channel): os.system('mkdir '+"BSub_logs/"+nlepton+"/"+version+"/"+channel)    
    if not os.path.exists("/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version): os.system('mkdir '+"/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version)
    if not os.path.exists("/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"/"+channel): os.system('mkdir '+"/eos/cms/store/user/jblee/Hcc/"+nlepton+"/"+version+"/"+channel)
    
    for file in fileList:
        print file
        log = file.split('/0000/')[1].split('.root')[0]        
        number = log.split('_')[1]        
        temp = file.split(d+'/')[1].split("/0000/")[0]
        label = temp.split('/')[0]+"_"+number
        count+=1    
        total+=1
        jdfName = 'condorJob_'+label+'.job'
        jdf=open(runDir+'/condorJDF/'+jdfName,'w')
        dict={'RUNDIR':runDir,'FILENAME':file, 'JDF':jdfName,'log':log}

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