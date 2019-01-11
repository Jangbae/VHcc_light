import time, sys, glob
start_time = time.time()
import numpy as np
import pandas as pd
from root_numpy import root2array, rec2array, array2root

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam

import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler

default_branch_names = ["event","DPhi_VH", "W_Tmass", "top_Mass", "DR_cc", "lepDR_cc", "M_lep_c", "centrality", "avgCvsLpT", "FWmoment_1", "FWmoment_2", "FWmoment_3", "FWmoment_4"]

branch_names = ["DPhi_VH", "W_Tmass", "top_Mass", "DR_cc", "lepDR_cc", "M_lep_c", "centrality", "avgCvsLpT", "FWmoment_1", "FWmoment_2", "FWmoment_3", "FWmoment_4"]

file_Path = "/eos/cms/store/user/jblee/Hcc/WlvHcc/v2_Hadd/"
file_pSignal = "WplusH_HToCC_WToLNu_M125_13TeV_powheg_pythia8_hadd.root"
file_mSignal = "WminusH_HToCC_WToLNu_M125_13TeV_powheg_pythia8_hadd.root"
file_Bkgs = "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root"
# list_Bkgs = glob.glob(file_Path+"WJetsToLNu_HT-*_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root")

array_pSignal = root2array(file_Path+file_pSignal, "Events", default_branch_names)
rArray_pSignal = rec2array(array_pSignal)

array_mSignal = root2array(file_Path+file_mSignal, "Events", default_branch_names)
rArray_mSignal = rec2array(array_mSignal)

list_Bkgs = [file_Bkgs]
list_array = []
for bkg in list_Bkgs:
    array_tempBkg = root2array(file_Path+bkg, "Events", default_branch_names)
    rArray_tempBkg = rec2array(array_tempBkg)
    list_array.append(rArray_tempBkg)

    
rArray_Bkg = np.concatenate((list_array))
rArray_Signal = np.concatenate((rArray_pSignal, rArray_mSignal))


df_sig = pd.DataFrame(rArray_Signal, columns=default_branch_names)
df_bkg = pd.DataFrame(rArray_Bkg, columns=default_branch_names)

df_sig_temp = df_sig[df_sig.event%2==0]
df_bkg_temp = df_bkg[df_bkg.event%2==0]

array_sig = df_sig_temp.drop(columns=['event']).values
array_bkg = df_bkg_temp.drop(columns=['event']).values

print "rArray_Signal.shape"
print rArray_Signal.shape
print "array_sig.shape"
print array_sig.shape

print "rArray_Bkg.shape"
print rArray_Bkg.shape
print "array_bkg.shape"
print array_bkg.shape


X = np.concatenate((array_sig, array_bkg))
y = np.concatenate((np.ones(array_sig.shape[0]), np.zeros(array_bkg.shape[0])))

X_train,X_test, y_train,y_test = train_test_split(X, y, test_size=0.33, random_state=492)

######################################### KERAS ##########################################
model = Sequential()

model.add(
    (
        Dense(100, activation="relu" ,input_shape=(12,))
    )
)
model.add(Dropout(0.5)) 
model.add((Dense(100, activation="relu")))
model.add(Dropout(0.5)) 
model.add((Dense(100, activation="relu")))
model.add(Dropout(0.5)) 
model.add((Dense(100, activation="relu")))
model.add(Dropout(0.2)) 
model.add(
    (
        Dense(1, activation="sigmoid")
    )
)

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

##########################################################################################
preprocessing = StandardScaler()
preprocessing.fit(X_train)
X_train = preprocessing.transform(X_train)

print y_train.shape
# sys.exit()
model.fit(X_train, y_train, verbose=2, epochs=10, batch_size=4096,shuffle=True)



def data_generator(batch_size, xtrain, ytrain):    
    while True:
        inputs = xtrain
        labels = ytrain        
        yield inputs, labels

model.fit_generator(
    data_generator(4096, X_train, y_train),
    steps_per_epoch=10,
    epochs=2,
    workers=8)


score = model.evaluate(X_test, y_test)

X_test = preprocessing.transform(X_test)
y_predicted = model.predict(X_test)
np.set_printoptions(threshold=np.inf)

