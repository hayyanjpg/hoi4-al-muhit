# -*- coding: utf-8 -*-
"""Generator mod 'Grand Sultanate of Al-Muhit' untuk HOI4 1.20.x.

Pendekatan tanpa konversi peta:
  - Tidak ada override map/ sama sekali -> error "Failed to load the map" hilang.
  - Memakai tag EGY yang sudah ada, bukan GSM (GSM di vanilla = Gansu Ma).
  - Delapan state Mesir yang awalnya owner = ENG (core EGY) dijadikan
    owner = EGY (merdeka) dan state_category = megalopolis.
  - Nama country & kota ditimpa lewat lokalisasi (termasuk kunci ideology).
  - Pemimpin: Khalifah Harun al-Rashid.
  - Total SDA nasional di-distribusikan ke 8 state.

Usage:  python tools/generate.py
"""
import os
import re
import shutil

GAME = r"D:\SteamLibrary\steamapps\common\Hearts of Iron IV"
MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TAG = "EGY"
COUNTRY_NAME = "Grand Sultanate of Al-Muhit"
CAPITAL = 907
LEADER_NAME = "Khalifah Harun al-Rashid"

EGYPT_STATES = [
    "446-Cairo.txt",
    "447-Alexandria.txt",
    "452-Marsa Matruh.txt",
    "453-Sinai.txt",
    "456-Luxor.txt",
    "457-Aswan.txt",
    "552-Western Egypt.txt",
    "907-Cairo.txt",
]

# Bobot distribusi SDA (state terakhir = ibukota, dapat porsi terbesar).
STATE_WEIGHTS = [1.0, 1.1, 0.9, 0.8, 0.75, 0.7, 0.65, 1.4]
RESOURCE_TOTALS = {
    "steel": 752,
    "tungsten": 300,
    "rubber": 50,
    "chromium": 210,
    "coal": 300,
    "aluminium": 200,
    "oil": 320,
}

# ------------------------------------------------- leader & nama -----------
LEADER_TRAITS = ("gsm_stability",)
DIVISION_NAMES = (
    "1. Al-Fatah Division",
    "2. Al-Nasr Division",
    "3. Al-Rashid Division",
    "4. Al-Andalus Division",
)

# 112 shared slot (8 state x 14 dengan Dispersed Industry I) diisi penuh.
# Proporsi nasional: 40% military (45), 35% dockyard (39), 25% sipil (28).
# Dockyard punya `only_costal = yes`, jadi tidak ditempatkan di state
# pedalaman 456-Luxor dan 552-Western Egypt.
BUILDINGS_PLAN = {
    "446-Cairo.txt":          {"arms_factory": 5, "dockyard": 6, "industrial_complex": 3},
    "447-Alexandria.txt":     {"arms_factory": 5, "dockyard": 6, "industrial_complex": 3},
    "452-Marsa Matruh.txt":   {"arms_factory": 4, "dockyard": 7, "industrial_complex": 3},
    "453-Sinai.txt":          {"arms_factory": 4, "dockyard": 7, "industrial_complex": 3},
    "456-Luxor.txt":          {"arms_factory": 9, "dockyard": 0, "industrial_complex": 5},
    "457-Aswan.txt":          {"arms_factory": 5, "dockyard": 6, "industrial_complex": 3},
    "552-Western Egypt.txt":  {"arms_factory": 9, "dockyard": 0, "industrial_complex": 5},
    "907-Cairo.txt":          {"arms_factory": 4, "dockyard": 7, "industrial_complex": 3},
}
SHARED_BUILDINGS = ("industrial_complex", "arms_factory", "dockyard",
                    "synthetic_refinery", "fuel_silo", "rocket_site",
                    "nuclear_reactor", "commercial_nuclear_reactor")

# Wilayah core Sudan / Transjordan(YOR) / Israel / Lebanon yang diambil alih.
# large_city = 8 base slot + 20% Dispersed Industry I -> 9 slot/state.
# 11 state x 9 = 99 slot, proporsi 30% military / 50% civilian / 20% dockyard
# -> 30 military, 49 civilian, 20 dockyard.
NEW_STATES = [
    "549-Sudan.txt", "551-Khartoum.txt", "767-North Darfur.txt",
    "883-Kassala.txt", "884-Upper Nile.txt", "885-Bahr al Ghazal.txt",
    "886-Blue Nile.txt", "887-South Darfur.txt",
    "455-Jordan.txt", "454-Israel.txt", "553-Lebanon.txt",
]
NEW_BUILDINGS_PLAN = {
    # coastal (boleh dockyard)
    "883-Kassala.txt":         (2, 5, 2),
    "455-Jordan.txt":          (2, 5, 2),
    "454-Israel.txt":          (1, 5, 3),
    "553-Lebanon.txt":         (1, 5, 3),
    # pedalaman (dockyard = 0)
    "549-Sudan.txt":           (4, 0, 5),
    "551-Khartoum.txt":        (4, 0, 5),
    "767-North Darfur.txt":    (4, 0, 5),
    "884-Upper Nile.txt":      (3, 0, 6),
    "885-Bahr al Ghazal.txt":  (3, 0, 6),
    "886-Blue Nile.txt":       (3, 0, 6),
    "887-South Darfur.txt":    (3, 0, 6),
}
# tuple = (arms_factory, dockyard, industrial_complex)

# ------------------------------------------------------- karakter -----------
import random

RANDOM_SEED = 20261123  # ganti angka ini untuk me-roll ulang stat acak

FIELD_MARSHALS = [
    ("EGY_khalid_ibn_al_walid", "Khalid ibn al-Walid"),
    ("EGY_salah_al_din",        "Salah al-Din al-Ayyubi"),
    ("EGY_amr_ibn_al_as",       "Amr ibn al-As"),
]
GENERALS = [
    ("EGY_tariq_ibn_ziyad",       "Tariq ibn Ziyad"),
    ("EGY_musa_ibn_nusayr",       "Musa ibn Nusayr"),
    ("EGY_qutayba_ibn_muslim",    "Qutayba ibn Muslim"),
    ("EGY_zubayr_ibn_al_awwam",   "Zubayr ibn al-Awwam"),
    ("EGY_sad_ibn_abi_waqqas",    "Sa'd ibn Abi Waqqas"),
    ("EGY_abu_ubayda",            "Abu Ubayda ibn al-Jarrah"),
    ("EGY_qaqa_ibn_amr",          "Al-Qa'qa' ibn Amr"),
    ("EGY_ikrima_ibn_abi_jahl",   "Ikrima ibn Abi Jahl"),
    ("EGY_walid_ibn_uqba",        "Walid ibn Uqba"),
    ("EGY_habib_ibn_maslama",     "Habib ibn Maslama"),
    ("EGY_shurahbil_ibn_hasana",  "Shurahbil ibn Hasana"),
    ("EGY_numan_ibn_muqrin",      "Nu'man ibn Muqrin"),
]

