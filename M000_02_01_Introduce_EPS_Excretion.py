'''
Created on Nov 22, 2018

This is to simulate Masuda 2013
Equations based on Kei213-14~20

Here we test using "d" for time instead of "s"
@author: Keisuke
'''
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# Importing
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
from pylab import *
from FigSetting2 import *
from Savefig2 import *

rcParams['axes.prop_cycle'] = (cycler('color',['b', 'r', 'g']) + cycler('ls',['-', ':', '--']) + cycler('lw',[3, 4.5, 3]))
rcParams.update({'legend.edgecolor': 'k'})
rcParams.update({'legend.labelspacing':1})
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# Flaggin for plot
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

FigAllinOne = 0     #When it is in "1" plotting all the figures in one panel; else, plot one figure in one panel
if FigAllinOne == 1:    #Here setting figures for one panel version
    rcParams.update({'font.size': 15,
                 'lines.markersize':10,
                 'lines.markeredgewidth':0.5})
    rcParams['figure.figsize']=15.7,9.75

#------------------------------------------------
#Here defining steps of dilution rates (x-axis)
#------------------------------------------------
DdStep = 0.001
DdMax = 0.5
Dd = arange(DdStep,DdMax+DdStep,DdStep)
U = arange(size(Dd))
#-------------------------

#OOOOOOOOOOOOOOOOOOOOOOOOO
# Define functions
#OOOOOOOOOOOOOOOOOOOOOOOOO

def gft(FileName):   #This function generate files from a certain folder 
    return genfromtxt('..\\Data\\'+FileName+'.csv',delimiter=',')

def xy0():   #As it is... 
    ylim(bottom=0)
    xlim(left=0,right=DdMax)

def x0():
    xlim(left=0,right=DdMax)

def it(a):
    return '$\mathit{' + str(a) + '}$'

def sup(FigNum): #subplot; here if it is in one panel, plot in subplot. Otherwise, plot in one pane.
    if FigAllinOne == 1:
        subplot(3,5,FigNum)
    else:
        figure(FigNum)
    xlabel(it('\mu')+' (d$^{-1}$)')