fpr_deep, tpr_deep, _ = roc_curve(y_test, y_predicted)
auc = auc(fpr_deep, tpr_deep)

plt.figure(figsize=(6,6))
plt.plot(tpr_deep, 1.0-fpr_deep, lw=3, alpha=0.8,
        label="Deep (AUC={:.2f})".format(auc))
plt.xlabel("Signal efficiency")
plt.ylabel("Background rejection")
plt.legend(loc=3)
plt.xlim((0.0, 1.0))
plt.ylim((0.0, 1.0))
plt.savefig("HIGGS_roc.png", bbox_inches="tight")
plt.close()

df = pd.DataFrame(np.hstack((X_test, y_predicted)), columns=branch_names+['y_predicted'])
fig, axs = plt.subplots(7, 2, figsize=(15,15))
_axs = axs.flatten()

print "df : ",df
sig = df[df.y_predicted>0.5]
bkg = df[df.y_predicted<0.5]
for i, col in enumerate(df[df.y_predicted<0.5].columns):
    print col, "  ", i
    low = min(sig[col].min(), bkg[col].min())
    high= max(sig[col].max(), bkg[col].max())
    weight_s = np.ones_like(sig[col])/float(len(sig[col]))
    weight_b = np.ones_like(bkg[col])/float(len(bkg[col]))
    _axs[i].hist(sig[col], 100, color='r', alpha=0.5, range=(low, high),weights=weight_s)
    _axs[i].hist(bkg[col], 100, color='b', alpha=0.5, range=(low, high),weights=weight_b)
    _axs[i].set_title(col)
    
fig.subplots_adjust(wspace=0.3, hspace=0.3)
plt.savefig("variables.png", bbox_inches="tight")
plt.close(fig)


decisions = []
for X, y in ((X_train, y_train), (X_test, y_test)):
    d1 = model.predict(X[y>0.5]).ravel()
    d2 = model.predict(X[y<0.5]).ravel()
    decisions += [d1, d2]
low = min(min(d) for d in decisions)
max = max(max(d) for d in decisions)
low_high = (low, high)
plt.hist(decisions[0], color='r', alpha=0.5, normed=True, label = 'S (train)', range=low_high, bins=30,histtype='stepfilled')
plt.hist(decisions[1], color='b', alpha=0.5, normed=True, label = 'B (train)', range=low_high, bins=30,histtype='stepfilled')
hist, nb1 = np.histogram(decisions[2], normed=True, range=low_high, bins=30)
center = (nb1[:-1]+nb1[1:])/2
scale = len(decisions[2])/sum(hist)
err = np.sqrt(hist*scale)/scale
plt.errorbar(center, hist, yerr=err, fmt='o', c='r', label = 'S (test)')

hist, nb2 = np.histogram(decisions[3], normed=True, range=low_high, bins=30)
center = (nb2[:-1]+nb2[1:])/2
scale = len(decisions[3])/sum(hist)
err = np.sqrt(hist*scale)/scale
plt.errorbar(center, hist, yerr=err, fmt='o', c='b', label = 'B (test)')
plt.xlabel("DNN response")
plt.ylabel("Arbitrary units")
plt.legend(loc='best')
plt.savefig("overtraining.png", bbox_inches="tight")
plt.close()


def correlation(data, count):
    corrmat = data.drop('y_predicted',1).corr()
    cofig, coax = plt.subplots(1, figsize=(15,15))
    corMap = coax.pcolor(corrmat, vmin=-1.0, vmax=1.0, cmap = plt.get_cmap("RdBu"))
    plt.colorbar(corMap, ax=coax)
    coax.set_title("Correlations")
    labels = corrmat.columns.values
    print labels
    coax.set_xticks(np.arange(len(labels))+0.5)
    coax.set_yticks(np.arange(len(labels))+0.5)
    coax.set_xticklabels(labels,rotation=45)
    coax.set_yticklabels(labels)
    plt.tight_layout()
    if count == 0:
        plt.savefig("correlation_sig.png", bbox_inches="tight")
    else:
        plt.savefig("correlation_bkg.png", bbox_inches="tight")
    count+=1
    plt.close(fig)

correlation(sig, 0)
correlation(bkg, 1)
plt.close()


print "--- %s seconds ---" % (time.time() - start_time)
