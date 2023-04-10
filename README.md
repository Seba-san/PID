# PID
Implementación de un PID. Para usarlo hay que hacer:

    from pid import PID

    if __name__=='__main__':
        controlador=PID()
        controlador.set_parameters(Kp=1.0,Ki=0.0,Kd=0.0,Ts=0.1)
        u=controlador.run() # Control signal

## Forma de la discretización
El PID implementado se resume en:
  
    u=Kp(e(k)+D(k)+I(k))
    
donde Kp es la ganancia proporcional, D es la parte derivativa e I es la parte integral. En detalle:

    e(k)=set_point(k)-valor_medido(k)
    D(k)=Kd ( D_1[e(k)-e(k-1)] )-D_0 D(k-1)
    I(k)= Ki I_1 e + I(k-1)
 
 
