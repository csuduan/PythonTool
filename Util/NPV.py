import numpy
ir=0.06/12
cf=92000
n=48

a=cf/n+cf*0.0756/n
npv=0;
for i in range(1,n+1):
    npv+=a/pow(1+ir,i-1)
    #b+=a

print(npv)