# Sprint 1 Raporu — Scrum Master

**Takım:** AZURA · **Challenge:** Planet X and SPHEREx · **Tarih:** 14 Kasım 2026 (hackathon 1. gün)
**Scrum Master:** *(isim)*

## Sprint Hedefleri ve Planlanan Görevler

1. Challenge analizi ve problem tanımı (SPHEREx görüntülerinden blink movie aracı)
2. Veri kaynağı keşfi: IRSA TAP, cutout servisi, uygun tablolar ve filtreler
3. Çalışan Minimum Yaşanabilir Ürün (MVP): koordinat girişi → epoch listesi → blink animasyonu
4. Difference ve Spectrum modlarının ilk sürümleri
5. Hata dayanıklılığı: her hata yolunda JSON sözleşmesi, otomatik retry, çok katmanlı cache

## Tamamlanan Çalışmalar

- Challenge metni analizi; test hedefleri belirlendi (Barnard's Star, WISE 0855, Epsilon Indi B, RW Aurigae)
- IRSA veri erişimi doğrulandı: `spherex.artifact` × `spherex.plane` TAP sorgusu + cutout URL kalıbı
  (resmi IRSA tutorial kalıbıyla)
- Backend MVP (app.py): TAP proxy, FITS → PNG (sqrt-stretch), `/api/query`, `/api/cutout`,
  `/api/difference`, `/api/spectrum` endpoint'leri
- Frontend MVP (static/index.html): vanilla HTML5+JS, Aladin Lite arka plan, 4 preset hedef,
  blink oynatıcı, scrub, URL parametreleri
- Dayanıklılık: 9 edge-case testi — eksik/geçersiz parametre, aralık dışı, kötü band, evil URI —
  tümü tutarlı JSON döndü; frontend'de tüm property erişimleri korumalı hale getirildi
  ("Cannot read properties of undefined (reading 'time')" hatası kökünden giderildi)
- Performans: 3 denemeli retry + backoff; FITS LRU cache (300); PNG RAM+disk cache;
  tarayıcıda ön yükleme + Cache-Control — replay/seek anlık
- Yerleşik demo modu: IRSA TAP kesintiye uğradığında sentetik epoch'larla film oynamaya devam eder

## Tamamlanamayan Çalışmalar

- IRSA TAP'ın gerçek verisiyle uçtan uca doğrulama: TAP sunucusu hackathon günü 502 Proxy Error
  veriyordu (hem geliştirici makinesi hem ikinci bağımsız ağdan sınandı). Demo mod devreye girdi.
- 102 bandın tamamının görselleştirilmesi (şu an 6 dedektör bandpass'ı) — Sprint 3 hedefi
- Dedektör dizilerinin toplanmasıyla sinyal-gürültü iyileştirme — Sprint 3 hedefi

## Karşılaşılan Sorunlar

| Sorun | Tür |
|---|---|
| IRSA TAP 502 Proxy Error (upstream) | Teknik / dış bağımlılık |
| Frontend'de stale frames durumunda TypeError | Teknik |
| Aynı karelerin tekrar tekrar indirilmesi (yavaşlık) | Teknik / performans |
| Solo takımda görev dağılımı | Organizasyonel |

## Uygulanan Çözümler

1. **TAP 502:** otomatik 3 deneme + backoff; kalıcı kesintide sentetik demo epoch fallback'i —
   araç her koşulda çalışır hale geldi
2. **TypeError:** backend'de "her hata JSON" sözleşmesi + input validasyonu; frontend'de guard'lı
   erişimler ve content-type kontrolü
3. **Yavaşlık:** FITS dizileri için LRU cache, PNG için RAM+disk cache, tarayıcıda toplu ön yükleme;
   replay/seek artık ağ isteği yapmıyor
4. **Solo organizasyon:** yapay zeka ajanları (Cursor / Claude Code / Genspark) geliştirme
   ortakları olarak kullanıldı; PROJECT_BRIEF.md ile ajanlara bağlam ve kurallar verildi

## Takım Üyelerinin Katkıları

- **Scrum Master (tek kişi):** problem tanımı, mimari, backend + frontend geliştirme, test,
  dokümantasyon, sprint raporu
- **Yapay zeka ajanları:** kod üretimi, hata teşhisi (log analizi), edge-case sınaması, dokümantasyon
  düzenlemesi

## Bir Sonraki Sprint İçin Hedefler

1. IRSA TAP ayıldığında gerçek veriyle uçtan uca doğrulama (ilk öncelik)
2. 17/102 band görselleştirmesine geçiş için bant listesi ve seçici UI
3. Demo videosu senaryosu ve çekimi (3 dk)
4. GitHub Pages statik tanıtım sayfasının canlıya alınması
