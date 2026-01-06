#GASES-FSQI
import streamlit as st
from Handbook import pesos_moleculares as pm
from Handbook.densidades import densidad_agua
import pandas as pd
from sympy import symbols, Eq,solve
from math import*
st.title("LABORATORIO DE GASES-FSQI")
st.sidebar.header("Condiciones del laboratorio")
temp=st.sidebar.number_input("Temperatura (℃):")
pres=st.sidebar.number_input("Presion (mmhg): ")

print("=============================================")
st.header("             DENSIDAD DE GASES                ")
print("=============================================")
excel=st.file_uploader("SUBA EL ARCHIVO CORRECTO :D",type=["xlsx"])
if excel is None:
    st.info("PORFAVOR SUBA EL ARCHIVO ")
else:
    df1=pd.read_excel(excel, sheet_name=0) #Tabla 1
    Pb=float(str(df1["Presion"][0]).replace("mmhg","").strip())
    Pvap=float(str(df1["Presion de vapor a temperatura ambiente"][0]).replace("mmhg","").strip())
    Temp_pera=float(str(df1["Temperatura en la pera"][0]).replace("K","").strip())
    masa_g=float(str(df1["Masa de componente orgánico"][0]).replace("g","").strip())
    vol_des_ml=float(str(df1["Volumen desalojado"][0]).replace("ml","").strip())
    Hum_rel=float(str(df1["%Humedad relativa"][0]).replace("%","").strip())
    
    #a)
    Pb_nuevo=Pb-(100-Hum_rel)*Pvap/100
    
    #b)
    V_CN=symbols("V_CN")
    P_CN=760 #mmhg
    T_CN=273.15 #K
    ecua1=Eq(V_CN*P_CN/T_CN,vol_des_ml*Pb_nuevo/Temp_pera)
    solu1=(solve(ecua1,V_CN)) #ml
    v_corr=solu1[0]
    #c)
    
    den=symbols("den")
    Pc=40880.4 #mmgh
    Tc=536.55 #K
    R=62.36 #mmgh*L/molK
    if M:    
        M=pm.masa(st.text_input("Ingrese el compuesto organico: "),(int(st.number_input("Ingrese el numero de decimales a contar para su peso molecular "))))
    else:
        st.info("Ingrese la formula quimica correcta")
    ecua2 = Eq(P_CN * M, den * R * T_CN * (1 + (9 * P_CN * Tc / (128 * Pc * T_CN)) * (1 - 6 * (Tc**2 / T_CN**2))))
    solu2=(solve(ecua2,den))
    den_teorica=solu2[0]
    #d)
    den_ex=masa_g/(v_corr*10**-3)
    #%Error exp
    Error_exp=abs(den_ex-den_teorica)/den_teorica*100
    st.write(f"a) Presion barometrica corregida: {Pb_nuevo} mmhg")
    st.write(f"b) Volumen de aire desplazado corregido(CN): {v_corr} ml")
    st.write(f"c) Densidad teorica (CN): {den_teorica} g/L")
    st.write(f"d) Densidad experimental: {den_ex} g/L")
    st.write(f"e) Error experimental: {Error_exp} %")
    #RELACION DE CAPACIDADES CALORIFICAS
    print("=============================================")
    st.header("   DETERMINACION DE CAPACIDADES CALORIFICAS    ")
    print("=============================================")
    densidad_del_agua=densidad_agua(temp)
    df2=pd.read_excel(excel, sheet_name=1)
    H1=pd.to_numeric(df2["H1"].astype(str).str.replace("cm","").str.strip()).tolist()
    H2=pd.to_numeric(df2["H2"].astype(str).str.replace("cm","").str.strip()).tolist()
    def p_total(altura):
        P_agua=float(densidad_del_agua)*1000*(9.81/100)*(760/(101.3*10**3))*float(altura)
        Ptotal=Pb+P_agua
        return Ptotal
    
    #considerando que el primer par es 10 cm
    lista_presionesP1=[]
    for i in H1:
        P=p_total(i)
        lista_presionesP1.append(P)
    lista_presionesP2=[]
    for i in H2:
        P=p_total(i)
        lista_presionesP2.append(P)
    datos={
        "P1(mmhg)/corresponde a H1":lista_presionesP1,
        "P2(mmhg)/corresponde a H2":lista_presionesP2
    }
    df3=pd.DataFrame(datos, index=["Desnivel: 10 cm","Desnivel: 15cm","Desnivel: 20 cm","Desnivel: 25cm"])
    
    st.dataframe(df3)
    #PARA HALLAR EL Y
    print("CAPACIDADES  CALORIFICAS")
    lista_y=[]
    for i,j in zip(lista_presionesP1,lista_presionesP2):
        y=(log(i)-log(Pb))/(log(i)-log(j))
        lista_y.append(y)
    datos2=lista_y
    df4=pd.DataFrame(datos2,index=["Y1","Y2","Y3","Y4"]).T
    
    st.dataframe(df4,hide_index=True)
    
    #yprom
    Y_promedio=sum(lista_y)/len(lista_y)
    R=8.314 #J/mol*K
    CV=symbols("CV")
    #Y=CP/CV
    ecua3=Eq(Y_promedio,(CV+R)/CV)
    solu3=solve(ecua3,CV)
    #EXPERIMENTALES
    CV=solu3[0]
    CP=CV+R
    #TEORICOS
    Y_teorico=1.4
    CV_T=symbols("CV_T")
    ecua4=Eq(Y_teorico,(CV_T+R)/CV_T)
    solu4=solve(ecua4,CV_T)
    CV_teorico=solu4[0]
    CP_teorico=CV_teorico+R
    #ERRORESS
    E_Y=abs(Y_teorico-Y_promedio)*100/Y_teorico
    E_CV=abs(CV_teorico-CV)*100/CV_teorico
    E_CP=abs(CP_teorico-CP)*100/CP_teorico
    st.header("RESULTADOS")
    
    df5=pd.DataFrame({
        "Teorico":[Y_teorico,CV_teorico,CP_teorico],
        "Experimental":[Y_promedio,CV,CP],
        "Error":[E_Y,E_CV,E_CP]
    },index=["Y","CV","CP"])
    
    st.dataframe(df5)









