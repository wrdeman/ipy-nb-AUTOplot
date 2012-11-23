#!/usr/bin/env python
from matplotlib import pyplot as plt
import pylab
import numpy as np
import bifDiag
import parseB
import parseS
import parseC
import parseD
import re


def plotb(r2, **kwargs):
    colors=['b', 'g', 'r', 'c', 'm', 'y', 'k']
    fig=plt.figure()
    fig.clf()
    ax=fig.add_subplot(111)

    n1b=parseB.parseB(r2)
    ap=n1b[0]
    c=parseC.parseC(n1b[0]) 

    xlT=False
    ylT=False
    if kwargs.get('xlim'):
        ax.set_xlim(kwargs.get('xlim'))
        xl=kwargs.get('xlim')
        xlT=True
    if kwargs.get('ylim'):
        ax.set_ylim(kwargs.get('ylim'))
        yl=kwargs.get('ylim')   
        ylT=True
    
    if kwargs.get('x'):
        x=kwargs.get('x')
        numx=re.sub('\D', '',x)
        param=x.strip(numx)
        if param=='U':
            paramx='U('+numx+')'
        if param=='P':
                paramx='PAR('+numx+')'
        if param=='L':
            paramx='L2-NORM'
        if param=='T':
            paramx='PERIOD'
    else:
        paramx='PAR(1)'

    if kwargs.get('y'):
        y=kwargs.get('y')
        numy=re.sub('\D', '',y)
        param=y.strip(numy)
        if param=='U':
            paramy='U('+numy+')'
        if param=='P':
            paramy='PAR('+numy+')'
        if param=='L':
            paramy='L2-NORM'
        if param=='T':
            paramy='PERIOD'
    else:
        paramy='L2-NORM'


    if kwargs.get('stable'):
        if  kwargs.get('stable')=='True':
            stab_dashed=True
    else:
        stab_dashed=False


    yl=kwargs.get('ylim')

    x=[]
    y=[]
    special=[]
    Branch=0
    BranchLast=0
    if ap['PT']>0:
        current=True
        last=True
    else:
        current=False
        last=False

    try:
        xvalue=c[paramx]
    except KeyError:
        xvalue=c['MAX U('+numx+')']
    try:
        yvalue=c[paramy]
    except KeyError:
        yvalue=c['MAX U('+numy+')']

    if ap['TY name']!='No Label':
        special.append([ap['TY name'],xvalue,yvalue])
    
    x.append(xvalue)
    y.append(yvalue)
    Bchange=False #branch change
    Bchecklast=ap['BR']
    Bcheckcurrent=Bchecklast
    Schange=False #changed of stability
    #also can have different calculations
    for i in range(1,len(n1b)):
        if Schange==True or Bchange==True or i==len(n1b)-1:
            color=colors[Branch%7]
            if Bchange==True:
                Branch=BranchLast+1
            if last==True and stab_dashed==True:
                ax.plot(x[0:len(x)-2],y[0:len(x)-2],color=color,ls='dotted')         
            else:
                ax.plot(x[0:len(x)-2],y[0:len(x)-2],color=color,ls='solid')
            x=[]
            y=[]
            ap=n1b[i]
            if ap['PT']>0:
                current=True
            else:
                current=False
            last=current
            Schange=False
            Bchange=False
        last=current
        Bcheckcurrent=ap['BR']
        ap=n1b[i]

        c=parseC.parseC(n1b[i]) 
        try:
            xvalue=c[paramx]
        except KeyError:
            print paramx
            xvalue=c['MAX U('+numx+')']
        try:
            yvalue=c[paramy]
        except KeyError:
            yvalue=c['MAX U('+numy+')']
        x.append(xvalue)
        y.append(yvalue)
        if ap['TY name']!='No Label':
            special.append([ap['TY name'],xvalue,yvalue])

        if ap['PT']==1 or ap['PT']==-1 or Bchecklast!=Bcheckcurrent:
            Bchange=True
#this is a fudge because sometimes ap['PT'] returned NoneType
        # this should detect when new line is plotted as first point is 1
        if ap['PT']>0:
            current=True
        else:
            current=False
        if current!=last:
            Schange=True
        BranchLast=Branch
        Bchecklast=Bcheckcurrent

    for i,sp in enumerate(special):
        if xlT==True:
            if sp[1]>xl[0] and sp[1]<xl[1]:
                sp1=sp[1]
            if ylT==True:
                if sp[2]>yl[0] and sp[2]<yl[1]:
                    sp2=sp[2]
                    ax.plot(sp[1],sp[2],ls='None',marker='x',color='k',markersize=3)
                    ax.text(sp[1],sp[2],sp[0])
            else:
                ax.plot(sp[1],sp[2],ls='None',marker='x',color='k',markersize=3)
                ax.text(sp[1],sp[2],sp[0])
        elif ylT==True:
            if sp[2]>yl[0] and sp[2]<yl[1]:
                sp2=sp[2]
                ax.plot(sp[1],sp[2],ls='None',marker='x',color='k',markersize=3)
                ax.text(sp[1],sp[2],sp[0])
        else:
            ax.plot(sp[1],sp[2],ls='None',marker='x',color='k',markersize=3)
            ax.text(sp[1],sp[2],sp[0])
    ax.set_xlabel(paramx)
    ax.set_ylabel(paramy)



