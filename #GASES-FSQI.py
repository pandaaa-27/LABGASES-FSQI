import streamlit as st
from Handbook.pesos_moleculares import masa 
import pandas as pd
if 'humedad_calculada' not in st.session_state:
    st.session_state.humedad_calculada = 0.0
if 'cenizas_calculadas' not in st.session_state:
    st.session_state.cenizas_calculadas = 0.0
if 'calcio_calculado' not in st.session_state:
    st.session_state.calcio_calculado = 0.0
tab1,tab2,tab3=st.tabs(["CÁLCULOS","FÓRMULAS","RXNS"])
with tab1:
    st.title("LABORATORIO GRAVIMETRIA-CENIZAS")
    #inventario:
    st.header("DETERMINACION GRAVIMETRICA I")
    st.subheader("CALCULO DE LA HUMEDAD")
    with st.expander("DATOS INICIALES"):
        col1,col2=st.columns(2)
        with col1:
            wcrish=st.number_input("Peso del crisol o luna de reloj(g)",value=0.0000,step=0.0001,format="%.4f")
        with col2:
            wmCuesh=st.number_input("Peso del crisol+muestra(g)",value=0.0000,step=0.0001,format="%.4f")
    WMCSECOH=st.number_input("Peso del crisol+muestra seca(g)/Despues de pasar por la estufa",format="%.4f")
    if wcrish and wmCuesh:
        if WMCSECOH:
            wmsech=WMCSECOH-wcrish
            wmuhumh=wmCuesh-wcrish
            Humedad=round(abs(wmuhumh-wmsech)*100/wmuhumh,2)
            st.session_state.humedad_calculada = Humedad
            df2 = pd.DataFrame({
                "Descripción": [
                    "Peso del crisol o luna de reloj(g)", 
                    "Peso inicial de la muestra(g)", 
                    "Peso final de la muestra(g)", 
                    "% Humedad"
                ],
                "Resultado": [wcrish, wmuhumh, wmsech, Humedad]
            })
            st.table(df2.set_index("Descripción"))

    st.subheader("CALCULO DE CENIZAS")
    with st.expander("DATOS INICIALES"):
        col1,col2=st.columns(2)
        with col1:
            wcris=st.number_input("Peso del crisol(g)",value=0.0000,step=0.0001,format="%.4f")
        with col2:
            wmCues=st.number_input("Peso del crisol+muestra(g)",value=0.0000,step=0.0001,format="%.4f",key="ceniza")

    WMCSECO=st.number_input("Peso del crisol+muestra seca(g)",format="%.4f")
    if wcris and wmCues:
        if WMCSECO:
            st.subheader("RESULTADOS")
            Wmuestra=wmCues-wcris
            Wceniza=WMCSECO-wcris
            porcen_Ceniza=round(abs(Wceniza)*100/Wmuestra,4)
            st.session_state.cenizas_calculadas = porcen_Ceniza
            porcen_organico=round(100-porcen_Ceniza,4)
            df1 = pd.DataFrame({
                "Descripción": [
                    "Peso del crisol(g)", 
                    "Peso inicial de la muestra(g)", 
                    "Peso final de la muestra(g)", 
                    "% Cenizas", 
                    "% Comp. Organico"
                ],
                "Resultado": [
                    wcris, 
                    Wmuestra, 
                    Wceniza, 
                    porcen_Ceniza, 
                    porcen_organico
                ]
            })
            st.table(df1.set_index("Descripción"))
            if Wceniza:
                st.header("DETERMINACION GRAVIMETRICA II")
                st.info("Haciendo uso del residuo mineral del crisol luego de determinar las cenizas")
                #SI 500 ℃-> CaCO3
                #SI 1000℃-> CaO
                colcris,colfinal=st.columns(2)
                with colcris:
                    cris=st.number_input("Peso del crisol",min_value=0.0000,max_value=10000.0000,format="%.4f")
                with colfinal:
                    crisfinal=st.number_input("Peso final(crisol+residuo)",min_value=0.0000,max_value=10000.0000,format="%.4f")
                residuo=crisfinal-cris
                st.write("FACTOR GRAVIMETRICO ")
                compuesto = st.segmented_control(
                    "Compuesto de referencia:",
                    options=["CaCO3", "CaO"],
                    default="CaCO3"
                )
                if compuesto=="CaCO3":
                    FG=masa("Ca",4)/masa("CaCO3",4)
                else:
                    FG=masa("Ca",4)/masa("CaO",4)

                Ca=(residuo*FG)*100/Wmuestra
                st.session_state.calcio_calculado = Ca
                df3=pd.DataFrame({
                    "Descripción":[
                    "Peso inicial de la muestra(g)",
                    "Peso residuo (g)",
                    "Factor gravimetrico",
                    "% Calcio"
                    ],
                    "Resultados":[Wmuestra,Wceniza,FG,Ca]
                })
                st.table(df3.set_index("Descripción"))
                with st.expander("DETALLES"):
                    col1,col2=st.columns(2)
                    with col1:
                        st.metric(label="M molar Ca",value=f"{masa('Ca',4)} g/mol")
                    with col2:
                        if compuesto=="CaCO3":
                            st.metric(label="M molar de la cenizas",value=f"{masa('CaCO3',4)} g/mol")
                        else:
                            st.metric(label="M molar de las cenizas",value=f"{masa('CaO',4)} g/mol")

                st.header("RESUMEN DE LOS ANALISIS")

                opciones_leche = [
                    "Leche entera en polvo",
                    "Leche parcialmente descremada en polvo",
                    "Leche descremada en polvo",
                    "Leche entera en polvo instantánea",
                    "Leche parcialmente descremada en polvo instantánea",
                    "Leche descremada en polvo instantánea"
                ]
                seleccion = st.selectbox(
                    "Seleccione el tipo de producto :",
                    options=opciones_leche,
                    index=None,
                    placeholder="Elija el tipo de muestra analizada"
                )
                c,h,ca=0.0,0.0,0.0
                if seleccion=="Leche entera en polvo":
                    c=7.0
                    h=100
                    ca=1
                elif seleccion=="Leche parcialmente descremada en polvo":
                    c=8
                    h=100
                    ca=1
                elif seleccion=="Leche descremada en polvo":
                    c=9
                    h=100
                    ca=1
                elif seleccion=="Leche entera en polvo instantánea":
                    c=7
                    h=60
                    ca=1
                elif seleccion=="Leche parcialmente descremada en polvo instantánea":
                    c=8
                    h=60
                    ca=1
                else:
                    c=9
                    h=60
                    ca=1
                if st.session_state.humedad_calculada > 0:
                    df4=pd.DataFrame({
                        "%Cenizas":[st.session_state.cenizas_calculadas],
                        "%Humedad":[st.session_state.humedad_calculada],
                        "%Calcio":[st.session_state.calcio_calculado]
                    })
                    def pintar(fila, lim_c, lim_h,lim_ca):
                        estilos = [''] * len(fila)
                        
                        for i, col in enumerate(fila.index):

                                if col == "%Cenizas": lim = lim_c
                                elif col == "%Humedad": lim = lim_h
                                elif col == "%Calcio": lim = lim_ca
                                else: continue
                                if fila[col] > lim:
                                    estilos[i] = 'background-color: #EE7171; color: black; font-weight: bold;' 
                                else:
                                    estilos[i] = 'background-color: #5383C2; color: black; font-weight: bold;' 
                        return estilos
                    st.dataframe(df4.style.apply(pintar, lim_c=c, lim_h=h,lim_ca=ca, axis=1))
                    st.divider()
                    col_ley1, col_ley2, _ = st.columns([1, 1, 2])

                    with col_ley1:
                        st.markdown("🟦 **Aceptable**")
                        st.caption("Dentro de los límites")

                    with col_ley2:
                        st.markdown("🟥 **No aceptable**")
                        st.caption("Fuera de norma")
                    st.info("PARA EL ANALISIS DE RESULTADOS, LOS VALORES LIMITES SE BASARON EN EL NTP202.005")
                else:
                    df4=pd.DataFrame({
                        "%Cenizas":[st.session_state.cenizas_calculadas],
                        "%Calcio":[st.session_state.calcio_calculado]
                    })
                    def pintar(fila, lim_c,lim_ca):
                        estilos = [''] * len(fila)
                        
                        for i, col in enumerate(fila.index):

                                if col == "%Cenizas": lim = lim_c
                                elif col == "%Calcio": lim = lim_ca
                                else: continue
                                if fila[col] > lim:
                                    estilos[i] = 'background-color: #EE7171; color: black; font-weight: bold;' 
                                else:
                                    estilos[i] = 'background-color: #5383C2; color: black; font-weight: bold;' 
                        return estilos
                    st.dataframe(df4.style.apply(pintar, lim_c=c,lim_ca=ca, axis=1))
                    st.divider()
                    col_ley1, col_ley2, _ = st.columns([1, 1, 2])

                    with col_ley1:
                        st.markdown("🟦 **Aceptable**")
                        st.caption("Dentro de los límites")

                    with col_ley2:
                        st.markdown("🟥 **No aceptable**")
                        st.caption("Fuera de norma")
                    st.info("PARA EL ANALISIS DE RESULTADOS, LOS VALORES LIMITES SE BASARON EN EL NTP202.005")
