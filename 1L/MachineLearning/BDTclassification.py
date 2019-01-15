#!/usr/bin/env python

# --------------------------------------------
# Standard python import
import os,sys  # exit
import time   # time accounting
import getopt # command line parser
import ROOT as r
import varsList

# --------------------------------------------
weightStrC = "CalibReaderRewgt*TrigEffWeight*pileupWeight*isoSF*lepIdSF*EGammaGsfSF*MuTrkSF*MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc)"
weightStrS = weightStrC+"*xsecEff"
weightStrB = weightStrC+"*xsecEff"
fold = 6
### fold = 2 uses 1/3 of sig + TTinclusive samples for training 
### fold = 3 uses 1/3 of sig + TTsemi/dilepton samples for training 
cutStrC = "(NJets_singleLepCalc >= 5 && NJetsCSV_singleLepCalc >= 2) && ((leptonPt_singleLepCalc > 35 && isElectron) || (leptonPt_singleLepCalc > 30 && isMuon)) && isTau_singleLepCalc==0"

cutStrS = cutStrC+" && ( isTraining == 1 || isTraining == 2 )"
cutStrB = cutStrC
if fold == 2:
    cutStrS = cutStrC+" && ( isTraining == 3 )"
if fold == 3:
    cutStrS = cutStrC+" && ( isTraining == 3 )"
if fold == 4:
    cutStrS = cutStrC+" && ( isTraining == 3 )"
    cutStrB = cutStrC+" && ( isTraining == 3 )"
if fold == 5:
    cutStrS = cutStrC+" && ( isTraining == 1 || isTraining == 2 )"
    cutStrB = cutStrC+" && ( isTraining == 1 || isTraining == 2 )"
if fold == 6:
    cutStrS = cutStrC+" && ( isTraining == 1 )"


# Default settings for command line arguments
DEFAULT_OUTFNAME = "weights/TMVA.root"
DEFAULT_INFNAME  = "180"
DEFAULT_TREESIG  = "TreeS"
DEFAULT_TREEBKG  = "TreeB"
DEFAULT_METHODS  = "Cuts,CutsD,CutsPCA,CutsGA,CutsSA,Likelihood,LikelihoodD,LikelihoodPCA,LikelihoodKDE,LikelihoodMIX,PDERS,PDERSD,PDERSPCA,PDEFoam,PDEFoamBoost,KNN,LD,Fisher,FisherG,BoostedFisher,HMatrix,FDA_GA,FDA_SA,FDA_MC,FDA_MT,FDA_GAMT,FDA_MCMT,MLP,MLPBFGS,MLPBNN,CFMlpANN,TMlpANN,SVM,BDT,BDTD,BDTG,BDTB,BDTF,RuleFit"
DEFAULT_NTREES   = "400"
DEFAULT_MDEPTH   = "2"#str(len(varList))
DEFAULT_MASS     = "180"
DEFAULT_VARLISTKEY = "Brown"
def usage():
    print " "
    print "Usage: python %s [options]" % sys.argv[0]
    print "  -m | --methods    : gives methods to be run (default: all methods)"
    print "  -i | --inputfile  : name of input ROOT file (default: '%s')" % DEFAULT_INFNAME
    print "  -o | --outputfile : name of output ROOT file containing results (default: '%s')" % DEFAULT_OUTFNAME
    print "  -n | --nTrees : amount of trees for BDT study (default: '%s')" %DEFAULT_NTREES 
    print "  -d | --maxDepth : maximum depth for BDT study (default: '%s')" %DEFAULT_MDEPTH 
    print "  -k | --mass : mass of the signal (default: '%s')" %DEFAULT_MASS 
    print "  -l | --varListKey : BDT input variable list (default: '%s')" %DEFAULT_VARLISTKEY 
    print "  -t | --inputtrees : input ROOT Trees for signal and background (default: '%s %s')" \
          % (DEFAULT_TREESIG, DEFAULT_TREEBKG)
    print "  -v | --verbose"
    print "  -? | --usage      : print this help message"
    print "  -h | --help       : print this help message"
    print " "

