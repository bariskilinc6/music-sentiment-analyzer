import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Müzik Uygulamaları Sentiment Analizi Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .app-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Ana başlık
st.markdown('<h1 class="main-header">🎵 Müzik Uygulamaları Sentiment Analizi Dashboard</h1>', unsafe_allow_html=True)

# Veri yükleme fonksiyonu
@st.cache_data
def load_data():
    """Tüm CSV dosyalarını yükler ve uygulama adlarını ekler"""
    apps = {
        'fizy_konu_analizi.csv': 'Fizy',
        'spotify_konu_analizi.csv': 'Spotify', 
        'applemusic_konu_analizi.csv': 'Apple Music',
        'ytmusic_konu_analizi.csv': 'YouTube Music'
    }
    
    all_data = []
    for filename, app_name in apps.items():
        try:
            df = pd.read_csv(filename)
            df['uygulama'] = app_name
            
            # sentiment_score sütununu güvenli şekilde float'a çevir
            def safe_float_convert(x):
                try:
                    if pd.isna(x) or x == '' or str(x).strip() == '':
                        return 0.0
                    return float(str(x).strip())
                except (ValueError, TypeError):
                    return 0.0
            
            df['sentiment_score'] = df['sentiment_score'].apply(safe_float_convert)
            
            all_data.append(df)
        except FileNotFoundError:
            st.error(f"❌ {filename} dosyası bulunamadı!")
            return None
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return None

# Veriyi yükle
data = load_data()

if data is None:
    st.error("Veri yüklenemedi. Lütfen tüm CSV dosyalarının mevcut olduğundan emin olun.")
    st.stop()

# Sidebar - Filtreler
st.sidebar.markdown("## 🔍 Filtreler")

# Uygulama seçimi
selected_apps = st.sidebar.multiselect(
    "Uygulamaları Seçin:",
    options=data['uygulama'].unique(),
    default=data['uygulama'].unique()
)

# Konu filtresi
topics = data['konu'].unique()
selected_topics = st.sidebar.multiselect(
    "Konuları Seçin:",
    options=topics,
    default=topics
)

# Duygu filtresi
emotions = data['duygu'].unique()
selected_emotions = st.sidebar.multiselect(
    "Duyguları Seçin:",
    options=emotions,
    default=emotions
)

# Veriyi filtrele
filtered_data = data[
    (data['uygulama'].isin(selected_apps)) &
    (data['konu'].isin(selected_topics)) &
    (data['duygu'].isin(selected_emotions))
]

# Ana metrikler
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_reviews = len(filtered_data)
    st.metric("📊 Toplam Yorum", total_reviews)

with col2:
    avg_sentiment = filtered_data['sentiment_score'].mean()
    st.metric("😊 Ortalama Sentiment", f"{avg_sentiment:.1f}")

with col3:
    positive_pct = (filtered_data['sentiment'] == 'pozitif').mean() * 100
    st.metric("👍 Pozitif Yüzde", f"%{positive_pct:.1f}")

with col4:
    negative_pct = (filtered_data['sentiment'] == 'negatif').mean() * 100
    st.metric("👎 Negatif Yüzde", f"%{negative_pct:.1f}")

st.markdown("---")

# 1. Uygulama Bazında Sentiment Dağılımları
st.markdown('<h2 class="app-title">📈 Uygulama Bazında Sentiment Dağılımları</h2>', unsafe_allow_html=True)

# Her uygulama için sentiment dağılımı
app_sentiment_counts = filtered_data.groupby(['uygulama', 'sentiment']).size().unstack(fill_value=0)

# Pie chart'lar için subplot
fig_pie = make_subplots(
    rows=2, cols=2,
    subplot_titles=selected_apps,
    specs=[[{"type": "pie"}, {"type": "pie"}],
           [{"type": "pie"}, {"type": "pie"}]]
)

colors = {'pozitif': '#2ecc71', 'negatif': '#e74c3c', 'nötr': '#95a5a6'}

