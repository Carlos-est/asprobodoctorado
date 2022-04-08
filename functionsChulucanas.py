"""
Created on Thu Sep 30 11:33:12 2021

@author: JeanCarlos
"""

def numHojas(fec):
    from sqlalchemy import create_engine
    import pandas as pd
    from datetime import datetime
   
    sqlEngine = create_engine("mysql+pymysql://" + "labsacco_dia" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" +"labsacco_banano")
    dbConnection = sqlEngine.connect()
    
    try:
        df_data = pd.read_sql("select * from VARIABLES_DIA_ASPROBO", dbConnection)
        #print("Se importo la base de datos correctamente.")
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    finally:
        dbConnection.close()
        #print("MySQL conexion terminada extraccion de dato")
    fec = datetime.strptime(fec, '%d/%m/%Y')
    if fec.month < 10:
        fec = str(fec.day)+'/0'+str(fec.month)+'/'+str(fec.year)
    else:
        fec = str(fec.day)+'/'+str(fec.month)+'/'+str(fec.year)
    #fec = str(fec.day)+'/'+str(fec.month)+'/'+str(fec.year)
    #fec = fec.strftime("%d/%m/%Y")
    
    GD_calculo = df_data['GDD']
    fecha = df_data['Fecha_D']
    Temp = df_data['Temperatura_D'].values
    i = df_data.loc[df_data.Fecha_D == fec].index[0]
    cont = 0
    GDA = 0
    data = []
    
    while (i<=len(fecha)-1):
        cont += 1
        GDA += GD_calculo[i]       
        data.append((fecha[i], round(Temp[i],1), round(GDA,1)))
        i += 1
    
    nHojas = GDA/108
    return nHojas, data
#fec = input('Ingrese fecha (en formato d/mm/yyyy):')
#print(numHojas(fec))

def GDA_backward(fec):
    from sqlalchemy import create_engine
    import pandas as pd
    from datetime import datetime

    sqlEngine = create_engine("mysql+pymysql://" + "labsacco_dia" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" +"labsacco_banano")
    dbConnection = sqlEngine.connect()
    
    try:
        df_data = pd.read_sql("select * from VARIABLES_DIA_ASPROBO", dbConnection)
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    finally:
        dbConnection.close()
    
    fec = datetime.strptime(fec, '%d/%m/%Y')
    #fec = str(fec.day)+'/'+str(fec.month)+'/'+str(fec.year)
    #fec = fec.strftime("%d/%m/%Y")
    if fec.month < 10:
        fec = str(fec.day)+'/0'+str(fec.month)+'/'+str(fec.year)
    else:
        fec = str(fec.day)+'/'+str(fec.month)+'/'+str(fec.year)


    GD_calculo = df_data['GDD']
    fecha = df_data['Fecha_D'].values
    Temp = df_data['Temperatura_D'].values
    #i = len(fecha) - 1
    i = df_data.loc[df_data.Fecha_D == fec].index[0]
    GDA = 0
    data = []
    while (GDA<900 and i>=1):
        GDA += GD_calculo[i]
        data.append((fecha[i], round(Temp[i],1), round(GDA,1)))
        i += -1

    nSemanas = int((len(fecha)-i)/7)
    # print("Se han acumulado","{:.2f}".format(GDA), "desde la fecha", fecha[i], "al dia de hoy.")
    # print("Le ha tomado", nSemanas, "semanas.")
    return round(GDA,1), fecha[i+1], nSemanas, data

def GDA_forward(fec):
    from sqlalchemy import create_engine
    import pandas as pd
    from datetime import datetime, timedelta
    
    sqlEngine = create_engine("mysql+pymysql://" + "labsacco_dia" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" +"labsacco_banano")
    dbConnection = sqlEngine.connect()
    
    try:
        df_data = pd.read_sql("select * from VARIABLES_DIA_ASPROBO", dbConnection)
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    finally:
        dbConnection.close()
    
    fec = datetime.strptime(fec, '%d/%m/%Y')
    #fec = str(fec.day)+'/'+str(fec.month)+'/'+str(fec.year)
    #fec = fec.strftime("%d/%m/%Y")
    if fec.month < 10:
        fec = str(fec.day)+'/0'+str(fec.month)+'/'+str(fec.year)
    else:
        fec = str(fec.day)+'/'+str(fec.month)+'/'+str(fec.year)

        
    GD_calculo = df_data['GDD']
    fecha = df_data['Fecha_D']
    Temp = df_data['Temperatura_D'].values
    HR = df_data['Hr_D'].values
    i = df_data.loc[df_data.Fecha_D == fec].index[0]
    fec = datetime.strptime(fec, '%d/%m/%Y')
    cont = 0
    GDA = 0
    data = []
    
    while (i<=len(fecha)-1):
        cont += 1
        GDA += GD_calculo[i]
        if GDA > 900:
            estimacion = 0
            fec_final = fecha[i]
            
        else:
            GDA_restantes = 900 - GDA
            promGDA = GDA/cont
            estimacion = int(GDA_restantes/promGDA)
            fec_final = fec + timedelta(cont + estimacion)
            fec_final = fec_final.strftime("%d/%m/%Y")
        
        data.append((fecha[i], round(Temp[i],1), round(HR[i],1), round(GDA,1)))
        i += 1

    fec = fec.strftime("%d/%m/%Y")
    return round(GDA,1), fec, fec_final, estimacion, data 

def graficas():
    from sqlalchemy import create_engine
    import pandas as pd
    from datetime import datetime
    from calendar import monthrange
    import numpy as np
   
    sqlEngine = create_engine("mysql+pymysql://" + "labsacco_dia" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" +"labsacco_banano")
    dbConnection = sqlEngine.connect()
    
    try:
        df_data = pd.read_sql("select * from VARIABLES_DIA_ASPROBO", dbConnection)
        #print("Se importo la base de datos correctamente.")
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    finally:
        dbConnection.close()
        #print("MySQL conexion terminada extraccion de dato")
    
    GD_calculo = df_data['GDD']
    fecha = df_data['Fecha_D']
    Temp = df_data['Temperatura_D'].values
    Temp_min = df_data['Temp_min_D']
    Temp_max = df_data['Temp_max_D']
    hum = df_data['Hr_D']

    today = datetime.today()
    year = today.year
    month = today.month

    num_days = int(monthrange(year, month)[1])
    #print("num_days:", num_days, type(num_days))

    fechas = np.array(fecha[-num_days:])

    temperatura = np.array(Temp[-num_days:])
    temperatura_max = np.array(Temp_max[-num_days:])
    temperatura_min = np.array(Temp_min[-num_days:])
    humedad = np.array(hum[-num_days:])

    data = []
    for k in range(num_days):
        data.append((fechas[k], round(temperatura[k],2), round(temperatura_max[k],2),round(humedad[k],2), round(temperatura_min[k],2)))
    #print("data:",data)
    return data

def DescargarDatos(año,NroSemana,CantSemana):
    from sqlalchemy import create_engine
    from operator import index
    from sqlalchemy import create_engine
    import pandas as pd
    from datetime import datetime, timedelta
    from calendar import monthrange
    import numpy as np
    import time

    sqlEngine = create_engine("mysql+pymysql://" + "labsacco_dia" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" +"labsacco_banano")
    dbConnection = sqlEngine.connect()

    try:
        df_data = pd.read_sql("select * from VARIABLES_DIA_ASPROBO", dbConnection)
        #print("Se importo la base de datos correctamente.")
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    finally:
        dbConnection.close()
        #print("MySQL conexion terminada extraccion de dato")

    ##extraemos radiacion solar


    GD_calculo = df_data['GDD']
    fecha = df_data['Fecha_D']
    Temp = df_data['Temperatura_D'].values
    Temp_min = df_data['Temp_min_D']
    Temp_max = df_data['Temp_max_D']
    hum = df_data['Hr_D']
    prec = df_data['Precipitacion_D']
    rad =df_data['Energia_solar_D']
    viento=df_data['V_viento_D']
    evapo = df_data['ET_D']

    # formato de fechas
    lunes=1


    try:
        conca= "{} {} {}".format(año, NroSemana, lunes)
        ##encontrar la fecha de cada lunes de la semana
        fecha_lunes = time.asctime(time.strptime(conca, "%Y %W %w"))

        fecha_start = datetime.strptime(fecha_lunes, '%a %b %d %H:%M:%S %Y')
        #print(fecha_start, type(fecha_start))
        fecha_end = fecha_start + timedelta(7*CantSemana-1)

        year=fecha_start.year
        mes=fecha_start.month
        dia=fecha_start.day
        fec ="{}/{}/{}".format(dia,mes,year)

        fec = datetime.strptime(fec, '%d/%m/%Y')
        if fec.month < 10:
            fec = str(fec.day)+'/0'+str(fec.month)+'/'+str(fec.year)
        else:
            fec = str(fec.day)+'/'+str(fec.month)+'/'+str(fec.year)

        i = df_data.loc[df_data.Fecha_D == fec].index[0]


        data = []
        for k in range(i,i+7*CantSemana):
            data.append((fecha[k], round(Temp_max[k],2), round(Temp_min[k],2), round(hum[k],2), round(prec[k],2), round((rad[k]/0.0864),2),round(viento[k],2) ,round(evapo[k],2)))

        df_Excel = pd.DataFrame(data, columns=["Fecha", "Max", "Min", "Humedad","Precipitacion", "Rad_Solar", "Viento","Evapo"])

        data2 = [[NroSemana, CantSemana-1, str(año)]]
        df_entradas = pd.DataFrame(data2, columns=["Semana", "cantidad", "año"])
        #Insertamos a la base de datos

        sqlEngine = create_engine( "mysql+pymysql://" + "labsacco_banano" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" + "labsacco_banano_iot" )
        dbConnection = sqlEngine.connect()
        #dbConnection2 = sqlEngine.connect()

        try:
            df_Excel.to_sql("Download", con = dbConnection, if_exists='replace', index_label="ID")
            return('tablas insertadas')
        except ValueError as vx:
            return(vx)
        except Exception as ex:   
            return(ex)
        finally:
            dbConnection.close()

    except:
        return("Datos no encontrados")