from openai import OpenAI
import pandas as pd
import json
from time import sleep

# ✅ API Key (senin anahtarın)
client = OpenAI(api_key="sk-proj")

# ✅ CSV'den ilk 200 yorum okunuyor (Spotify)
df = pd.read_csv("spotify_yorumlari.csv")
yorumlar = df["content"].dropna().iloc[:200].tolist()

# ✅ Sonuçları tutacak liste
analizler = []

# ✅ GPT ile her yorumu analiz et
for i, yorum in enumerate(yorumlar):
    try:
        prompt = f"""
Aşağıdaki kullanıcı yorumunu hem konu hem de duygu açısından değerlendir.
Yalnızca aşağıdaki gibi kısa bir JSON döndür:
{{"konu": "performans/arşiv/arayüz/fiyat/içerik/reklam", "sentiment": "pozitif/negatif/nötr", "sentiment_score": "0-100", "duygu": "mutluluk, utanç, nötr, öfke, korku, üzüntü, şaşkinlik, tiksinti, güven, beklenti, hayal kirikligi, ilgi, sakinlik"}}

Yorum: "{yorum}"
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        gpt_cevap = response.choices[0].message.content.strip()
        sonuc = json.loads(gpt_cevap)

        print(f"[{i+1}] {yorum} → {sonuc}")

        analizler.append({
            "yorum": yorum,
            "konu": sonuc["konu"],
            "sentiment": sonuc["sentiment"],
            "sentiment_score": sonuc["sentiment_score"],
            "duygu": sonuc["duygu"]
        })

        sleep(1.2)

    except Exception as e:
        print(f"[{i+1}] HATA: {e}")
        analizler.append({
            "yorum": yorum,
            "konu": "bilinmiyor",
            "sentiment": "bilinmiyor",
            "sentiment_score": "0",
            "duygu": "bilinmiyor"
        })

# ✅ Sonuçları CSV'ye kaydet (Spotify için ayrı dosya)
analiz_df = pd.DataFrame(analizler)
analiz_df.to_csv("spotify_konu_analizi.csv", index=False)
print("✅ Spotify konu analizi tamamlandı.")