# Main routine
def main():

    try:
        # retrive command line options
        shortopts  = "m:i:n:d:k:l:t:o:vh?"
        longopts   = ["methods=", "inputfile=", "nTrees=", "maxDepth=", "mass=", "varListKey=", "inputtrees=", "outputfile=", "verbose", "help", "usage"]
        opts, args = getopt.getopt( sys.argv[1:], shortopts, longopts )

    except getopt.GetoptError:
        # print help information and exit:
        print "ERROR: unknown options in argument %s" % sys.argv[1:]
        usage()
        sys.exit(1)

    infname     = DEFAULT_INFNAME
    treeNameSig = DEFAULT_TREESIG
    treeNameBkg = DEFAULT_TREEBKG
    outfname    = DEFAULT_OUTFNAME
    methods     = DEFAULT_METHODS
    nTrees      = DEFAULT_NTREES
    mDepth      = DEFAULT_MDEPTH
    mass        = DEFAULT_MASS
    varListKey  = DEFAULT_VARLISTKEY
    verbose     = True
    for o, a in opts:
        if o in ("-?", "-h", "--help", "--usage"):
            usage()
            sys.exit(0)
        elif o in ("-m", "--methods"):
            methods = a
        elif o in ("-d", "--maxDepth"):
        	mDepth = a
        elif o in ("-k", "--mass"):
        	mass = a
        elif o in ("-l", "--varListKey"):
        	varListKey = a
        elif o in ("-i", "--inputfile"):
            infname = a
        elif o in ("-n", "--nTrees"):
            nTrees = a
        elif o in ("-o", "--outputfile"):
            outfname = a
        elif o in ("-t", "--inputtrees"):
            a.strip()
            trees = a.rsplit( ' ' )
            trees.sort()
            trees.reverse()
            if len(trees)-trees.count('') != 2:
                print "ERROR: need to give two trees (each one for signal and background)"
                print trees
                sys.exit(1)
            treeNameSig = trees[0]
            treeNameBkg = trees[1]
        elif o in ("-v", "--verbose"):
            verbose = True

    varList = varsList.varList[varListKey]
    nVars = str(len(varList))+'vars'
    Note='Fold'+str(fold)+'_'+methods+'_'+varListKey+'_'+nVars+'_mDepth'+mDepth+'_M'+mass
    outfname = "weights/TMVA_"+Note+".root"
    # Print methods
    mlist = methods.replace(' ',',').split(',')
    print "=== TMVAClassification: use method(s)..."
    for m in mlist:
        if m.strip() != '':
            print "=== - <%s>" % m.strip()
			
    # Import ROOT classes
    from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut
    
    # check ROOT version, give alarm if 5.18 
    if gROOT.GetVersionCode() >= 332288 and gROOT.GetVersionCode() < 332544:
        print "*** You are running ROOT version 5.18, which has problems in PyROOT such that TMVA"
        print "*** does not run properly (function calls with enums in the argument are ignored)."
        print "*** Solution: either use CINT or a C++ compiled version (see TMVA/macros or TMVA/examples),"
        print "*** or use another ROOT version (e.g., ROOT 5.19)."
        sys.exit(1)
    
    from ROOT import TMVA

    # Output file
    outputFile = TFile( outfname, 'RECREATE' )
    
    factory = TMVA.Factory( "TMVAClassification", outputFile, 
                            "!V:!Silent:Color:DrawProgressBar:Transformations=I;:AnalysisType=Classification" )

    # Set verbosity
    factory.SetVerbose( verbose )
    (TMVA.gConfig().GetIONames()).fWeightFileDir = "weights/"+Note

    # Define the input variables that shall be used for the classifier training
    # note that you may also use variable expressions, such as: "3*var1/var2*abs(var3)"
    # [all types of expressions that can also be parsed by TTree::Draw( "expression" )]

    for iVar in varList:
        if iVar[0]=='NJets_singleLepCalc': factory.AddVariable(iVar[0],iVar[1],iVar[2],'I')
        else: factory.AddVariable(iVar[0],iVar[1],iVar[2],'F')

    inputDir = varsList.inputDir
    print 'mass point '+mass
    infname = "ChargedHiggs_HplusTB_HplusToTB_M-%s_13TeV_amcatnlo_pythia8_hadd.root" %(mass)
    iFileSig = TFile.Open(inputDir+infname)
    sigChain = iFileSig.Get("ljmet")

    factory.AddSignalTree(sigChain)
    bkg_list = []
    bkg_trees_list = []
    hist_list = []
    weightsList = []
    bkgList = varsList.bkg
    if fold == 2 or fold == 4 or fold == 5:
        bkgList = varsList.bkgTTInc
    if fold == 3 or fold == 6:
        bkgList = varsList.bkg
    
    for i in range(len(bkgList)):
        bkg_list.append(TFile.Open(inputDir+bkgList[i]))
        print inputDir+bkgList[i]
        bkg_trees_list.append(bkg_list[i].Get("ljmet"))
        bkg_trees_list[i].GetEntry(0)

        if bkg_trees_list[i].GetEntries() == 0:
            continue
        factory.AddBackgroundTree( bkg_trees_list[i], 1)

    signalWeight = 1 #0.0159/sigChain.GetEntries() #xs (pb)  
    factory.SetSignalWeightExpression( weightStrS )
    factory.SetBackgroundWeightExpression( weightStrB )

    mycutSig = TCut( cutStrS )
    mycutBkg = TCut( cutStrB ) 

    factory.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
                                        "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

    # --------------------------------------------------------------------------------------------------

    # ---- Book MVA methods
