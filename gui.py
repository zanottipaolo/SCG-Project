import streamlit as st
import pandas as pd
import plotly.express as px

# Variance analysis script
from variance_analysis import variance_analysis

st.set_page_config(page_title='SCG - Analisi scostamenti',
                   layout='centered', page_icon=':bar_chart:', initial_sidebar_state="expanded", menu_items={
                    'Get Help': 'mailto:hello@paolozanotti.dev',
                    'Report a bug': "https://github.com/zanottipaolo/SCG-Project/issues",
    })

st.title('Analisi degli scostamenti :bar_chart:')

with st.expander("Scopri di più"):
    st.write('''
    Progetto realizzato per l'esame di **Sistemi di Controllo di Gestione (A.A. 2022/2023) @ UniBg** da _Paolo Zanotti, Matteo Soldini, Silvia Bernardi e Francesco Foresti_. 
    Il codice è disponibile su [Github](https://github.com/zanottipaolo/SCG-project).

    Presi in input i dati dell'azienda (i nostri o quelli caricati dall'utente) viene eseguito uno script Python che, tramite Pandas,
    crea dei file XLSX contenenti tutti gli elementi utili per l'analisi degli scostamenti. Questi file vengono poi elaborati tramite
    Streamlit per estrapolare le informazioni più importanti da visualizzare qui nel sito.
    ''')

DATA_URL = ('export/scostamento_totale.xlsx')
data = None
result = False
uploaded_files = []
missing_files = []

# All'inizio carica i nostri dati. 
# Se l'utente vuole visualizzare i suoi dati allora può caricarli dalla sidebar.
variance_analysis()
data = pd.read_excel(DATA_URL)

# Upload files
with st.sidebar:
    required_files = [
        'Clienti.xlsx',
        'Consumi.xlsx',
        'Costo orario risorse - budget.xlsx',
        'Costo orario risorse - consuntivo.xlsx',
        'Impiego orario risorse.xlsx',
        'Tassi di cambio.xlsx',
        'Vendite.xlsx'
    ]

    st.subheader('Caricamento file :file_folder:')
    uploaded_files = st.file_uploader(
        "Carica i tuoi file xlsx (seguire il formato dei file già presenti nella cartella 'Files' su Github):", type=".xlsx", accept_multiple_files=True)

    for required_file in required_files:
        if not required_file in [uploaded_file.name for uploaded_file in uploaded_files]:
            missing_files.append(required_file)

    if len(missing_files) > 0:
        st.info('File rimanenti da caricare', icon="ℹ️")
        for missing_file in missing_files:
            st.text(missing_file)
    else:
        # Save file
        for uploaded_file in uploaded_files:
            f = open("files/" + uploaded_file.name, "wb")
            f.write(uploaded_file.read())
            f.close()

        # Ri-esegue lo script con i nuovi dati dell'utente
        try:
            variance_analysis()
            data = pd.read_excel(DATA_URL)
            st.success("Script eseguito correttamente", icon="✅")
            st.balloons()
        except:
            st.error("L'esecuzione dello script è fallita! Verifica i file caricati.", icon="⚠️")

st.write("#")

# Resoconto analisi scostamento
st.subheader('Risultati a consuntivo :dart:')

if st.checkbox("Mostra tutti i dati", key="scostamento_totale"):
    st.dataframe(data.set_index("Unnamed: 0").style.format(thousands="˙", decimal=",",
                                    precision="2"), use_container_width=True)

st.metric("MOL", f"€ {data['Consuntivo'][4]:,.2f}".replace(",", " ").replace(".", ","), "{:,.2f}".format(
    data['Consuntivo'][4] - data['Budget'][4]).replace(",", " ").replace(".", ","))

col1, col2, col3 = st.columns(3)
col1.metric("Ricavi", f"€ {data['Consuntivo'][0]:,.2f}".replace(",", " ").replace(
    ".", ","), "{:,.2f}".format(data['Consuntivo'][0] - data['Budget'][0]).replace(",", " ").replace(".", ","))
col2.metric("Costi MP", f"€ {data['Consuntivo'][2]:,.2f}".replace(",", " ").replace(
    ".", ","), "{:,.2f}".format(data['Consuntivo'][2] - data['Budget'][2]).replace(",", " ").replace(".", ","))
col3.metric("Costi risorse", f"€ {data['Consuntivo'][3]:,.2f}".replace(",", " ").replace(
    ".", ","), "{:,.2f}".format(data['Consuntivo'][3] - data['Budget'][3]).replace(",", " ").replace(".", ","))

st.write("#")

# Analisi orizzontale
st.subheader("Scostamenti orizzontali :left_right_arrow:")

