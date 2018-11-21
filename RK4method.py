import numpy as np
import matplotlib.pyplot as plt


temp=np.zeros(4)# (t1,t2,w1,w2)
# Peninfo=(g,m1,m2,l1,l2)
#         (0, 1, 2, 3, 4)
def F(U_i,Peninfo):
    st1=np.sin(U_i[0])
    st2=np.sin(U_i[1])
    ct1t2=np.cos(U_i[0]-U_i[1])
    st1t2=np.sin(U_i[0]-U_i[1])
    s2t1t2=np.sin(2*(U_i[0]-U_i[1]))
    w1=U_i[2]
    w2=U_i[3]
    g=Peninfo[0]
    mr=Peninfo[1]/Peninfo[2]
    l1=Peninfo[3]
    l2=Peninfo[4]
    lx=l2/l1
    denominator=1+mr-ct1t2**2
    w1_numerator=g/l1*(st1*ct1t2-(mr+1)*st1)-w1**2/2*s2t1t2-lx*w2**2*st1t2
    w2_numerator=(1+mr)*w1**2/lx*st1t2+w2**2/2*s2t1t2-g/l2*(mr+1)*(st2+st1*ct1t2)
    temp[0]=w1
    temp[1]=w2
    temp[2]=w1_numerator/denominator
    temp[3]=w2_numerator/denominator
    return temp


def F1(U_i,dt,F,Peninfo):
    return dt*F(U_i,Peninfo)

def F2(U_i,dt,F,Peninfo):
    U_f1=U_i+F1(U_i,dt,F,Peninfo)/2
    return dt*F(U_f1,Peninfo)

def F3(U_i,dt,F,Peninfo):
    U_f2=U_i+F2(U_i,dt,F,Peninfo)/2
    return dt*F(U_f2,Peninfo)

def F4(U_i,dt,F,Peninfo):
    U_f3=U_i+F3(U_i,dt,F,Peninfo)
    return dt*F(U_f3,Peninfo)
    
def RK4(dt,Tmax,F,U_0,Peninfo):
    t=np.arange(0,Tmax,dt)
    U=np.zeros((np.size(t),4))
    U[0]=U_0
    for i in range(1,np.size(t)):
        U[i]=U[i-1]+F1(U[i-1],dt,F,Peninfo)/6+2/6*(F2(U[i-1],dt,F,Peninfo)+F3(U[i-1],dt,F,Peninfo))+F4(U[i-1],dt,F,Peninfo)/6
    return t,U



