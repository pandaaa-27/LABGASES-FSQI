import streamlit as st
from Handbook.pesos_moleculares import masa 
import pandas as pd
import numpy as np
#PREPARACION DE SOLUCIONES
tab1,tab2,tab3=st.tabs(["CÁLCULOS","FÓRMULAS","RXNS"])
with tab1:
    st.title("LABORATORIO DE VOLUMETRIA I")
    with st.expander("DATOS INICIALES"):
        col1,col2=st.columns(2)
        with col1:
            N_A_T=st.number_input("Concentracion teorica del AgNo3(ac)",value=0.1,format="%.4f")
        with col2:
            V_A_T=st.number_input("Volumen teorico del AgNo3(ac)(ml)",value=100.0,format="%.2f")

    if N_A_T>0 and V_A_T>0:
        gram_AG=N_A_T*V_A_T*masa("AgNO3",4)/1000
        #gramos teoricos de NaCl necesarios para preparar la solucion teorica
        g_NaCl_t=N_A_T*25*masa("NaCl",4)/1000
        #asumimos que el gasto de la bureta será 25 ml
        with st.expander("GRAMOS TEORICOS A MEDIR EN EL LABORATORIO"):
            ag,na=st.columns(2)
            with ag:
                st.metric(label="Gramos de AgNO3 necesarios ", value=f"{gram_AG:.4f} g")
            with na:
                st.metric(label="Gramos de NaCl necesarios ", value=f"{g_NaCl_t:.4f} g")
                st.info("Esta cantidad significa que debe exisitir un gasto de AgNO3 de 25 ml aprox")

        mp_eq_nacl=masa("NaCl",4)/1000
        st.warning(f"El peso equivalente de NaCl es: {mp_eq_nacl:.4f} g/eq")
        mp_eq_agno3=masa("AgNO3",4)/1000
        #ley de equivalencia: Eq Agno3=Eq NaCl
        st.header("Valoración de AgNO3")
        t2=st.number_input("¿Cuantas valorizaciones realizará?",key="titulacionAgNO3")
        va=int(t2)
        nva=(t2-va)*100
        if nva>0:
            st.warning("INGRESE UN NUMERO ENTERO")
        elif va>0:
            st.subheader("Valoracion de AgNO3")
            if "df3" not in st.session_state or len(st.session_state.df3) != int(t2):
                st.session_state.df3=pd.DataFrame({
                    "Volumen gastado(ml)":[0.0]*int(t2),
                    "Gramos NaCl":[0.0]*int(t2),
                    "Concentracion corregida(N)":[0.0]*int(t2),
                    "%_ERROR CONCENTRACION":[0.0]*int(t2)

                })
            df3=st.data_editor(st.session_state.df3,num_rows="fixed",disabled=["Concentracion corregida(N)","%_ERROR CONCENTRACION"],hide_index=True,key="titulacion_agno3_df")

        #correr el gasto blanco

        V_blanco=st.number_input("Ingrese el volumen gastado en el blanco(ml)",value=0.0,key="blanco")

        if st.button("Calcular",key="calcular_agno3"):
            #este indica a que vol se puede ver  el color rojizo
            #al restarlo con el v gastado se quita el exceso de AgNo3 que se usó para ver el cambio de color, y así se obtiene el volumen real gastado en la valoración
            for i in range(len(df3)):
                v_gastaAg=df3.at[i,"Volumen gastado(ml)"]
                gram_NaCl=df3.at[i,"Gramos NaCl"]
                N_real_ag=gram_NaCl/((v_gastaAg-V_blanco)*(mp_eq_nacl))
                df3.at[i,"Concentracion corregida(N)"]=N_real_ag
                error_con=abs(N_A_T-N_real_ag)/N_A_T*100
                gramos=N_real_ag*mp_eq_nacl*(v_gastaAg-V_blanco)
                df3.at[i,"Gramos NaCl"]=gramos
                df3.at[i,"%_ERROR CONCENTRACION"]=error_con
            st.session_state.df3 = df3
            st.session_state.promedio_ag = df3["Concentracion corregida(N)"].mean()
            st.session_state.calculado = True
            st.rerun()
        if st.session_state.get("calculado", False):
            promedio = st.session_state.promedio_ag
            st.info(f"La normalidad real de la solucion de AgNO3 es: {promedio:.4f} N")
            ERROR=abs(N_A_T-promedio)/N_A_T*100
            st.error(f"%_ERROR en la normalidad de AgNO3: {ERROR:.2f}%")
        #PLATA EXACTO-> NACL
        #EXCESO PLATA->ROJO LADRILLO
        #VOLUMEN USADO PARA ATRAPAR TOD EL CLORURO DE SODIO=VOLUMEN GASTADO-VOLUMEN BLANCO
            factor_correcion=promedio/N_A_T
            st.info(f"El factor de corrección es: {factor_correcion}")
            st.header("Analisis de precision")
            st.divider()
            st.subheader("Factor de correcion")
            if factor_correcion>1.0500:
                st.warning("Tu solución está muy concentrada. Probablemente pesaste de más o hubo evaporación del solvente❌")
            elif factor_correcion<0.9500:
                st.warning("Tu solución está muy diluida. Probablemente pesaste de menos o hubo errores en el aforo de la fiola.❌")
            else:
                st.success("Tu solución está dentro del rango de corrección aceptable.✅")
            datos=np.array(df3["Concentracion corregida(N)"])
            desviacion_estandar=np.std(datos,ddof=1)
            coef_variacion=(desviacion_estandar/promedio)*100
            col1,col2=st.columns(2)
            with col1:
                st.metric(label="Desviación estándar", value=f"{desviacion_estandar:.4f}")
            with col2:
                st.metric(label="Coeficiente de variación (%)", value=f"{coef_variacion:.2f}")
            if coef_variacion<1:
                st.success("La precisión de las valoraciones es buena.✅")
            else:
                st.warning("La precisión de las valoraciones es deficiente.❌")
            
            
            st.divider()
            #SUERO FISIOLOGICO
            st.header("Valoración de suero fisiológico")
            N_AG=promedio
            t=st.number_input("¿Cuantas valorizaciones realizará?",key="titulacionsuero")
            v=int(t)
            nv=(t-v)*100
            if nv>0:
                st.warning("INGRESE UN NUMERO ENTERO")
            if v>0:
                st.subheader("Suero fisiologico")
                if "df_suero" not in st.session_state or len(st.session_state.df_suero) != int(t):
                    st.session_state.df_suero=pd.DataFrame({
                        "Volumen gastado(ml)":[0.0]*int(t),
                        "NaCl(g)":[0.0]*int(t),
                        "%_g NaCl(p/v)":[0.0]*int(t),
                        "ppm NaCl":[0.0]*int(t)
                    })
                    df_suero=st.data_editor(st.session_state.df_suero,num_rows="fixed",disabled=["NaCl(g)","%_g NaCl(p/v)","ppm NaCl"],hide_index=True,key="sueroo")
                    Vneto=df_suero["Volumen gastado(ml)"]-V_blanco
                v_ali=st.number_input("Ingrese el volumen del aliquot(ml)",value=0.0,key="aliquot_suero")
                if st.button("Calcular suero",key="calcular_suero"):
                    g_NaCl=(Vneto*mp_eq_nacl)*N_AG
                    df_suero["NaCl(g)"]=g_NaCl
                    df_suero["%_g NaCl(p/v)"]=(g_NaCl/v_ali)*100 if v_ali > 0 else 0
                    df_suero["ppm NaCl"]=((g_NaCl/v_ali)*1000000) if v_ali > 0 else 0
                    st.session_state.df_suero = df_suero
                    st.session_state.calculado_suero = True
                    promedio_sero=df_suero["%_g NaCl(p/v)"].mean()
                    st.info(f"La concentración promedio de NaCl en el suero es: {promedio_sero:.4f} % p/v")
                    error_sero=abs(0.9-promedio_sero)/0.9*100
                    st.error(f"%_ERROR en la concentración de NaCl en el suero: {error_sero:.2f}%")
                    st.text("Considerando que la concentración permitida de NaCl en el suero fisiológico es del 0.9% p/v")
                    if len(df_suero)>1:
                        desviacion_estandar_sero=np.std(df_suero["%_g NaCl(p/v)"],ddof=1)
                        coef_variacion_sero=(desviacion_estandar_sero/promedio_sero)*100
                        col1,col2=st.columns(2)
                        with col1:
                            st.metric(label="Desviación estándar", value=f"{desviacion_estandar_sero:.4f}")
                        with col2:
                            st.metric(label="Coeficiente de variación (%)", value=f"{coef_variacion_sero:.2f}")
                        if coef_variacion_sero<1:
                            st.success("La precisión de las valoraciones es buena.✅")
                        else:
                            st.warning("La precisión de las valoraciones es deficiente.❌")
    with tab2:
        st.title("FÓRMULAS")
        st.subheader("Cálculo de gramos teóricos de AgNO3")
        st.latex(r"m (g) = M(mol/L) \times V (L) \times {M (g/mol)}")
        st.latex(r"N=M(mol/L) \times ɵ")
        st.subheader("Valoración de AgNO3")
        st.latex(r"Eq_{AgNO3} = Eq_{NaCl}")
        st.info("Bureta->AgNO3")
        st.info("Erlenmeyer->NaCl")
        st.latex(r"V_{real} = V_{gastado} - V_{blanco}")
        st.latex(r"N_{real} = \frac{g_{NaCl}}{V_{real} \times mp_{eq NaCl}}")
        st.text("Cálculo del error en la normalidad de AgNO3")
        st.latex(r"%_{error} = \frac{|N_{teorico}   - N_{real}|}{N_{teorico}} \times 100")
        with st.expander("Peso miliequivalente"):
            ag,na=st.columns(2)
            with ag:
                st.metric(label="Peso miliequivalente de AgNO3", value=f"{mp_eq_agno3:.4f} g/eq")                   
            with na:
                st.metric(label="Peso miliequivalente de NaCl", value=f"{mp_eq_nacl:.4f} g/eq")
        st.subheader("Factor de corrección")   
        st.latex(r"Factor de corrección = \frac{N_{real}}{N_{teorico}}")
    with tab3:
        st.title("REACCIONES QUÍMICAS")
        st.subheader("Reacción de neutralización entre AgNO3 y NaCl")
        st.latex(r"AgNO_3 (ac) + NaCl (ac) \rightarrow AgCl (s) + NaNO_3 (ac)")
        st.info("En esta reacción, el ion plata (Ag+) reacciona con el ion cloruro (Cl-) para formar un precipitado de cloruro de plata (AgCl), mientras que el ion sodio (Na+) y el ion nitrato (NO3-) permanecen en solución acuosa.")
        st.latex(r"2Ag^{+} + CrO_4^{-2} \rightarrow Ag_2CrO_4 (s)")
        st.info("En esta reacción, dos iones plata (Ag+) reaccionan con un ion cromato (CrO4^2-) para formar un precipitado de cromato de plata (Ag2CrO4).")
        st.text("He aqui la importancia de medir el volumen blanco pues, el exceso de AgNo3 indica que el color es rojo ladrillo, lo que significa que se ha formado el precipitado de cromato de plata, lo que indica que se ha pasado el punto final de la valoración.")

    




