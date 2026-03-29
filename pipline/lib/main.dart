import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:fl_chart/fl_chart.dart';

void main() {
  runApp(const PerfectumApp());
}

class PerfectumApp extends StatelessWidget {
  const PerfectumApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Kozmik Veri İstasyonu',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0A0E21), 
        appBarTheme: const AppBarTheme(color: Color(0xFF111328)),
      ),
      home: const DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  // Grafikte göstereceğimiz veri noktalarını (X, Y) tutacak listeler
  List<FlSpot> kirliVeriNoktalari = [];
  List<FlSpot> temizVeriNoktalari = [];
  bool yukleniyor = false;

  // Python API'mizden veriyi çeken asenkron fonksiyon
  Future<void> verileriGetir() async {
    setState(() { yukleniyor = true; });

    try {
      final url = Uri.parse('http://127.0.0.1:8000/telemetri_getir'); 
      final response = await http.get(url);

      if (response.statusCode == 200) {
        final jsonVeri = jsonDecode(response.body);
        
        // JSON'dan gelen listeleri Dart listelerine almak için
        List<dynamic> kirliVoltajlar = jsonVeri['kirli_veri'];
        List<dynamic> temizVoltajlar = jsonVeri['temiz_veri'];

        List<FlSpot> geciciKirli = [];
        List<FlSpot> geciciTemiz = [];

        // Verileri fl_chart'ın anlayacağı X ve Y koordinatlarına dönüştürmek için
        for (int i = 0; i < kirliVoltajlar.length; i++) {
          // Eğer veri null (radyasyon körlüğü) ise sıfır olarak göstereceğim
          double kirliY = kirliVoltajlar[i] != null ? kirliVoltajlar[i].toDouble() : 0.0;
          double temizY = temizVoltajlar[i].toDouble();

          geciciKirli.add(FlSpot(i.toDouble(), kirliY));
          geciciTemiz.add(FlSpot(i.toDouble(), temizY));
        }

        setState(() {
          kirliVeriNoktalari = geciciKirli;
          temizVeriNoktalari = geciciTemiz;
          yukleniyor = false;
        });
      }
    } catch (e) {
      print("Hata oluştu: $e");
      setState(() { yukleniyor = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🛰️ Perfectum Ventus | Telemetri Paneli', style: TextStyle(fontWeight: FontWeight.bold)),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // Kontrol Paneli Kartı
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF1D1E33),
                borderRadius: BorderRadius.circular(15),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    "Sistem Durumu: Beklemede",
                    style: TextStyle(color: Colors.white70, fontSize: 16),
                  ),
                  ElevatedButton.icon(
                    onPressed: yukleniyor ? null : verileriGetir,
                    icon: yukleniyor 
                        ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                        : const Icon(Icons.download),
                    label: const Text("Veri Akışını Başlat"),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blueAccent,
                      foregroundColor: Colors.white,
                    ),
                  ),
                ],
              ),
            ),
            
            const SizedBox(height: 30),

            // Grafik Alanı
            Expanded(
              child: kirliVeriNoktalari.isEmpty && !yukleniyor
                  ? const Center(child: Text("Veri akışını başlatmak için butona tıklayın.", style: TextStyle(color: Colors.white54)))
                  : Container(
                      padding: const EdgeInsets.only(right: 20, top: 20),
                      decoration: BoxDecoration(
                        color: const Color(0xFF1D1E33),
                        borderRadius: BorderRadius.circular(15),
                      ),
                      // fl_chart kütüphanesi ile grafiği çizdirdim
                      child: LineChart(
                        LineChartData(
                          minY: 0,
                          maxY: 30, // Voltaj radyasyonla 30'lara fırladığı için tavanı yüksek tuttum
                          lineTouchData: const LineTouchData(enabled: false), // Performans için dokunmayı kapattım
                          gridData: const FlGridData(show: true, drawVerticalLine: false),
                          titlesData: const FlTitlesData(
                            topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                            rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                            bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, reservedSize: 30)),
                          ),
                          lineBarsData: [
                            // 1. Çizgi: Kırmızı ve kesik (Radyasyonlu Kirli Veri)
                            LineChartBarData(
                              spots: kirliVeriNoktalari,
                              isCurved: true,
                              color: Colors.redAccent.withOpacity(0.5),
                              barWidth: 2,
                              isStrokeCapRound: true,
                              dotData: const FlDotData(show: false),
                            ),
                            // 2. Çizgi: Parlak Mavi ve kalın (Temiz Veri)
                            LineChartBarData(
                              spots: temizVeriNoktalari,
                              isCurved: true,
                              color: Colors.cyanAccent,
                              barWidth: 4,
                              isStrokeCapRound: true,
                              dotData: const FlDotData(show: false),
                              belowBarData: BarAreaData(
                                show: true,
                                color: Colors.cyanAccent.withOpacity(0.1),
                              )
                            ),
                          ],
                        ),
                        // Grafik yüklendiğinde hafif bir animasyonla gelsin diye
                        duration: const Duration(milliseconds: 800),
                        curve: Curves.easeInOut,
                      ),
                    ),
            ),
            
            const SizedBox(height: 20),
            
            // Lejant (Bilgi Kutusu)
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildLegendItem(Colors.redAccent.withOpacity(0.5), "Radyasyonlu (Ham) Veri"),
                const SizedBox(width: 20),
                _buildLegendItem(Colors.cyanAccent, "Filtrelenmiş Temiz Veri"),
              ],
            )
          ],
        ),
      ),
    );
  }

  // Lejant elemanlarını oluşturan küçük bir yardımcı widget
  Widget _buildLegendItem(Color color, String text) {
    return Row(
      children: [
        Container(width: 15, height: 15, decoration: BoxDecoration(color: color, shape: BoxShape.circle)),
        const SizedBox(width: 5),
        Text(text, style: const TextStyle(color: Colors.white70)),
      ],
    );
  }
}