# 🎵 Müzik Uygulamaları Sentiment Analizi Dashboard

Bu dashboard, 4 farklı müzik uygulamasının (Fizy, Spotify, Apple Music, YouTube Music) kullanıcı yorumlarının sentiment analizi sonuçlarını görsel olarak karşılaştırmanızı sağlar.

## 📋 Özellikler

- **📊 Ana Metrikler**: Toplam yorum sayısı, ortalama sentiment skoru, pozitif/negatif yüzde
- **📈 Uygulama Karşılaştırmaları**: Her uygulamanın sentiment dağılımı (pie chart)
- **📊 Ortalama Skorlar**: Uygulamaların ortalama sentiment skorları (horizontal bar chart)
- **📊 Sentiment Sayıları**: Pozitif/negatif/nötr yorum sayıları karşılaştırması
- **🎯 Konu Analizi**: Konulara göre sentiment dağılımı
- **😊 Duygu Analizi**: Kullanıcı duygularının dağılımı
- **📋 Detaylı Tablo**: Filtrelenebilir ve aranabilir veri tablosu

## 🚀 Kurulum ve Çalıştırma

### 1. Gerekli Kütüphaneleri Yükleyin
```bash
pip install -r requirements.txt
```

### 2. Dashboard'u Çalıştırın
```bash
streamlit run dashboard.py
```

### 3. Tarayıcıda Açın
Dashboard otomatik olarak `http://localhost:8501` adresinde açılacaktır.

## 📁 Gerekli Dosyalar

Dashboard'un çalışması için aşağıdaki CSV dosyalarının mevcut olması gerekir:

- `fizy_konu_analizi.csv`
- `spotify_konu_analizi.csv`
- `applemusic_konu_analizi.csv`
- `ytmusic_konu_analizi.csv`

Her CSV dosyasında şu sütunlar bulunmalıdır:
- `yorum`: Kullanıcı yorumu
- `konu`: Yorumun konusu
- `sentiment`: Sentiment kategorisi (pozitif/negatif/nötr)
- `sentiment_score`: Sentiment skoru (0-100)
- `duygu`: Tespit edilen duygu

## 🎛️ Kullanım

### Filtreler (Sol Sidebar)
- **Uygulamalar**: Hangi uygulamaları analiz etmek istediğinizi seçin
- **Konular**: Belirli konulara odaklanın
- **Duygular**: Belirli duyguları filtreleyin

### Grafikler
- **Pie Chart'lar**: Her uygulamanın sentiment dağılımını gösterir
- **Bar Chart'lar**: Uygulamalar arası karşılaştırmalar
- **Stacked Bar**: Konu bazında sentiment analizi
- **Pie Chart**: Genel duygu dağılımı

### Arama
Detaylı tablo bölümünde yorum içinde arama yapabilirsiniz.

## 🎨 Özelleştirme

Dashboard'u özelleştirmek için `dashboard.py` dosyasını düzenleyebilirsiniz:

- **Renkler**: CSS stillerini değiştirin
- **Grafikler**: Plotly konfigürasyonlarını güncelleyin
- **Metrikler**: Yeni metrikler ekleyin
- **Filtreler**: Yeni filtre seçenekleri ekleyin

## 📊 Veri Yapısı

Dashboard, sentiment analizi sonuçlarınızı şu şekilde işler:

1. **Veri Yükleme**: Tüm CSV dosyalarını birleştirir
2. **Filtreleme**: Seçilen kriterlere göre veriyi filtreler
3. **Analiz**: Çeşitli istatistiksel analizler yapar
4. **Görselleştirme**: Sonuçları interaktif grafiklerle sunar

## 🔧 Sorun Giderme

### "Dosya bulunamadı" Hatası
- Tüm CSV dosyalarının doğru konumda olduğundan emin olun
- Dosya isimlerinin doğru yazıldığından emin olun

### Grafik Görünmüyor
- Veri filtrelenmiş olabilir, filtreleri kontrol edin
- CSV dosyalarında veri olduğundan emin olun

### Performans Sorunları
- Büyük veri setleri için filtreleri kullanın
- Streamlit cache'i temizleyin: `streamlit cache clear`

## 📈 Gelecek Özellikler

- [ ] Zaman serisi analizi
- [ ] Word cloud görselleştirmesi
- [ ] Export özellikleri (PDF, Excel)
- [ ] Daha gelişmiş filtreleme seçenekleri
- [ ] Otomatik rapor oluşturma

## 🤝 Katkıda Bulunma

Bu projeye katkıda bulunmak istiyorsanız:

1. Fork yapın
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Pull request gönderin

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 