scostamento_totale = pd.DataFrame({
    "Scostamento":
        data["Unnamed: 0"].values,
    "Budget":
        data["Budget"].values,
    "Mix standard":
        data["Mix standard"].values,
    "Mix effettivo":
        data["Mix effettivo"].values,
    "Consuntivo":
        data["Consuntivo"].values
}).transpose()

# serve per usare la prima riga come intestazione della tabella
scostamento_totale.columns = scostamento_totale.iloc[0]
scostamento_totale = scostamento_totale[1:]
scostamento_totale.drop('Costi MP', inplace=True, axis=1)
scostamento_totale.drop('Costi risorse', inplace=True, axis=1)

# Per il grafico non si riusciva ad usare i dati nel formato Wide di Plotly, allora tramite la funzione "melt()" 
# di Pandas sono stati trasformati nel formato Long
scostamento_totale = scostamento_totale.reset_index()
scostamento_totale = pd.melt(scostamento_totale, id_vars=[
    'index'], var_name='Scostamenti', value_name='value')
chart_scostamento_totale = px.bar(
    scostamento_totale, x="index", y="value", color="Scostamenti", barmode="group", labels={
"index": "",
"value": "€"
}, text_auto=True)
st.plotly_chart(chart_scostamento_totale,
                theme="streamlit", use_container_width=True)

st.write("#")

# Analisi verticale
st.subheader("Scostamenti verticali :arrow_up_down:")
tab1, tab2, tab3, tab4 = st.tabs(
    ["Scostamento volume", "Scostamento MIX", "Scostamento prezzo", "Scostamento costi"])

# Scostamento volume
with tab1:
    temp_scostamento_volume_per_articolo = pd.read_excel(
        "export/scostamento_volume_mix_articolo.xlsx")

    col1, col2 = st.columns(2)
    with col1:
        # budget
        scostamento_volume_per_articolo_budget = pd.DataFrame({
            'Articolo':
                temp_scostamento_volume_per_articolo['Nr articolo'].values,
            'qta budget':
                temp_scostamento_volume_per_articolo['Quantità budget'].values,
        })

        if st.checkbox("Mostra tutti i dati", key="volume_budget"):
            st.dataframe(scostamento_volume_per_articolo_budget.set_index("Articolo"))

        # mostra solo gli articoli maggiori dell'1% rispetto al totale
        scostamento_volume_per_articolo_budget.loc[(scostamento_volume_per_articolo_budget['qta budget'] * 100) /
                                                    scostamento_volume_per_articolo_budget['qta budget'].sum() < 1, 'Articolo'] = 'Altri articoli'
        fig_volume_budget = px.pie(scostamento_volume_per_articolo_budget,
                                    values="qta budget", names="Articolo", title="Articoli a budget")
        fig_volume_budget.update_traces(
            textposition='inside', textinfo='value+label')

        st.plotly_chart(fig_volume_budget, theme="streamlit",
                        use_container_width=True)

    with col2:
        # consuntivo
        scostamento_volume_per_articolo_consuntivo = pd.DataFrame({
            'Articolo':
                temp_scostamento_volume_per_articolo['Nr articolo'].values,
            'qta consuntivo':
                temp_scostamento_volume_per_articolo['Quantità consuntivo'].values,
        })

        if st.checkbox("Mostra tutti i dati", key="volume_consuntivo"):
            st.dataframe(scostamento_volume_per_articolo_consuntivo.set_index("Articolo"))

        scostamento_volume_per_articolo_consuntivo.loc[(scostamento_volume_per_articolo_consuntivo['qta consuntivo'] * 100) /
                                                        scostamento_volume_per_articolo_consuntivo['qta consuntivo'].sum() < 1, 'Articolo'] = 'Altri articoli'
        fig_volume_consuntivo = px.pie(scostamento_volume_per_articolo_consuntivo,
                                        values="qta consuntivo", names="Articolo", title="Articoli a consuntivo")
        fig_volume_consuntivo.update_traces(
            textposition='inside', textinfo='value+label')

        st.plotly_chart(fig_volume_consuntivo,
                        theme="streamlit", use_container_width=True)

