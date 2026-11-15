# AZURA - SPHEREx Sky Movie — Proje Briefi (Yapay Zeka Ajanları İçin)

Bu belge, projeyi geliştirmesi veya düzenlemesi için görevlendirilecek yapay zeka ajanları (Cursor, Claude Code, Antigravity vb.) içindir. Projeye bu dosyayı okumadan müdahale etmeyin.

---

## 1. Projenin Amacı Nedir?

**Yarışma:** NASA Space Apps Challenge 2026 — "Planet X and SPHEREx" challenge'ı.
**Challenge'ın resmi görevi:** NASA'nın SPHEREx görevinden elde edilen gökyüzü görüntülerini sergileyen ve herkesin zaman içindeki değişimleri hızlıca görmesini kolaylaştıran, **herkese açık bir web aracı** oluşturmak. Kullanıcı koordinat (RA/Dec) girecek, araç bu gökyüzü bölümünün bir dizi görüntüsünü küçük bir video gibi (blink movie) gösterecek — böylece hareket eden nesneler (asteroitler, kuyruklu yıldızlar, kahverengi cüceler, yüksek özdevinimli yıldızlar) tespit edilecek. Bu, Plüton'un 1930'da keşfetme yönteminin (iki görüntü arasında ışık noktası kayması) modern hali.

**Takım:** AZURA — tek kişi + yapay zeka destekli geliştirme.
**Hedef kitle:** Astronomi meraklıları, sivil bilim gönüllüleri (backyardworlds.org topluluğu gibi), öğrenciler.

## 2. Ne İçin Kullanılacak? (Kullanım Senaryosu)

