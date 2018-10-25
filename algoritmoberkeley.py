import time


#------------------------------------- Cliente -----------------------------------#
def Cliente():
    #
    pass

def getHoraCliente1():

    #horaServidor = horaServer.split(' ') # guardo la hora del servidor en una lista

    horaUTC = time.localtime() # se define horaUTC obteniendo la hora local
    #print(horaUTC)


    desface = 20
    minutos  = int(horaUTC[3])*60 + int(horaUTC[4])+ desface # se cambia la hora a minutos con desface
    print(minutos)
    #print "minutos : "+ str(minutos)


    horaTotal = [int(minutos/60), minutos%60] #se cambian los minutos a horas
    #print "hora Cliente 1 -> " + str(horaTotal)
    

    return horaTotal #se retorna la diferencia y la hora total

#cliente1=getHoraCliente1()

def setHoraCliente1():
    pass

def getHoraCliente2():

    horaUTC = time.localtime() # se define horaUTC obteniendo la hora local
    desface = -10
    minutos  = int(horaUTC[3])*60 + int(horaUTC[4])+ desface # se cambia la hora a minutos con desface
   #print "minutos : "+ str(minutos)
    print(minutos)

    horaTotal = []
    horaTotal.append(int(minutos/60))
    horaTotal.append(minutos%60)
    #horaTotal = [int(minutos/60), minutos%60] #se cambian los minutos a horas
    #print "hora Cliente 2 -> " + str(horaTotal)
    #print(horaTotal)
    return horaTotal #se retorna la diferencia y la hora total

#cliente2=getHoraCliente2()


def setHoraCliente2():
    pass

#------------------------------------- Servidor ----------------------------------#

#Obtiene la hora del servidor
def getHoraServer():

    horaUTC = time.localtime() # se define horaUTC obteniendo el tiempo local
    horaServer = [horaUTC[3], horaUTC[4]] # se define la hora del server

    #print "Hora Server ->" +str(horaServer)

    return horaServer #se retorna la diferencia y la hora total
    

#clienteusuario=getHoraServer()  #la hora del servidor si es la del PC la de los clientes tiene el desface


#ASIGNA LA HROA DEL SERVIDOR
def setHoraServer():
    pass

def calcularDiferencias(horaCliente, horaServer):

    minutosCliente = int(horaCliente[0])*60  + int(horaCliente[1]) # se cambian las horas del cliente a minutos
    #print "minutos Cliente : "+ str(minutosCliente)

    minutosServer = int(horaServer[0])*60 + int(horaServer[1]) # se cambian las horas del server a minutos
    #print "minutos Servidor : "+ str(minutosServer)

    diferencia = minutosCliente - minutosServer #se hace la diferencia de los minutos
    #print "diferencia : "+ str(diferencia)
    #print(str(diferencia) + " "+ "esta es la diferencia")
    return str(diferencia)



def calcularHoras(diferencias, *horas):
    
    #horas = horitas.split(' ')
    print ("horas: "+str(horas))

    minutos = []
    
    i = 0
    for hora in horas:
        print(hora)
    #print (horas[i][0])
    for hora in horas:
        while(i<len(horas)+2):
            minutos.append(int(hora[i][0])*60+int(hora[i][1]))
            i += 1

    print ("minutos: "+ str(minutos))


    #calculando promedios--------------------------------
    cantidadDiferencias = len(diferencias)
    suma = 0
    for diferencia in diferencias:
        suma = suma + int(diferencia)
    promedio = suma / cantidadDiferencias
    print ("promedio : " + str(promedio))

    #calculando nuevas diferencias ----------------------
    nuevasDiferencias = []
    for diferencia in diferencias:
        nuevasDiferencias.append(promedio-int(diferencia))
    print ("nuevas Diferencias: "+ str(nuevasDiferencias))

    #calculando nuevas horas ----------------------------
    pos = 0
    nuevasHoras = []
    print(minutos)
    for nuevaDiferencia in nuevasDiferencias:

        nuevasHoras.append(minutos[pos] + int(nuevaDiferencia))
        

    print ("nuevas Horas: "+ str(nuevasHoras))

    return nuevasHoras

def obtenerHoraCliente():

    horas = []
    diferencias = [] # cadena de diferencias

    horaServer = getHoraServer() # obtiene la hora del Servidor
    print ("hora servidor : "+ str(horaServer))
    diferenciaServer = calcularDiferencias(horaServer, horaServer)
    diferencias.append(diferenciaServer)
    horas.append(str(horaServer))
    #print(str(diferenciaServer)+" "+"diferencia")

    horaCliente1 = getHoraCliente1() # obtiene la hora del Cliente 1
    print ("hora cliente 1: "+ str(horaCliente1))
    diferenciaCliente1 = calcularDiferencias(horaCliente1, horaServer) #calcula diferencia del cliente con respecto al servidor
    diferencias.append(diferenciaCliente1)
    horas.append(str(horaCliente1))


    horaCliente2 = getHoraCliente2() # obtiene la hora del Cliente 2
    print ("hora cliente 2 : "+ str(horaCliente2))
    diferenciacliente2 = calcularDiferencias(horaCliente2, horaServer) #calcula diferencia del cliente con respecto al servidor
    horaAux = [horaCliente2[0], horaCliente2[1]]
    diferencias.append(diferenciacliente2)
    horas.append(str(horaCliente2))

    #Grenerando cadena de Horas ---------------------------
    strHoras = ' '.join(horas) #
    print(strHoras + "str horas")
    bracketLeft = strHoras.replace("[", "")
    print(bracketLeft+ "bracketleft")
    bracketRight = bracketLeft.replace ("]", "")
    print(bracketRight+" bracketright")
    commas = bracketRight.replace (",", "")

    print (commas+" comas")
    hrs = commas.split(" ")
    print (hrs)
    print(horas)

    i = 0
    horas = []
    while i < len(hrs):
        hourAux = []
        hourAux.append(hrs[i])
        hourAux.append(hrs[i+1])
        horas.append(hourAux)
        i+=2
    #------------------------------------------------------
    

    print ("diferencias: "+str(diferencias))
    print(horas)
    print(diferencias)
    nuevasHoras = calcularHoras(diferencias, horas)
    print (nuevasHoras)
    nuevaHora = []
    for nuevashoras in nuevasHoras:
        hora=int(nuevashoras/60)
        minu=int(nuevashoras%60)
        print(hora, minu)
        nuevaHora.append([hora,minu])
    
obtenerHoraCliente()