STAT_KEYS = ("skill", "attack_skill", "defense_skill",
             "planning_skill", "logistics_skill")

# Stat khusus yang diminta user (boleh > 5, game menerima sampai 9).
SPECIAL_STATS = {
    "EGY_khalid_ibn_al_walid": {
        "skill": 7, "attack_skill": 8, "defense_skill": 4,
        "planning_skill": 6, "logistics_skill": 6,
    },
}

# Trait `type = land` boleh dipakai dua-duanya. Trait `type = field_marshal`
# hanya untuk marshal, `type = corps_commander` hanya untuk general.
# Trait `type = navy`/`all`(negatif) sengaja tidak dipakai.
LAND_SHARED = [
    "brilliant_strategist", "brave", "career_officer", "engineer_officer",
    "infantry_officer", "old_guard", "motivated", "harsh_leader",
    "armor_officer", "cavalry_officer", "trait_cautious", "trait_reckless",
]
FIELD_MARSHAL_TRAITS = LAND_SHARED + [
    "aggressive_assaulter", "defensive_doctrine", "expert_delegator",
    "fast_planner", "inspirational_leader", "logistics_wizard",
    "offensive_doctrine", "organisational_leader", "thorough_planner",
    "unyielding_defender",
]
GENERAL_TRAITS = LAND_SHARED + [
    "adaptable", "ambusher", "camouflage_expert", "combined_arms_expert",
    "desert_fox", "expert_improviser", "fortress_buster", "guerilla_fighter",
    "hill_fighter", "infantry_expert", "infantry_leader", "jungle_rat",
    "organizer", "paratrooper", "ranger", "skirmisher", "swamp_fox",
    "trait_engineer", "trait_mountaineer", "trickster",
    "urban_assault_specialist", "winter_expert",
]
# Pasangan yang saling mutually_exclusive di game.
TRAIT_CONFLICTS = {
    "offensive_doctrine": {"defensive_doctrine"},
    "defensive_doctrine": {"offensive_doctrine"},
    "fast_planner": {"thorough_planner"},
    "thorough_planner": {"fast_planner"},
    "unyielding_defender": {"aggressive_assaulter"},
    "aggressive_assaulter": {"unyielding_defender"},
    "infantry_expert": {"ambusher"},
    "ambusher": {"infantry_expert"},
    "trait_cautious": {"trait_reckless"},
    "trait_reckless": {"trait_cautious"},
}

PORTRAITS = [
    ("GFX_portrait_AFG_generic_land_%d" % i,
     "GFX_portrait_AFG_generic_land_%d_small" % i)
    for i in range(1, 5)
] + [
    ("GFX_portrait_arabia_generic_land_%d" % i,
     "GFX_portrait_arabia_generic_land_%d_small" % i)
    for i in (5, 6, 7)
]

# ------------------------------------------------------------ admiral -------
NAVY_STATS = ("skill", "attack_skill", "defense_skill",
              "maneuvering_skill", "coordination_skill")

# Stat utama per fokus: tetap di-roll acak 3-5, tapi stat ini dijamin 5.
PRIMARY_NAVY_STATS = {
    "submarine": ("attack_skill", "maneuvering_skill"),
    "surface":   ("attack_skill", "defense_skill"),
    "management": ("coordination_skill", "skill"),
}

# (token, display, fokus, trait navy yang sudah dicek tipenya)
ADMIRALS = [
    # 2 spesialis kapal selam
    ("EGY_admiral_abu_al_fath", "Abu al-Fath", "submarine",
     ("submarine_officer", "seawolf", "silent_hunter", "hunter_killer")),
    ("EGY_admiral_uthman_al_ghazi", "Uthman al-Ghazi", "submarine",
     ("submarine_officer", "seawolf", "lone_wolf", "torpedo_expert",
      "search_pattern_expert")),
    # 2 perwira permukaan campuran: destroyer + battleship + carrier
    ("EGY_admiral_khalil_al_bahri", "Khalil al-Bahri", "surface",
     ("destroyer_officer", "fleet_protector", "battleship_adherent",
      "heavy_ship_officer", "carrier_officer", "air_controller")),
    ("EGY_admiral_nur_al_din", "Nur al-Din", "surface",
     ("destroyer_leader", "smoke_screen_expert", "ironside",
      "big_guns_expert", "aviation_enthusiast", "flight_deck_manager")),
    # 1 manajemen
    ("EGY_admiral_ishaq_al_muhandis", "Ishaq al-Muhandis", "management",
     ("chief_engineer", "safety_first", "navy_career_officer",
      "loading_drill_master")),
]

NAVY_PORTRAITS = [
    ("GFX_portrait_AFG_generic_navy_1", "GFX_portrait_AFG_generic_navy_1_small"),
    ("GFX_portrait_AFG_generic_navy_2", "GFX_portrait_AFG_generic_navy_2_small"),
    ("GFX_Portrait_Arabia_Generic_navy_1",
     "GFX_Portrait_Arabia_Generic_navy_1_small"),
    ("GFX_Portrait_Arabia_Generic_navy_2",
     "GFX_Portrait_Arabia_Generic_navy_2_small"),
    ("GFX_portrait_arabia_generic_navy_3",
     "GFX_portrait_arabia_generic_navy_3_small"),
]

# Warna peta/UI (emas) — dipakai colors.txt + country definition.
MAP_COLOR = (212, 175, 55)
MAP_COLOR_UI = (255, 215, 100)
# Warna bendera: emas menyeluruh (basis emas, pinggir emas terang, lambang perunggu).
FLAG_BASE = (212, 175, 55)
GOLD = (255, 215, 100)
FLAG_DARK = (96, 68, 16)


