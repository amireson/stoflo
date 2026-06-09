# Andrew Ireson's system's dynamics model
# 13th January 2026
#
import numpy as np
# import pandas as pd

class model:
    def __init__(self):
        
        # Provide a default time grid:
        self.dt=1.
        self.niter=1
        self.tMax=20.
        self.tStart=0.
        self.t=np.arange(self.tStart,self.tMax+self.dt,self.dt)
        self.nt=len(self.t)

        # Empty parameters
        self.pars=None

        # Empty dictionaries for stocks and flows
        self.stocks={}  # stocks will be numpy arrays in a dictionary
        self.flows={}   # flows will be classes with functions
        self.drivers={} # drivers are numpy arrays in a dictionary
        
    def addTime(self,dt,tMax,tStart=0.,niter=1):
        self.dt=dt
        self.tMax=tMax
        self.niter=niter
        self.tStart=tStart
        self.t=np.arange(tStart,tMax+dt,dt)
        self.nt=len(self.t)
        
    def addPars(self,pars):
        self.pars=pars
        
    def addStock(self,name,initial):
        self.stocks[name]=np.zeros(self.nt)
        self.stocks[name][0]=initial

    def addFlow(self,name,func,into=None,outfrom=None):
        self.flows[name]=flow(name,func,into,outfrom)

    def addDriver(self,name,ts,into=None,outfrom=None):
        self.drivers[name]={'ts': ts, 'into': into, 'outfrom': outfrom}

    def runEuler(self):
        # Loop in time using explicit Euler with niter calculation steps
        for i in range(self.nt-1):
            
            # Update stocks at t_i+1 with result from t_i
            for s in self.stocks:
                self.stocks[s][i+1]=self.stocks[s][i]

            # 
            for iteration in range(self.niter):
                ti=self.t[i]+iteration*self.dt/self.niter
                # Get the stocks at previous timestep:
                i_stocks={s: self.stocks[s][i+1] for s in self.stocks}
                dSdt={s: 0. for s in self.stocks}
                
                # Get all the flows for the current timestep:
                for f in self.flows.values():
                    rate=f.func(ti,i_stocks,self.pars)
                    if f.into:
                        dSdt[f.into]+=rate*self.dt/self.niter
                    if f.outfrom:
                        dSdt[f.outfrom]-=rate*self.dt/self.niter
    
                # Get all the drivers for the current timestep:
                for dr in self.drivers.values():
                    if dr['into']:
                        dSdt[dr['into']]+=dr['ts'][i]*self.dt/self.niter
                    if dr['outfrom']:
                        dSdt[dr['outfrom']]-=dr['ts'][i]*self.dt/self.niter
                        
                # Update stocks at t_i+1
                for s in self.stocks:
                    self.stocks[s][i+1]=i_stocks[s]+dSdt[s]

        # Save all the flows:
        flowOutput={}
        for flow in self.flows.values():
            flowOutput[flow.name]=np.zeros(self.nt)
            for i in range(self.nt):
                flowOutput[flow.name][i]=flow.func(self.t[i],{x: self.stocks[x][i] for x in self.stocks},self.pars)
        self.flowOutput=flowOutput

        
# Since flows have functions within them, this needs to be a separate class:
class flow:
    def __init__(self,name,func,into=None,outfrom=None):
        self.name = name
        self.func = func          # function that computes flow rate
        self.into = into          # Name of Stock flow goes into or None
        self.outfrom = outfrom    # 
