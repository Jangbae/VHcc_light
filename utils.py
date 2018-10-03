from array import array
from ROOT import TH1F, TCanvas, TLine, gPad

def drawRatio(dataPlot,hBKG_Total,can,Title,TAG, unit):
    can.cd(2)
    gPad.SetGrid()
    xbinsListTemp = []
    Nbins = dataPlot.GetNbinsX()
    for iBin in range(1, Nbins+1):
        xbinsListTemp.append(dataPlot.GetXaxis().GetBinLowEdge(iBin))
    xbinsListTemp.append(dataPlot.GetXaxis().GetBinLowEdge(Nbins+1))
    xbins = array('d',sorted(xbinsListTemp))
    ratio = TH1F("Ratio"," ",len(xbins)-1, xbins)
    ratio.GetYaxis().SetRangeUser(0.,2.)
    ratio.GetYaxis().SetNdivisions(5)
    for iBin in range(0, Nbins+1):
        if dataPlot.GetBinContent(iBin+1) > 0:
            num = dataPlot.GetBinContent(iBin+1)
#             den = hBKG_Total.GetBinContent(iBin+1)
            den = hBKG_Total.GetStack().Last().GetBinContent(iBin+1)
            if num >0 and den> 0 :            
                eps = num/(den)
                ratio.SetBinContent(iBin+1, eps)
        
    line = TLine(xbinsListTemp[0],1,xbinsListTemp[-1],1)
    line.SetLineColor(2)
    ratio.SetMarkerStyle(20)
    ratio.SetMarkerSize(0.8)
    ratio.GetXaxis().SetTitle(unit)
    ratio.GetXaxis().SetTitleSize(0.15)
    ratio.GetXaxis().SetTitleOffset(0.70)
    ratio.GetYaxis().SetTitle("Data/MC")
    ratio.GetYaxis().SetTitleOffset(0.27)
    ratio.GetYaxis().SetTitleSize(0.10)
    ratio.GetYaxis().SetLabelSize(0.08)
    ratio.GetXaxis().SetLabelSize(0.10) 
    ratio.Draw('P')
    line.Draw('SAME')
    can.SaveAs(Title+'__'+TAG+'.png')
    can.Clear()
    can.Update()