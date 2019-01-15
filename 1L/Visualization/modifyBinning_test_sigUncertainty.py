#!/usr/bin/python

import matplotlib.pyplot as plt
import os,sys,time,math,fnmatch
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from array import array
from weights import *
from modSyst import *
from utils import *
from ROOT import *
start_time = time.time()

gROOT.SetBatch(1)
iPlot='HTpBDT'
if len(sys.argv)>1: iPlot=str(sys.argv[1])
massPt='300'
if len(sys.argv)>2: massPt=str(sys.argv[2])

templateDir = '/user_data/jlee/chargedHiggs/Combine/CMSSW_8_1_0/src/ChargedHiggsCombindCards_Condor/templates/BDT_v77_noQCD_stat0p15_FinalNNBBCRCount_SigbkgBasedBin_2017-07-27_HTpBDT/'

print templateDir


outDir = templateDir#os.getcwd()+'/templates_BDTGfullTT_Comb_28vars_M'+massPt+'_2017_3_14/'
combinefile = 'templates_'+iPlot+'M'+massPt+'_35p867fb_countingCR_sigbkgBased.root'
lumiStr = '35p867fb'
sigName = 'Hptb'
era = "13TeV"
xbinsListTemp = {}
signalHists = {}


def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

rfiles = []         
for file in findfiles(templateDir, '*HTpBDTM'+massPt+'_'+'*.root'):
	if 'allSig' in file : continue
	rfiles.append(file)
tfile = TFile(rfiles[0])

dataName = 'data_obs'
sighists = [k.GetName() for k in tfile.GetListOfKeys() if '__Hptb'+massPt in k.GetName() and not 'Up' in k.GetName() and not 'Down' in k.GetName()]
print sighists
channels = [hist[hist.find('fb_')+3:hist.find('__')] for hist in sighists if 'isL_' not in hist]

for hist in sighists:
	channel = hist[hist.find('fb_')+3:hist.find('__')]
	signalHists[channel]=tfile.Get(hist.replace('__'+dataName,'__Hptb')).Clone()

el_ratio = {}
mu_ratio = {}
el_total = []
mu_total = []

for chn in signalHists.keys():
	if 'isE' not in chn: continue
	if 'isCR' in chn: continue
	print "==="*30
	print "==="*30
	print chn
	print signalHists[chn]
	xbinsListTemp[chn]=[signalHists[chn].GetXaxis().GetBinUpEdge(signalHists[chn].GetXaxis().GetNbins())]
	Nbins = signalHists[chn].GetNbinsX()
	print Nbins
	bin_List=[]
	binErr_List=[]
	binCon_List=[]
	binXbi_List=[]
	binReErr_List=[]
	for iBin in range(1,Nbins+1):
		totTempBinContent = 0.
		totTempBinErrSquared = 0.
		totTempBinContent = signalHists[chn].GetBinContent(iBin)
		totTempBinErrSquared = signalHists[chn].GetBinError(iBin)**2
		try:
			if math.sqrt(totTempBinErrSquared)/totTempBinContent>0.9:
				print "################################################### bin to check : ", iBin
				bin_List.append(iBin)
			el_total.append(math.sqrt(totTempBinErrSquared)/totTempBinContent)
		except:
			el_total.append(0)
			print "totTempBinContent : ", totTempBinContent
	for iB in range(1,Nbins+1):
		try:
			binReErr_List.append(signalHists[chn].GetBinError(iB)/signalHists[chn].GetBinContent(iB))
		except:
			binReErr_List.append(0)
		binErr_List.append(signalHists[chn].GetBinError(iB))
		binCon_List.append(signalHists[chn].GetBinContent(iB))
		binXbi_List.append(signalHists[chn].GetXaxis().GetBinCenter(iB))
	plt.figure()
	plt.xlim(-1,1)
	plt.grid(which='both',linestyle=':',color='gray', linewidth=1)
	plt.errorbar(binXbi_List,binCon_List, yerr=binErr_List,ls = "None",marker=".")
	for ibin, iReError in enumerate(binReErr_List):
		if iReError>0.2:
			plt.scatter(binXbi_List[ibin],binCon_List[ibin], marker=".", s=180,color='r')
	plt.title('M'+massPt+'__'+chn)
	plt.text(-0.99,max(binCon_List)*0.999999,'Reds : Relative Stat. Uncertainty > 20%')
	plt.xlabel('BDT discriminant')
	plt.savefig(chn+'_BinningSig_'+massPt+'.png', bbox_inches="tight")
	plt.close()
	
