import streamlit as st
from Handbook.pesos_moleculares import masa 
import pandas as pd
import numpy as np
st.header("PREPARACIÓN DE SOLUCIONES")
tab1,tab2,tab3,tab4=st.tabs(["Cálculos","Estadistica","Formulas","Rxns"])
with tab1:
    with st.expander("EDTA"):
        v1,pesar=st.columns(2)
        with v1:
            E_N=st.number_input("Ingrese la concentración de EDTA(M),", min_value=0.0, step=0.01)
            V1=st.number_input("Ingrese el volumen de la solución (ml)", min_value=0.0, step=0.01)
            M=masa("C10H14N2Na2O8(H2O)2",4)
            st.write("La masa molar del EDTA es:",M,"g/mol")
        with pesar:
            masa_EDTA=E_N*(V1/1000)*M
            st.write("La masa de EDTA necesaria para preparar la solución es:",f"{masa_EDTA:.4f} g")
    with st.expander("CaCO3", expanded=True):
        v2,pesar2=st.columns(2)
        with v2:
            C_N=st.number_input("Ingrese la concentración de CaCO3(M)", min_value=0.0, step=0.01)
            V2=st.number_input("Ingrese el volumen de la solución (ml)", min_value=0.0, step=0.01,key="CaCO3")
            M2=masa("CaCO3",4)
            st.write(f"La masa molar del CaCO3 es: {M2:.4f} g/mol")
        with pesar2:
            masa_CaCO3=C_N*(V2/1000)*M2
            st.write(f"La masa de CaCO3 necesaria para preparar la solución es: {masa_CaCO3:.4f} g")

    st.subheader("TITULACION DE EDTA CON CaCO3")
    st.markdown("**En el Erlenmeyer:**")
    st.text("1. Colocar  10 ml de solucion de CaCO3")
    st.text("2. Añadir solucion buffer pH para que sea básico")
    st.text("3. Agregar indicador NET")

    #titulacion de EDTA con CaCO3

    with st.expander("Valoración de EDTA con CaCO3", expanded=True):
        val,cteo=st.columns(2)
        with val:
            t2=st.number_input("¿Cuantas valorizaciones realizará?",key="titulacionAgNO3")
        with cteo:
            EDTA_C=st.number_input("Ingrese la concentración teorica de la solución de EDTA(M)", min_value=0.0, step=0.01,key="titulacionAgNO3_EDTA")
    va=int(t2)
    nva=(t2-va)*100
    if nva>0:
        st.warning("INGRESE UN NUMERO ENTERO")
    elif va>0:
        if EDTA_C:
            st.subheader("Valoracion de EDTA con CaCO3")
            if "df3" not in st.session_state or len(st.session_state.df3) != int(t2):
                st.session_state.df3=pd.DataFrame({
                    "Volumen gastado(ml)":[0.0]*int(t2),
                    "Gramos CaCO3":[0.0]*int(t2),
                    "Concentracion corregida(N)":[0.0]*int(t2),
                    "%_ERROR CONCENTRACION":[0.0]*int(t2)

                })
            df3=st.data_editor(st.session_state.df3,num_rows="fixed",disabled=["Concentracion corregida(N)","%_ERROR CONCENTRACION"],hide_index=True,key="titulacion_EDTA_df")
            if st.button("Calcular",key="calcular_caco3"):
                for i in range(int(t2)):
                    V_gastado=df3.loc[i,"Volumen gastado(ml)"]
                    gramos_CaCO3=df3.loc[i,"Gramos CaCO3"]
                    N_corregida=gramos_CaCO3/(M2*V_gastado/1000)
                    df3.loc[i,"Concentracion corregida(N)"]=N_corregida
                    error_conc=abs((EDTA_C-N_corregida)/EDTA_C)*100
                    df3.loc[i,"%_ERROR CONCENTRACION"]=error_conc
                st.session_state.df3=df3
                st.session_state.promedio_EDTA = df3["Concentracion corregida(N)"].mean()
                st.session_state.calculado = True
            if st.session_state.get("calculado", False):
                promedio = st.session_state.promedio_EDTA
                C_EDTA=promedio
                st.markdown(f"◾La concentración corregida de la solución de EDTA es: {C_EDTA:.4f} M")      
                error_conc_final=abs((EDTA_C-C_EDTA)/EDTA_C)*100
                st.markdown(f"◾El error porcentual de la concentración corregida es: {error_conc_final:.2f} %")
                #dureza dela gua
                st.subheader("DUREZA  TOTAL DEL AGUA")
                t=st.number_input("¿Cuantas muestras analizará",key="dureza_total")
                v=int(t)
                nv=(t-v)*100
                if nv>0:
                    st.warning("INGRESE UN NUMERO ENTERO")
                elif v>0:
                    st.subheader("DUREZA TOTAL")
                    st.text("1. Colocar la muestra de agua")
                    st.text("2. Añadir solucion buffer pH 1o")
                    st.text("3. Agregar indicador NET")
                    if "df4" not in st.session_state or len(st.session_state.df4)       != int(v):
                        st.session_state.df4=pd.DataFrame({
                        "Volumen de EDTA(ml)":[0.0]*int(v),
                        "Volumen de Agua(ml)":[0.0]*int(v),
                        "mg CaCO3":[0.0]*int(v),
                        "Dureza Total(ppm)":[0.0]*int(v)
                        })
                    df4=st.data_editor(st.session_state.df4,num_rows="fixed",disabled=["mg CaCO3","Dureza Total(ppm)"],hide_index=True,key="dureza_total_df")
                if st.button("Calcular dureza total",key="calcular_dureza_total"):
                    for i in range(int(v)):
                        V_EDTA=df4.loc[i,"Volumen de EDTA(ml)"]
                        V_muestra=df4.loc[i,"Volumen de Agua(ml)"]
                        W_Ca=C_EDTA*M2*V_EDTA
                        df4.loc[i,"mg CaCO3"]=W_Ca
                        dureza_total = W_Ca / (V_muestra / 1000)
                        df4.loc[i,"Dureza Total(ppm)"]=dureza_total
                    st.session_state.df4=df4
                                #otras unidades:  
                    ppm=np.array(df4["Dureza Total(ppm)"])
                    gfrances=np.array(df4["Dureza Total(ppm)"])*0.1
                    galeman=np.array(df4["Dureza Total(ppm)"])*0.056
                    df_nuevo=pd.DataFrame({
                        "PPM":ppm,
                        "GRADOS FRANCESES(°F)":gfrances,
                        "GRADOS ALEMANES(°A)":galeman    
                            })
                    st.subheader("Dureza Total en otras unidades")      
                    st.dataframe(df_nuevo)
                        
                st.header("DUREZA CALCICA")
                cal=st.number_input("¿Cuantas muestras analizará?",key="dureza_calcica")
                if cal>0:
                    st.subheader("Dureza Calcica")
                    st.text("1. Colocar la muestra de agua")
                    st.text("2. Añadir NaOH para obtener Mg(OH)2, siendo un precipitado")
                    st.text("3. Añadir Murexida")
                    if "df5" not in st.session_state or len(st.session_state.df5) != int(cal):
                        st.session_state.df5=pd.DataFrame({
                            "Volumen de EDTA(ml)":[0.0]*int(cal),
                            "Volumen de Agua(ml)":[0.0]*int(cal),
                            "mg CaCO3":[0.0]*int(cal),
                            "Dureza Calcica(ppm)":[0.0]*int(cal)
                                })
                    df5=st.data_editor(st.session_state.df5,num_rows="fixed",disabled=["mg CaCO3","Dureza Calcica(ppm)"],hide_index=True,key="dureza_calcica_df")
                    if st.button("Calcular dureza calcica",key="calcular_dureza_calcica"):
                        for i in range(int(cal)):
                            V_EDTA=df5.loc[i,"Volumen de EDTA(ml)"]
                            V_muestra=df5.loc[i,"Volumen de Agua(ml)"]
                            W_Ca=C_EDTA*M2*V_EDTA
                            df5.loc[i,"mg CaCO3"]=W_Ca
                            dureza_calcica=W_Ca*1000/V_muestra
                            df5.loc[i,"Dureza Calcica(ppm)"]=dureza_calcica
                        st.session_state.df5=df5
                                #otras unidades:  
                        ppm=np.array(df5["Dureza Calcica(ppm)"])        
                        gfrances=np.array(df5["Dureza Calcica(ppm)"])*0.1
                        galeman=np.array(df5["Dureza Calcica(ppm)"])*0.056
                        df_calcico=pd.DataFrame({
                                    "PPM":ppm,
                                    "GRADOS FRANCESES(°F)":gfrances,
                                    "GRADOS ALEMANES(°A)":galeman    
                                }) 
                        st.subheader("Dureza Calcica en otras unidades")      
                        st.dataframe(df_calcico.style.format({"PPM":"{:.2f}","GRADOS FRANCESES(°F)":"{:.2f}","GRADOS ALEMANES(°A)":"{:.2f}"}))