def plots(sol, **kwargs):
    colors=['b', 'g', 'r', 'c', 'm', 'y', 'k']
    fig=plt.figure()
    fig.clf()
    ax=fig.add_subplot(111)

    s=parseS.parseS(sol)

    if kwargs.get('xlim'):
        ax.set_xlim(kwargs.get('xlim'))
    if kwargs.get('ylim'):
        ax.set_ylim(kwargs.get('ylim'))   

    if kwargs.get('x'):
        x=kwargs.get('x')
        numx=re.sub('\D', '',x)
        param=x.strip(numx)
        if param=='U':
            paramx='U'
        if param=='t':
            paramx='t'
    else:
        paramx='t'

    if kwargs.get('y'):
        y=kwargs.get('y')
        numy=re.sub('\D', '',y)
        param=y.strip(numy)
        if param=='U':
            paramy='U'
        if param=='t':
            paramy='t'
    else:
        paramy='U'
        numy=1

    x=[]
    y=[]
    
    for i in range(len(s)):
        sdata=s[i]
        if paramx=='t':
            xvalue=sdata['t']
        else:
            data=sdata['u']
            xvalue=sdata[int(numx)-1]
        if paramy=='t':
            yvalue=sdata['t']
        else:
            data=sdata['u']
            yvalue=sdata[int(numy)-1]

        x.append(xvalue)
        y.append(yvalue)

    ax.set_xlabel(paramx+'('+numx+')')
    ax.set_ylabel(paramy+'('+numy+')')
    ax.plot(x,y,color='k',ls='solid')


def datab(r2, **kwargs):
    n1b=parseB.parseB(r2)
    ap=n1b[0]
    c=parseC.parseC(n1b[0]) 

    xlT=False
    ylT=False
    
    if kwargs.get('x'):
        x=kwargs.get('x')
        numx=re.sub('\D', '',x)
        param=x.strip(numx)
        if param=='U':
            paramx='U('+numx+')'
        if param=='P':
                paramx='PAR('+numx+')'
        if param=='L':
            paramx='L2-NORM'
        if param=='T':
            paramx='PERIOD'
    else:
        paramx='PAR(1)'

    if kwargs.get('y'):
        y=kwargs.get('y')
        numy=re.sub('\D', '',y)
        param=y.strip(numy)
        if param=='U':
            paramy='U('+numy+')'
        if param=='P':
            paramy='PAR('+numy+')'
        if param=='L':
            paramy='L2-NORM'
        if param=='T':
            paramy='PERIOD'
    else:
        paramy='L2-NORM'

    x=[]
    y=[]
    special=[]
    Branch=0
    BranchLast=0
    if ap['PT']>0:
        current=True
        last=True
    else:
        current=False
        last=False

    try:
        xvalue=c[paramx]
    except KeyError:
        xvalue=c['MAX U('+numx+')']
    try:
        yvalue=c[paramy]
    except KeyError:
        yvalue=c['MAX U('+numy+')']

    if ap['TY name']!='No Label':
        special.append([ap['TY name'],xvalue,yvalue])
    
    x.append(xvalue)
    y.append(yvalue)
    Bchange=False #branch change
    Bchecklast=ap['BR']
    Bcheckcurrent=Bchecklast
    Schange=False #changed of stability
    #also can have different calculations
    for i in range(1,len(n1b)):
        if Schange==True or Bchange==True or i==len(n1b)-1:
            if Bchange==True:
                Branch=BranchLast+1
            # x=[]
            # y=[]
            ap=n1b[i]
            if ap['PT']>0:
                current=True
            else:
                current=False
            last=current
            Schange=False
            Bchange=False
        last=current
        Bcheckcurrent=ap['BR']
        ap=n1b[i]

        c=parseC.parseC(n1b[i]) 
        try:
            xvalue=c[paramx]
        except KeyError:
            print paramx
            xvalue=c['MAX U('+numx+')']
        try:
            yvalue=c[paramy]
        except KeyError:
            yvalue=c['MAX U('+numy+')']
        x.append(xvalue)
        y.append(yvalue)
        if ap['TY name']!='No Label':
            special.append([ap['TY name'],xvalue,yvalue])

        if ap['PT']==1 or ap['PT']==-1 or Bchecklast!=Bcheckcurrent:
            Bchange=True
#this is a fudge because sometimes ap['PT'] returned NoneType
        # this should detect when new line is plotted as first point is 1
        if ap['PT']>0:
            current=True
        else:
            current=False
        if current!=last:
            Schange=True
        BranchLast=Branch
        Bchecklast=Bcheckcurrent

    return x,y