# Scostamento MIX
with tab2:
    temp_scostamento_mix_per_articolo = pd.read_excel(
        "export/scostamento_volume_mix_articolo.xlsx")

    col1, col2 = st.columns(2)
    with col1:
        # budget
        scostamento_mix_per_articolo_budget = pd.DataFrame({
            'Articolo':
                temp_scostamento_mix_per_articolo['Nr articolo'].values,
            'MIX budget':
                temp_scostamento_mix_per_articolo['Mix budget (%)'].values,
        })

        if st.checkbox("Mostra tutti i dati", key="mix_budget"):
            st.dataframe(scostamento_mix_per_articolo_budget.set_index("Articolo"))

        # mostra solo gli articoli maggiori dell'1% rispetto al totale
        scostamento_mix_per_articolo_budget.loc[(scostamento_mix_per_articolo_budget['MIX budget'] * 100) /
                                                scostamento_mix_per_articolo_budget['MIX budget'].sum() < 1, 'Articolo'] = 'Altri articoli'
        fig_mix_budget = px.pie(scostamento_mix_per_articolo_budget,
                                values="MIX budget", names="Articolo", title="Articoli a budget")
        fig_mix_budget.update_traces(
            textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig_mix_budget, theme="streamlit",
                        use_container_width=True)

    with col2:
        # consuntivo
        scostamento_mix_per_articolo_consuntivo = pd.DataFrame({
            'Articolo':
                temp_scostamento_mix_per_articolo['Nr articolo'].values,
            'MIX consuntivo':
                temp_scostamento_mix_per_articolo['Mix consuntivo (%)'].values,
        })

        if st.checkbox("Mostra tutti i dati", key="mix_consuntivo"):
            st.dataframe(scostamento_mix_per_articolo_consuntivo.set_index("Articolo"))

        scostamento_mix_per_articolo_consuntivo.loc[(scostamento_mix_per_articolo_consuntivo['MIX consuntivo'] * 100) /
                                                    scostamento_mix_per_articolo_consuntivo['MIX consuntivo'].sum() < 1, 'Articolo'] = 'Altri articoli'
        fig_mix_consuntivo = px.pie(scostamento_mix_per_articolo_consuntivo,
                                    values="MIX consuntivo", names="Articolo", title="Articoli a consuntivo")
        fig_mix_consuntivo.update_traces(
            textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig_mix_consuntivo, theme="streamlit",
                        use_container_width=True)

# Scostamento prezzo
with tab3:
    temp_scostamento_prezzo = pd.read_excel(
        "export/scostamento_prezzo.xlsx")

    scostamento_prezzo = temp_scostamento_prezzo.transpose()
    scostamento_prezzo.columns = scostamento_prezzo.iloc[0]
    scostamento_prezzo = scostamento_prezzo[1:]
    scostamento_prezzo.drop("Δ Tasso di cambio", inplace=True, axis=0)
    scostamento_prezzo.drop("Δ Prezzo", inplace=True, axis=0)

    # TODO: dividere per valuta
    chart_scostamento_prezzo = px.bar(
        scostamento_prezzo.reset_index(), x="index", y="Prezzi", labels={
    "index": "",
    "Prezzi": "Prezzi (€)"
}, text_auto=True)
    st.plotly_chart(chart_scostamento_prezzo,
                    theme="streamlit", use_container_width=True)

    st.dataframe(temp_scostamento_prezzo.set_index('Unnamed: 0').style.format(
        thousands="˙", decimal=",", precision="2"), use_container_width=True)