with tab2:
    st.title("📊 ANÁLISIS ESTADÍSTICO")
    st.header("TITULACION DE EDTA")

    if st.session_state.get("df3") is not None and "Concentracion corregida(N)" in st.session_state.df3.columns:
        df_val = st.session_state.df3
        media = st.session_state.promedio_EDTA
        n = len(df_val)
        
        # Cálculos Estadísticos
        desviacion_estandar = df_val["Concentracion corregida(N)"].std()
        coeficiente_variacion = (desviacion_estandar / media) * 100 if media > 0 else 0
        
        # Incertidumbre
        incertidumbre_estandar = desviacion_estandar / np.sqrt(n)
        expandida = 2 * incertidumbre_estandar

        # Mostrar métricas principales en columnas para que se vea mejor
        col1, col2, col3 = st.columns(3)
        col1.metric("Media (M)", f"{media:.4f}")
        col2.metric("Desv. Estándar", f"{desviacion_estandar:.4f}")
        col3.metric("Coeficiente de Variación. (%)", f"{coeficiente_variacion:.2f}%")

        st.divider()
        
        st.subheader("Incertidumbre de la Medición")
        st.info("Se determinó la incertidumbre aleatoria basada en las repeticiones realizadas.")
        
        # Explicación de fórmulas
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**1. Incertidumbre estándar:**")
            st.latex(r"u = \frac{s}{\sqrt{n}}")
        with col_b:
            st.write("**2. Incertidumbre expandida (k=2):**")
            st.latex(r"U = k \cdot u")

        # RESULTADO FINAL IMPACTANTE
        st.subheader("Reporte de Concentración Real")
        # Formato: Valor +- Incertidumbre
        resultado_texto = f"{media:.4f} \pm {expandida:.4f}"
        st.latex(r"M_{EDTA} = " + resultado_texto + r" \text{ M}")
        
        st.success(f"Con un nivel de confianza del 95%, la concentración real del EDTA se encuentra entre **{(media - expandida):.4f} M** y **{(media + expandida):.4f} M**.")
    st.header("DUREZA TOTAL DEL AGUA EN PPM")
    if st.session_state.get("df4") is not None and "Dureza Total(ppm)" in st.session_state.df4.columns:
        df_dureza = st.session_state.df4
        media_dureza = df_dureza["Dureza Total(ppm)"].mean()
        desviacion_estandar_dureza = df_dureza["Dureza Total(ppm)"].std()
        coeficiente_variacion_dureza = (desviacion_estandar_dureza / media_dureza) * 100 if media_dureza > 0 else 0
        
        # Incertidumbre
        n_dureza = len(df_dureza)
        incertidumbre_estandar_dureza = desviacion_estandar_dureza / np.sqrt(n_dureza)
        expandida_dureza = 2 * incertidumbre_estandar_dureza

        # Mostrar métricas principales en columnas para que se vea mejor
        col1, col2, col3 = st.columns(3)
        col1.metric("Media (ppm)", f"{media_dureza:.2f}")
        col2.metric("Desv. Estándar", f"{desviacion_estandar_dureza:.2f}")
        col3.metric("Coeficiente de Variación. (%)", f"{coeficiente_variacion_dureza:.2f}%")

        st.divider()
        
        st.subheader("Incertidumbre de la Medición")
        st.info("Se determinó la incertidumbre aleatoria basada en las repeticiones realizadas.")
        
        # Explicación de fórmulas
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**1. Incertidumbre estándar:**")
            st.latex(r"u = \frac{s}{\sqrt{n}}")
        with col_b:
            st.write("**2. Incertidumbre expandida (k=2):**")
            st.latex(r"U = k \cdot u")
        # RESULTADO FINAL IMPACTANTE
        st.subheader("Reporte de Dureza Total Real")
        resultado_texto = f"{media_dureza:.2f} \pm {expandida_dureza:.2f}"
        st.latex(r"D_{Total} = " + resultado_texto + r" \text{ ppm}")
    st.header("DUREZA CALCICA DEL AGUA EN PPM")
    if st.session_state.get("df5") is not None and "Dureza Calcica(ppm)" in st.session_state.df5.columns:
        df_calcica = st.session_state.df5
        media_calcica = df_calcica["Dureza Calcica(ppm)"].mean()
        desviacion_estandar_calcica = df_calcica["Dureza Calcica(ppm)"].std()
        coeficiente_variacion_calcica = (desviacion_estandar_calcica / media_calcica) * 100 if media_calcica > 0 else 0
        
        # Incertidumbre
        n_calcica = len(df_calcica)
        incertidumbre_estandar_calcica = desviacion_estandar_calcica / np.sqrt(n_calcica)
        expandida_calcica = 2 * incertidumbre_estandar_calcica

        # Mostrar métricas principales en columnas para que se vea mejor
        col1, col2, col3 = st.columns(3)
        col1.metric("Media (ppm)", f"{media_calcica:.2f}")
        col2.metric("Desv. Estándar", f"{desviacion_estandar_calcica:.2f}")
        col3.metric("Coeficiente de Variación. (%)", f"{coeficiente_variacion_calcica:.2f}%")

        st.divider()
        
        st.subheader("Incertidumbre de la Medición")
        st.info("Se determinó la incertidumbre aleatoria basada en las repeticiones realizadas.")
        
        # Explicación de fórmulas
        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**1. Incertidumbre estándar:**")
            st.latex(r"u = \frac{s}{\sqrt{n}}")
        with col_b:
            st.write("**2. Incertidumbre expandida (k=2):**")
            st.latex(r"U = k \cdot u")
        
        # RESULTADO FINAL IMPACTANTE
        st.subheader("Reporte de Dureza Cálcica Real")
        resultado_texto = f"{media_calcica:.2f} \pm {expandida_calcica:.2f}"
        st.latex(r"D_{Calcico} = " + resultado_texto + r" \text{ ppm}")