# bdtSetting for "BDT" 
    bdtSetting = '!H:!V:NTrees=%s:MaxDepth=%s' %(nTrees,mDepth)
    bdtSetting += ':MinNodeSize=2.5%:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20'
    bdtSetting += ':IgnoreNegWeightsInTraining=True'
# bdtSetting for "BDTMitFisher" 
    bdtFSetting = '!H:!V:NTrees=%s' %nTrees
    bdtFSetting += ':MinNodeSize=2.5%:UseFisherCuts:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:SeparationType=GiniIndex:nCuts=20'
    bdtFSetting += ':IgnoreNegWeightsInTraining=True'
# bdtSetting for "BDTG" 
    bdtGSetting = '!H:!V:NTrees=%s:MaxDepth=%s' %(nTrees,mDepth)
    bdtGSetting += ':MinNodeSize=2.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20'
    bdtGSetting += ':Pray' #Pray takes into account the effect of negative bins in BDTG
    #bdtGSetting += ':IgnoreNegWeightsInTraining=True'
# bdtSetting for "BDTB" 
    bdtBSetting = '!H:!V:NTrees=%s' %nTrees
    bdtBSetting += ':MinNodeSize=2.5%:BoostType=Bagging:SeparationType=GiniIndex:nCuts=20'
    bdtBSetting += ':IgnoreNegWeightsInTraining=True'
# bdtSetting for "BDTD" 
    bdtDSetting = '!H:!V:NTrees=%s' %nTrees
    bdtDSetting += ':MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=20:VarTransform=Decorrelate'
    bdtDSetting += ':IgnoreNegWeightsInTraining=True'



#BOOKING AN ALGORITHM
    if methods=="BDT": factory.BookMethod( TMVA.Types.kBDT, "BDT",bdtSetting)
    if methods=="BDTG": factory.BookMethod( TMVA.Types.kBDT, "BDTG",bdtGSetting)
    if methods=="BDTMitFisher": factory.BookMethod( TMVA.Types.kBDT, "BDTMitFisher",bdtFSetting)
    if methods=="BDTB": factory.BookMethod( TMVA.Types.kBDT, "BDTB",bdtBSetting)
    if methods=="BDTD": factory.BookMethod( TMVA.Types.kBDT, "BDTD",bdtDSetting)
    # --------------------------------------------------------------------------------------------------
            
    # ---- Now you can tell the factory to train, test, and evaluate the MVAs. 

    # Train MVAs
    factory.TrainAllMethods()

    # Test MVAs
    factory.TestAllMethods()
    
    # Evaluate MVAs
    factory.EvaluateAllMethods()    

    # Save the output.
    outputFile.Close()
    
    # save plots:
    os.chdir('weights/'+Note)
    gROOT.SetBatch(1)
    TMVA.efficiencies( "../../"+outfname ) #Classifier Background Rejection vs Signal Efficiency (ROC curve)
    TMVA.mvas( "../../"+outfname, 0 ) #Classifier Output Distributions (test sample)
    TMVA.correlations( "../../"+outfname ) #Input Variable Linear Correlation Coefficients
    TMVA.variables( "../../"+outfname ) #Input variables (training sample)
    if not gROOT.IsBatch(): TMVA.TMVAGui( "../../"+outfname )
    print "DONE"

# ----------------------------------------------------------

if __name__ == "__main__":
    main()
