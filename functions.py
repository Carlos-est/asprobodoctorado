# def suma (a):
#     b= 3
#     return a + b

# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 01:04:28 2021

@author: JeanCarlos
"""
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import numpy as np

def NroHojas():

    sqlEngine = create_engine("mysql+pymysql://" + "labsacco_dia" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" +"labsacco_banano")
    dbConnection = sqlEngine.connect()

    try:
        df_data = pd.read_sql("select * from VARIABLES_DIA_ASPROBO", dbConnection)
        print("Se importo la base de datos correctamente.")
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    finally:
        dbConnection.close()
        print("MySQL conexion terminada extraccion de dato")


    #df_data = pd.read_csv("pretratamiento.csv")
    #df_data = df_data.drop('index', axis=1)
    GD_calculo = df_data['GDD']
    fecha = df_data['Fecha_D']




    GDA14 = np.array(GD_calculo[-14:]).sum()
    GDA28 = np.array(GD_calculo[-28:]).sum()
    nHojas14 = GDA14/108
    nHojas28 = GDA28/108
    return nHojas14, nHojas28



def GDA_backward():

    sqlEngine = create_engine("mysql+pymysql://" + "labsacco_dia" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" +"labsacco_banano")
    dbConnection = sqlEngine.connect()

    try:
        df_data = pd.read_sql("select * from VARIABLES_DIA_ASPROBO", dbConnection)
        print("Se importo la base de datos correctamente.")
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    finally:
        dbConnection.close()
        print("MySQL conexion terminada extraccion de dato")

    #df_data = df_data.drop('index', axis=1)
    GD_calculo = df_data['GDD']
    fecha = df_data['Fecha_D']

    print('Calculo de GDA al día de hoy.')
    
    GDA = 0
    i = len(fecha)
    while (GDA<900 and i>=1):
        GDA += GD_calculo[i-1]
        i += -1
    
    nSemanas = int((len(fecha)-i-1)/7)
    print("Se han acumulado","{:.2f}".format(GDA), "desde la fecha", fecha[i], "al dia de hoy.")
    print("Le ha tomado", nSemanas, "semanas.")
    return GDA, fecha[i], nSemanas
#GDA_backward()



def GDA_forward(fec):
    
    from sqlalchemy import create_engine
    import pandas as pd
    from datetime import datetime, timedelta
    
    sqlEngine = create_engine("mysql+pymysql://" + "labsacco_dia" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" +"labsacco_banano")
    dbConnection = sqlEngine.connect()
    
    try:
        df_data = pd.read_sql("select * from VARIABLES_DIA_AGROSAVIA", dbConnection)
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    finally:
        dbConnection.close()
    
    fec_0 = datetime.strptime(fec, '%d/%m/%Y')
    fec = datetime.strptime(fec, '%d/%m/%Y')
    
    if fec.month < 10:
        fec = str(fec.day)+'/0'+str(fec.month)+'/'+str(fec.year)
    else:
        fec = str(fec.day)+'/'+str(fec.month)+'/'+str(fec.year)
    GD_calculo = df_data['GDD']
    fecha = df_data['Fecha_D']
    i = df_data.loc[df_data.Fecha_D == fec].index[0]
    GDA = 0
    cont = 0
    
    while (i<=len(fecha)-1):
        cont += 1
        GDA += GD_calculo[i]
        i += 1
        if GDA > 900:
            break
    if GDA < 900:
        GDA_restantes = 900 - GDA
        promGDA = GDA/cont
        estimacion = GDA_restantes/promGDA
        fec_final = fec_0 + timedelta(cont+estimacion)
        fec_final_str = fec_final.strftime("%d/%m/%Y")
        print("Se han acumulado","{:.2f}".format(GDA), "desde la fecha", fec)
        print("Fecha estimada para completar los 900 GDA:", fec_final_str)
    else:
        print("Los 900 GDA se completaron en la fecha", fecha[i])
        fec_final = datetime.strptime(fecha[i], '%d/%m/%Y')
    
    return GDA, fec, fec_final_str



# def GDA_forward(fec):
#     sqlEngine = create_engine("mysql+pymysql://" + "labsacco_dia" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" +"labsacco_banano")
#     dbConnection = sqlEngine.connect()

#     try:
#         df_data = pd.read_sql("select * from VARIABLES_DIA_ASPROBO", dbConnection)
#         print("Se importo la base de datos correctamente.")
#     except ValueError as vx:
#         print(vx)
#     except Exception as ex:   
#         print(ex)
#     finally:
#         dbConnection.close()
#         print("MySQL conexion terminada extraccion de dato")

#     from datetime import datetime
#     fec = datetime.strptime(fec, '%d/%m/%Y')
#     if fec.month < 10:
#         fec = str(fec.day)+'/0'+str(fec.month)+'/'+str(fec.year)
#     else:
#         fec = str(fec.day)+'/'+str(fec.month)+'/'+str(fec.year)
#     #df_data = pd.read_csv("pretratamiento.csv")
#     #df_data = df_data.drop('index', axis=1)
#     GD_calculo = df_data['GDD']
#     fecha = df_data['Fecha_D']

#     from datetime import datetime, timedelta
#     print('Estimación fecha de cosecha.')
#     # fec = input('Ingrese fecha (en formato d/mm/yyyy):')
#     #fec = datetime(2021,5,1).date() #FECHA A INGRESAR DESDE LA WEB 15/09/2021  - 9/09/2021 /  -- 4/07/2021
#     #fec = "30/08/2021"
#     #print("fecha en fuctions", fechaWeb)
#     #fec = fechaWeb


#     i = df_data.loc[df_data.Fecha_D == fec].index[0]
#     print(i)
#     GDA = 0
#     cont = 0
    
#     while (i<=len(fecha)-1):
#         cont += 1
#         GDA += GD_calculo[i]
#         i += 1
#         if GDA > 900:
#             break
#     fec = datetime. strptime(fec, '%d/%m/%Y')  #A DESCOMENTAR

#     if GDA < 900:
#         GDA_restantes = 900 - GDA
#         promGDA = GDA/cont
#         estimacion = GDA_restantes/promGDA
#         fec_final = fec + timedelta(estimacion)
#         fec_str = fec.strftime("%d/%m/%Y")
#         fec_final_str = fec_final.strftime("%d/%m/%Y")
#         print("Se han acumulado","{:.2f}".format(GDA), "desde la fecha", fec_str)
#         print("Fecha estimada para completar los 900 GDA:", fec_final_str)
#     else:
#         print("Los 900 GDA se completaron en la fecha", fecha[i])
#         fec_final = datetime. strptime(fecha[i], '%d/%m/%Y')
    
#     return GDA, fec.date(), fec_final.date() 











        
# #GDA_forward()
# nHojas14, nHojas28 = numHojas()
# GDA_b, fecha_b, nSemanas = GDA_backward()
# GDA_f, fec_f, fec_final =  GDA_forward()

# variables = pd.DataFrame()
# variables['nHojas14'] = nHojas14
# variables['nHojas28'] = nHojas28
# variables['GDA_backward'] = GDA_b
# variables['fecha_backward'] = fecha_b
# variables['nSemanas_backward'] = nSemanas
# variables['GDA_forward'] = GDA_f
# variables['fecha_forward'] = fec_f
# variables['fecha_finak_forward'] = fec_final

# dbConnection = sqlEngine.connect()
# try:
#     variables.to_sql("VARIABLES", con = dbConnection, if_exists='replace')
# except ValueError as vx:
#     print(vx)
# except Exception as ex:   
#     print(ex)
# else:
#     print("Table VARIABLES created successfully.")  
# finally:
#     dbConnection.close()




def Graficas(fec):
    
    from sqlalchemy import create_engine
    from datetime import datetime, timedelta
    import pandas as pd
    
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
        
    fec_0 = datetime.strptime(fec, '%d/%m/%Y')
    fec = datetime.strptime(fec, '%d/%m/%Y')
    
    if fec.month < 10:
        fec = str(fec.day)+'/0'+str(fec.month)+'/'+str(fec.year)
    else:
        fec = str(fec.day)+'/'+str(fec.month)+'/'+str(fec.year)
        
    fecha = df_data['Fecha_D'].values
    GD_calculo = df_data['GDD'].values
    Temp = df_data['Temperatura_D'].values
    HR = df_data['Hr_D'].values
    i = df_data.loc[df_data.Fecha_D == fec].index[0]
    print(fecha)
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
            fec_final = fec_0 + timedelta(cont + estimacion)
            fec_final = fec_final.strftime("%d/%m/%Y")
        
        #data.append((fecha[i], Temp[i], HR[i], GDA))
        data.append((fecha[i], round(Temp[i],2), round(HR[i],2), round(GDA,2)))
        i += 1
    
    return data

#fec = input('Ingrese fecha (en formato d/mm/yyyy):')
#print(Graficas(fec))


# def Graficas(fec):
    
#     from sqlalchemy import create_engine
#     import pymysql
#     from datetime import datetime, timedelta
#     import pandas as pd
    
#     sqlEngine = create_engine("mysql+pymysql://" + "labsacco_dia" + ":" + "ciba15153232" + "@" + "labsac.com" + "/" +"labsacco_banano")
#     dbConnection = sqlEngine.connect()
    
#     try:
#         df_data = pd.read_sql("select * from VARIABLES_DIA_ASPROBO", dbConnection)
#         print("Se importo la base de datos correctamente.")
#     except ValueError as vx:
#         print(vx)
#     except Exception as ex:   
#         print(ex)
#     finally:
#         dbConnection.close()
#         print("MySQL conexion terminada extraccion de dato")
        
#     #df_data = df_data.drop('index', axis=1)
#     from datetime import datetime
#     fec = datetime.strptime(fec, '%d/%m/%Y')
#     if fec.month < 10:
#         fec = str(fec.day)+'/0'+str(fec.month)+'/'+str(fec.year)
#     else:
#         fec = str(fec.day)+'/'+str(fec.month)+'/'+str(fec.year)


#     fecha = df_data['Fecha_D'].values
#     GD_calculo = df_data['GDD'].values
#     Temp = df_data['Temperatura_D'].values
#     HR = df_data['Hr_D'].values
    
    
    
#     fec = datetime.strptime(fec, '%d/%m/%Y')
#     cont = 0
#     GDA = 0
#     data = []
#     i = df_data.loc[df_data.Fecha_D == fec].index[0]
    
#     while (i<=len(fecha)-1):
#         cont += 1
#         GDA += GD_calculo[i]
#         if GDA > 900:
#             estimacion = 0
#             fec_final = fecha[i]
            
#         else:
#             GDA_restantes = 900 - GDA
#             promGDA = GDA/cont
#             estimacion = int(GDA_restantes/promGDA)
#             fec_final = fec + timedelta(estimacion)
#             fec_final = fec_final.strftime("%d/%m/%Y")
        
#         data.append((fecha[i], round(Temp[i],2), round(HR[i],2), round(GDA,2)))
#         i += 1
    
#     return data

#fec = input('Ingrese fecha (en formato d/mm/yyyy):')
#print(Graficas(fec))
