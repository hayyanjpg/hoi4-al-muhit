# Grand Sultanate of Al-Muhit

Mod HOI4 1.20.x. Tanpa konversi peta (tidak ada error map).

## Isi mod
- Tag `EGY` (GSM di vanilla adalah Gansu Ma, jadi tidak dipakai).
- 8 state Mesir merdeka: `owner = EGY`, `add_core_of = EGY`.
- Semua state Mesir: `state_category = megalopolis`.
- Nama tampil: **Grand Sultanate of Al-Muhit** (termasuk kunci
  `EGY_neutrality`, bukan hanya `EGY`).
- Kota/state dinamai ulang: Dar al-Khilafah, Al-Qasr, Bandar Al-Nur, dll.
- Pemimpin: **Khalifah Harun al-Rashid**.
- Total SDA nasional: steel 752, tungsten 300, rubber 50, chromium 210, coal 300, aluminium 200, oil 320.
- **112/112 shared slot industri terisi penuh**: 45 military factory,
  39 dockyard, 28 civilian factory (40/35/25 persen).
  Dockyard tidak ditempatkan di 456-Luxor & 552-Western Egypt karena
  aturan `only_costal = yes`.
- 11 state core Sudan, Transjordan (JOR), Israel, Lebanon diambil alih
  (`owner = EGY` + `add_core_of = EGY`) dan jadi `large_city`.
- 99/99 slot industri di wilayah baru: 30 military, 49 civilian,
  20 dockyard (30/50/20 persen).
- 3 field marshal + 12 general dengan stat acak 4-5 (seed 20261123),
  trait sudah disesuaikan dengan role (type = land/field_marshal untuk
  marshal, type = land/corps_commander untuk general). Khalid ibn al-Walid
  memakai stat khusus: 7/8/4/6/6.
- 5 admiral dengan stat acak 3-5 (stat utama fokus dijamin 5):
  2 submarine, 2 permukaan campuran (destroyer + battleship + CV),
  1 manajemen.
  Semua sudah di-`recruit_character` di 1936.
- Warna peta/UI negara: emas (212 175 55 / 255 215 100); bendera `EGY` emas
  (basis 212 175 55, pinggir 255 215 100, lambang perunggu 96 68 16).
  Bendera `CAL` sesudah proklamasi: emas terang (255 215 100) dengan lambang
  dan pinggir perunggu, jadi jelas berubah dari bendera `EGY`.
- Tampilan kota: hanya `map/cities.bmp` yang di-override. Piksel gaya `unciv`
  (indeks 2) di 19 state mod diganti jadi gaya `westerngfx` (indeks 15),
  sehingga kota Mesir tampak seperti New York/London. File `map/` lain
  tetap vanilla (tidak ada konversi peta yang dulu menyebabkan error).
- Tech awal: 200 tech dari save Al-Muhit 1941.12.1 (199 level 1, mechanised_infantry2 level 2).
- Grand doctrine seperti awal: hanya `grand_battleplan`.
- 4 research slot sejak 1936.
- Focus tree `egy_tree` berisi 3 focus berurutan:
  1. `EGY_scientific_industrial_renaissance` (+100 PP; idea dockyard output sudah
     jadi bawaan sejak 1936, fokus ini jadi tambahan PP).
  2. `EGY_islamic_unity` (+150 PP, +15000 manpower).
  3. `EGY_proclaim_caliphate` — syarat sama dengan decision, memicu event
     `gsm_caliphate.1` (jalur alternatif selain decision).
- Sejak 1936 Khalifah memakai `gsm_stability` (+10% stability) dan negara
  sudah punya national spirit bawaan `gsm_scientific_industry` (+10% dockyard
  output). Trait `gsm_caliph` setelah proklamasi bersifat kosmetik.
- Decision `gsm_proclaim_caliphate` muncul bila TUR/IRQ/SAU/ISR/LEB/JOR sudah
  jadi vassal EGY atau tidak ada lagi (dianeksasi). Mengambilnya memicu event
  `gsm_caliphate.1`: cosmetic tag `CAL` (nama + warna berubah),
  +25000 manpower sekali, national spirit permanen `gsm_caliphate_legacy`
  dan trait pemimpin diganti `gsm_stability` -> `gsm_caliph` (kosmetik).
  Total buff kekhalifahan: +10% war support, +15% stability,
  +1% conscription (rekrutmen) — tanpa weekly manpower / mobilisasi.
  Decision ada di kategori sendiri "The Caliphate", bukan political actions umum.
- OOB 4 divisi dengan nama bertema: 1. Al-Fatah Division, 2. Al-Nasr Division, 3. Al-Rashid Division, 4. Al-Andalus Division.

## Cara pakai
1. `python tools/generate.py`
2. Aktifkan mod `Al-Muhit` di launcher.
3. Mainkan scenario 1936.
