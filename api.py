from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest 

app = FastAPI(title="Perfectum Ventus - Kozmik Veri API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/telemetri_getir")
def telemetri_verilerini_getir():
    print("Flutter'dan istek geldi! Makine Öğrenmesi modeli çalışıyor...")
    
    # 1. Ham Veriyi Okumak için
    df = pd.read_csv('uydu_telemetri.csv')
    
    # ML modelinin kafası karışmasın diye önce NaN (Boş) değerleri hızlıca doldurdum
    df['Gecici_Voltaj'] = df['Bozuk_Voltaj'].interpolate(method='linear').bfill().ffill()
    
    # MAKİNE ÖĞRENMESİ AŞAMASI 
    print("İzolasyon Ormanı (Isolation Forest) anomalileri arıyor...")
    
    # Modeli tanımlıyoruz. contamination=0.05 demek "Benim tahminimce verimin %5'i radyasyonlu" demektir.
    ml_modeli = IsolationForest(contamination=0.05, random_state=42)
    
    # Modeli eğitiyoruz ve tahmin yaptırıyoruz.
    # Model normal verilere 1, anomali (radyasyon) bulduğu yerlere -1 etiketini basarcak
    df['Radyasyon_Tespiti'] = ml_modeli.fit_predict(df[['Gecici_Voltaj']])
    
    # ONARIM AŞAMASI
    # Modelin "-1" (Radyasyon!) dediği yerleri tespit edip o değerleri sildim (NaN yaptım)
    df.loc[df['Radyasyon_Tespiti'] == -1, 'Gecici_Voltaj'] = np.nan
    
    # Sildiğim o hastalıklı pikselleri, yanındaki sağlıklı verilere bakarak (İnterpolasyon) düzelttim
    df['Filtreli_Voltaj'] = df['Gecici_Voltaj'].interpolate(method='linear').bfill().ffill()
    
    # Veriyi Flutter'a hazırlama
    df['Zaman'] = pd.to_datetime(df['Zaman']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df_subset = df.head(100)
    
    df_subset = df_subset.replace({np.nan: None})
    
    paket = {
        "durum": "basarili",
        "mesaj": "Veriler Isolation Forest Yapay Zeka modeliyle temizlendi.",
        "zaman_etiketleri": df_subset['Zaman'].tolist(),
        "kirli_veri": df_subset['Bozuk_Voltaj'].tolist(),
        "temiz_veri": df_subset['Filtreli_Voltaj'].tolist()
    }
    
    return paket