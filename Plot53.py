'''
Created on Feb 4, 2019

@author: Keisuke
'''
from pylab import *
from Savefig2 import *

Xlabel = '$\mathit{t}$ (d)'

row = 4
col = 5

FileLoc = "01\\Masuda2013\\Dynamic"

def plot3(t,tMin,tMax,Nother,Pother,Xcro,Xphy,Xzoo,N,P,NlimCro,NlimPhy,MuCro,MuPhy,NgrowthCro,NstoreCro,NgrowthPhy,NstorePhy,PrnaCro,PrnaPhy,Nfix,VnCro,VnPhy):

    def sup2(loc,Title,Ylabel):
        figure(loc)
        xlim(tMin,tMax)
        title(Title,y=1.02)
        ylabel(Ylabel)
        xlim(tMin,tMax)
    
    def sup3(loc):
        figure(loc)
    
    def sup0(loc,y,Label):
        sup3(loc)
        plot(t,y)
        xlabel(Xlabel)
        xlim(tMin,tMax)
        
    def sup1(loc,y,Ylabel,Title):
        sup3(loc)
        plot(t,y)
        title(Title,y=1.02)
        ylabel(Ylabel)
        xlabel(Xlabel)
        xlim(tMin,tMax)
    
    def sf(loc):
        Savefig2(FileLoc,loc,300)
    
    sup0(1,Xcro,'Cro')
    title('[$\mathit{Q_C}$]$\mathit{_{Cro}}$',y=1.02)
    ylabel('nmol C L$^{-1}$')
    ylim(0.3, 0.600001)
    sf(1)
    
    sup0(2,Xphy,'Phy')
    title('[$\mathit{Q_C}$]$\mathit{_{Phy}}$',y=1.02)
    ylabel('nmol C L$^{-1}$')
    ylim(top=1)
    sf(2)

    sup0(3,MuCro,'Cro')
    title('Mu')
    ylabel('Mu (d$^{-1}$)')
    sf(3)
    
    sup0(4,MuPhy,'Phy')
    title('Mu')
    ylabel('Mu (d$^{-1}$)')
    sf(4)

    sup1(6,N,'N (nmol L$^{-1}$)','N')
    sf(6)  
    sup1(7,P,'P (nmol L$^{-1}$)','P')
    sf(7)  
    sup1(8,NlimCro,'1: N, 0: P','Cro limitation')  
    ylim(-0.1,1.1)
    sf(8)  
    sup1(9,NlimPhy,'1: N, 0: P','Phy limitation')
    ylim(-0.1,1.1)
    sf(9)  
    
    sup1(20,VnCro*Xcro,'N uptake Cro (nmol L$^{-1}$ d$^{-1}$)','N uptake Cro')
    sf(20)
    
    sup1(21,VnPhy*Xphy,'N uptake Phy (nmol L$^{-1}$ d$^{-1}$)','N uptake Phy')
    sf(21)
    
    sup2(11,'N allocation Cro','N (mol N mol C$^{-1}$)')
    stackplot(t,Nother*ones(size(t)),NgrowthCro,NstoreCro)
    sf(11)
    
    sup2(12,'N allocation Phy','N (mol N mol C$^{-1}$)')
    stackplot(t,Nother*ones(size(t)),NgrowthPhy,NstorePhy)
    sf(12)

    sup2(13,'P allocation Cro','P (mol P mol C$^{-1}$)')
    stackplot(t,Pother*ones(size(t)),PrnaCro)
    sf(13)
    
    sup2(14,'P allocation Phy','P (mol P mol C$^{-1}$)')
    stackplot(t,Pother*ones(size(t)),PrnaPhy)
    sf(14)
    
    sup1(5,Nfix/(Nfix+VnCro),'Nfix fraction (n.d.)','Nfix fraction')
    sf(5)
    