def w(rel, text):
    path = os.path.join(MOD, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return path


def w_bom(rel, text):
    path = os.path.join(MOD, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="\n") as f:
        f.write(text)
    return path


def cleanup_legacy():
    """Hapus semua hasil percobaan lama (peta Atlantik + tag GSM)."""
    shutil.rmtree(os.path.join(MOD, "map"), ignore_errors=True)
    shutil.rmtree(os.path.join(MOD, "gfx", "flags"), ignore_errors=True)
    legacy = [
        "common/country_tags/01_gsm.txt",
        "common/countries/Al-Muhit.txt",
        "common/ideas/GSM_ideas.txt",
        "history/countries/GSM - Al-Muhit.txt",
        "history/countries/GSM - Gansu Ma.txt",
        "history/units/GSM_1936.txt",
        "history/units/GSM_1936_sea.txt",
    ]
    legacy += ["history/states/%d-" % n for n in range(9001, 9005)]
    for rel in legacy:
        path = os.path.join(MOD, rel)
        if os.path.isfile(path):
            os.remove(path)
        else:
            d = os.path.dirname(path)
            prefix = os.path.basename(path)
            if os.path.isdir(d):
                for fn in os.listdir(d):
                    if fn.startswith(prefix):
                        os.remove(os.path.join(d, fn))


def distribute_resources():
    """Bagi total SDA secara presisi ke 8 state (total sama persis)."""
    total_w = sum(STATE_WEIGHTS)
    out = []
    for weight in STATE_WEIGHTS:
        out.append({k: int(v * weight / total_w) for k, v in RESOURCE_TOTALS.items()})
    # Sisa pembagian dibuang ke state dengan bobot terbesar (ibukota).
    for k, total in RESOURCE_TOTALS.items():
        used = sum(s[k] for s in out)
        out[-1][k] += total - used
    return out


# ------------------------------------------------------------- states -------
def write_states():
    src = os.path.join(GAME, "history", "states")
    dist = distribute_resources()
    count = 0
    for fn, res in zip(EGYPT_STATES, dist):
        path = os.path.join(src, fn)
        with open(path, encoding="utf-8-sig", errors="replace") as f:
            txt = f.read()

        txt = re.sub(r"owner\s*=\s*ENG", "owner = EGY", txt)
        txt, n = re.subn(r"state_category\s*=\s*\w+",
                         "state_category = megalopolis", txt, count=1)
        if n == 0:
            txt = re.sub(r"(name\s*=\s*\"[^\"]*\"[^\n]*\n)",
                         r"\1\tstate_category = megalopolis\n", txt, count=1)

        res_block = "resources={\n" + "".join(
            "\t\t%s=%d\n" % (k, v) for k, v in res.items()) + "\t}"
        txt, n = re.subn(r"resources\s*=\s*\{[^}]*\}", res_block, txt, count=1)
        if n == 0:
            txt = re.sub(r"(state_category\s*=\s*megalopolis[^\n]*\n)",
                         r"\1\t" + res_block.replace("\n", "\n\t") + "\n",
                         txt, count=1)

        # Hapus semua shared building vanilla, lalu pasang alokasi penuh.
        for b in SHARED_BUILDINGS:
            txt = re.sub(r"^[ \t]*%s[ \t]*=[ \t]*\d+[ \t]*\r?\n" % b, "", txt,
                         flags=re.M)
        plan = BUILDINGS_PLAN[fn]
        ins = "".join("\t\t\t%s = %d\n" % (k, v)
                      for k, v in plan.items() if v)
        txt, n = re.subn(r"(buildings\s*=\s*\{\r?\n)",
                         lambda m: m.group(1) + ins, txt, count=1)
        if n == 0:
            raise RuntimeError("buildings block hilang di %s" % fn)

        txt = ("# Al-Muhit: merdeka, megalopolis, SDA + 112 slot industri penuh\n"
               + txt)
        w("history/states/" + fn, txt)
        count += 1
    return count


def set_shared_buildings(txt, arms, dock, civ, fn):
    """Hapus shared building lama, pasang alokasi baru di blok buildings."""
    for b in SHARED_BUILDINGS:
        txt = re.sub(r"^[ \t]*%s[ \t]*=[ \t]*\d+[ \t]*\r?\n" % b, "", txt,
                     flags=re.M)
    ins = ("\t\t\tarms_factory = %d\n" % arms
           + "\t\t\tdockyard = %d\n" % dock
           + "\t\t\tindustrial_complex = %d\n" % civ)
    txt, n = re.subn(r"(buildings\s*=\s*\{\r?\n)",
                     lambda m: m.group(1) + ins, txt, count=1)
    if n == 0:
        raise RuntimeError("buildings block hilang di %s" % fn)
    return txt


def write_new_states():
    """Ambil alih core Sudan, Transjordan (JOR), Israel, Lebanon."""
    src = os.path.join(GAME, "history", "states")
    count = 0
    for fn in NEW_STATES:
        with open(os.path.join(src, fn), encoding="utf-8-sig",
                  errors="replace") as f:
            txt = f.read()

        #owner = {ENG|PAL|JOR|LEB} -> EGY
        txt = re.sub(r"owner\s*=\s*(ENG|PAL|JOR|LEB)", "owner = EGY", txt)

        # Tambahkan core EGY bila belum ada
        if re.search(r"add_core_of\s*=\s*EGY\b", txt) is None:
            txt, n = re.subn(r"(owner\s*=\s*EGY[^\n]*\n)",
                             r"\1\t\tadd_core_of = EGY\n", txt, count=1)
            if n == 0:
                raise RuntimeError("owner EGY hilang di %s" % fn)

        txt, n = re.subn(r"state_category\s*=\s*\w+",
                         "state_category = large_city", txt, count=1)
        if n == 0:
            txt = re.sub(r"(name\s*=\s*\"[^\"]*\"[^\n]*\n)",
                         r"\1\tstate_category = large_city\n", txt, count=1)

        arms, dock, civ = NEW_BUILDINGS_PLAN[fn]
        txt = set_shared_buildings(txt, arms, dock, civ, fn)

        txt = ("# Al-Muhit: core SUD/JOR/ISR/LEB diambil alih, large_city, "
               "99 slot industri\n" + txt)
        w("history/states/" + fn, txt)
        count += 1
    return count


def roll_stats(rng, token, marshal=False):
    """Acak 5 stat (4-5), kecuali token punya stat khusus dari user."""
    if token in SPECIAL_STATS:
        return dict(SPECIAL_STATS[token])
    st = {k: rng.randint(4, 5) for k in STAT_KEYS}
    if marshal and all(v == 4 for v in st.values()):
        st[rng.choice(STAT_KEYS)] = 5
    return st


def roll_traits(rng, pool):
    """Ambil 1-3 trait yang tidak saling mutually_exclusive."""
    while True:
        picks = rng.sample(pool, rng.randint(1, 3))
        clash = any(b in TRAIT_CONFLICTS.get(a, ()) for a in picks
                    for b in picks if a != b)
        if not clash:
            return picks


def write_characters():
    """3 field marshal + 12 general, trait sesuai role, stat acak minimum 4."""
    rng = random.Random(RANDOM_SEED)
    lines = ["characters = {"]
    rows = []

    for group, marshal in ((FIELD_MARSHALS, True), (GENERALS, False)):
        pool = FIELD_MARSHAL_TRAITS if marshal else GENERAL_TRAITS
        for token, display in group:
            large, small = PORTRAITS[rng.randrange(len(PORTRAITS))]
            st = roll_stats(rng, token, marshal)
            traits = roll_traits(rng, pool)
            kind = "field_marshal" if marshal else "corps_commander"
            lines.append("\t%s = {" % token)
            lines.append("\t\tname = %s" % token)
            lines.append("\t\tportraits = {")
            lines.append("\t\t\tarmy = {")
            lines.append("\t\t\t\tlarge = %s" % large)
            lines.append("\t\t\t\tsmall = %s" % small)
            lines.append("\t\t\t}")
            lines.append("\t\t}")
            lines.append("\t\t%s = {" % kind)
            lines.append("\t\t\ttraits = { %s }" % " ".join(traits))
            for k in STAT_KEYS:
                lines.append("\t\t\t%s = %d" % (k, st[k]))
            lines.append("\t\t}")
            lines.append("\t}")
            lines.append("")
            rows.append((token, display, kind, st, traits))

    # 5 admiral: stat acak 3-5, stat utama fokus dijamin 5
    for i, (token, display, focus, traits) in enumerate(ADMIRALS):
        large, small = NAVY_PORTRAITS[i]
        st = {k: rng.randint(3, 5) for k in NAVY_STATS}
        for k in PRIMARY_NAVY_STATS[focus]:
            st[k] = 5
        lines.append("\t%s = {" % token)
        lines.append("\t\tname = %s" % token)
        lines.append("\t\tportraits = {")
        lines.append("\t\t\tarmy = {")
        lines.append("\t\t\t\tlarge = %s" % large)
        lines.append("\t\t\t\tsmall = %s" % small)
        lines.append("\t\t\t}")
        lines.append("\t\t}")
        lines.append("\t\tnavy_leader = {")
        lines.append("\t\t\ttraits = { %s }" % " ".join(traits))
        for k in NAVY_STATS:
            lines.append("\t\t\t%s = %d" % (k, st[k]))
        lines.append("\t\t}")
        lines.append("\t}")
        lines.append("")
        rows.append((token, display, "navy_leader", st, traits))

    lines.append("}")
    w("common/characters/EGY.txt", "\n".join(lines) + "\n")
    return rows


# ------------------------------------------------------------ country -------
def write_country_history():
    leader_traits = "\n".join("\t\t%s" % tr for tr in LEADER_TRAITS)
    recruits = "\n".join(
        "recruit_character = %s" % entry[0]
        for entry in FIELD_MARSHALS + GENERALS + ADMIRALS)
    txt = """# Grand Sultanate of Al-Muhit (ex-Kingdom of Egypt)
capital = 907 # Mina Al-Azam

set_oob = "EGY_1936"
set_convoys = 30

create_country_leader = {
\tname = "%s"
\tdesc = "Khalifah of the Grand Sultanate of Al-Muhit"
\tpicture = "GFX_portrait_AFG_generic_land_1"
\tideology = despotism
\ttraits = {
%s
\t}
}

# National spirit bawaan: +10%% produksi dok/kapal perang sejak 1936
add_ideas = gsm_scientific_industry

set_research_slots = 4

set_technology = {
	# 200 tech dari save Al-Muhit 1941.12.1 (save terbaru)
	early_ship_hull_light = 1
	basic_ship_hull_light = 1
	improved_ship_hull_light = 1
	advanced_ship_hull_light = 1
	smoke_generator = 1
	basic_depth_charges = 1
	improved_depth_charges = 1
	advanced_depth_charges = 1
	modern_depth_charges = 1
	sonar = 1
	improved_sonar = 1
	advanced_sonar = 1
	modern_sonar = 1
	early_ship_hull_cruiser = 1
	basic_ship_hull_cruiser = 1
	improved_ship_hull_cruiser = 1
	advanced_ship_hull_cruiser = 1
	basic_cruiser_armor_scheme = 1
	early_ship_hull_heavy = 1
	basic_ship_hull_heavy = 1
	basic_heavy_armor_scheme = 1
	improved_heavy_armor_scheme = 1
	early_ship_hull_carrier = 1
	basic_ship_hull_carrier = 1
	early_ship_hull_submarine = 1
	basic_ship_hull_submarine = 1
	improved_ship_hull_submarine = 1
	advanced_ship_hull_submarine = 1
	sp_aip_engine_improved_tech = 1
	sp_aip_engine_advanced_tech = 1
	sp_naval_proximity_fuze_tech = 1
	basic_battery = 1
	basic_heavy_battery = 1
	improved_heavy_battery = 1
	advanced_heavy_battery = 1
	basic_heavy_shell = 1
	improved_heavy_shell = 1
	advanced_dp_light_battery = 1
	basic_torpedo = 1
	magnetic_detonator = 1
	homing_torpedo = 1
	improved_ship_torpedo_launcher = 1
	advanced_ship_torpedo_launcher = 1
	modern_ship_torpedo_launcher = 1
	damage_control_1 = 1
	damage_control_2 = 1
	damage_control_3 = 1
	fire_control_methods_1 = 1
	fire_control_methods_2 = 1
	fire_control_methods_3 = 1
	mtg_transport = 1
	mtg_landing_craft = 1
	mtg_tank_landing_craft = 1
	sp_improved_support_ship = 1
	sp_improved_repair_ship = 1
	gwtank_chassis = 1
	basic_light_tank_chassis = 1
	improved_light_tank_chassis = 1
	advanced_light_tank_chassis = 1
	basic_medium_tank_chassis = 1
	improved_medium_tank_chassis = 1
	advanced_medium_tank_chassis = 1
	main_battle_tank_chassis = 1
	engine_tech_1 = 1
	engine_tech_2 = 1
	gw_artillery = 1
	interwar_artillery = 1
	artillery1 = 1
	artillery2 = 1
	artillery3 = 1
	artillery4 = 1
	artillery5 = 1
	rocket_artillery = 1
	interwar_antiair = 1
	antiair1 = 1
	antiair2 = 1
	antiair3 = 1
	antiair4 = 1
	antiair5 = 1
	interwar_antitank = 1
	antitank1 = 1
	antitank2 = 1
	antitank3 = 1
	antitank4 = 1
	antitank5 = 1
	sp_artillery_rocket_assisted_projectiles_tech = 1
	sp_artillery_purpose_built_gun_motor_carriages_tech = 1
	sp_shock_hardening_techniques = 1
	sp_land_large_caliber_kinetic_energy_sabot_gd_tech = 1
	sp_advance_sabot_shells = 1
	bba_early_transport_plane = 1
	bba_improved_transport_plane = 1
	bba_strategic_airlifter = 1
	iw_small_airframe = 1
	basic_small_airframe = 1
	improved_small_airframe = 1
	advanced_small_airframe = 1
	modern_small_airframe = 1
	early_bombs = 1
	heavy_bombs = 1
	armor_piercing_bombs = 1
	air_torpedoe_1 = 1
	air_torpedoe_2 = 1
	air_torpedoe_3 = 1
	aa_lmg = 1
	survivability_studies = 1
	aa_hmg = 1
	aa_cannon_1 = 1
	aa_cannon_2 = 1
	aa_cannon_3 = 1
	engines_1 = 1
	engines_2 = 1
	engines_3 = 1
	engines_4 = 1
	range_improvements = 1
	aircraft_construction = 1
	sp_centrifugal_jet_tech = 1
	electronic_mechanical_engineering = 1
	radio = 1
	improved_radio = 1
	advanced_radio = 1
	radio_detection = 1
	cavity_magnatron = 1
	centimetric_radar = 1
	phased_array = 1
	monopulse_radar = 1
	mechanical_computing = 1
	computing_machine = 1
	improved_computing_machine = 1
	advanced_computing_machine = 1
	improved_fire_control_system = 1
	advanced_fire_control_system = 1
	experimental_rockets = 1
	atomic_research = 1
	nuclear_reactor = 1
	nukes = 1
	sp_rockets_dual_chamber_rocket_engine_1 = 1
	basic_machine_tools = 1
	improved_machine_tools = 1
	advanced_machine_tools = 1
	assembly_line_production = 1
	streamlined_line = 1
	improved_equipment_conversion = 1
	advanced_equipment_conversion = 1
	dispersed_industry = 1
	dispersed_industry2 = 1
	dispersed_industry3 = 1
	dispersed_industry4 = 1
	dispersed_industry5 = 1
	construction1 = 1
	construction2 = 1
	excavation2 = 1
	construction3 = 1
	construction4 = 1
	construction5 = 1
	infantry_weapons = 1
	infantry_weapons1 = 1
	infantry_weapons2 = 1
	improved_infantry_weapons = 1
	improved_infantry_weapons_2 = 1
	infantry_at = 1
	infantry_at2 = 1
	advanced_infantry_weapons = 1
	advanced_infantry_weapons2 = 1
	paratroopers = 1
	paratroopers2 = 1
	paratroopers3 = 1
	marines = 1
	night_vision = 1
	night_vision2 = 1
	support_weapons = 1
	support_weapons2 = 1
	support_weapons3 = 1
	support_weapons4 = 1
	tech_trucks = 1
	motorised_infantry = 1
	mechanised_infantry = 1
	mechanised_infantry2 = 2
	mechanised_infantry3 = 1
	early_destroyer = 1
	basic_destroyer = 1
	land_multi_charge_large_caliber_gun_tech = 1
	commercial_nuclear_reactor_tech = 1
	stronghold_network_tech = 1
	thermonuclear_bombs = 1
	tech_support = 1
	tech_engineers = 1
	tech_engineers2 = 1
	tech_engineers3 = 1
	tech_engineers4 = 1
	tech_recon = 1
	tech_recon2 = 1
	tech_recon3 = 1
	tech_recon4 = 1
	tech_military_police = 1
	tech_signal_company = 1
	basic_train = 1
	wartime_train = 1
	sp_armored_engineer_tech = 1
	sp_helicopter_artillery_observers_tech = 1
}

set_grand_doctrine = grand_battleplan

set_politics = {
\truling_party = neutrality
\tlast_election = "1936.1.1"
\telection_frequency = 48
\telections_allowed = no
}

set_popularities = {
\tneutrality = 75
\tdemocratic = 12
\tfascism = 8
\tcommunism = 5
}

# Perwira Al-Muhit siap dipakai di 1936
%s
""" % (LEADER_NAME, leader_traits, recruits)
    w("history/countries/EGY - Egypt.txt", txt)


def write_oob():
    txt = """division_template={
\tname="EGY Infantry"
\tregiments={
\t\tinfantry={ x=0 y=0 }
\t\tinfantry={ x=0 y=1 }
\t\tinfantry={ x=1 y=0 }
\t}
\tsupport={
\t\tartillery={ x=0 y=0 }
\t}
}

units={
"""
    for name, pid in zip(DIVISION_NAMES, (7011, 1068, 3996, 4055)):
        txt += """\tdivision={
\t\tname="%s"
\t\tlocation=%d
\t\tdivision_template="EGY Infantry"
\t\tstart_experience_factor=0.6
\t}
""" % (name, pid)
    txt += "}\n"
    w("history/units/EGY_1936.txt", txt)


def write_country_definition():
    w("common/countries/Egypt.txt",
      "\n# %s\ngraphical_culture = middle_eastern_gfx\n"
      "graphical_culture_2d = middle_eastern_2d\n\n"
      "color = { %d %d %d }\n" %
      ((COUNTRY_NAME,) + MAP_COLOR))


def write_colors():
    src = os.path.join(GAME, "common", "countries", "colors.txt")
    with open(src, encoding="utf-8-sig", errors="replace") as f:
        txt = f.read()
    block = ("EGY = {\n"
             "\tcolor = rgb { %d %d %d }\n"
             "\tcolor_ui = rgb { %d %d %d }\n"
             "}\n" % (MAP_COLOR + MAP_COLOR_UI))
    # Hati-hati: blok warna punya brace bertingkat (rgb { ... }), jadi regex
    # harus mencapai penutup blok di awal baris, bukan '}' pertama.
    txt, n = re.subn(r"EGY\s*=\s*\{.*?\n\}", block, txt, count=1, flags=re.S)
    if n == 0:
        txt += "\n" + block
    w("common/countries/colors.txt", txt)


def write_idea():
    """Ide nasional yang dipakai oleh focus Scientific & Industrial Renaissance."""
    txt = """ideas = {
\tcountry = {
\t\tgsm_scientific_industry = {
\t\t\tallowed = { original_tag = EGY }
\t\t\tpicture = GFX_idea_PLACEHOLDER_idea_icon
\t\t\tremoval_cost = -1
\t\t\tmodifier = {
\t\t\t\tindustrial_capacity_dockyard = 0.1
\t\t\t}
\t\t}
\t\tgsm_caliphate_legacy = {
\t\t\tallowed = { original_tag = EGY }
\t\t\tpicture = GFX_idea_PLACEHOLDER_idea_icon
\t\t\tremoval_cost = -1
\t\t\tmodifier = {
\t\t\t\twar_support_factor = 0.1
\t\t\t\tstability_factor = 0.15
\t\t\t\tconscription_factor = 0.01
\t\t\t}
\t\t}
\t}
}
"""
    w("common/ideas/EGY_ideas.txt", txt)


def write_leader_traits():
    """Trait awal: stability. Trait gsm_caliph baru aktif setelah proklamasi."""
    txt = """leader_traits = {
\tgsm_stability = {
\t\trandom = no
\t\tsprite = 13
\t\tstability_factor = 0.1
\t\tai_will_do = { factor = 0 }
\t}

\tgsm_caliph = {
\t\trandom = no
\t\tsprite = 13
\t\tai_will_do = { factor = 0 }
\t}
}
"""
    w("common/country_leader/EGY_traits.txt", txt)


def write_focus():
    """Pohon focus: industri, persatuan Islam, lalu proklamasi kekhalifahan."""
    txt = """focus_tree = {
\tid = egy_tree

\tcountry = {
\t\tfactor = 0
\t\tmodifier = {
\t\t\tadd = 10
\t\t\ttag = EGY
\t\t}
\t}

\tdefault = no

\tfocus = {
\t\tid = EGY_scientific_industrial_renaissance
\t\ticon = GFX_focus_research
\t\tx = 0
\t\ty = 0
\t\tcost = 5
\t\tai_will_do = {
\t\t\tfactor = 10
\t\t}
\t\tcompletion_reward = {
\t\t\tadd_ideas = gsm_scientific_industry
\t\t\tadd_political_power = 100
\t\t}
\t}

\tfocus = {
\t\tid = EGY_islamic_unity
\t\ticon = GFX_focus_generic_manpower
\t\tx = 0
\t\ty = 1
\t\tcost = 10
\t\tprerequisite = {
\t\t\tfocus = EGY_scientific_industrial_renaissance
\t\t}
\t\tai_will_do = {
\t\t\tfactor = 10
\t\t}
\t\tcompletion_reward = {
\t\t\tadd_political_power = 150
\t\t\tadd_manpower = 15000
\t\t}
\t}

\tfocus = {
\t\tid = EGY_proclaim_caliphate
\t\ticon = GFX_focus_generic_monarchy_1
\t\tx = 0
\t\ty = 2
\t\tcost = 20
\t\tprerequisite = {
\t\t\tfocus = EGY_islamic_unity
\t\t}
\t\tavailable = {
\t\t\tNOT = { has_country_flag = gsm_caliphate_proclaimed }
\t\t\tOR = { TUR = { is_subject_of = EGY } TUR = { exists = no } }
\t\t\tOR = { IRQ = { is_subject_of = EGY } IRQ = { exists = no } }
\t\t\tOR = { SAU = { is_subject_of = EGY } SAU = { exists = no } }
\t\t\tOR = { ISR = { is_subject_of = EGY } ISR = { exists = no } }
\t\t\tOR = { LEB = { is_subject_of = EGY } LEB = { exists = no } }
\t\t\tOR = { JOR = { is_subject_of = EGY } JOR = { exists = no } }
\t\t}
\t\tai_will_do = {
\t\t\tfactor = 10
\t\t}
\t\tcompletion_reward = {
\t\t\tcountry_event = { id = gsm_caliphate.1 days = 1 }
\t\t}
\t}
}
"""
    w("common/national_focus/EGY.txt", txt)


def write_localisation():
    txt = """l_english:
\tEGY: "%s"
\tEGY_DEF: "Al-Muhit"
\tEGY_ADJ: "Al-Muhitian"
\tEGY_PLAN: "Al-Muhit"

\tEGY_neutrality: "%s"
\tEGY_neutrality_DEF: "the Grand Sultanate of Al-Muhit"
\tEGY_neutrality_ADJ: "Al-Muhitian"
\tEGY_brit_puppet: "%s"
\tEGY_brit_puppet_DEF: "the Grand Sultanate of Al-Muhit"
\tEGY_brit_puppet_ADJ: "Al-Muhitian"

\tSTATE_907: "Dar al-Khilafah"
\tSTATE_446: "Al-Qasr"
\tSTATE_447: "Bandar Al-Nur"
\tSTATE_452: "Madinat Al-Hadid"
\tSTATE_453: "Wadi Al-Sina'a"
\tSTATE_456: "Dar Al-Hikma"
\tSTATE_457: "Jazirat Al-Hikma"
\tSTATE_552: "Sahl Al-Fann"

\tVICTORY_POINTS_7011: "Dar al-Khilafah"
\tVICTORY_POINTS_3996: "Dar Al-Hikma"
\tVICTORY_POINTS_1068: "Bandar Al-Nur"
\tVICTORY_POINTS_12049: "Al-Qasr"
\tVICTORY_POINTS_4073: "Port Al-Salam"
\tVICTORY_POINTS_907: "Dar al-Khilafah"

\tgsm_scientific_industry: "Scientific & Industrial Renaissance"
\tgsm_scientific_industry_desc: "Our shipyards turn the Nile delta into the forge of a new fleet, raising dockyard output by ten percent."

\tEGY_scientific_industrial_renaissance: "Scientific & Industrial Renaissance"
\tEGY_scientific_industrial_renaissance_desc: "Empower our shipyards to forge a new fleet for the Grand Sultanate."

\tEGY_islamic_unity: "Islamic Unity"
\tEGY_islamic_unity_desc: "Rally the faithful behind the Caliph and prepare the realm for a greater union."

\tEGY_proclaim_caliphate: "Proclaim the Caliphate"
\tEGY_proclaim_caliphate_desc: "With the Islamic world united under our banner, declare the Grand Islamic Caliphate."

\tgsm_stability: "Steadfast Caliph"
\tgsm_stability_desc: "The Caliph's steady hand keeps the realm united."

\tgsm_caliph: "Caliph of the Faithful"
\tgsm_caliph_desc: "The Caliph's authority unites the faithful under one banner."

\tgsm_caliphate_legacy: "Legacy of the Caliphate"
\tgsm_caliphate_legacy_desc: "By the Caliph's decree: +10% war support, +15% stability and +1% recruitable population."

\tgsm_caliphate_category: "The Caliphate"

\tgsm_proclaim_caliphate: "Proclaim the Caliphate"
\tgsm_proclaim_caliphate_desc: "With the holy cities and the wider Islamic world under our sway, declare the Grand Islamic Caliphate."

\tgsm_caliphate.1.t: "The Grand Islamic Caliphate"
\tgsm_caliphate.1.d: "The Caliphate is proclaimed. Our flag changes, our name resounds across the Islamic world, and fresh manpower answers the call."

\tgsm_caliphate.1.a: "Long live the Caliphate"

\tCAL: "Grand Islamic Caliphate"
\tCAL_DEF: "the Grand Islamic Caliphate"
\tCAL_ADJ: "Caliphal"
\tCAL_PLAN: "Grand Islamic Caliphate"
\tCAL_neutrality: "Grand Islamic Caliphate"
\tCAL_democratic: "Grand Islamic Caliphate"
\tCAL_fascism: "Grand Islamic Caliphate"
\tCAL_communism: "Grand Islamic Caliphate"

%s
""" % (COUNTRY_NAME, COUNTRY_NAME, COUNTRY_NAME,
       "\n".join('\t%s: "%s"' % (entry[0], entry[1])
                 for entry in FIELD_MARSHALS + GENERALS + ADMIRALS))
    w_bom("localisation/english/GSM_l_english.yml", txt)


# ---------------------------------------------------------------- flag ------
def write_flag():
    from PIL import Image, ImageDraw
    size = (82, 52)
    im = Image.new("RGBA", size, FLAG_BASE + (255,))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 81, 51], outline=GOLD + (255,), width=2)
    d.ellipse([28, 14, 54, 40], fill=FLAG_DARK + (255,))
    d.ellipse([35, 10, 60, 35], fill=FLAG_BASE + (255,))
    d.polygon([(61, 17), (64, 22), (70, 23), (66, 27), (67, 33),
               (61, 30), (56, 33), (58, 27), (54, 22), (60, 23)],
              fill=FLAG_DARK + (255,))
    variants = [TAG] + ["%s_%s" % (TAG, x)
                        for x in ("neutrality", "democratic", "fascism", "communism")]
    for folder, fsize in (("", size), ("medium", (41, 26)), ("small", (10, 7))):
        out_dir = os.path.join(MOD, "gfx", "flags", folder)
        os.makedirs(out_dir, exist_ok=True)
        scaled = im if fsize == size else im.resize(fsize, Image.Resampling.LANCZOS)
        for name in variants:
            scaled.save(os.path.join(out_dir, name + ".tga"))


