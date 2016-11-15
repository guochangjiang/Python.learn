class Empates:
    def __init__(self):
        pass
    def cartaalta(self,listas):        
        print("Entro a carta alta")
        vals=[]
        print("Jugadore que estan en carta alta")
        for i in listas:
            print(i.nombre)
        print("")
        for i in listas:
            for p in i.lista:
                vals.append(p.nivel)
        vals.sort()
        valorultimo=vals[len(vals)-1]
        print("Comienza ciclo carta alta asi estan las cartas")
        for i in listas:
            print(i.nombre)
            for m in i.lista:
                print ("Nivel: "+str(m.nivel)+" Tipo: "+str(m.tipo))
            print("")
        print("")
        copialista=listas[:]
        if len(copialista)>1:
            for i in copialista:
                l=filter(lambda x:x.nivel==valorultimo,i.lista)
                print("El: "+str(i.nombre)+" se compara si tiene el valor alto "+str(valorultimo))
                if len(listas)==1:
                    print(listas[0].nombre)
                    ganador=listas[0].nombre
                    break    
                elif not l:
                    print("Este jugador no tiene la carta alta")
                    listas.remove(i)
                    if len(listas)==1:
                        break
        if len(listas)>1:
            for i in listas:
                l=filter(lambda x:x.nivel==valorultimo,i.lista)
                for mh in l:
                    i.lista.remove(mh)
            print("Termino ciclo carta alta asi quedaron las cartas")
            for i in listas:
                print(i.nombre)
                for m in i.lista:
                    print ("Nivel: "+str(m.nivel)+" Tipo: "+str(m.tipo))
                print("")
            print("")
            listas=self.cartaalta(listas)
        return listas
    def empatedoblesparejas(self,listas):
        vals=[]
        for i in listas:
            vals.append(i.diccn.keys()[i.diccn.values().index(2)])
        print(vals)

    def empatepareja(self,listas,comparar):
        vals=[]
        for i in listas:
            vals.append(i.diccn.keys()[i.diccn.values().index(comparar)])
        print(vals)
        vals.sort()
        valor=vals[len(vals)-1]
        listaregresa=[]
        for i in listas:
            print (i.diccn)
        p=filter(lambda x:x.diccn.get(valor)==comparar,listas)
        print(p)
        for i in p:
            for mm in i.lista:
                print ("Nivel: "+str(mm.nivel)+" Tipo: "+str(mm.tipo))
        if len(p)>1:
            for i in range(len(p)):
                h=filter(lambda x:x.nivel==valor,p[i].lista)
                for ii in h:
                        p[i].lista.remove(ii)
            self.cartaalta(p)
        else:
            print("Solo fue uno")
            listaregresa=p
        return listaregresa           
    