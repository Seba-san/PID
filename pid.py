#!/usr/bin/env python

import sys
import math

class PID:
    """
    Implementacion de un PID discreto en la forma:
    u=Kp(e + D + I)
    donde D es la parte derivativa discretizada mediante tustin (o bilineal) e I es la parte
    integral utilizando diferencias hacia atras.
    """
    def __init__(self):
        self.y=[0 for i in range(2)]
        self.y_sp=[0 for i in range(2)]
        self.I=0
        self.D=0
        self.limit=1
        self.u=0
        self.Normalizacion=1 

    def set_parameters(self,**kargs):
        self.Kp=kargs.get('Kp')
        self.Ki=kargs.get('Ki')
        self.Kd=kargs.get('Kd')
        self.Ts=kargs.get('Ts')
        self.N=kargs.get('N',10)
        N=self.N
        Ts=self.Ts
        self.D_0=(N * Ts - 2.0) / (N * Ts + 2.0) # Bilinear or tustin
        self.D_1=2.0 / (N * Ts + 2.0)# Bilinear or tustin
        self.I_1=Ts / 2.0

    def run(self,y_sp_,y_):
        """        
        y_sp: Set point
        y_: medida
        """
        # Se acomodan las unidades
        y_=y_ * self.Normalizacion
        y_sp_=y_sp_ * self.Normalizacion
        self.y.insert(0,y_)
        self.y.pop()
        self.y_sp.insert(0,y_sp_)
        self.y_sp.pop()
        
        self.D = self.Kd * (self.D_1 * (self.y[0] - self.y[1])) - self.D_0 * self.D
        self.u = self.Kp * (self.y_sp[0] - self.y[0] + self.D)
        temp = self.Ki * self.I_1 * (self.y_sp[0]  - self.y[0] ) 
        # Antiwindup for integral part
        if abs(self.u+self.Kp*(temp+self.I))<self.limit: 
             self.u= self.u+self.Kp*(temp+self.I)
             self.I=self.I+temp
        else:
            self.u=abs(self.u)*self.limit/self.u 
            self.I=self.I-temp

        return self.u

if __name__=='__main__':
   pid=PID()
   pid.set_parameters(Kp=1.0,Ki=0.0,Kd=0.0,Ts=0.1)
   u=pid.run() # Control signal
