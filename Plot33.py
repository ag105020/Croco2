'''
Created on Feb 4, 2019

@author: Keisuke
'''
from pylab import *

Xlabel = 't (d)'

row = 4
col = 5

def plot3(t,tMin,tMax,Nother,Pother,Xcro,Xphy,Xzoo,N,P,NlimCro,NlimPhy,MuCro,MuPhy,NgrowthCro,NstoreCro,NgrowthPhy,NstorePhy,PrnaCro,PrnaPhy,Nfix,VnCro):

    def sup2(loc,Title,Ylabel):
        subplot(row,col,loc)
        xlim(tMin,tMax)
        title(Title)
        ylabel(Ylabel)
    
    def sup3(loc):
        subplot(row,col,loc)
    
    def sup0(loc,y,Label):
        sup3(loc)
        plot(t,y,label=Label)
        xlabel(Xlabel)
        
    def sup1(loc,y,Ylabel,Title):
        sup3(loc)
        plot(t,y)
        title(Title,y=1.02)
        ylabel(Ylabel)
        xlabel(Xlabel)
   
    figure(1,figsize=(21,11))
    sup0(1,Xcro,'Cro')
    title('X')
    ylabel('nmol C L$^{-1}$')
    legend(loc=1)
    
    sup0(2,Xphy,'Phy')
    title('X')
    ylabel('nmol C L$^{-1}$')
    legend(loc=1)

    sup0(3,MuCro,'Cro')
    title('Mu')
    ylabel('Mu (d$^{-1}$)')
    
    sup0(4,MuPhy,'Phy')
    title('Mu')
    ylabel('Mu (d$^{-1}$)')

    sup1(6,N,'N (nmol L$^{-1}$)','N')
    sup1(7,P,'P (nmol L$^{-1}$)','P')
    sup1(8,NlimCro,'1: N, 0: P','Cro limitation')
    ylim(-0.1,1.1)
    sup1(9,NlimPhy,'1: N, 0: P','Phy limitation')
    ylim(-0.1,1.1)
    
    sup2(11,'N allocation Cro','N (mol N mol C$^{-1}$)')
    stackplot(t,Nother*ones(size(t)),NgrowthCro,NstoreCro)
    
    sup2(12,'N allocation Phy','N (mol N mol C$^{-1}$)')
    stackplot(t,Nother*ones(size(t)),NgrowthPhy,NstorePhy)
    
    sup2(13,'P allocation Cro','P (mol P mol C$^{-1}$)')
    stackplot(t,Pother*ones(size(t)),PrnaCro)
    
    sup2(14,'P allocation Phy','P (mol P mol C$^{-1}$)')
    stackplot(t,Pother*ones(size(t)),PrnaPhy)
    
    sup1(5,Nfix/(Nfix+VnCro),'Nfix fraction (n.d.)','Nfix fraction')
    

    