# ------------------------------------------------------ kekhalifahan -------
def write_caliphate_category():
    txt = """gsm_caliphate_category = {
\ticon = generic_political_actions
}
"""
    w("common/decisions/categories/EGY_caliphate_categories.txt", txt)


def write_caliphate_decision():
    txt = """gsm_caliphate_category = {
\tgsm_proclaim_caliphate = {
\t\tpriority = 100
\t\ticon = GFX_decision_eng_trade_unions_support

\t\tallowed = {
\t\t\toriginal_tag = EGY
\t\t}

\t\tavailable = {
\t\t\tOR = { TUR = { is_subject_of = EGY } TUR = { exists = no } }
\t\t\tOR = { IRQ = { is_subject_of = EGY } IRQ = { exists = no } }
\t\t\tOR = { SAU = { is_subject_of = EGY } SAU = { exists = no } }
\t\t\tOR = { ISR = { is_subject_of = EGY } ISR = { exists = no } }
\t\t\tOR = { LEB = { is_subject_of = EGY } LEB = { exists = no } }
\t\t\tOR = { JOR = { is_subject_of = EGY } JOR = { exists = no } }
\t\t}

\t\tvisible = {
\t\t\tNOT = { has_country_flag = gsm_caliphate_proclaimed }
\t\t}

\t\tfire_only_once = yes
\t\tcost = 100

\t\tcomplete_effect = {
\t\t\tcountry_event = { id = gsm_caliphate.1 days = 1 }
\t\t}
\t}
}
"""
    w("common/decisions/EGY_caliphate.txt", txt)