for chn in signalHists.keys():
	if 'isM' not in chn: continue
	if 'isCR' in chn: continue
	print "==="*30
	print "==="*30
	print chn
	print signalHists[chn]
	xbinsListTemp[chn]=[signalHists[chn].GetXaxis().GetBinUpEdge(signalHists[chn].GetXaxis().GetNbins())]
	Nbins = signalHists[chn].GetNbinsX()
	print Nbins
	mu_ratio[chn] = []
	bin_List=[]
	binErr_List=[]
	binCon_List=[]
	binXbi_List=[]
	binReErr_List=[]
	for iBin in range(1,Nbins+1):
		totTempBinContent = 0.
		totTempBinErrSquared = 0.
		totTempBinContent = signalHists[chn].GetBinContent(iBin)
		totTempBinErrSquared = signalHists[chn].GetBinError(iBin)**2
		try:
			if math.sqrt(totTempBinErrSquared)/totTempBinContent>0.9:
				print "################################################### bin to check : ", iBin
				bin_List.append(iBin)
			mu_total.append(math.sqrt(totTempBinErrSquared)/totTempBinContent)
		except:
			mu_total.append(0)
			print "totTempBinContent : ",totTempBinContent
	for iB in range(1,Nbins+1):
		try:
			binReErr_List.append(signalHists[chn].GetBinError(iB)/signalHists[chn].GetBinContent(iB))
		except:
			binReErr_List.append(0)
		binErr_List.append(signalHists[chn].GetBinError(iB))
		binCon_List.append(signalHists[chn].GetBinContent(iB))
		binXbi_List.append(signalHists[chn].GetXaxis().GetBinCenter(iB))
	plt.figure()
	plt.xlim(-1,1)
	plt.grid(which='both',linestyle=':',color='gray', linewidth=1)
	plt.errorbar(binXbi_List,binCon_List, yerr=binErr_List,ls = "None",marker=".")	

	for ibin, iReError in enumerate(binReErr_List):
		if iReError>0.2:
			plt.scatter(binXbi_List[ibin],binCon_List[ibin], marker=".",s=180, color='r')
	plt.title('M'+massPt+'__'+chn)
	plt.text(-0.99,max(binCon_List)*0.999999,'Reds : Relative Stat. Uncertainty > 20%')
	plt.xlabel('BDT discriminant')
	plt.savefig(chn+'_BinningSig_'+massPt+'.png', bbox_inches="tight")
	plt.close()

y, x, _ = plt.hist(el_total, bins=50, color='blue')
plt.axis([0,max(el_total)*1.3,0,y.max()*1.3])
plt.locator_params(axis='y', nbins=10)
plt.locator_params(axis='x', nbins=20)
plt.grid(which='both',linestyle=':',color='blue', linewidth=1)
plt.title(massPt+' El total number of bins : '+str(len(el_total)))
plt.xlabel('Relative statistical uncertainty')
plt.savefig("el_ratio_PosSigOnly_total_M"+massPt+".png", bbox_inches="tight")
plt.close()

y, x, _ = plt.hist(mu_total, bins=50, color='blue')
plt.axis([0,max(mu_total)*1.3,0,y.max()*1.3])
plt.locator_params(axis='y', nbins=10)
plt.locator_params(axis='x', nbins=20)
plt.grid(which='both',linestyle=':',color='blue', linewidth=1)
plt.title(massPt+' Mu total number of bins : '+str(len(mu_total)))
plt.xlabel('Relative statistical uncertainty')
plt.savefig("mu_ratio_PosSigOnly_total_M"+massPt+".png", bbox_inches="tight")
plt.close()


totBkgHists = {}
bkgProcList = ['ttlf','ttcc','ttb','top','ewk','qcd'] #put the most dominant process first
for hist in sighists:
	if 'isCR' in hist: continue
	channel = hist[hist.find('fb_')+3:hist.find('__')]
	totBkgHists[channel]=tfile.Get(hist.replace('__Hptb'+massPt,'__'+bkgProcList[0])).Clone()
	print "bkg N bins : ",totBkgHists[channel].GetNbinsX()
	for proc in bkgProcList:
		if proc==bkgProcList[0] or proc=='qcd': continue #EXCLUDING QCD FROM STAT THRESHOLD CHECK!!!
		try: totBkgHists[channel].Add(tfile.Get(hist.replace('__Hptb'+massPt,'__'+proc)))
		except: 
			print "Missing",proc,"for category:",hist
			pass
bkgUncer_List = []
xbinsListTemp = {}
for chn in totBkgHists.keys():
	if 'isCR' in chn: continue
	xbinsListTemp[chn]=[totBkgHists[chn].GetXaxis().GetBinUpEdge(totBkgHists[chn].GetXaxis().GetNbins())]
	Nbins = totBkgHists[chn].GetNbinsX()
	print "Nbins : ",Nbins
	totTempBinContent_E = 0.
	totTempBinErrSquared_E = 0.
	nBinsMerged = 0
	for iBin in range(1,Nbins+1):
		totTempBinContent_E = totBkgHists[chn].GetBinContent(Nbins+1-iBin)
		totTempBinErrSquared_E = totBkgHists[chn].GetBinError(Nbins+1-iBin)**2
		try:
			bkgUncer_List.append(math.sqrt(totTempBinErrSquared_E)/totTempBinContent_E)
		except:
			bkgUncer_List.append(0)

y, x, _ = plt.hist(bkgUncer_List, bins=50, color='blue')
plt.axis([0,max(bkgUncer_List)*1.3,0,y.max()*1.3])
plt.locator_params(axis='y', nbins=10)
plt.locator_params(axis='x', nbins=20)
plt.grid(which='both',linestyle=':',color='blue', linewidth=1)
plt.title(massPt+'e/m total number of bins : '+str(len(bkgUncer_List)))
plt.xlabel('Relative statistical uncertainty')
plt.savefig("e_m_uncertainty_bkg_in_sigBinning_total_M"+massPt+".png", bbox_inches="tight")
plt.close()




print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))