#OOOOOOOOOOOOOOOOOOOOOOOOOO
# Main function
#OOOOOOOOOOOOOOOOOOOOOOOOOO
def ModelRun(NfixFactor):
    Fpoc = 1/(1-0.22)  #Based on Sohm 2011 Fronteirs in Microbiology; ~22% of POC is EPS. 
    #OOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    # Reading data
    #OOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    data = gft('DataMasuda2013_nan1')[:-1].T
    
    #OOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    # Boundary conditions
    #OOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    Nin = 50e-3   #(mol m-3) from Masuda et al., 2013
    Pin = 20e-3   #(mol m-3) from Masuda et al., 2013
    
    #OOOOOOOOOOOOOOOOOOOOOOOOO
    # Parameterization
    #OOOOOOOOOOOOOOOOOOOOOOOOO
    E=0.7   #(dimensionless) CO2/Bio

    Nother = 0.01*Fpoc   #(molN molC-1) Baseline N
    Apho = 1.4      #Works inversively to N:C; coefficient of Ngrowth (see Kei213-15)
    
    Pother = 0.055*Fpoc  #(molP molC-1) Baseline P 
    Arna = 0.2      #Coefficient for rna
    
    Anfix = 0.07    #Coefficent for N2 fixation
    Anfix = Anfix * NfixFactor   #NfixFactor multiplied for each plot
    
    DONideal = 12.88333e-3 #(molN m-3) Taken from averaged value of the data (only NH4+ added cases)
    
    #OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    #Main Computation
    #OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    
    Ngrowth = ((1+E)*Dd)/Apho*Fpoc     #(molN molC-1) Growth dependent N
    print('Agrow',((1+E))/Apho*Fpoc)
    Nfix = Anfix*Ngrowth          #(molN molC-1 d-1) 
    Prna = (Ngrowth+Nother)*Dd*Arna   #(molP molC-1 d-1) 
    
    Qn0 = Ngrowth + Nother   #(molN molC-1) this is used for determining what is limiting
    Qp0 = Prna + Pother      #(molP molC-1) this is used for determing what is limiting
    
    Cn = (Nin-DONideal)/(Qn0-Nfix/Dd)   #(molC m-3) cell C in N limited case 
    Cn[Cn<0] = nan   #(molC m-3) negative values are removed
    Cp = Pin/Qp0     #(molC m-3) cell C in p limited case
    
    #------------------------------
    # Preparing array for loops
    #------------------------------
    which = zeros(size(Dd))
    C = zeros(size(Dd))
    Nstore = zeros(size(Dd))
    Pstore = zeros(size(Dd))
    
    #--------------------------------------------------
    # Determining what is limiting; Different equations for different limitation
    #--------------------------------------------------
    for i in U:
        if Cn[i]<Cp[i]:  #N limited case
            C[i] = Cn[i]
            Nstore[i] = 0
            Pstore[i] = Pin/C[i] - Qp0[i]  #All the excess P is in the store
            Pstore[i] = 0  #P store = 0, which turned out to work better
            which[i] = 1   #which = 1 means N limited
        else:
            C[i] = Cp[i]  #P limited case
            Nstore[i] = (Nin-DONideal+Nfix[i]/Dd[i]*C[i])/C[i] - Qn0[i]  #All the excess N is in the store
            Pstore[i] = 0
    
    Ctot = C*Fpoc #(multiplying it to include EPS)
    #---------------------------------------------------
    #Qn = (Nin+C*Nfix/Dd-DONideal)/Ctot     #(molN molC-1) Nitrogen quota (Kei213-20)
    Qn = (Ngrowth + Nother + Nstore)/Fpoc #(molN molC-1) Nitrogen quota (Kei 213-20)
    Qp = (Prna + Pother + Pstore)/Fpoc      #(molP molC-1) P quota

    Nexc = Dd*DONideal/Ctot     #(molN molC-1 d-1) N excretion rate per carbon
    P = Pin - Qp*Ctot           #(molP m-3) PO4 concentration in the culture
    Ntot = Nin + Nfix*C/Dd   #(molN m-3) TN; total nitrogen
    
    #OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    #Plotting
    #OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    '''
    Here the plot number must be incremental from 1 (for saving)
    If the number of figures change the value of a paramter 
    "NumberOfFigures" outside of this function must change
    '''
    #=============================
    # Preparation
    #=============================
    ConUnit = ' ($\mu$mol L$^{-1}$)'  # = concentration unit
    RatioUnit = ' (mol mol$^{-1}$)'
    NrateUnit = ' (mol N d$^{-1}$ mol C$^{-1}$)'
    DataColor = 'cyan'
    #=============================
    
    figure(1)
    sup(1)
    if NfixFactor==1:
         plot(nan,nan,'o',color=DataColor,label='Data')
         plot(nan,nan) #To adjust the subsequent color
         plot(nan,nan)
    plot(Dd,Qn,label= str(NfixFactor) + ' ' + 'x '  + it('N_{2Fix}'))
    plot(data[0],data[6],'o',color=DataColor)
    ylabel('N:C' + RatioUnit)
    xy0()
    legend(loc=2,labelspacing=0.3)
    
    sup(2)
    #plot(Dd,Qp)
    plot(Dd,Qp)
    plot(data[0],data[7],'o',color=DataColor)
    ylabel('P:C' + RatioUnit)
    xy0()
     
    sup(3)
    if NfixFactor==1:
         plot(nan,nan,'o',color=DataColor,label='Data')
         plot(nan,nan) #To adjust the subsequent color
         plot(nan,nan)
    plot(Dd,which,label= str(NfixFactor) + ' ' + 'x '  + it('N_{2Fix}'))
    ylabel('Nlim = 1, Plim = 0')
    x0()
  #  legend(loc=4)
     
    sup(4)
    plot(Dd,Ctot*1e3)
    plot(data[0],data[8],'o',color=DataColor)
    ylabel('C' + ConUnit)
    xy0()
     
    sup(5)
    plot()
    plot(Dd,Nfix/Fpoc)
    plot(data[0],data[5],'o',color=DataColor)
    ylabel('Nfix/C' + NrateUnit)
    xy0(), ylim(bottom=-0.002)
     
    sup(6)
    plot(Dd,P*1e3)
    plot(data[0],data[2],'o',color=DataColor)
    ylabel('PO$_{4}$$^{3-}$' + ConUnit)
    ylim(top=14)
    x0()
     
    sup(7)
    plot(Dd,DONideal*ones(size(Dd))*1e3)
    plot(data[0],data[3],'o',color=DataColor)
    ylabel('DON' + ConUnit)
    ylim(top=14)
    xy0()
      
    sup(8)
    plot(Dd,Nexc)
    plot(data[0],data[10],'o',color=DataColor)
    ylabel('Nexc' + NrateUnit)
    xy0()
      
    sup(9)
    if NfixFactor==1:
         plot(nan,nan,'o',color=DataColor,label='Data')
         plot(nan,nan) #To adjust the subsequent color
         plot(nan,nan)
    plot(Dd,Ntot*1e3,label= str(NfixFactor) + ' ' + 'x '  + it('N_{2Fix}'))
    plot(data[0],data[4],'o',color=DataColor)
    ylabel('Total N' + ConUnit)
    ylim(top=120)
    xy0()
    legend(loc=3,ncol=2,fontsize='23')

    sup(12)
    if NfixFactor==1:
         plot(nan,nan,'o',color=DataColor,label='Data')
         plot(nan,nan) #To adjust the subsequent color
         plot(nan,nan)
    plot(Dd,Ntot*1e3*nan,label= str(NfixFactor) + ' ' + 'x '  + it('N_{2Fix}'))
    plot(data[0],data[4]*nan,'o',color=DataColor)
    ylabel('Total N' + ConUnit)
    ylim(top=120)
    xy0()
    legend(loc=3,ncol=1,fontsize='25')

    sup(13)
    plot(Dd,Nexc*0)
    plot([0.1,0.15,0.2,0.25,0.3,0.35],[0.059,0.025,0.015,0.008,0.009,0],'o',color=DataColor)
    ylabel('Nexc' + NrateUnit)
    ylabel('NH$_{4}$$^{+}$' + ConUnit)
    x0()
    ylim(-0.01,0.05)

    if NfixFactor==1:
        sup(10)
        stackplot(Dd,Nother*ones(size(Dd))/Fpoc,Ngrowth/Fpoc,Nstore/Fpoc,colors=('b','cyan','r'))
        ylabel('N:C' + RatioUnit)
        xy0()
        #--------Manual Legend----------

        Names = [it('N_{Other}'),it('N_{Growth}'),it('N_{Store}')]
        Colors = ['blue','cyan','red']
        for i in arange(size(Names)):
            plot([],[],linewidth=12,color=Colors[-i-1],label=Names[-i-1])
        legend(loc=2)
    
        sup(11)
        stackplot(Dd,Pother*ones(size(Dd))/Fpoc,Prna/Fpoc,colors=('b','cyan'))
        ylabel('P:C' + RatioUnit)
        xy0()
            #--------Manual Legend----------
        Names = ['$\mathit{P_{Other}}$','$\mathit{P_{RNA}}$']
        Colors = ['blue','cyan']
        for i in arange(size(Names)):
            plot([],[],linewidth=12,color=Colors[-i-1],label=Names[-i-1])
        legend(loc=2)
    
    #OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

ModelRun(1)   # Normal run
ModelRun(2)   # Zero nitrogen fixation
ModelRun(0)   # Double nitrogn fixation
#OOOOOOOOOOOOOOOOOOOOOOOOOO
# Save figures
#OOOOOOOOOOOOOOOOOOOOOOOOOO

if FigAllinOne == 1:
    Savefig2('01\\Masuda2013\\Steady State 2','all',600)
else:
    NumberOfFigures = 13    #This value must be changed when the number of figures change
    for i in arange(NumberOfFigures):
        figure(i+1)
        Savefig2('01\\Masuda2013\\Steady State 2',i+1,600)
show()