def write_caliphate_event():
    txt = """add_namespace = gsm_caliphate

country_event = {
\tid = gsm_caliphate.1
\ttitle = gsm_caliphate.1.t
\tdesc = gsm_caliphate.1.d
\tpicture = GFX_report_event_generic_military_parade
\tis_triggered_only = yes
\tfire_only_once = yes

\timmediate = {
\t\thidden_effect = {
\t\t\tset_cosmetic_tag = CAL
\t\t\tset_country_flag = gsm_caliphate_proclaimed
\t\t\tremove_country_leader_trait = gsm_stability
\t\t\tadd_country_leader_trait = gsm_caliph
\t\t\tadd_manpower = 25000
\t\t\tadd_ideas = gsm_caliphate_legacy
\t\t}
\t}

\toption = {
\t\tname = gsm_caliphate.1.a
\t}
}
"""
    w("events/EGY_caliphate.txt", txt)


def write_caliphate_country():
    txt = """# Cosmetic tag untuk Kekhalifahan Islam (nama & warna di map)
graphical_culture = middle_eastern_gfx
graphical_culture_2d = middle_eastern_2d

color = { 30 120 65 }
"""
    w("common/countries/CAL.txt", txt)


def write_caliphate_flag():
    from PIL import Image, ImageDraw
    size = (82, 52)
    im = Image.new("RGBA", size, GOLD + (255,))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 81, 51], outline=FLAG_DARK + (255,), width=2)
    d.ellipse([28, 14, 54, 40], fill=FLAG_DARK + (255,))
    d.ellipse([35, 10, 60, 35], fill=GOLD + (255,))
    d.polygon([(61, 17), (64, 22), (70, 23), (66, 27), (67, 33),
               (61, 30), (56, 33), (58, 27), (54, 22), (60, 23)],
              fill=FLAG_DARK + (255,))
    variants = ["CAL"] + ["CAL_%s" % x
                          for x in ("neutrality", "democratic", "fascism", "communism")]
    for folder, fsize in (("", size), ("medium", (41, 26)), ("small", (10, 7))):
        out_dir = os.path.join(MOD, "gfx", "flags", folder)
        os.makedirs(out_dir, exist_ok=True)
        scaled = im if fsize == size else im.resize(fsize, Image.Resampling.LANCZOS)
        for name in variants:
            scaled.save(os.path.join(out_dir, name + ".tga"))


