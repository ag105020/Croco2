'''
Created on Feb 4, 2019

@author: Keisuke
'''
from pylab import *
from Savefig2 import *

Xlabel = '$\mathit{t}$ (d)'

row = 4
col = 5

FileLoc = "01\\Masuda2013\\Dynamic3"

def plot4(t,tMin,tMax,Nother,Pother,Xcro,Xphy,Xzoo,N,P,NlimCro,NlimPhy,MuCro,MuPhy,NgrowthCro,NstoreCro,NgrowthPhy,NstorePhy,PrnaCro,PrnaPhy,Nfix,VnCro,VnPhy):

    def sup2(loc,Title,Ylabel):
        figure(loc)
        xlim(tMin,tMax)
        title(Title,y=1.02)
        ylabel(Ylabel)
        Savefig2(FileLoc,loc,600)
    
    def sup3(loc):
        figure(loc)
    
    def sup0(loc,y,Label):
        sup3(loc)
        plot(t,y)
        xlabel(Xlabel)
        Savefig2(FileLoc,loc,600)
        
    def sup1(loc,y,Ylabel,Title):
        sup3(loc)
        plot(t,y)
        title(Title,y=1.02)
        ylabel(Ylabel)
        xlabel(Xlabel)
        Savefig2(FileLoc,loc,600)
        
    def sf(loc):
        Savefig2(FileLoc,loc,600)
   
    figure(1,figsize=(21,11))
    sup0(1,Xcro,'Cro')
    title('$\mathit{C_{Cro}}$',y=1.02)
    ylabel('nmol C L$^{-1}$')
    Names = ['1 x $\mathit{N_{2fix}}$','0 x $\mathit{N_{2fix}}$']
    Colors = ['blue','red']
    LineStyles = ['-',':']
    LineWidth = [3,4.5]
    for i in arange(size(Names)):
        plot([],[],color=Colors[i],label=Names[i],linestyle=LineStyles[i],linewidth=LineWidth[i])
    legend()
    sf(1)

    sup0(2,Xphy,'Phy')
    title('$\mathit{C_{Phy}}$',y=1.02)
    ylabel('nmol C L$^{-1}$')
    sf(2)

    sup0(3,MuCro,'Cro')
    title('$\mathit{Cro}$ growth rate',y=1.02)
    ylabel('$\mathit{\mu_{Cro}}$ (d$^{-1}$)')
    Names = ['1 x $\mathit{N_{2fix}}$','0 x $\mathit{N_{2fix}}$']
    Colors = ['blue','red']
    LineStyles = ['-',':']
    LineWidth = [3,4.5]
    for i in arange(size(Names)):
        plot([],[],color=Colors[i],label=Names[i],linestyle=LineStyles[i],linewidth=LineWidth[i])
    legend(loc=4)
    sf(3)

    sup0(4,MuPhy,'Phy')
    title('$\mathit{Phy}$ growth rate',y=1.02)
    ylabel('$\mathit{\mu_{Phy}}$ (d$^{-1}$)')
    sf(4)
    
    sup0(5,MuPhy/MuCro,'')
    title("Growth rate ratio",y=1.02)
    ylabel('$\mathit{\mu_{Phy} : \mu_{Cro}}$ (dimentionless)')
    ylim(-0.2,2.5); yticks=(0,1,2)
    sf(5)
    
    sup1(6,N,'nmol L$^{-1}$','NH$_4^+$')
    Names = ['1 x $\mathit{N_{2fix}}$','0 x $\mathit{N_{2fix}}$']
    Colors = ['blue','red']
    LineStyles = ['-',':']
    LineWidth = [3,4.5]
    for i in arange(size(Names)):
        plot([],[],color=Colors[i],label=Names[i],linestyle=LineStyles[i],linewidth=LineWidth[i])
    legend(loc=4)
    sf(6)

    
    sup1(7,P,'P (nmol L$^{-1}$)','P')
    sf(7)
    
    sup1(8,NlimCro,'1: N, 0: P','$\mathit{Cro}$ limitation')
    ylim(-0.1,1.1)
    sf(8)

    sup1(9,NlimPhy,'1: N, 0: P','$\mathit{Phy}$ limitation')
    ylim(-0.1,1.1)
    sf(9)

    sup1(20,VnCro*Xcro,'nmol L$^{-1}$ d$^{-1}$','NH$_4^+$ uptake $\mathit{Cro}$')
    ylim(top=VnCro[-1]*Xcro[-1]+0.005)
    Colors = ['blue','red']
    LineStyles = ['-',':']
    LineWidth = [3,4.5]
    for i in arange(size(Names)):
        plot([],[],color=Colors[i],label=Names[i],linestyle=LineStyles[i],linewidth=LineWidth[i])
    legend(loc=4)
    sf(20)

    
    sup1(21,VnPhy*Xphy,'nmol L$^{-1}$ d$^{-1}$','NH$_4^+$ uptake $\mathit{Phy}$ ')
    ylim(top=VnPhy[-1]*Xphy[-1]+0.005)
    sf(21)

    
    sup2(16,'N allocation Cro','N (mol N mol C$^{-1}$)')
    stackplot(t,Nother*ones(size(t)),NgrowthCro,NstoreCro)
    sf(16)

    sup2(17,'N allocation Phy','N (mol N mol C$^{-1}$)')
    stackplot(t,Nother*ones(size(t)),NgrowthPhy,NstorePhy)
    sf(17)

    sup2(18,'P allocation Cro','P (mol P mol C$^{-1}$)')
    stackplot(t,Pother*ones(size(t)),PrnaCro)
    sf(18)

    sup2(19,'P allocation Phy','P (mol P mol C$^{-1}$)')
    stackplot(t,Pother*ones(size(t)),PrnaPhy)
    sf(19)
    
    sup1(22,Nfix/(Nfix+VnCro),'dimensionless','N$_2$ fix fraction')        

    