1. Kullanıcı sayfayı açar — varsayılan hedef (Barnard's Star) otomatik yüklenir.
2. Dört hazır hedeften birini seçer veya kendi RA/Dec koordinatını girer:
   - Barnard's Star (RA 269.4520, Dec 4.6933, FOV 0.5°)
   - WISE 0855 (RA 133.7953, Dec -7.2451, FOV 0.5°) — hızlı hareket eden kahverengi cüce, challenge metninde verilmiş koordinatlar
   - Epsilon Indi B (RA 330.8040, Dec -56.7860, FOV 0.4°)
   - RW Aurigae (RA 76.9850, Dec 30.4010, FOV 0.2°)
3. "Fetch epochs and build movie" butonuna basar.
4. Araç IRSA'dan o konumu kaplayan tüm SPHEREx epoch'larını zaman sırasıyla getirir, ön yükleme yapar, blink animasyonu oynatır.
5. "Difference" modu: epoch N - epoch N-1 fark görüntüsü — hareketli kaynaklar dipol çift olarak belirir.
6. "Spectrum" (deneysel): 6 dedektör bandpass'ı üzerinden merkez piksel flux'ı vs dalga boyu grafiği.
7. URL parametreleri (`?ra=&dec=&fov=&band=`) ile sorgu paylaşılabilir — başka sitelere gömülebilir.

## 3. Veri Kaynağı (Kodda Kullanıldığı Haliyle)

- **Servis:** NASA/IPAC Infrared Science Archive (IRSA), Caltech.
- **TAP sorgusu:** `astroquery.ipac.irsa.Irsa.query_tap()` ile. Tablolar: `spherex.artifact` (a) × `spherex.plane` (p), `a.planeid = p.planeid` join. Sorgu şablonu `app.py` içinde `TAP_TEMPLATE` sabitindedir.
- **Cutout URL kalıbı:** `https://irsa.ipac.caltech.edu/' || a.uri || '?center={ra},{dec}d&size={size}'` — yani artifact URI'sinin başına IRSA base URL'si, sonuna merkez koordinat (derece, 'd' sonekiyle) ve boyut (derece) eklenir.
- **Band filtresi:** `p.energy_bandpassname` alanı, değerler `SPHEREx-D1` ... `SPHEREx-D6` (altı dedektör dizisi). `app.py` içinde regex `_BAND_RE` ile doğrulanır.
- **Sıralama:** `p.time_bounds_lower` (zaman sıralı blink için).
- **Aktif veri sürümleri:** DR1 ve QR3 (QR2 süperseded). Kod tablolara `spherex.artifact` üzerinden gittiği için sürüm güncellemelerinden etkilenmez — yeni veri haftalık ingest edilir.
- **Atıf zorunluluğu:** README'de IRSA atıf metni var; submission'da korunmalı.

## 4. Mimari ve Dosya Ağacı

```
spherex-sky-movie/
├── app.py                 # Flask backend (tek dosya): TAP proxy + FITS->PNG + cache
├── static/
│   └── index.html         # Tek sayfa frontend: vanilla JS + Aladin Lite v3 (CDN)
├── requirements.txt       # flask, requests, numpy, pillow, astropy, astroquery
├── README.md              # Kamu yüzyüze README (kurulum, deploy, atıflar)
├── PROJECT_BRIEF.md       # Bu dosya — AI ajanları için brief
└── data/
    ├── demo_cutouts.json  # IRSA erişilemezse fallback frame listesi (opsiyonel)
    └── cache/             # Render edilmiş PNG önbelleği (çalışma anında oluşur)
```

**Backend endpoint'leri (app.py):**
- `GET /` → `static/index.html`
- `GET /api/query?ra=&dec=&size=&band=&limit=` → `{ok, frames:[{uri,time,demo}], error}` — TAP sorgusu, zaman sıralı epoch listesi. Hatalı girdide bile **her zaman JSON** döner (input validasyonu: ra 0-360, dec -90/+90, size 0.01-1.5, band regex, limit 1-200).
- `GET /api/cutout?uri=` → PNG (FITS cutout indirilir, sqrt-stretch uygulanır, 384px PNG). Sadece `https://irsa.ipac.caltech.edu/` ile başlayan URI kabul edilir (SSRF koruması). Üç katmanlı cache: RAM → disk (`data/cache/`) → render.
- `GET /api/difference?uri1=&uri2=` → fark PNG'si (b - a). FITS dizileri RAM'de LRU cache'lenir (son 300), ikinci istekte NASA'ya gitmez.
- `GET /api/spectrum?ra=&dec=&size=` → `{ok, points:[{wavelength_um, flux, detector}]}` — deneysel, 6 dedektör için merkez piksel.
- `GET /favicon.ico` → 204 (log gürültüsünü önler).

**Frontend (index.html) akışı:**
1. `DOMContentLoaded` → URL parametreleri okunur, `loadMovie()` çağrılır.
2. `/api/query` cevabı JSON olmayan bir şey gelirse (500/HTML) frontend `content-type` kontrolüyle yakalar, okunur hata gösterir.
3. Tüm kareler `Promise.all` ile **bir kez** preload edilir (`imgCache[]`), ilerleme "Preloading frames... X/N" olarak gösterilir.
4. Oynatma/seek/scrub sadece canvas'a cache'den çizim yapar — ağ isteği yok.
5. `draw(i)` fonksiyonu `frames[i]` yoksa guard ile çıkar; `play()` boş frames'te çalışmaz. `window.error` yakalayıcı son çare "crash yerine dur" sağlar.

## 5. Nasıl Çalıştırılır?

```bash
pip install -r requirements.txt
python app.py            # http://localhost:5000
```
Windows'ta sanal ortam: `python -m venv venv` → `venv\Scripts\activate` → `pip install -r requirements.txt` → `python app.py`.

Deploy: PythonAnywhere (Flask, kurulum gerektirmez) veya Render/Railway/Fly.io (start: `python app.py`). Frontend tek başına GitHub Pages'te çalışmaz — CORS yüzünden proxy şart.

## 6. Şu An Çalışanlar (Doğrulanmış)

- Flask sunucu ayağa kalkar, `/` 200, `/favicon.ico` 204 döner (sandbox'ta curl ile test edildi).
- Tüm API endpoint'leri hatalı/boş girdide tutarlı JSON döner — HTML 500 sayfası yok (curl ile 7 edge-case test edildi: missing params, bad ra, out-of-range, bad band, evil uri, bad spectrum).
- Frontend'de tüm `frames[i].xxx` erişimleri guard'lı; "Cannot read properties of undefined (reading 'time')" hatasının kök nedeni giderildi.
- Cache sistemi: replay/seek/difference tekrarında ağ isteği yok.
- Otomatik retry: IRSA'nın arada 502 döndüğü durumda 3 deneme (1.5s/3s/4.5s backoff).

## 7. Bilinen Hatalar ve Sınırlamalar

1. **IRSA sandbox'tan erişilemiyor:** Geliştirme ortamında (bu sandbox) IRSA'ya gerçek veri çekme testi yapılamadı — `502 Proxy Error`. Bu yüzden "gerçek FITS indirildi → PNG render edildi" akışı **kullanıcı makinesinde** doğrulanmalı. Sunucu kodu ve fallback (demo mode) bu durumda çalışıyor.
2. **IRSA arada 502 döndürüyor:** Ücretsiz servis; retry var ama 3 deneme de düşerse o kare boş kalır. Frontend boş kareyi atlar (crash etmez).
3. **Spectrum deneysel:** WCS'den dalga boyu okuma her MEF'te çalışmayabilir; hata durumunda "Spectrum: no data" mesajı gösterilir, çökmez.
4. **Difference sadece ardışık epoch'lar arasında anlamlı:** İki epoch arasında cisim kareyi terk ederse dipol görünmez.
5. **Yüksek özdevinimli hedefler kareyi terk edebilir:** FOV 0.4-0.5° ile geniş tutuldu; gerekirse 0.8'e çıkar.
6. **Aladin arka plan opsiyonel:** CDN yüklenmezse uygulama çalışmaya devam eder.

## 8. Hedeflenen Özellikler ve Yol Haritası (Challenge "Potansiyel Hususlar"dan)

- [ ] **102 bandın tamamını gösterme:** Şu an 6 dedektör bandpass'ı (D1-D6) var; challenge 102 near-IR bandını görselleştirmeyi öneriyor. TAP sorgusunda `energy_bandpassname` yerine bant listesi genişletilmeli.
- [ ] **Sinyal-gürültü iyileştirme:** Altı dedektör dizisinden gelen verilerin ayrı ayrı toplanması (challenge ipucu: bu ekstra puan kazandırır).
- [ ] **Görüntü ekleme/çıkarma seçenekleri:** Difference modunun genişletilmesi (kullanıcı seçimli epoch çifti).
- [ ] **Gaia/WISE kataloğu bindirme:** Aladin Lite UI üzerinden mümkün; UI'da açık buton yapılmalı.
- [ ] **Yeni veri sürümleriyle kolay güncelleme:** Zaten TAP üzerinden; QR4/DR2 geldiğinde kod değişikliği gerekmemeli (doğrulanacak).
- [ ] **Meta veri gösterimi:** Kirlenme işaretleri (contamination flags) — MEF header'larından okunabilir.
- [ ] **Performans:** Sunucu tarafı frame render'ının paralelleştirilmesi (şu an istek başına tek FITS).
- [ ] **Demo video + submission:** 3 dakikalık video, GitHub repo, executive summary (≤150 kelime) — submission checklist'i README'de.

## 9. AI Ajanları İçin Kritik Kurallar

1. `app.py`'deki `TAP_TEMPLATE` ve cutout URL kalıbı **resmi IRSA tutorial'ından** alınmıştır — değiştirmeyin; sadece `band` ve koordinatlar değişken.
2. Backend'in **her hata yolunda JSON** döndürmesi gerekiyor — yeni endpoint eklerken bu sözleşmeyi bozmayın (HTML error page frontend'i çökertir).
3. Frontend'de `frames[i].xxx` gibi korumasız erişim bırakmayın; tüm property erişimleri guard'lı olmalı.
4. Emoji kullanmayın (kod, UI metinleri ve README dahil) — takım kararı.
5. Renk paleti: koyu lacivert #0A1F44, azure #3D8BFD, buz mavisi #BFE0FF, arka plan #05080f. Tipografi: sistem fontu.
6. Test etmek için: `python app.py` → http://localhost:5000 → varsayılan Barnard's Star otomatik yüklenir.

---

*Bu brief 15 Kasım 2026'da, kodun o anki gerçek durumundan (v4) derlenmiştir.*