def write_cities_bmp():
    """Gaya kota: ganti mesh 'unciv' (index 2) jadi 'westerngfx' (index 15).

    Hanya map/cities.bmp yang di-override. File map lain (provinces.bmp,
    definition.csv, terrain.bmp, default.map, dll.) tetap memakai vanilla,
    jadi tidak ada ketidakcocokan yang memicu 'Failed to load the map'.
    """
    import csv
    import numpy as np
    from PIL import Image

    map_dir = os.path.join(GAME, "map")
    prov_img = Image.open(os.path.join(map_dir, "provinces.bmp")).convert("RGB")
    city_img = Image.open(os.path.join(map_dir, "cities.bmp"))

    wanted = set()
    state_dir = os.path.join(MOD, "history", "states")
    for fn in os.listdir(state_dir):
        if not fn.endswith(".txt"):
            continue
        txt = open(os.path.join(state_dir, fn), encoding="utf-8-sig",
                   errors="replace").read()
        m = re.search(r"provinces\s*=\s*\{(.*?)\}", txt, re.S)
        if m:
            wanted.update(int(x) for x in m.group(1).split())

    keys = set()
    with open(os.path.join(map_dir, "definition.csv"), encoding="utf-8-sig",
              errors="replace") as f:
        for row in csv.reader(f, delimiter=";"):
            if len(row) >= 4 and row[0].isdigit() and int(row[0]) in wanted:
                keys.add((int(row[1]) << 16) | (int(row[2]) << 8) | int(row[3]))

    lut = np.zeros(1 << 24, dtype=bool)
    lut[list(keys)] = True
    p = np.asarray(prov_img, dtype=np.uint32)
    h, w = p.shape[:2]
    packed = (p[:, :, 0] << 16) | (p[:, :, 1] << 8) | p[:, :, 2]
    mask = lut[packed.reshape(-1)].reshape((h, w))

    c = np.array(city_img)
    target = mask & (c == 2)
    changed = int(np.count_nonzero(target))
    c[target] = 15
    out = Image.fromarray(c, mode="P")
    out.putpalette(city_img.getpalette())
    os.makedirs(os.path.join(MOD, "map"), exist_ok=True)
    out.save(os.path.join(MOD, "map", "cities.bmp"))
    return changed