# Scostamento costo
with tab4:
    temp_scostamento_costo_aree = pd.read_excel(
        "export/production_areas.xlsx")
    temp_scostamento_costo_aree.drop('Unnamed: 0', inplace=True, axis=1)

    if st.checkbox("Mostra tutti i dati", key="costo_aree"):
        st.dataframe(temp_scostamento_costo_aree.set_index("Area di produzione").style.format(
            thousands="˙", decimal=",", precision="2"))

    col1, col2 = st.columns(2)
    with col1:
        # budget
        scostamento_costo_aree_budget = pd.DataFrame({
            'Area di prduzione':
                temp_scostamento_costo_aree['Area di produzione'].values,
            'Costo (€) budget':
                temp_scostamento_costo_aree['Costo (€) budget'].values,
        })

        scostamento_costo_aree_budget.loc[(scostamento_costo_aree_budget['Costo (€) budget'] * 100) /
                                            scostamento_costo_aree_budget['Costo (€) budget'].sum() < 1, 'Area di prduzione'] = 'Altre aree'
        fig_costo_aree_budget = px.pie(scostamento_costo_aree_budget, values="Costo (€) budget",
                                        names="Area di prduzione", title="Impiego risorse nelle aree - budget")
        fig_costo_aree_budget.update_traces(
            textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig_costo_aree_budget,
                        theme="streamlit", use_container_width=True)

    with col2:
        # consuntivo
        scostamento_costo_aree_consuntivo = pd.DataFrame({
            'Area di prduzione':
                temp_scostamento_costo_aree['Area di produzione'].values,
            'Costo (€) consuntivo':
                temp_scostamento_costo_aree['Costo (€) consuntivo'].values,
        })

        scostamento_costo_aree_consuntivo.loc[(scostamento_costo_aree_consuntivo['Costo (€) consuntivo'] * 100) /
                                                scostamento_costo_aree_consuntivo['Costo (€) consuntivo'].sum() < 1, 'Area di prduzione'] = 'Altre aree'
        fig_costo_aree_consuntivo = px.pie(scostamento_costo_aree_consuntivo, values="Costo (€) consuntivo",
                                            names="Area di prduzione", title="Impiego risorse nelle aree - consuntivo")
        fig_costo_aree_consuntivo.update_traces(
            textposition='inside', textinfo='percent+label')

        st.plotly_chart(fig_costo_aree_consuntivo,
                        theme="streamlit", use_container_width=True)

    # Focus risorse
    st.subheader("Focus risorse")
    temp_scostamento_risorse = pd.read_excel(
        "export/scostamento_risorse.xlsx")

    # tornitura (A20)
    st.caption("Tornitura (A20)")
    area = "A20"
    temp_scostamento_tornitura = temp_scostamento_risorse.query(
        "(`Area di produzione` == @area)"
    )

    temp_scostamento_tornitura = temp_scostamento_tornitura.iloc[:, 2:]

    if st.checkbox("Mostra tutti i dati", key="risorsa_tornitura"):
        st.dataframe(temp_scostamento_tornitura.set_index("Risorsa").style.format(
            thousands="˙", decimal=",", precision="2"), use_container_width=True)

    scostamento_tornitura = pd.DataFrame(
        {
            "Risorsa":
                temp_scostamento_tornitura["Risorsa"].values,
            "Costo budget":
                temp_scostamento_tornitura["Costo budget"].values,
            "Costo ore effettive":
                temp_scostamento_tornitura["Costo ore effettive"].values,
            "Costo consuntivo":
                temp_scostamento_tornitura["Costo consuntivo"].values,
        }
    ).transpose()

    scostamento_tornitura.columns = scostamento_tornitura.iloc[0]
    scostamento_tornitura = scostamento_tornitura[1:]

    scostamento_tornitura = scostamento_tornitura.reset_index()
    scostamento_tornitura = pd.melt(scostamento_tornitura, id_vars=[
                                    'index'], var_name='risorse', value_name='value')
    chart_scostamento_tornitura = px.bar(
        scostamento_tornitura, x="index", y="value", color="risorse", barmode="group", labels={
    "index": "",
    "value": "€"
})
    st.plotly_chart(chart_scostamento_tornitura,
                    theme="streamlit", use_container_width=True)

    # fresatura (A30)
    st.caption("Fresatura (A30)")
    area = "A30"
    temp_scostamento_fresatura = temp_scostamento_risorse.query(
        "(`Area di produzione` == @area)"
    )

    temp_scostamento_fresatura = temp_scostamento_fresatura.iloc[:, 2:]

    if st.checkbox("Mostra tutti i dati", key="risorsa_fresatura"):
        st.dataframe(temp_scostamento_fresatura.set_index("Risorsa").style.format(
            thousands="˙", decimal=",", precision="2"), use_container_width=True)

    scostamento_fresatura = pd.DataFrame(
        {
            "Risorsa":
                temp_scostamento_fresatura["Risorsa"].values,
            "Costo budget":
                temp_scostamento_fresatura["Costo budget"].values,
            "Costo ore effettive":
                temp_scostamento_fresatura["Costo ore effettive"].values,
            "Costo consuntivo":
                temp_scostamento_fresatura["Costo consuntivo"].values,
        }
    ).transpose()

    scostamento_fresatura.columns = scostamento_fresatura.iloc[0]

    scostamento_fresatura = scostamento_fresatura[1:]

    scostamento_fresatura = scostamento_fresatura.reset_index()
    scostamento_fresatura = pd.melt(scostamento_fresatura, id_vars=[
                                    'index'], var_name='risorse', value_name='value')
    chart_scostamento_fresatura = px.bar(
        scostamento_fresatura, x="index", y="value", color="risorse", barmode="group", labels={
    "index": "",
    "value": "€"
})
    st.plotly_chart(chart_scostamento_fresatura,
                    theme="streamlit", use_container_width=True)

    # montaggio (A40)
    st.caption("Montaggio (A40)")
    area = "A40"
    temp_scostamento_montaggio = temp_scostamento_risorse.query(
        "(`Area di produzione` == @area)"
    )

    temp_scostamento_montaggio = temp_scostamento_montaggio.iloc[:, 2:]

    if st.checkbox("Mostra tutti i dati", key="risorsa_montaggio"):
        st.dataframe(temp_scostamento_montaggio.set_index("Risorsa").style.format(
            thousands="˙", decimal=",", precision="2"), use_container_width=True)

    scostamento_montaggio = pd.DataFrame(
        {
            "Risorsa":
                temp_scostamento_montaggio["Risorsa"].values,
            "Costo budget":
                temp_scostamento_montaggio["Costo budget"].values,
            "Costo ore effettive":
                temp_scostamento_montaggio["Costo ore effettive"].values,
            "Costo consuntivo":
                temp_scostamento_montaggio["Costo consuntivo"].values,
        }
    ).transpose()

    scostamento_montaggio.columns = scostamento_montaggio.iloc[0]
    scostamento_montaggio = scostamento_montaggio[1:]

    scostamento_montaggio = scostamento_montaggio.reset_index()
    scostamento_montaggio = pd.melt(scostamento_montaggio, id_vars=[
                                    'index'], var_name='risorse', value_name='value')
    chart_scostamento_montaggio = px.bar(
        scostamento_montaggio, x="index", y="value", color="risorse", barmode="group", labels={
    "index": "",
    "value": "€"
})
    st.plotly_chart(chart_scostamento_montaggio,
                    theme="streamlit", use_container_width=True)

    # saldatura (A11)
    st.caption("Saldatura (A11)")
    area = "A11"
    temp_scostamento_saldatura = temp_scostamento_risorse.query(
        "(`Area di produzione` == @area)"
    )

    temp_scostamento_saldatura = temp_scostamento_saldatura.iloc[:, 2:]

    if st.checkbox("Mostra tutti i dati", key="risorsa_saldatura"):
        st.dataframe(temp_scostamento_saldatura.set_index("Risorsa").style.format(
            thousands="˙", decimal=",", precision="2"), use_container_width=True)

    scostamento_saldatura = pd.DataFrame(
        {
            "Risorsa":
                temp_scostamento_saldatura["Risorsa"].values,
            "Costo budget":
                temp_scostamento_saldatura["Costo budget"].values,
            "Costo ore effettive":
                temp_scostamento_saldatura["Costo ore effettive"].values,
            "Costo consuntivo":
                temp_scostamento_saldatura["Costo consuntivo"].values,
        }
    ).transpose()

    scostamento_saldatura.columns = scostamento_saldatura.iloc[0]
    scostamento_saldatura = scostamento_saldatura[1:]

    scostamento_saldatura = scostamento_saldatura.reset_index()
    scostamento_saldatura = pd.melt(scostamento_saldatura, id_vars=[
                                    'index'], var_name='risorse', value_name='value')
    chart_scostamento_saldatura = px.bar(
        scostamento_saldatura, x="index", y="value", color="risorse", barmode="group", labels={
    "index": "",
    "value": "€"
})
    st.plotly_chart(chart_scostamento_saldatura,
                    theme="streamlit", use_container_width=True)

    # pre. materiale (A10)
    st.caption("Prep. materiale/Taglio/ Sbavatura (A10)")
    area = "A10"
    temp_scostamento_preparazione = temp_scostamento_risorse.query(
        "(`Area di produzione` == @area)"
    )

    temp_scostamento_preparazione = temp_scostamento_preparazione.iloc[:, 2:]

    if st.checkbox("Mostra tutti i dati", key="risorsa_preparazione"):
        st.dataframe(temp_scostamento_preparazione.set_index("Risorsa").style.format(
            thousands="˙", decimal=",", precision="2"), use_container_width=True)

    scostamento_preparazione = pd.DataFrame(
        {
            "Risorsa":
                temp_scostamento_preparazione["Risorsa"].values,
            "Costo budget":
                temp_scostamento_preparazione["Costo budget"].values,
            "Costo ore effettive":
                temp_scostamento_preparazione["Costo ore effettive"].values,
            "Costo consuntivo":
                temp_scostamento_preparazione["Costo consuntivo"].values,
        }
    ).transpose()

    scostamento_preparazione.columns = scostamento_preparazione.iloc[0]
    scostamento_preparazione = scostamento_preparazione[1:]

    scostamento_preparazione = scostamento_preparazione.reset_index()
    scostamento_preparazione = pd.melt(scostamento_preparazione, id_vars=[
        'index'], var_name='risorse', value_name='value')
    chart_scostamento_preparazione = px.bar(
        scostamento_preparazione, x="index", y="value", color="risorse", barmode="group", labels={
    "index": "",
    "value": "€"
})
    st.plotly_chart(chart_scostamento_preparazione,
                    theme="streamlit", use_container_width=True)