for i, app in enumerate(selected_apps):
    if app in app_sentiment_counts.index:
        app_data = app_sentiment_counts.loc[app]
        values = [app_data.get('pozitif', 0), app_data.get('negatif', 0), app_data.get('nötr', 0)]
        labels = ['Pozitif', 'Negatif', 'Nötr']
        
        fig_pie.add_trace(
            go.Pie(
                labels=labels,
                values=values,
                name=app,
                marker_colors=[colors['pozitif'], colors['negatif'], colors['nötr']],
                textinfo='label+percent',
                textposition='inside'
            ),
            row=(i//2)+1, col=(i%2)+1
        )

fig_pie.update_layout(height=600, showlegend=False)
st.plotly_chart(fig_pie, use_container_width=True)

# 2. Ortalama Sentiment Skorları Karşılaştırması
st.markdown('<h2 class="app-title">📊 Ortalama Sentiment Skorları</h2>', unsafe_allow_html=True)

avg_scores = filtered_data.groupby('uygulama')['sentiment_score'].mean().sort_values()

fig_avg = px.bar(
    x=avg_scores.values,
    y=avg_scores.index,
    orientation='h',
    title="Uygulamaların Ortalama Sentiment Skorları",
    labels={'x': 'Ortalama Sentiment Skoru', 'y': 'Uygulama'},
    color=avg_scores.values,
    color_continuous_scale='RdYlGn'
)

fig_avg.update_layout(height=400)
st.plotly_chart(fig_avg, use_container_width=True)

# 3. Pozitif/Negatif Yorum Sayıları Karşılaştırması
st.markdown('<h2 class="app-title">📊 Pozitif vs Negatif Yorum Sayıları</h2>', unsafe_allow_html=True)

sentiment_counts = filtered_data.groupby(['uygulama', 'sentiment']).size().unstack(fill_value=0)

fig_counts = go.Figure()

# Pozitif yorumlar
fig_counts.add_trace(go.Bar(
    name='Pozitif',
    x=sentiment_counts.index,
    y=sentiment_counts['pozitif'],
    marker_color='#2ecc71'
))

# Negatif yorumlar
fig_counts.add_trace(go.Bar(
    name='Negatif',
    x=sentiment_counts.index,
    y=sentiment_counts['negatif'],
    marker_color='#e74c3c'
))

# Nötr yorumlar
fig_counts.add_trace(go.Bar(
    name='Nötr',
    x=sentiment_counts.index,
    y=sentiment_counts['nötr'],
    marker_color='#95a5a6'
))

fig_counts.update_layout(
    title="Uygulamaların Sentiment Dağılımı",
    xaxis_title="Uygulama",
    yaxis_title="Yorum Sayısı",
    barmode='group',
    height=400
)

st.plotly_chart(fig_counts, use_container_width=True)

# 4. Konu Analizi
st.markdown('<h2 class="app-title">🎯 Konu Bazında Analiz</h2>', unsafe_allow_html=True)

topic_sentiment = filtered_data.groupby(['konu', 'sentiment']).size().unstack(fill_value=0)
topic_sentiment_pct = topic_sentiment.div(topic_sentiment.sum(axis=1), axis=0) * 100

fig_topic = px.bar(
    topic_sentiment_pct,
    title="Konulara Göre Sentiment Dağılımı (%)",
    labels={'value': 'Yüzde (%)', 'konu': 'Konu', 'sentiment': 'Sentiment'},
    barmode='stack'
)

fig_topic.update_layout(height=500)
st.plotly_chart(fig_topic, use_container_width=True)

# 5. Duygu Analizi
st.markdown('<h2 class="app-title">😊 Duygu Analizi</h2>', unsafe_allow_html=True)

emotion_counts = filtered_data['duygu'].value_counts()

fig_emotion = px.pie(
    values=emotion_counts.values,
    names=emotion_counts.index,
    title="Duygu Dağılımı",
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig_emotion.update_layout(height=500)
st.plotly_chart(fig_emotion, use_container_width=True)

# 6. Detaylı Tablo
st.markdown('<h2 class="app-title">📋 Detaylı Veri Tablosu</h2>', unsafe_allow_html=True)

# Tablo için veriyi düzenle
table_data = filtered_data[['uygulama', 'yorum', 'konu', 'sentiment', 'sentiment_score', 'duygu']].copy()
table_data['sentiment_score'] = table_data['sentiment_score'].round(1)

# Arama kutusu
search_term = st.text_input("🔍 Yorum içinde ara:", "")

if search_term:
    table_data = table_data[table_data['yorum'].str.contains(search_term, case=False, na=False)]

st.dataframe(
    table_data,
    use_container_width=True,
    height=400
)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🎵 Müzik Uygulamaları Sentiment Analizi Dashboard | 
    <a href='#' style='color: #1f77b4;'>Detaylı Rapor</a></p>
</div>
""", unsafe_allow_html=True) 