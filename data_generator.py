import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_telemetry_data(senaryo="karisik"):
    print(f"Uydu zaman çizelgesi oluşturuluyor... (Seçilen Senaryo: {senaryo.upper()})")
    time_index = pd.date_range(start='2026-01-01', periods=720, freq='h')
    t = np.linspace(0, 30, 720) 
    
    clean_signal = 12.0 + np.sin(t) * 2.0 + np.random.normal(0, 0.2, 720)
    df = pd.DataFrame({'Zaman': time_index, 'Temiz_Voltaj': clean_signal})
    df['Bozuk_Voltaj'] = df['Temiz_Voltaj'].copy()
    
    # 1. SENARYO: Anlık Radyasyon Sıçramaları (SEU)
    if senaryo in ["seu", "karisik"]:
        num_anomalies = int(len(df) * 0.05) 
        anomaly_indices = np.random.choice(df.index, num_anomalies, replace=False)
        for idx in anomaly_indices:
            df.loc[idx, 'Bozuk_Voltaj'] += np.random.choice([15.0, -15.0]) * np.random.random()

    # 2. SENARYO: Güneş Fırtınası Gürültüsü (Sürekli dalgalanma)
    if senaryo in ["firtina", "karisik"]:
        # 200. saat ile 300. saat arasında devasa bir manyetik fırtına kopsun
        firtina_indeksleri = df.index[200:300] 
        df.loc[firtina_indeksleri, 'Bozuk_Voltaj'] += np.random.normal(0, 5.0, 100) # Ciddi gürültü ekler

    # 3. SENARYO: Sensör Körlüğü (Uzun süreli veri kopması)
    if senaryo in ["kesinti", "karisik"]:
        # 450. ile 500. saatler arası sensör tamamen kapansın
        kesinti_indeksleri = df.index[450:500] 
        df.loc[kesinti_indeksleri, 'Bozuk_Voltaj'] = np.nan

    print("Felaket verisi üretimi tamamlandı!")
    return df

if __name__ == "__main__":
    # Test etmek istediğiniz senaryoyu buraya yazın: "seu", "firtina", "kesinti" veya "karisik"
    uydu_verisi = generate_telemetry_data(senaryo="karisik")
    
    uydu_verisi.to_csv('uydu_telemetri.csv', index=False)
    print("Veriler 'uydu_telemetri.csv' dosyasına kaydedildi.")
    
    plt.figure(figsize=(12, 6))
    plt.plot(uydu_verisi['Zaman'], uydu_verisi['Bozuk_Voltaj'], label='Felaket Senaryosu (Kirli)', color='red', alpha=0.6)
    plt.plot(uydu_verisi['Zaman'], uydu_verisi['Temiz_Voltaj'], label='Hedeflenen (Temiz)', color='green', alpha=0.8)
    plt.title("Uzay Felaketleri Simülasyonu")
    plt.legend()
    plt.show()