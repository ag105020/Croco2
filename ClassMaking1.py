'''
Created on Feb 4, 2019

@author: Keisuke
'''

from pylab import *

class Params: #parameters
    def __init__(self,t,dt,Sn,Sp,Phyfactor,Gmax,Kg,mZoo1,mZoo2,VnMaxCro,VnMaxPhy,VpMaxCro,VpMaxPhy,KnCro,KnPhy,KpCro,KpPhy,\
                 Anfix,AgrowCro,AgrowPhy,Nother,ArnaCro,ArnaPhy,Pother,Xcro0,Xphy0,Xzoo0,QnCro0,QnPhy0,QpCro0,QpPhy0,N0,P0):
        self.t = t
        self.dt = dt
        self.Sn = Sn
        self.Sp = Sp
        self.Phyfactor = Phyfactor
        self.Gmax = Gmax
        self.Kg = Kg
        self.mZoo1 = mZoo1
        self.mZoo2 = mZoo2
        self.VnMaxCro = VnMaxCro
        self.VnMaxPhy = VnMaxPhy
        self.VpMaxCro = VpMaxCro
        self.VpMaxPhy = VpMaxPhy
        self.KnCro = KnCro
        self.KnPhy = KnPhy
        self.KpCro = KpCro
        self.KpPhy = KpPhy
        self.Anfix = Anfix
        self.AgrowCro = AgrowCro
        self.AgrowPhy = AgrowPhy
        self.Nother = Nother
        self.ArnaCro = ArnaCro 
        self.ArnaPhy = ArnaPhy
        self.Pother = Pother
        self.Xcro0 = Xcro0
        self.Xphy0 = Xphy0
        self.Xzoo0 = Xzoo0
        self.QnCro0 = QnCro0
        self.QnPhy0 = QnPhy0
        self.QpCro0 = QpCro0
        self.QpPhy0 = QpPhy0
        self.N0 = N0
        self.P0 = P0