with tab3:
    st.title("📐 FORMULAS QUÍMICAS")
    st.subheader("Cálculo de masa para preparar soluciones")
    st.latex(r"m = C \cdot V \cdot M")
    st.markdown("- **m**: masa a pesar (g)")
    st.markdown("- **C**: concentración deseada (M)")
    st.markdown("- **V**: volumen de la solución (L)")
    st.markdown("- **M**: masa molar del soluto (g/mol)")
    st.subheader("Cálculo de concentración corregida en titulaciones")
    st.latex(r"N = \frac{m}{M \cdot V_{gastado}}")
    st.markdown("- **N**: concentración corregida (M)")
    st.markdown("- **m**: masa del soluto (g)")
    st.markdown("- **M**: masa molar del soluto (g/mol)")           
    st.markdown("- **V_{gastado}**: volumen de titulante gastado (L)")
    st.subheader("Cálculo de dureza total en ppm")  
    st.latex(r"D_{Total} = \frac{m_{CaCO3}}{V_{muestra}} \cdot 10^6")
    st.markdown("- **D_{Total}**: dureza total (ppm)")
    st.markdown("- **m_{CaCO3}**: masa de CaCO3 equivalente (g)")
    st.markdown("- **V_{muestra}**: volumen de la muestra de agua (L)")
    st.subheader("Cálculo de dureza cálcica en ppm")
    st.latex(r"D_{Calcico} = \frac{m_{CaCO3}}{V_{muestra}} \cdot 10^6")
    st.markdown("- **D_{Calcico}**: dureza cálcica (ppm)")  
    st.markdown("- **m_{CaCO3}**: masa de CaCO3 equivalente (g)")
    st.markdown("- **V_{muestra}**: volumen de la muestra de agua (L)")
    st.subheader("Conversion a unidades diferentes de ppm")
    st.markdown("PPM a Grados Franceses")
    st.latex(r"°F = \frac{D_{Total ppm}}{10}")
    st.markdown("PPM a Grados Alemanes")
    st.latex(r"°A = \frac{D_{Total ppm}}{17.86}")
