import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='SCG - Analisi scostamenti', layout='wide', page_icon=':bar_chart:')
st.title('Analisi degli scostamenti :bar_chart:')

DATA_URL = ('export/scostamento_totale.xlsx')

@st.cache
def load_data():
    data = pd.read_excel(DATA_URL)
    return data

data = load_data()

# upload files
uploaded_files = st.file_uploader("Choose your xlsx files:", type=".xlsx", accept_multiple_files=True)

# Resoconto analisi scostamento
st.subheader('Risultati')

st.metric("MOL", data["Consuntivo"][4], data["Consuntivo"][4] - data["Budget"][4])

col1, col2, col3 = st.columns(3)
col1.metric("Ricavi", data["Consuntivo"][0], data["Consuntivo"][0] - data["Budget"][0])
col2.metric("Costi MP", data["Consuntivo"][2], data["Consuntivo"][2] - data["Budget"][2])
col3.metric("Costi risorse",data["Consuntivo"][3], data["Consuntivo"][3] - data["Budget"][3])

st.dataframe(data, use_container_width=True)

# Analisi orizzontale
scostamento_ricavi = {
    data["Budget"][0],
    data["Mix standard"][0],
    data["Mix effettivo"][0],
    data["Consuntivo"][0],
}

st.subheader("Scostamento fatturato")
st.bar_chart(scostamento_ricavi)

scostamento_costi = {
    data["Budget"][1],
    data["Mix standard"][1],
    data["Mix effettivo"][1],
    data["Consuntivo"][1],
}

st.subheader("Scostamento costi MP e risorse")
st.bar_chart(scostamento_costi)

scostamento_mol = {
    data["Budget"][4],
    data["Mix standard"][4],
    data["Mix effettivo"][4],
    data["Consuntivo"][4],
}

st.subheader("Scostamento MOL")
st.bar_chart(scostamento_mol)

# Focus tipo di scostamento
tab1, tab2, tab3, tab4 = st.tabs(["Scostamento volume", "Scostamento MIX", "Scostamento prezzo", "Scostamento costi"])

# Scostamento volume
with tab1:
    st.subheader("Scostamento volume")
    temp_scostamento_volume_per_articolo = pd.read_excel("export/scostamento_volume_mix_articolo.xlsx")

    # budget
    scostamento_volume_per_articolo_budget = pd.DataFrame({
        'Articolo':
            temp_scostamento_volume_per_articolo['Nr articolo'].values,
        'qta budget':
            temp_scostamento_volume_per_articolo['Quantità budget'].values,
    })

    if st.checkbox("Mostra tutti i dati", key="volume_budget"):
        st.dataframe(scostamento_volume_per_articolo_budget)

    # mostra solo gli articoli maggiori dell'1% rispetto al totale 
    scostamento_volume_per_articolo_budget.loc[(scostamento_volume_per_articolo_budget['qta budget']*100)/scostamento_volume_per_articolo_budget['qta budget'].sum() < 1, 'Articolo'] = 'Altri articoli'
    fig_volume_budget = px.pie(scostamento_volume_per_articolo_budget, values="qta budget", names="Articolo", title="Articoli a budget")
    fig_volume_budget.update_traces(textposition='inside', textinfo='value+label')
    
    st.plotly_chart(fig_volume_budget, theme="streamlit")

    # consuntivo
    scostamento_volume_per_articolo_consuntivo = pd.DataFrame({
        'Articolo':
            temp_scostamento_volume_per_articolo['Nr articolo'].values,
        'qta consuntivo':
            temp_scostamento_volume_per_articolo['Quantità consuntivo'].values,
    })

    if st.checkbox("Mostra tutti i dati", key="volume_consuntivo"):
        st.dataframe(scostamento_volume_per_articolo_consuntivo)
        
    scostamento_volume_per_articolo_consuntivo.loc[(scostamento_volume_per_articolo_consuntivo['qta consuntivo']*100)/scostamento_volume_per_articolo_consuntivo['qta consuntivo'].sum() < 1, 'Articolo'] = 'Altri articoli'
    fig_volume_consuntivo = px.pie(scostamento_volume_per_articolo_consuntivo, values="qta consuntivo", names="Articolo", title="Articoli a consuntivo")
    fig_volume_consuntivo.update_traces(textposition='inside', textinfo='value+label')
    
    st.plotly_chart(fig_volume_consuntivo, theme="streamlit")