# ----------------------------------------------------------- descriptor -----
def write_descriptor():
    txt = """version="1.20.0.0"
tags={
\t"Country"
}
name="%s"
supported_version="1.20.*"
path="mod/Al-Muhit"
""" % COUNTRY_NAME
    w("descriptor.mod", txt)
    w(os.path.join("..", "Al-Muhit.mod"), txt)


def write_readme():
    res = ", ".join("%s %d" % (k, v) for k, v in RESOURCE_TOTALS.items())
    mil = sum(v["arms_factory"] for v in BUILDINGS_PLAN.values())
    dock = sum(v["dockyard"] for v in BUILDINGS_PLAN.values())
    civ = sum(v["industrial_complex"] for v in BUILDINGS_PLAN.values())
    nm = sum(v[0] for v in NEW_BUILDINGS_PLAN.values())
    nd = sum(v[1] for v in NEW_BUILDINGS_PLAN.values())
    nc = sum(v[2] for v in NEW_BUILDINGS_PLAN.values())
    txt = """# Grand Sultanate of Al-Muhit

Mod HOI4 1.20.x. Tanpa konversi peta (tidak ada error map).

## Isi mod
- Tag `EGY` (GSM di vanilla adalah Gansu Ma, jadi tidak dipakai).
- 8 state Mesir merdeka: `owner = EGY`, `add_core_of = EGY`.
- Semua state Mesir: `state_category = megalopolis`.
- Nama tampil: **Grand Sultanate of Al-Muhit** (termasuk kunci
  `EGY_neutrality`, bukan hanya `EGY`).
- Kota/state dinamai ulang: Mina Al-Azam, Al-Qasr, Bandar Al-Nur, dll.
- Pemimpin: **%s**.
- Total SDA nasional: %s.
- **112/112 shared slot industri terisi penuh**: %d military factory,
  %d dockyard, %d civilian factory (40/35/25 persen).
  Dockyard tidak ditempatkan di 456-Luxor & 552-Western Egypt karena
  aturan `only_costal = yes`.
- 11 state core Sudan, Transjordan (JOR), Israel, Lebanon diambil alih
  (`owner = EGY` + `add_core_of = EGY`) dan jadi `large_city`.
- 99/99 slot industri di wilayah baru: %d military, %d civilian,
  %d dockyard (30/50/20 persen).
- 3 field marshal + 12 general dengan stat acak 4-5 (seed %d),
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
- Sejak 1936 Khalifah memakai `gsm_stability` (+10%% stability) dan negara
  sudah punya national spirit bawaan `gsm_scientific_industry` (+10%% dockyard
  output). Trait `gsm_caliph` setelah proklamasi bersifat kosmetik.
- Decision `gsm_proclaim_caliphate` muncul bila TUR/IRQ/SAU/ISR/LEB/JOR sudah
  jadi vassal EGY atau tidak ada lagi (dianeksasi). Mengambilnya memicu event
  `gsm_caliphate.1`: cosmetic tag `CAL` (nama + warna berubah),
  +25000 manpower sekali, national spirit permanen `gsm_caliphate_legacy`
  dan trait pemimpin diganti `gsm_stability` -> `gsm_caliph` (kosmetik).
  Total buff kekhalifahan: +10%% war support, +15%% stability,
  +1%% conscription (rekrutmen) — tanpa weekly manpower / mobilisasi.
  Decision ada di kategori sendiri "The Caliphate", bukan political actions umum.
- OOB 4 divisi dengan nama bertema: %s.

## Cara pakai
1. `python tools/generate.py`
2. Aktifkan mod `Al-Muhit` di launcher.
3. Mainkan scenario 1936.
""" % (LEADER_NAME, res, mil, dock, civ, nm, nc, nd, RANDOM_SEED,
       ", ".join(DIVISION_NAMES))
    w("README.md", txt)


