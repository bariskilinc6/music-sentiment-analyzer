from google_play_scraper import reviews, Sort
import pandas as pd

result, _ = reviews(
    'com.spotify.music',
    lang='tr',
    country='tr',
    sort=Sort.NEWEST,
    count=500
)

df = pd.DataFrame(result)
df = df[['content', 'score', 'at']]
df.to_csv("spotify_yorumlari.csv", index=False, encoding='utf-8-sig')
print("✅ Spotify yorumları kaydedildi.")
