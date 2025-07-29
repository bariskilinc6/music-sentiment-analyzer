from google_play_scraper import reviews, Sort
import pandas as pd

# Apple Music yorumlarını çek
result, _ = reviews(
    'com.apple.android.music',  # ← Apple Music paket adı
    lang='tr',
    country='tr',
    sort=Sort.NEWEST,
    count=500  # Yorum sayısını burada artırabilirsin
)

# DataFrame'e dönüştür
df = pd.DataFrame(result)

# Sadece ilgili sütunlar
df = df[['content', 'score', 'at']]

# CSV dosyasına kaydet
df.to_csv("apple_music_yorumlari.csv", index=False, encoding='utf-8-sig')

print("✅ Apple Music yorumları kaydedildi.")