# Scostamento MIX
with tab2:
    st.subheader("Scostamento MIX")
    temp_scostamento_mix_per_articolo = pd.read_excel("export/scostamento_volume_mix_articolo.xlsx")

    # budget
    scostamento_mix_per_articolo_budget = pd.DataFrame({
        'Articolo':
            temp_scostamento_mix_per_articolo['Nr articolo'].values,
        'MIX budget':
            temp_scostamento_mix_per_articolo['Mix budget (%)'].values,
    })

    if st.checkbox("Mostra tutti i dati", key="mix_budget"):
        st.dataframe(scostamento_mix_per_articolo_budget)

    # mostra solo gli articoli maggiori dell'1% rispetto al totale 
    scostamento_mix_per_articolo_budget.loc[(scostamento_mix_per_articolo_budget['MIX budget']*100)/scostamento_mix_per_articolo_budget['MIX budget'].sum() < 1, 'Articolo'] = 'Altri articoli'
    fig_mix_budget = px.pie(scostamento_mix_per_articolo_budget, values="MIX budget", names="Articolo", title="Articoli a budget")
    fig_mix_budget.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(fig_mix_budget, theme="streamlit")

    # consuntivo
    scostamento_mix_per_articolo_consuntivo = pd.DataFrame({
        'Articolo':
            temp_scostamento_mix_per_articolo['Nr articolo'].values,
        'MIX consuntivo':
            temp_scostamento_mix_per_articolo['Mix consuntivo (%)'].values,
    })

    if st.checkbox("Mostra tutti i dati", key="mix_consuntivo"):
        st.dataframe(scostamento_mix_per_articolo_consuntivo)
        
    scostamento_mix_per_articolo_consuntivo.loc[(scostamento_mix_per_articolo_consuntivo['MIX consuntivo']*100)/scostamento_mix_per_articolo_consuntivo['MIX consuntivo'].sum() < 1, 'Articolo'] = 'Altri articoli'
    fig_mix_consuntivo = px.pie(scostamento_mix_per_articolo_consuntivo, values="MIX consuntivo", names="Articolo", title="Articoli a consuntivo")
    fig_mix_consuntivo.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(fig_mix_consuntivo, theme="streamlit")

# Scostamento prezzo
with tab3:
    st.subheader("Scostamento Prezzo")
    temp_scostamento_prezzo = pd.read_excel("export/scostamento_prezzo.xlsx")
    scostamento_prezzo = pd.DataFrame({
        'Mix effettivo':
            temp_scostamento_prezzo['Mix effettivo'],
        'Δ E-TE':
            temp_scostamento_prezzo['Δ E-TE'],
        'Mix tasso effettivo':
            temp_scostamento_prezzo['Mix tasso effettivo'],
        'Δ TE-C':
            temp_scostamento_prezzo['Δ TE-C'],
        'Consuntivo':
            temp_scostamento_prezzo['Consuntivo'],
    })

    # TODO: dividere per valuta
    st.line_chart({
            temp_scostamento_prezzo['Mix effettivo'][0],
            temp_scostamento_prezzo['Mix tasso effettivo'][0],
            temp_scostamento_prezzo['Consuntivo'][0],
    })

    st.dataframe(scostamento_prezzo, use_container_width=True)