with tab2:
    st.header("DETERMINACION DE LA HUMEDAD")
    st.latex(r"\%Humedad=\frac{W_{muestra\ inicial}-W_{muestra\ seca}}{W_{muestra\ inicial}} \times 100")
    st.header("DETERMINACION DE CENIZAS")
    st.text("Analito=cenizas totales")
    st.text("Las cenizas representan los residuos minerales inorganicos")
    st.latex(r"\%Cenizas=\frac{W_{cenizas}}{W_{muestra\ inicial}} \times 100")
    st.header("DETERMINACION DE CALCIO")
    st.subheader("Factor gravimetrico")
    st.latex(r"FG=\frac{Masa\ molar\ del\ analito\ deseado(Ca)}{Masa\ molar\ del\ compuesto\ pesado(CaCO3\ o\ CaO)}")
    st.text("Si 500 ℃-> CaCO3")
    st.text("Si 1000℃-> CaO")
    st.latex(r"\%Calcio=\frac{W_{precipitado} \times FG}{W_{muestra\ original}} \times 100")
    st.text("VALORES LIMITE PARA EL ANALISIS DE RESULTADOS:") 
with tab3:  
    st.header("Reacciones quimicas")
    st.subheader("I) ATAQUE ÁCIDO")
    st.latex(r"CaO_{(s)} + 2HCl_{(ac)} \rightarrow CaCl_{2(ac)} + H_{2}O_{(l)}")
    st.latex(r"CaCO_{3(s)} + 2HCl_{(ac)} \rightarrow CaCl_{2(ac)} + CO_{2(g)} \uparrow + H_{2}O_{(l)}")
    st.subheader("II) FORMACION DE OXALATO")
    st.latex(r"(NH_{4})_{2}C_{2}O_{4(ac)} \rightleftharpoons 2NH_{4(ac)}^{+} + C_{2}O_{4(ac)}^{2-}")
    st.latex(r"Ca_{(ac)}^{2+} + C_{2}O_{4(ac)}^{2-} + H_{2}O_{(l)} \xrightarrow{pH \approx 4} CaC_{2}O_{4} \cdot H_{2}O_{(s)} \downarrow")
    st.subheader("III)CALCINACION")
    st.info("A 500°C se obtiene Carbonato de Calcio (Forma de pesada en tu informe):")
    st.latex(r"CaC_{2}O_{4} \cdot H_{2}O_{(s)} \xrightarrow{500^{\circ}C} CaCO_{3(s)} + CO_{(g)} \uparrow + H_{2}O_{(g)} \uparrow")

    st.info("A temperaturas superiores (>800°C) se obtendría Óxido de Calcio:")
    st.latex(r"CaCO_{3(s)} \xrightarrow{>800^{\circ}C} CaO_{(s)} + CO_{2(g)} \uparrow") 
    
    
    
    
    
    




