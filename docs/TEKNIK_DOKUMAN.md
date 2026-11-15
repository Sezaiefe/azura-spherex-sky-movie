# Teknik Dokümantasyon — AZURA SPHEREx Sky Movie

## 1. Sistem Bileşenleri

### 1.1 Backend (`app.py`) — tek dosya Flask

| Endpoint | Girdi | Çıktı | Açıklama |
|---|---|---|---|
| `GET /` | — | `static/index.html` | Tek sayfa uygulama |
| `GET /api/query` | `ra` (0–360), `dec` (−90/+90), `size` (0.01–1.5), `band` (`SPHEREx-D1..D6`), `limit` (1–200) | `{ok, frames:[{uri,time,demo}], error}` | TAP sorgusu; zaman sıralı epoch listesi. TAP düşükse sentetik demo epoch'ları döner (`demo: true`) |
| `GET /api/cutout` | `uri` (IRSA veya `local://demo/`) | PNG (384px) | FITS cutout indirir, sqrt-stretch uygular |
| `GET /api/difference` | `uri1`, `uri2` | PNG | b − a farkı; hareketli kaynak dipol çıkar |
| `GET /api/spectrum` | `ra`, `dec`, `size` | `{ok, points:[{wavelength_um, flux, detector}]}` | Deneysel: 6 dedektör için merkez piksel |
| `GET /favicon.ico` | — | 204 | Log gürültüsünü önler |

**Sözleşme:** her hata yolunda JSON döner (HTML 500 yok). Input validasyonu `_num` / `_int_num`
yardımcılarıyla yapılır; band regex `_BAND_RE` ile beyaz listededir. Cutout URI'ları yalnızca
`https://irsa.ipac.caltech.edu/` veya `local://demo/` önekli olabilir (SSRF koruması).

### 1.2 Performans Katmanı

- `_fetch()`: 3 deneme + üstel backoff (1.5s / 3s / 4.5s) — IRSA'nın arada 502 dönmesine karşı
- `_ARR_CACHE`: çözülmüş FITS dizileri, LRU, 300 giriş — difference ikinci kez NASA'ya gitmez
- `_MEM_PNG` + `data/cache/`: render edilmiş PNG'ler RAM + disk
- Tarayıcı: `Cache-Control: public, max-age=86400`
- Frontend: tüm kareler bir kez preload edilir (`imgCache[]`), oynatma/seek/scrub ağ isteği yapmaz

### 1.3 Frontend (`static/index.html`)

Tek dosya, framework yok, build yok. Aladin Lite v3 (CDN) opsiyonel gökyüzü arka planı.
Tüm `frames[i].xxx` erişimleri guard'lı; JSON olmayan cevap `content-type` kontrolüyle yakalanır;
`window.error` son çare yakalayıcıdır. URL parametreleri (`?ra=&dec=&fov=&band=`) yükleme anında okunur.

## 2. Veri Akışı (gerçek mod)

1. Kullanıcı koordinat girer → `/api/query`
2. Backend `astroquery.ipac.irsa.Irsa.query_tap()` çağırır:

```sql
SELECT TOP {limit}
    'https://irsa.ipac.caltech.edu/' || a.uri || '?center={ra},{dec}d&size={size}' AS uri,
    p.time_bounds_lower AS obs_time
FROM spherex.artifact a
JOIN spherex.plane p ON a.planeid = p.planeid
WHERE 1 = CONTAINS(POINT('ICRS', {ra}, {dec}), p.poly)
  AND p.energy_bandpassname = '{band}'
ORDER BY p.time_bounds_lower
```

3. Frontend her `uri` için `/api/cutout` çağırır → PNG
4. Blink animasyonu + scrub + difference + spectrum

Bu sorgu kalıbı resmi IRSA tutorial'ından alınmıştır:
https://github.com/Caltech-IPAC/irsa-tutorials/blob/main/tutorials/spherex/spherex_cutouts.md

## 3. Veri Sürümleri

- Aranabilir sürümler: **DR1** ve **QR3** (QR2 süperseded, Şubat 2027'ye kadar indirilebilir)
- Kod `spherex.artifact` / `spherex.plane` tablolarına gittiği için yeni sürümler (QR4, DR2) kod
  değişikliği gerektirmez — IRSA haftalık ingest yapar

## 4. Demo Modu (IRSA erişilemezken)

TAP düşükse veya konumda kapsam yoksa sunucu 12 sentetik epoch üretir: gürültü alanı + 4 sabit
alan yıldızı + epoch başına ~2 piksel kayan tek kaynak. URI şeması `local://demo/<i>?ra=..&dec=..`;
cutout ve difference endpoint'leri bu şemayı da işler. Amaç: jüri ve kullanıcı **her koşulda**
aracın ne yaptığını görebilsin.

## 5. Bilinen Sınırlar

1. Spectrum deneysel — WCS dalga boyu okuma her MEF'te çalışmayabilir
2. Difference ardışık epoch'lar arasında anlamlıdır; cisim kareyi terk ederse dipol görünmez
3. Yüksek özdevinimli hedefler için FOV 0.4–0.5° önerilir; gerekirse 0.8'e çıkar
4. İlk yükleme ağ hızına bağlı 10–60 sn sürebilir; sonrasında cache devrededir

## 6. Test Edilen Yollar (15 Kas 2026, v5)

- 9 edge-case (eksik/geçersiz parametre, aralık dışı, kötü band, evil URI, boş cevap) → tümü tutarlı JSON
- Demo fallback: `/api/query` TAP hatasında 12 demo epoch döndü; `/api/cutout` ve `/api/difference`
  demo URI'larıyla 200 PNG üretti
- Gerçek IRSA FITS → PNG yolu, IRSA TAP kesintisi nedeniyle sandbox/sahne makinelerinde uçtan uca
  doğrulanamadı; TAP ayıldığında aynı kod yolu otomatik devreye girer

## 7. Yol Haritası (challenge "Potansiyel Hususlar"dan)

- [ ] 102 bandın tamamının görselleştirilmesi (şu an 6 dedektör bandpass'ı)
- [ ] Altı dedektör dizisinin ayrı ayrı toplanarak sinyal-gürültü iyileştirme (challenge ipucu: ekstra puan)
- [ ] Kullanıcı seçimli epoch çiftiyle genişletilmiş difference
- [ ] Gaia/WISE katalog bindirme butonu (Aladin UI üzerinden mümkün)
- [ ] Kirlenme işaretleri (contamination flags) MEF header'larından gösterim
- [ ] Sunucu tarafı paralel render