# Scostamento costo
with tab4:
    st.subheader("Scostamento Costo")
    temp_scostamento_costo_aree = pd.read_excel("export/production_areas.xlsx")

    if st.checkbox("Mostra tutti i dati", key="costo_aree"):
        st.dataframe(temp_scostamento_costo_aree)

    # budget
    scostamento_costo_aree_budget = pd.DataFrame({
        'Area di prduzione':
            temp_scostamento_costo_aree['Area di produzione'].values,
        'Costo (€) budget':
            temp_scostamento_costo_aree['Costo (€) budget'].values,
    })
    
    scostamento_costo_aree_budget.loc[(scostamento_costo_aree_budget['Costo (€) budget']*100)/scostamento_costo_aree_budget['Costo (€) budget'].sum() < 1, 'Area di prduzione'] = 'Altre aree'
    fig_costo_aree_budget = px.pie(scostamento_costo_aree_budget, values="Costo (€) budget", names="Area di prduzione", title="Impiego risorse nell aree di produzione - budget")
    fig_costo_aree_budget.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(fig_costo_aree_budget, theme="streamlit")

    # consuntivo
    scostamento_costo_aree_consuntivo = pd.DataFrame({
        'Area di prduzione':
            temp_scostamento_costo_aree['Area di produzione'].values,
        'Costo (€) consuntivo':
            temp_scostamento_costo_aree['Costo (€) consuntivo'].values,
    })
    
    scostamento_costo_aree_consuntivo.loc[(scostamento_costo_aree_consuntivo['Costo (€) consuntivo']*100)/scostamento_costo_aree_consuntivo['Costo (€) consuntivo'].sum() < 1, 'Area di prduzione'] = 'Altre aree'
    fig_costo_aree_consuntivo = px.pie(scostamento_costo_aree_consuntivo, values="Costo (€) consuntivo", names="Area di prduzione", title="Impiego risorse nell aree di produzione - budget")
    fig_costo_aree_consuntivo.update_traces(textposition='inside', textinfo='percent+label')
    
    st.plotly_chart(fig_costo_aree_consuntivo, theme="streamlit")

    # Focus risorse
    st.subheader("Focus risorse")
    temp_scostamento_risorse = pd.read_excel("export/scostamento_risorse.xlsx")

    if st.checkbox("Mostra tutti i dati", key="costo_risorse"):
        st.dataframe(temp_scostamento_risorse)

    # tornitura (A20)
    st.subheader("Tornitura (A20)")
    area = "A20"
    scostamento_tornitura = temp_scostamento_risorse.query(
        "(`Area di produzione` == @area)"
    )

    if st.checkbox("Mostra tutti i dati", key="risorsa_tornitura"):
        st.dataframe(scostamento_tornitura)

    # fresatura (A30)
    st.subheader("Fresatura (A30)")
    area = "A30"
    scostamento_fresatura = temp_scostamento_risorse.query(
        "(`Area di produzione` == @area)"
    )

    if st.checkbox("Mostra tutti i dati", key="risorsa_fresatura"):
        st.dataframe(scostamento_fresatura)

    # montaggio (A40)
    st.subheader("Montaggio (A40)")
    area = "A40"
    scostamento_montaggio = temp_scostamento_risorse.query(
        "(`Area di produzione` == @area)"
    )

    if st.checkbox("Mostra tutti i dati", key="risorsa_montaggio"):
        st.dataframe(scostamento_montaggio)

    # saldatura (A11)
    st.subheader("Saldatura (A11)")
    area = "A11"
    scostamento_saldatura = temp_scostamento_risorse.query(
        "(`Area di produzione` == @area)"
    )

    if st.checkbox("Mostra tutti i dati", key="risorsa_saldatura"):
        st.dataframe(scostamento_saldatura)

    # pre. materiale (A10)
    st.subheader("Prep. materiale/Taglio/ Sbavatura (A10)")
    area = "A10"
    scostamento_preparazione = temp_scostamento_risorse.query(
        "(`Area di produzione` == @area)"
    )

    if st.checkbox("Mostra tutti i dati", key="risorsa_preparazione"):
        st.dataframe(scostamento_preparazione)