def main():
    cleanup_legacy()
    n = write_states()
    n2 = write_new_states()
    write_country_history()
    write_oob()
    write_characters()
    write_country_definition()
    write_colors()
    write_idea()
    write_leader_traits()
    write_caliphate_category()
    write_caliphate_decision()
    write_caliphate_event()
    write_caliphate_country()
    write_caliphate_flag()
    changed = write_cities_bmp()
    write_focus()
    write_localisation()
    write_flag()
    write_descriptor()
    write_readme()
    mil = sum(v["arms_factory"] for v in BUILDINGS_PLAN.values())
    dock = sum(v["dockyard"] for v in BUILDINGS_PLAN.values())
    civ = sum(v["industrial_complex"] for v in BUILDINGS_PLAN.values())
    nm = sum(v[0] for v in NEW_BUILDINGS_PLAN.values())
    nd = sum(v[1] for v in NEW_BUILDINGS_PLAN.values())
    nc = sum(v[2] for v in NEW_BUILDINGS_PLAN.values())
    print("OK: %d state Mesir + %d state core SUD/JOR/ISR/LEB, leader %s" %
          (n, n2, LEADER_NAME))
    print("INDUSTRI MESIR : %d military + %d dockyard + %d civilian = %d/112" %
          (mil, dock, civ, mil + dock + civ))
    print("INDUSTRI BARU   : %d military + %d dockyard + %d civilian = %d/99" %
          (nm, nd, nc, nm + nd + nc))
    print("PERWIRA         : %d field marshal + %d general (stat >= 4, seed %d)" %
          (len(FIELD_MARSHALS), len(GENERALS), RANDOM_SEED))
    print("KHALID          : %s" % SPECIAL_STATS["EGY_khalid_ibn_al_walid"])
    print("ADMIRAL         : %d (submarine 2, mixed surface 2, management 1)" %
          len(ADMIRALS))
    print("TECH            : 200 tech dari save 1941.12.1, grand doctrine = grand_battleplan")
    print("FOKUS/IDEA      : gsm_scientific_industry (+10%% dockyard output, riset default)")
    print("BUFF KHALIFAH   : +10%% war support, +15%% stability, +1%% conscription")
    print("TRAIT KHALIFAH  : awal gsm_stability -> event gsm_caliph (kosmetik)")
    print("FOKUS           : 3 focus (industri -> islamic unity -> proklamasi)")
    print("KEKHALIFAHAN    : decision + focus + event gsm_caliphate.1, cosmetic tag CAL")
    print("KOTA            : %d piksel gaya unciv -> westerngfx di map/cities.bmp" % changed)
    print("MOD:", MOD)


if __name__ == "__main__":
    main()
