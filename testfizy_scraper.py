from google_play_scraper import reviews, Sort
import pandas as pd

# Fizy yorumlarını çek
result, _ = reviews(
    'com.turkcell.gncplay',
    lang='tr',
    country='tr',
    sort=Sort.NEWEST,
    count=200
)

# DataFrame'e dönüştür
df = pd.DataFrame(result)

# İlgili sütunları al
df = df[['content', 'score', 'at']]

# CSV'ye kaydet
df.to_csv("fizy_scraper_yorumlari.csv", index=False, encoding='utf-8-sig')

print("✅ Yorumlar başarıyla kaydedildi.")
