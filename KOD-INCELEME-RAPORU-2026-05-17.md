# Kod Inceleme Raporu - 2026-05-17

## Kapsam

Incelenen klasor: `AI Reklam Ajansi`

Bu workspace tek bir monolit uygulama degil; Botfusions icin reklam ajansi operasyon dosyalari, CMO dashboard, GSC/NocoDB pipeline, Google Ads MCP alt modulu, SEO yardimci modulleri, Remotion video uretim projesi, gorsel/video varliklari ve hafiza/context dokumanlarindan olusuyor.

## Genel Mimari

- `gsc_api_server.py`: Flask tabanli lokal API. Dashboard'a GSC, PageSpeed, GA4, Google Ads, OmniSocials ve Supabase proxy endpointleri sagliyor.
- `cmo-dashboard.html`: Tek dosyalik CMO dashboard arayuzu. Lokal `http://localhost:8765` API'sine baglaniyor.
- `05-gsc-nocodb/`: GSC verilerini cekip NocoDB'ye yazan agentic pipeline.
- `04-araclar/google_ads_mcp/`: Google Ads MCP server submodule'u.
- `04-araclar/seo-machine-modules/`: SEO, GSC, GA4, landing analizleri icin Python modulleri.
- `04-araclar/remotion-kaynak/`: React + TypeScript + Remotion ile video kompozisyonlari ve render scriptleri.
- `.agents/skills/`: Pazarlama/reklam/SEO/medya skill envanteri.

## Kritik Bulgular

### 1. Canli gizli anahtarlar kod ve dokumanda duruyor

Etki: Yuksek. Repo paylasilirsa sosyal medya yayinlama, Supabase REST erisimi ve Google OAuth client secret bilgileri aciga cikabilir.

Kanıtlar:

- `gsc_api_server.py:302` OmniSocials anahtari kod icinde.
- `gsc_api_server.py:306` Supabase anon JWT kod icinde.
- `04-araclar/seo-machine-modules/modules/google_search_console.py:20-21` Google OAuth client id/secret kod icinde.
- `CLAUDE.md:34` OmniSocials API key dokumanda acik yazilmis.

Oneri:

- Ilgili anahtarlari hemen rotate edin.
- Kodda `os.getenv("OMNI_KEY")`, `os.getenv("SUPA_KEY")`, `os.getenv("GSC_CLIENT_SECRET")` kullanin.
- `.env.example` olusturup sadece degisken adlarini dokumante edin.
- Git gecmisinde bu degerler varsa history temizligi veya repo private tutma karari alin.

### 2. Remotion TypeScript projesi su an typecheck gecmiyor

Komut:

```powershell
cd 04-araclar\remotion-kaynak
npx tsc --noEmit
```

Sonuc:

```text
src/index.ts(2,30): error TS1261: Already included file name ...\src\Root.tsx differs from file name ...\src\root.tsx only in casing.
```

Etki: Orta-yuksek. Windows'ta dosya sistemi case-insensitive oldugu icin sorun gizlenebilir; Linux/CI/render ortaminda build kirilabilir.

Kanıt:

- `04-araclar/remotion-kaynak/src/index.ts:2` import `./Root`
- Gercek dosya `04-araclar/remotion-kaynak/src/root.tsx`

Oneri:

- Import'u `./root` yapin veya dosyayi tek casing standardina tasiyin.
- `forceConsistentCasingInFileNames` varsayilan davranisi korunmali.

### 3. `package.json` ile README arasinda script uyumsuzlugu var

Etki: Orta. Yeni biri README'ye gore calistirinca komut hata verir.

Kanıt:

- README `npm run build:prompts` komutundan bahsediyor.
- `04-araclar/remotion-kaynak/package.json:6-15` icinde `build:prompts` yok; mevcut scriptler `build`, `build:v2`, `build:skills`, `build:geo`, `build:instagram`, `build:geopost`.

Oneri:

- Ya `build:prompts` scriptini ekleyin:

```json
"build:prompts": "npx remotion render PromptsChatVideo out/prompts-chat-video.mp4"
```

- Ya da README'deki komutlari mevcut scriptlerle guncelleyin.

### 4. Runtime'da otomatik `pip install` yapiliyor

Etki: Orta. Sunucu calisirken paket kurmak deterministik degil, internet/sandbox/izin sorunlari cikarir ve ortam guvenligini zayiflatir.

Kanıt:

- `gsc_api_server.py:295-300` `requests` yoksa runtime'da `pip install requests --break-system-packages` calistiriyor.
- `start-cmo-dashboard.bat` baslangicta global pip install yapiyor.
- `05-gsc-nocodb/get_gsc_token.py` benzer sekilde runtime kurulum mantigi iceriyor.

Oneri:

- Kok veya servis bazli `requirements.txt` olusturun.
- Kurulumu tek seferlik setup scriptine tasiyin.
- Uygulama runtime'inda paket kurulumu yapmayin.

### 5. API endpointlerinde auth yok, CORS tamamen acik

Etki: Lokal kullanim icin kabul edilebilir, ancak makine disina acilirsa riskli.

Kanıt:

- `gsc_api_server.py` `Access-Control-Allow-Origin: *` veriyor.
- `/api/publish/video` ve `/api/publish/image` sosyal medyaya yayin tetikleyebiliyor.
- `HOST = "127.0.0.1"` oldugu icin su an lokal sinirlandirma var; bu iyi bir kontrol.

Oneri:

- Host kesinlikle `127.0.0.1` kalsin.
- Yayin endpointlerine basit bir local admin token veya header kontrolu ekleyin.
- CORS'u dashboard origin'i ile sinirlandirin.

## Orta Oncelikli Bulgular

### 6. Git calisma agaci yogun sekilde dirty

`git status --short` cok sayida modified/untracked dosya gosteriyor. Bunlar arasinda gorseller, videolar, `.obsidian/`, raporlar, config dosyalari ve `05-gsc-nocodb/ga4-service-account.json` var.

Risk:

- Neyin kaynak kod, neyin uretilmis cikti oldugu belirsizlesiyor.
- Secret veya buyuk medya dosyalarinin yanlislikla commit edilme riski var.

Oneri:

- `*.json` icin secret adlandirma kurallari ekleyin: `*service-account*.json`, `*credentials*.json`.
- `out/`, medya ciktilari, Obsidian klasoru ve gecici raporlar icin net commit politikasini belirleyin.

### 7. Workspace boyutu buyuk

Olcum:

- Toplam dosya: yaklasik 46.410
- Toplam boyut: yaklasik 1.03 GB

Risk:

- Arama, yedekleme, deployment ve context okuma sureleri artar.
- `node_modules`, `.venv`, medya ciktilari ve submodule dosyalari kaynak kod incelemesini agirlastirir.

Oneri:

- Kod, medya varliklari ve uretilmis ciktilar ayrilmali.
- Deployment paketinde `node_modules`, `.venv`, `out`, video/mp4 ve ham gorseller haric tutulmali.

### 8. GSC/NocoDB pipeline onceki donemle gercek anomali karsilastirmasi yapmiyor

`05-gsc-nocodb/agent.py` icinde `AnomalyDetector.detect(summary)` onceki summary olmadan cagriliyor. Bu nedenle raporda "anomali yok" sonucu yanıltıcı olabilir; cunku karsilastirma verisi verilmemis.

Oneri:

- NocoDB'den onceki `gsc_summary` kaydini okuyup `prev_summary` olarak gecin.
- Rapor metninde "onceki donem bulunamadi" durumunu ayri belirtin.

## Guclu Taraflar

- README ve `CLAUDE.md` proje amacini, klasorleri ve operasyon akisini iyi anlatiyor.
- Flask API'de endpointler islevsel olarak ayrilmis; GSC, OmniSocials, Supabase, yayin ve dashboard isleri okunabilir bloklara bolunmus.
- Remotion projesinde composition mantigi net; GEO video, Instagram reklam ve LinkedIn reklam ciktilari ayri scriptlere ayrilmis.
- Google Ads MCP ayrica submodule olarak tutulmus; ana workspace'e gomulu vendor kod yerine daha izlenebilir bir yapi var.
- `.gitignore` temel Python/Node/build ciktilarini kapsiyor.

## Dogrulama Sonuclari

- `rg --files` ile genel dosya envanteri cikarildi.
- `git status --short` ile calisma agaci kontrol edildi.
- `npx tsc --noEmit` calistirildi ve Remotion casing hatasi nedeniyle basarisiz oldu.
- `python -m py_compile ...` denendi; mevcut Microsoft Store Python launcher `Belirtilen oturum yok` hatasi verdigi icin Python compile dogrulamasi tamamlanamadi.

## Oncelikli Aksiyon Plani

1. Tum acik anahtarlari rotate edin ve `.env` degiskenlerine tasiyin.
2. Remotion `Root.tsx` / `root.tsx` casing hatasini duzeltin.
3. README ile `package.json` scriptlerini esitleyin.
4. Runtime `pip install` bloklarini kaldirip deterministic setup dosyalarina tasiyin.
5. Yayin endpointlerine local auth ekleyin.
6. Dirty git agacini temizleyin: kaynak kod, config, secret, medya ve cikti dosyalarini ayri gruplara ayirin.
7. GSC anomaly agent'inda onceki donem ozetini gercekten okuyacak mekanizmayi ekleyin.

