---
title: "Hafiza Katmani Yapisi"
tags: [hafiza, arsiv, is-akisi]
source: "GOREV.md"
date: 2026-05-17
status: aktif
---

# Hafiza Katmani Yapisi

## Amac
Tum modullerin ortak deposu olarak hafiza katmaninin yapisini ve isleyisini tanimlamak.

## Ne Yapildi
5 alt klasor tanimlandi ve arsiv kurallari belirlendi.

## Anahtar Noktalar
- **rakip-arsivi/** — Gunluk rakip post snapshot'lari
- **trend-log/** — Haftalik trend ozetleri
- **hook-kutuphanesi/** — Denenmis tum hook'lar + performans skoru
- **icerik-arsivi/** — Yayinlanan tum icerikler + metrikler
- **performans-tarihi/** — Uzun donem kanal bazli performans

## Kararlar
- Icerik paketleri yayinlandiktan 7 gun sonra performans notuyla arsivlenir
- Hook kutuphanesi aylik guncellenir, en iyi 20 hook listesi tutulur

## Acik Konular
- Arsiv otomasyonu henuch yok — manuel islem
- Performans skoru metrikleri tanimlanmali

## Kaynaklar
- [GOREV.md](../GOREV.md)

## Ilgili
- [[hafiza-wiki-yapisi]]
