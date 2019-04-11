'''
Created on Feb 4, 2019
Equations mainly from 214-35~38
@author: Keisuke
'''

from pylab import *
import time

def Eco(p):
    t = p.t
    dt = p.dt
    Sn = p.Sn
    Sp = p.Sp
    Phyfactor = p.Phyfactor
    Gmax = p.Gmax
    Kg = p.Kg
    mZoo1 = p.mZoo1
    mZoo2 = p.mZoo2
    Nother = p.Nother
    Pother = p.Pother
    
    #========================
    # Defining arrays
    #========================
    Nphy = 2 #Number of Phytoplankton
    
    def o(): 
        return zeros((Nphy,size(t)))
    
    Mu = o()  #(d-1) Growth rate
    X = o()   #(nmol C L-1) C
    Qn = o()  #(mol N mol C-1) N in a cell
    Qp = o()  #(mol P mol C-1) P in a cell
    Ngrowth = o() #(mol N mol C-1) Growth related molecules in N
    Nstore = o()  #(mol N mol C-1) N storage
    Prna = o()   #(mol P mol C-1) P RNA
    Nlim = o() #(n.d.) N limitation or not 
    Nfix = o() #(nmol N L-1 d-1)
    Vn = o() #(mol N mol C-1 d-1)
    
    def o1():
        return zeros(size(t))
    N = o1()      #(nmol N L-1) NH4 concentration
    P = o1()      #(nmol P L-1) PO4 concentration
    Xzoo = o1()   #(nmol C L-1) Zoo C
    
    def on(): #zero array for number of phytoplankton
        return zeros(Nphy)
    
    VnMax = on()
    VpMax = on()
    Kn = on()
    Kp = on()
    Anfix = on()
    Agrow = on()
    Arna = on()
    G = on()
    Vp = on()

    #========================
    # Initial values
    #========================
    
    X[0,0] = p.Xcro0
    X[1,0] = p.Xphy0
    Xzoo[0] = p.Xzoo0
    Qn[0,0] = p.QnCro0
    Qn[1,0] = p.QnPhy0
    Qp[0,0] = p.QpCro0
    Qp[1,0] = p.QpPhy0
    N[0] = p.N0
    P[0] = p.P0

    #=========================
    # Phyto parameters
    #=========================
    VnMax[0] = p.VnMaxCro
    VnMax[1] = p.VnMaxPhy
    VpMax[0] = p.VpMaxCro
    VpMax[1] = p.VpMaxPhy
    Kn[0] = p.KnCro
    Kn[1] = p.KnPhy
    Kp[0] = p.KpCro
    Kp[1] = p.KpPhy
    Anfix[0] = p.Anfix
    Anfix[1] = 0
    Agrow[0] = p.AgrowCro
    Agrow[1] = p.AgrowPhy
    Arna[0] = p.ArnaCro 
    Arna[1] = p.ArnaPhy
    
    #=======================
    # Preparation
    #=======================
    U = arange(size(t))
    
    #==================================================
    # Mu0 calculation
    #==================================================

    def solver2D(a,b,c):
        return (-b+(b**2-4*a*c)**(1/2))/(2*a)
    
    for j in arange(Nphy):
        MuN = (Qn[j,0] - Nother)/Agrow[j]
        MuP = solver2D(Arna[j]*Agrow[j],Arna[j]*Nother,Pother - Qp[j,0])
        
        if MuN < MuP:
            Mu[j,0] = MuN
            Nlim[j,0] = 1
            Qp[j,0] = Arna[j]*Qn[j,0]*Mu[j,0]+Pother
        elif MuN >= MuP:
            Mu[j,0] = MuP
        
        Ngrowth[j,0] = Mu[j,0]*Agrow[j]
        Prna[j,0] = Arna[j]*(Ngrowth[j,0] + Nother)*Mu[j,0]
        Nstore[j,0] = Qn[j,0] - (Ngrowth[j,0] + Nother)
        
        Nfix[j,0] = Ngrowth[j,0]*Anfix[j]
    
    t0 = time.time()
    
    #OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    # Loop starts here
    #OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    for i in U[:-1]:
        if mod(i,10000) == 0:
            t1 = time.time()
            print(i,t1-t0)
            t0 = t1
            
        for j in arange(Nphy):
            #========================
            # Parts calculation
            #========================
            
            G[j] = Gmax*(X[j,i]**2/sum(X[:,i]**2))*(sum(X[:,i])**2/(Kg**2 + sum(X[:,i])**2))
            Vn[j,i] = VnMax[j]*N[i]/(N[i] + Kn[j]) 
            Vp[j] = VpMax[j]*P[i]/(P[i] + Kp[j])
                
            #=================================================
            # Time step effect
            #=================================================
    
            dX = X[j,i]*Mu[j,i] - Xzoo[i]*G[j]
            dQn = Vn[j,i] - Mu[j,i]*Qn[j,i] + Nfix[j,i]
            dQp = Vp[j] - Mu[j,i]*Qp[j,i]
        
            def upd(f,df):  #upd = update
                f[j,i+1] = f[j,i] + df*dt 
                return f
            
            X = upd(X,dX)
            Qn = upd(Qn,dQn)
            Qp = upd(Qp,dQp)
            
            #====================================================
            # Mu computation and quota and uptake adjustment
            #====================================================
            
            MuN = (Qn[j,i+1] - Nother)/Agrow[j]   
            MuP = solver2D(Arna[j]*Agrow[j],Arna[j]*Nother,Pother - Qp[j,i+1])
   
            if MuN < MuP: # N lim
                Mu[j,i+1] = MuN
                Qp[j,i+1] = Arna[j]*Qn[j,i+1]*Mu[j,i+1]+Pother
                Vp[j] = (Qp[j,i+1] - Qp[j,i])/dt + Mu[j,i]*Qp[j,i]
                Nlim[j,i+1] = 1 
            elif MuN >= MuP: # P lim
                Mu[j,i+1] = MuP
    
            Ngrowth[j,i+1] = Mu[j,i+1]*Agrow[j]
            Prna[j,i+1] = Arna[j]*(Ngrowth[j,i+1] + Nother)*Mu[j,i+1]
            Nstore[j,i+1] = Qn[j,i+1] - (Ngrowth[j,i+1] + Nother)
            Nfix[j,i+1] = Ngrowth[j,i+1]*Anfix[j]
            

        dN = - sum(Vn[:,i]*X[:,i]) + Sn
        dP = - sum(Vp*X[:,i]) + Sp     
        dXzoo = Xzoo[i]*sum(G) - mZoo1*Xzoo[i] - mZoo2*Xzoo[i]**2

        def upd1(f,df):  #upd = update
            f[i+1] = f[i] + df*dt 
            return f
        
        Xzoo = upd1(Xzoo,dXzoo)
        N = upd1(N,dN)
        P = upd1(P,dP)
        
        if i==U[-2]: #This is for filling the last value in the array
            Vn[:,i+1] = VnMax*N[i+1]/(N[i+1] + Kn) #if plotting Vp is needed, it should be added as well

    return X[0],X[1],Xzoo,N,P,Nlim[0],Nlim[1],Mu[0],Mu[1],Ngrowth[0],Nstore[0],Ngrowth[1],Nstore[1],Prna[0],Prna[1],Nfix[0],Vn[0],Vn[1]                     
    