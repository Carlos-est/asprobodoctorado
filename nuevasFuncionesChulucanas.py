# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 20:01:14 2021

@author: JeanCarlos
"""

def ODE_PobThrips(PT, t, x):
    import numpy as np
    psi = 1.01403739
    rho = 0.12473843
    TempMax = 37.69901692
    TempOpt = 29.72893052
    mu = 0.17730199
    alfa1 = 0.50644651
    alfa2 = 0.15671537
    gamma = 0.06655349
    degF1 = 0.044298
    degF2 = 0.59392462
    degL = 0.24856982
    
    Temp = x[0]
    time_F1 = x[1]
    time_F2 = x[2]
    time_L = x[3]
    
    tao = (TempMax-Temp)/(TempMax-TempOpt)
    F1 = np.exp(-degF1*time_F1)
    F2 = np.exp(-degF2*time_F2)
    L = np.exp(-degL*time_L)
    
    dPT = (psi*(np.exp(rho*Temp)-np.exp(rho*TempMax - tao)) - mu - alfa1*F1 - alfa2*F2 - gamma*(L))*PT
    
    return dPT

#print('Defining Integration function...')
def IntODE(t, PT0, matriz_x):
    from scipy.integrate import odeint
    sol = PT0
    for k in range(len(t)-1):
        time1 = [t[k], t[k+1]]
        x = matriz_x[k,:]
        sol = odeint(ODE_PobThrips, sol, time1, args=(x,))
        sol = sol[-1].item()
        if sol < 0.04:
            sol = 0.04
    return sol

#print('Defining Prediccion integration function ...')
def IntPrediccion(vector_t, PT0, MATRIZ_X):
    import numpy as np
    PT_sim = []
    PT_sim.append(PT0) 
    for k in range(len(vector_t)-1):
        t = np.linspace(vector_t[k],vector_t[k+1],vector_t[k+1]-vector_t[k]+1)
        matriz_x = MATRIZ_X[vector_t[k]:vector_t[k+1],:]
        PT_sim.append(IntODE(t, PT_sim[k], matriz_x)) 
    return PT_sim


def Prediccion(fecha_F1, fecha_F2, fecha_C, ID_parcela):
    import numpy as np
    from sqlalchemy import create_engine
    import pandas as pd
    from datetime import date, timedelta, datetime
    
    
    sqlEngine = create_engine("mysql+pymysql://" + "labsacco_dia" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" +"labsacco_banano")
    dbConnection = sqlEngine.connect()
    
    try:
        df_data = pd.read_sql("SELECT * FROM VARIABLES_DIA_ASPROBO GROUP BY VARIABLES_DIA_ASPROBO.ID DESC LIMIT 60", dbConnection)
        df_Fecha = pd.read_sql("SELECT Fecha_D FROM VARIABLES_DIA_ASPROBO AS FECHA", dbConnection)
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    finally:
        dbConnection.close()
    
    ult_fecha = datetime.strptime(np.array(df_Fecha)[-1][0], '%d/%m/%Y')
    
    sqlEngine = create_engine("mysql+pymysql://" + "labsacco_banano" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" +"labsacco_banano_iot")
    dbConnection = sqlEngine.connect()
    
    try:
        ID_dato = pd.read_sql("SELECT * FROM evaluacion_plagas AS EV WHERE EV.ID_PARCELA={} GROUP BY EV.ID DESC LIMIT 1".format(ID_parcela), dbConnection)
        id_evaluacion = ID_dato['ID'][0]
        fec_t = ID_dato['FECHA_CREACION'][0].date()
        str_v = "SELECT * FROM evaluacion_plagas_detalle AS epd WHERE epd.ID_EVALUACION_PLAGAS=" + str(id_evaluacion) + " AND epd.ID_PLAGA_DETALLE IN (1,2)"
        #print("STR_V:", str_v)
        df_thrips = pd.read_sql(str_v, dbConnection)        
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    finally:
        dbConnection.close()
    fecha_evaluacion = fec_t.strftime('%d/%m/%Y')
    print("Fecha de última evaluación:", fecha_evaluacion)
    #print("fec_t:", fec_t, type(fec_t))
    PT0 = df_thrips['VALOR'].mean()*2  
    print("PT0:", PT0)
    fec_F1 = datetime.strptime(fecha_F1, '%d/%m/%Y')
    fec_F2 = datetime.strptime(fecha_F2, '%d/%m/%Y')
    fec_C = datetime.strptime(fecha_C, '%d/%m/%Y')
    fec_p = date.today() + timedelta(7)
    
    MATRIX_X = []
    #cdamos un formato en especifico a la fecha
    if fec_t.month < 10:
        fec = str(fec_t.day)+'/0'+str(fec_t.month)+'/'+str(fec_t.year)
    else:
        fec = str(fec_t.day)+'/'+str(fec_t.month)+'/'+str(fec_t.year)
    #print(fec)
    if fec_t > ult_fecha.date():
        Temp = df_data.Temperatura_D[-7:].mean()
        n_f =  (fec_p - fec_t)/timedelta(1)
    else:
        i = df_data.loc[df_data.Fecha_D == fec].ID.values[0]
        Temp = df_data.loc[df_data.ID >= i].Temperatura_D.mean()
        Temp_vector = df_data.loc[df_data.ID >= i].Temperatura_D.values
        for i in range(len(Temp_vector)):
            f_F1 = (fec_t + timedelta(i)) - fec_F1.date()
            f_F2 = (fec_t + timedelta(i)) - fec_F2.date()
            f_C = (fec_t + timedelta(i)) - fec_C.date()
            MATRIX_X.append([Temp_vector[i], f_F1/timedelta(1), f_F2/timedelta(1), f_C/timedelta(1)])
        n_f =  (fec_p - ult_fecha.date())/timedelta(1)
        
    
    for i in range(int(n_f)):
        f_F1 = (fec_p - timedelta(n_f-i)) - fec_F1.date()
        f_F2 = (fec_p - timedelta(n_f-i)) - fec_F2.date()
        f_C = (fec_p - timedelta(n_f-i)) - fec_C.date()
        MATRIX_X.append([Temp, f_F1/timedelta(1), f_F2/timedelta(1), f_C/timedelta(1)])
    
    
    MATRIX_X = np.array(MATRIX_X)
    t = np.arange(MATRIX_X.shape[0])
    
    PT_sim = IntPrediccion(t, PT0, MATRIX_X)
    j = 0
    fechas=[]
    for resultado in PT_sim:
        f = fec_t + timedelta(j)
        #print("Para la fecha: {} se predicen {:.2f} Thrips por planta".format(f, resultado))
        j += 1
        fechas.append(str(f))
    Datos=[]
    i=0
    #print("fechas:", np.shape(fechas))
    #print("PT_sim:", np.shape(PT_sim))
    for x in fechas:
        Datos.append((x,round(PT_sim[i],1)))
        i=i+1
        #print(np.shape(Datos))
        #print(np.shape(PT_sim))
    #print("Datos:", Datos, type(Datos))
    #print("fechas:",fechas , type(fechas))
    #print("predicciones:",PT_sim, type(PT_sim))
    
    return Datos,fecha_evaluacion, PT0
