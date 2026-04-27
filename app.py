import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Configurare pagină
st.set_page_config(page_title="My Music Stats", layout="wide")

st.title("Muzica Mea în Cifre")
st.markdown("---")

def load_data():
    try:
        # Ne conectăm la baza de date creată de scrobbler.py
        conn = sqlite3.connect('muzica_mea.db')
        df = pd.read_sql_query("SELECT * FROM istoric_muzica", conn)
        conn.close()
        
        if not df.empty:
            # Normalizăm timpul la UTC (pentru a se potrivi cu ce salvează scrobbler-ul)
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', utc=True)
            # Convertim la ora locală pentru afișare (opțional, dar util)
            df['timestamp'] = df['timestamp'].dt.tz_convert('Europe/Bucharest')
        return df
    except Exception as e:
        st.sidebar.error(f"Eroare la citirea bazei de date: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- SECȚIUNE STATISTICI RAPIDE ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Piese", len(df))
    with col2:
        st.metric("Artiști Unici", df['artist'].nunique())
    with col3:
        st.metric("Ultima piesă", df.sort_values('timestamp', ascending=False).iloc[0]['piesa'])

    st.markdown("---")

    # --- GRAFICE ---
    col_stanga, col_dreapta = st.columns([1, 1])

    with col_stanga:
        st.subheader("Top 10 Artiști")
        
        # Pregătim datele pentru top artiști
        top_artisti = df['artist'].value_counts().head(10).reset_index()
        top_artisti.columns = ['Artist', 'Ascultări']
        
        # Creăm graficul
        fig_artisti = px.bar(
            top_artisti, 
            x='Ascultări', 
            y='Artist', 
            orientation='h',
            color='Ascultări',
            color_continuous_scale='Viridis',
            text='Ascultări'
        )

        # MODIFICAREA CERUTĂ: Ordonare descrescătoare (Locul 1 să fie sus)
        fig_artisti.update_layout(
            yaxis={'categoryorder':'total ascending'},
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_artisti, use_container_width=True)

    with col_dreapta:
        st.subheader("Istoric Recent")
        # Afișăm ultimele 10 piese într-un mod tabelar curat
        recent_df = df.sort_values('timestamp', ascending=False)[['timestamp', 'artist', 'piesa']].head(10)
        # Formatăm timpul pentru a fi mai ușor de citit
        recent_df['timestamp'] = recent_df['timestamp'].dt.strftime('%d %b, %H:%M')
        st.table(recent_df)

    # --- TABELUL COMPLET ---
    st.markdown("---")
    with st.expander("Vezi tot istoricul bazei de date"):
        st.dataframe(df.sort_values('timestamp', ascending=False), use_container_width=True)

else:
    st.info("Baza de date pare să fie goală. Asigură-te că `scrobbler.py` rulează și a salvat primele piese!")

# Buton de refresh manual în sidebar
if st.sidebar.button('Refresh Date'):
    st.rerun()
