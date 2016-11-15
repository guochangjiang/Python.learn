from Empates import Empates
class Pokar(Empates):
    def __init__(self,lista):      
        self.lidic=[self.genediccn(lista),self.genedicct(lista)]
    def genediccn(self,lista):
        dicc={}
        for i in lista:
            p=i.nivel in dicc
            if p:
                dicc[i.nivel]=dicc[i.nivel]+1
            else:
                dicc[i.nivel]=1
        return dicc
    def genedicct(self,lista):
        dicc={}
        for i in lista:
            p=i.tipo in dicc
            if p:
                dicc[i.tipo]=dicc[i.tipo]+1
            else:
                dicc[i.tipo]=1
        return dicc
    def parejasotrioypokar(self,val):
        ban=False
        for i,v in self.lidic[0].iteritems():
            if v==val:
                ban=True
                break
        return ban
    def doblesparejas(self):
        ban,cont=False,0
        for i,v in self.lidic[0].iteritems():
            if v==2:
                cont=cont+1
                if cont==2:
                    ban=True
                    break
        return ban
    def full(self):
        ban,cont2,cont3=False,0,0
        for i,v in self.lidic[0].iteritems():
            if v==3 and cont3==0:
                cont3=cont3+1
            elif v==2 and cont2==0:
                cont2=cont2+1
            if cont3==1 and cont2==1:
                 ban=True
                 break
        return ban
    def escalera(self,tipo):
        ban=True
        if tipo==1:
            vin=self.lidic[0].keys()[0]
        else:
            if len(self.lidic[1].keys())!=1:
                return
            elif tipo==2:
                vin=self.lidic[0].keys()[0]
            else:
                vin=10
        for v,i in self.lidic[0].iteritems():
            if vin!=v or i==2:
                ban=False
                break
            vin=vin+1
        return ban
    def color(self):
        ban=False
        if len(self.lidic[1].keys())==1:
            ban=True
        return ban
    def empates(self,nivel,listas):
        vals=[]
        if nivel==2:
            vals=self.empatepareja(listas,2)
        elif nivel==4:
            vals=self.empatepareja(listas,3)
        elif nivel==3:
            vals=self.empatepareja(listas,2)
        return vals



