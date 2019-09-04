'''
Created on Feb 3, 2019
Ecological version of the model
@author: Keisuke
'''

from pylab import *
from FigSetting2 import *
from Eco13 import *
from ClassMaking1 import *
rcParams['axes.prop_cycle'] = (cycler('color',['b', 'r', 'g']) + cycler('ls',['-', ':', '--']) + cycler('lw',[3, 4.5, 3]))
rcParams.update({'legend.edgecolor': 'k'})

FigAllinOne = 0     #When it is in "1" plotting all the figures in one panel; else, plot one figure in one panel
if FigAllinOne == 1:    #Here setting figures for one panel version
    from Plot33 import *
    from Plot34 import *
    rcParams.update({'font.size': 15,
             'lines.markersize':10,
             'lines.markeredgewidth':0.5})
    rcParams['figure.figsize']=15.7,9.75
else:
    from Plot73 import *
    from Plot74 import *

#========================
# Time setting
#========================
tMax = 500 #(d)
dt= tMax/10000
tMin = 0
t = arange(tMin,tMax+dt,dt)

Fpoc = 1/(1-0.22)

#========================
# Initial values
#========================

Xcro0 = 1
Xphy0 = 1
Xzoo0 = 1
QnCro0 = 0.1/Fpoc
QnPhy0 = 0.1/Fpoc
QpCro0 = 0.06/Fpoc
QpPhy0 = 0.06/Fpoc
print(QpCro0)
N0 = 6
P0 = 3.2

#========================
# Parameterization
#========================

Sn = 0.1*Fpoc
Sp = 0.0277*Fpoc

Phyfactor = 2 

Gmax = 1
Kg = 5
mZoo1 = 0.0
mZoo2 = 0.01
VnMaxCro = 0.2*Fpoc #(mol N mol C-1 d-1)
VnMaxPhy = VnMaxCro * Phyfactor
VpMaxCro = 0.06*Fpoc
VpMaxPhy = VpMaxCro * Phyfactor  
KnCro = 20  #(nmol N L-1)
KnPhy = 20  #(nmol N L-1)
KpCro = 10  #(nmol P L-1)
KpPhy = 10  #(nmol P L-1)

Anfix = 0.07    #Coefficent for N2 fixation
#Anfix = 0

AgrowCro = 1.2142857142857144*Fpoc
AgrowPhy = AgrowCro / Phyfactor
Nother = 0.01*Fpoc
ArnaCro = 0.2
ArnaPhy = 0.2 / Phyfactor
Pother = 0.055*Fpoc

#=====================================
# With N2 fixation
#=====================================
p = Params(t,dt,Sn,Sp,Phyfactor,Gmax,Kg,mZoo1,mZoo2,VnMaxCro,VnMaxPhy,VpMaxCro,VpMaxPhy,KnCro,KnPhy,KpCro,KpPhy,\
                 Anfix,AgrowCro,AgrowPhy,Nother,ArnaCro,ArnaPhy,Pother,Xcro0,Xphy0,Xzoo0,QnCro0,QnPhy0,QpCro0,QpPhy0,N0,P0)
Xcro,Xphy,Xzoo,N,P,NlimCro,NlimPhy,MuCro,MuPhy,NgrowthCro,NstoreCro,NgrowthPhy,NstorePhy,PrnaCro,PrnaPhy,Nfix,VnCro,VnPhy = Eco(p)
plot3(t,tMin,tMax,Nother,Pother,Xcro,Xphy,Xzoo,N,P,NlimCro,NlimPhy,MuCro,MuPhy,NgrowthCro,NstoreCro,NgrowthPhy,NstorePhy,PrnaCro,PrnaPhy,Nfix,VnCro,VnPhy)

#=====================================
# Without N2 fixation
#=====================================
Anfix0 = 0
p = Params(t,dt,Sn,Sp,Phyfactor,Gmax,Kg,mZoo1,mZoo2,VnMaxCro,VnMaxPhy,VpMaxCro,VpMaxPhy,KnCro,KnPhy,KpCro,KpPhy,\
                 Anfix0,AgrowCro,AgrowPhy,Nother,ArnaCro,ArnaPhy,Pother,Xcro0,Xphy0,Xzoo0,QnCro0,QnPhy0,QpCro0,QpPhy0,N0,P0)
Xcro,Xphy,Xzoo,N,P,NlimCro,NlimPhy,MuCro,MuPhy,NgrowthCro,NstoreCro,NgrowthPhy,NstorePhy,PrnaCro,PrnaPhy,Nfix,VnCro,VnPhy = Eco(p)
plot4(t,tMin,tMax,Nother,Pother,Xcro,Xphy,Xzoo,N,P,NlimCro,NlimPhy,MuCro,MuPhy,NgrowthCro,NstoreCro,NgrowthPhy,NstorePhy,PrnaCro,PrnaPhy,Nfix,VnCro,VnPhy)

#=====================================
# x2 N2 fixation
#=====================================
# Anfix2 = Anfix*10
# p = Params(t,dt,Sn,Sp,Phyfactor,Gmax,Kg,mZoo1,mZoo2,VnMaxCro,VnMaxPhy,VpMaxCro,VpMaxPhy,KnCro,KnPhy,KpCro,KpPhy,\
#                  Anfix2,AgrowCro,AgrowPhy,Nother,ArnaCro,ArnaPhy,Pother,Xcro0,Xphy0,Xzoo0,QnCro0,QnPhy0,QpCro0,QpPhy0,N0,P0)
# Xcro,Xphy,Xzoo,N,P,NlimCro,NlimPhy,MuCro,MuPhy,NgrowthCro,NstoreCro,NgrowthPhy,NstorePhy,PrnaCro,PrnaPhy,Nfix,VnCro = Eco(p)
# plot4(t,tMin,tMax,Nother,Pother,Xcro,Xphy,Xzoo,N,P,NlimCro,NlimPhy,MuCro,MuPhy,NgrowthCro,NstoreCro,NgrowthPhy,NstorePhy,PrnaCro,PrnaPhy,Nfix,VnCro)

show()