with tab4:
    st.title("⚗️ REACCIONES QUÍMICAS")
    st.subheader("Reacción de EDTA con CaCO3")
    st.latex(r"CaCO_3 + H_2O + CO_2 + EDTA^{4-} \rightarrow CaEDTA^{2-} + HCO_3^-")
    st.markdown("- El EDTA forma un complejo con el ion calcio, permitiendo su titulación.")
    st.text("🟥Coloracion inicial: Rojo Vino o Rojo Grosella")
    st.text("🟦Coloracion final: Azul")


    st.subheader("Reacción para determinar dureza total del agua")
    st.latex(r"Ca^{2+} + Mg^{2+} + 2OH^- \rightarrow Ca(OH)_2 \downarrow + Mg(OH)_2 \downarrow")
    st.markdown("- Se precipitan los hidróxidos de calcio y magnesio, permitiendo la titulación del exceso de EDTA.")
    st.text("🟥Coloracion inicial: Rojo Vino o Rojo Grosella")
    st.text("🟦Coloracion final: Azul")
    st.subheader("Reacción para determinar dureza cálcica del agua")
    st.latex(r"Mg^{2+} + 2OH^- \rightarrow Mg(OH)_2 \downarrow")
    st.markdown("- Se precipita el hidróxido de magnesio y queda solo el calcio  a un pH de 12-13 , en el que no precipita, haciendo que la Murexida se una a los iones de Calcio")    
    st.text("💗Coloracion inicial: Rosado o Rojizo")
    st.text("🪻Coloracion final: Violeta")     

    




