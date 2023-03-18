import math
FS=1.5
tflex=100
tcis=100
done=0

b = 1.07
n6 = -2231
n5 = 5779
n4 = -5689
n3 = 2607
n2 = -589.8
n1 = 31.93
n0 = 112.4
#cortante
n7 = n6/7
n6 = n5/6
n5 = n4/5
n4 = n3/4
n3 = n2/3
n2 = n1/2
n1 = n0
n0 = -((n7*pow(b,7))+(n6*pow(b,6))+(n5*pow(b,5))+(n4*pow(b,4))+(n3*pow(b,3))+(n2*pow(b,2))+(n1*pow(b,1)))
Vmax=n0
print(n7)
print(n6)
print(n5)
print(n4)
print(n3)
print(n2)
print(n1)
print(n0)
print()

#momentofletor
n8 = n7/8
n7 = n6/7
n6 = n5/6
n5 = n4/5
n4 = n3/4
n3 = n2/3
n2 = n1/2
n1 = n0
n0 = -((n8*pow(b,8))+(n7*pow(b,7))+(n6*pow(b,6))+(n5*pow(b,5))+(n4*pow(b,4))+(n3*pow(b,3))+(n2*pow(b,2))+(n1*pow(b,1)))
Mmax=n0
print(n8)
print(n7)
print(n6)
print(n5)
print(n4)
print(n3)
print(n2)
print(n1)
print(n0)
print()

print('O vetor cortante máximo é', Vmax)
print('O momento fletor máximo é', Mmax)

TEscAl = 125
tadm = TEscAl/FS
re=12.495

while tcis > tadm or tflex > tadm:
    ri=re-1
    De=2*re
    Di=2*ri

    AreaCirAl=((pow(re,2)*math.pi)-(pow(ri,2)*math.pi))
    inerciaal=(math.pi/64)*(pow(De,4)-pow(Di,4))

    tcis=((4*(-Vmax))/(3*AreaCirAl))*((pow(re,2)+re*ri+pow(ri,2))/(pow(re,2)+pow(ri,2)))
    tflex=Mmax*1000*(re)/inerciaal

    print('A tensão admissivel', tadm)
    print('A tensão flex', tflex)
    print('A tensão cis', tcis)
    print('A seção circular', AreaCirAl)
    print('Inercia', inerciaal)

    if tcis<tadm and tflex<tadm:
        Dial=2*re

    re=re+0.00001

    massaal=b*AreaCirAl*0.00238


print('A tensão flex', tflex,'A tensão cis', tcis ,'A tensão admissivel', tadm, 'Diametro externo', Dial, 'Massa:', massaal)
