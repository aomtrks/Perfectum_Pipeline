import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def clean_telemetry_data(file_path):
    print("1. Bozuk telemetri verisi uzaydan alınıyor (CSV okunuyor)...")
    df = pd.read_csv(file_path)
    
    # Zaman sütununu tekrar tarih formatına çevirmek için
    df['Zaman'] = pd.to_datetime(df['Zaman'])
    
    print("2. Aşama 1 Filtresi: Sensör Körlükleri (NaN) gideriliyor...")
    # İnterpolasyon (Linear): Boş veriyi, bir önceki ve bir sonraki verinin ortalamasını alarak tahmin eder.
    df['Filtreli_Voltaj'] = df['Bozuk_Voltaj'].interpolate(method='linear')
    
    print("3. Aşama 2 Filtresi: Radyasyon Sıçramaları (SEU) temizleniyor...")
    # Kayan Medyan Filtresi (Rolling Median): 
    # window=5 demek, her bir veri noktası için kendisine, 2 sağına ve 2 soluna bakar.
    # Bu 5 değer içindeki "ortanca" değeri seçer. Böylece anlık uçuk fırlamalar yok edilir.
    df['Filtreli_Voltaj'] = df['Filtreli_Voltaj'].rolling(window=5, center=True).median()
    
    # Uçlarda (ilk 2 ve son 2 satırda) rolling yüzünden NaN oluşabilir diye
    df['Filtreli_Voltaj'] = df['Filtreli_Voltaj'].bfill().ffill()
    
    print("4. Başarı Oranı Hesaplanıyor...")
    # Temizlediğimiz veri, orijinal kusursuz veriye ne kadar yaklaştı? test
    hata_payi = np.abs(df['Temiz_Voltaj'] - df['Filtreli_Voltaj']).mean()
    print(f"-> Orijinal veriden ortalama sapma (Hata Payı): Sadece {hata_payi:.3f} Volt!")
    
    return df

if __name__ == "__main__":
    # Az önce ürettiğimiz dosyayı okumak için
    temizlenmis_veri = clean_telemetry_data('uydu_telemetri.csv')
    
    # Sonuçları çizdirmek için
    plt.figure(figsize=(14, 7))
    
    # 1. Bozuk Veri (Arka planda soluk kırmızı)
    plt.plot(temizlenmis_veri['Zaman'], temizlenmis_veri['Bozuk_Voltaj'], 
             label='Kozmik Gürültülü Veri', color='red', alpha=0.3, linestyle='--')
    
    # 2. Bizim Temizlediğimiz Veri (Kalın Mavi)
    plt.plot(temizlenmis_veri['Zaman'], temizlenmis_veri['Filtreli_Voltaj'], 
             label='Perfectum Pipeline ile Temizlenmiş Veri', color='blue', linewidth=2)
    
    # 3. Gerçek/Orijinal Veri (Siyah Kesik Çizgi - Ne kadar yaklaştığımızı görmek için)
    plt.plot(temizlenmis_veri['Zaman'], temizlenmis_veri['Temiz_Voltaj'], 
             label='Orijinal Hedef Veri', color='black', alpha=0.8, linestyle=':')
    
    plt.title("Uzay Çevre Şartlarında Otonom Veri Kurtarma (Filtreleme Aşaması)")
    plt.xlabel("Zaman (Saat)")
    plt.ylabel("Batarya Voltajı (V)")
    plt.legend()
    plt.grid(True)
    plt.show()