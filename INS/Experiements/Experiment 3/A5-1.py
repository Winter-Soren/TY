alp=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',' ']

def maj(a,b,c):
  lst=[a,b,c]
  a1=a0=0
  for i in lst:
    if(i==0):
      a0+=1
    else:
      a1+=1
  if(a1>a):
    return 1
  else:
    return 0


# print(maj(1,0,0))
def decimalToBinary(n):
  return "{0:b}".format(int(n))

def shiftx(x):
  n=len(x)
  t=x[13]^x[16]^x[17]^x[18]
  i=n-1
  while(i>0):
    x[i]=x[i-1]
    i-=1
  x[0]=t

def shifty(x):
  n=len(x)
  t=x[20]^x[21]
  i=n-1
  while(i>0):
    x[i]=x[i-1]
    i-=1
  x[0]=t
  
def shiftz(x):
  n=len(x)
  t=x[20]^x[21]^x[22]^x[7]
  i=n-1
  while(i>0):
    x[i]=x[i-1]
    i-=1
  x[0]=t

def keygen(a):
  xi=19
  x=[0]*xi
  yi=22
  y=[0]*yi
  zi=23
  z=[0]*zi
  x[13]=x[16]=x[17]=x[18]=0
  y[20]=y[21]=0
  z[20]=z[21]=z[22]=z[7]=0

  c=0
  c1=0
  for i in range(64):
    x[c1]=x[13]^x[16]^x[17]^x[18]^a[c]
    c+=1
    if(c1<xi-1):
      c1+=1
    else:
      c1=0
  c=0
  c1=0

  for j in range(64):
    y[c1]=y[20]^y[21]^a[c]
    c+=1
    if(c1<yi-1):
      c1+=1
    else:
      c1=0
  c=0
  c1=0
  for k in range(64):
    z[c1]=z[20]^z[21]^z[22]^z[7]^a[c]
    c+=1
    if(c1<zi-1):
      c1+=1
    else:
      c1=0

  a=[]
  
  while(c>0):
    t=maj(x[8],y[10],z[10])
    if(x[8]==t):
      shiftx(x)
    if(y[10]==t):
      shifty👍
    if(z[10]==t):
      shiftz(z)
    a.append(x[len(x)-1]^y[len(y)-1]^z[len(z)-1])
    c-=1
  return a

def encrypt(text,key):
  n=len(text)
  n1=len(key)
  i=0
  s=""
  while(i<n):
    t=decimalToBinary(alp.index(text[i]))
    s+=t
    i+=1
  n2=len(s)
  i=0
  j=0
  ctext=""
  while(i<n2):
    if(j<n1):
      temp=int(s[i])^key[j]
      ctext+=str(temp)
    else:
      temp=int(s[i])^0
      ctext+=str(temp)
    j+=1
    i+=1
  return ctext
lst=[]
a="1010100110000101000010101010101010101011101110101011101010101000"
for ch in a:
  lst.append(int(ch))
a=keygen(lst)
text="SOHAM SATISH BHOIR"
ctext=encrypt(text,a)
print("text is ",text)
print("Secret text is ",ctext)