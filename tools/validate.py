# -*- coding: utf-8 -*-
"""Validator statis mod Al-Muhit (Mesir merdeka, tanpa peta baru)."""
import os
import re
import sys
from collections import defaultdict

from PIL import Image

MOD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT = os.path.dirname(MOD)
DESCRIPTOR = os.path.join(PARENT, "Al-Muhit.mod")
LEADER_TRAITS = ("gsm_stability",)
DIVISION_NAMES = (
    "1. Al-Fatah Division", "2. Al-Nasr Division",
    "3. Al-Rashid Division", "4. Al-Andalus Division",
)
EXPECTED_TECHS = {
    "early_ship_hull_light": 1,
    "basic_ship_hull_light": 1,
    "improved_ship_hull_light": 1,
    "advanced_ship_hull_light": 1,
    "smoke_generator": 1,
    "basic_depth_charges": 1,
    "improved_depth_charges": 1,
    "advanced_depth_charges": 1,
    "modern_depth_charges": 1,
    "sonar": 1,
    "improved_sonar": 1,
    "advanced_sonar": 1,
    "modern_sonar": 1,
    "early_ship_hull_cruiser": 1,
    "basic_ship_hull_cruiser": 1,
    "improved_ship_hull_cruiser": 1,
    "advanced_ship_hull_cruiser": 1,
    "basic_cruiser_armor_scheme": 1,
    "early_ship_hull_heavy": 1,
    "basic_ship_hull_heavy": 1,
    "basic_heavy_armor_scheme": 1,
    "improved_heavy_armor_scheme": 1,
    "early_ship_hull_carrier": 1,
    "basic_ship_hull_carrier": 1,
    "early_ship_hull_submarine": 1,
    "basic_ship_hull_submarine": 1,
    "improved_ship_hull_submarine": 1,
    "advanced_ship_hull_submarine": 1,
    "sp_aip_engine_improved_tech": 1,
    "sp_aip_engine_advanced_tech": 1,
    "sp_naval_proximity_fuze_tech": 1,
    "basic_battery": 1,
    "basic_heavy_battery": 1,
    "improved_heavy_battery": 1,
    "advanced_heavy_battery": 1,
    "basic_heavy_shell": 1,
    "improved_heavy_shell": 1,
    "advanced_dp_light_battery": 1,
    "basic_torpedo": 1,
    "magnetic_detonator": 1,
    "homing_torpedo": 1,
    "improved_ship_torpedo_launcher": 1,
    "advanced_ship_torpedo_launcher": 1,
    "modern_ship_torpedo_launcher": 1,
    "damage_control_1": 1,
    "damage_control_2": 1,
    "damage_control_3": 1,
    "fire_control_methods_1": 1,
    "fire_control_methods_2": 1,
    "fire_control_methods_3": 1,
    "mtg_transport": 1,
    "mtg_landing_craft": 1,
    "mtg_tank_landing_craft": 1,
    "sp_improved_support_ship": 1,
    "sp_improved_repair_ship": 1,
    "gwtank_chassis": 1,
    "basic_light_tank_chassis": 1,
    "improved_light_tank_chassis": 1,
    "advanced_light_tank_chassis": 1,
    "basic_medium_tank_chassis": 1,
    "improved_medium_tank_chassis": 1,
    "advanced_medium_tank_chassis": 1,
    "main_battle_tank_chassis": 1,
    "engine_tech_1": 1,
    "engine_tech_2": 1,
    "gw_artillery": 1,
    "interwar_artillery": 1,
    "artillery1": 1,
    "artillery2": 1,
    "artillery3": 1,
    "artillery4": 1,
    "artillery5": 1,
    "rocket_artillery": 1,
    "interwar_antiair": 1,
    "antiair1": 1,
    "antiair2": 1,
    "antiair3": 1,
    "antiair4": 1,
    "antiair5": 1,
    "interwar_antitank": 1,
    "antitank1": 1,
    "antitank2": 1,
    "antitank3": 1,
    "antitank4": 1,
    "antitank5": 1,
    "sp_artillery_rocket_assisted_projectiles_tech": 1,
    "sp_artillery_purpose_built_gun_motor_carriages_tech": 1,
    "sp_shock_hardening_techniques": 1,
    "sp_land_large_caliber_kinetic_energy_sabot_gd_tech": 1,
    "sp_advance_sabot_shells": 1,
    "bba_early_transport_plane": 1,
    "bba_improved_transport_plane": 1,
    "bba_strategic_airlifter": 1,
    "iw_small_airframe": 1,
    "basic_small_airframe": 1,
    "improved_small_airframe": 1,
    "advanced_small_airframe": 1,
    "modern_small_airframe": 1,
    "early_bombs": 1,
    "heavy_bombs": 1,
    "armor_piercing_bombs": 1,
    "air_torpedoe_1": 1,
    "air_torpedoe_2": 1,
    "air_torpedoe_3": 1,
    "aa_lmg": 1,
    "survivability_studies": 1,
    "aa_hmg": 1,
    "aa_cannon_1": 1,
    "aa_cannon_2": 1,
    "aa_cannon_3": 1,
    "engines_1": 1,
    "engines_2": 1,
    "engines_3": 1,
    "engines_4": 1,
    "range_improvements": 1,
    "aircraft_construction": 1,
    "sp_centrifugal_jet_tech": 1,
    "electronic_mechanical_engineering": 1,
    "radio": 1,
    "improved_radio": 1,
    "advanced_radio": 1,
    "radio_detection": 1,
    "cavity_magnatron": 1,
    "centimetric_radar": 1,
    "phased_array": 1,
    "monopulse_radar": 1,
    "mechanical_computing": 1,
    "computing_machine": 1,
    "improved_computing_machine": 1,
    "advanced_computing_machine": 1,
    "improved_fire_control_system": 1,
    "advanced_fire_control_system": 1,
    "experimental_rockets": 1,
    "atomic_research": 1,
    "nuclear_reactor": 1,
    "nukes": 1,
    "sp_rockets_dual_chamber_rocket_engine_1": 1,
    "basic_machine_tools": 1,
    "improved_machine_tools": 1,
    "advanced_machine_tools": 1,
    "assembly_line_production": 1,
    "streamlined_line": 1,
    "improved_equipment_conversion": 1,
    "advanced_equipment_conversion": 1,
    "dispersed_industry": 1,
    "dispersed_industry2": 1,
    "dispersed_industry3": 1,
    "dispersed_industry4": 1,
    "dispersed_industry5": 1,
    "construction1": 1,
    "construction2": 1,
    "excavation2": 1,
    "construction3": 1,
    "construction4": 1,
    "construction5": 1,
    "infantry_weapons": 1,
    "infantry_weapons1": 1,
    "infantry_weapons2": 1,
    "improved_infantry_weapons": 1,
    "improved_infantry_weapons_2": 1,
    "infantry_at": 1,
    "infantry_at2": 1,
    "advanced_infantry_weapons": 1,
    "advanced_infantry_weapons2": 1,
    "paratroopers": 1,
    "paratroopers2": 1,
    "paratroopers3": 1,
    "marines": 1,
    "night_vision": 1,
    "night_vision2": 1,
    "support_weapons": 1,
    "support_weapons2": 1,
    "support_weapons3": 1,
    "support_weapons4": 1,
    "tech_trucks": 1,
    "motorised_infantry": 1,
    "mechanised_infantry": 1,
    "mechanised_infantry2": 2,
    "mechanised_infantry3": 1,
    "early_destroyer": 1,
    "basic_destroyer": 1,
    "land_multi_charge_large_caliber_gun_tech": 1,
    "commercial_nuclear_reactor_tech": 1,
    "stronghold_network_tech": 1,
    "thermonuclear_bombs": 1,
    "tech_support": 1,
    "tech_engineers": 1,
    "tech_engineers2": 1,
    "tech_engineers3": 1,
    "tech_engineers4": 1,
    "tech_recon": 1,
    "tech_recon2": 1,
    "tech_recon3": 1,
    "tech_recon4": 1,
    "tech_military_police": 1,
    "tech_signal_company": 1,
    "basic_train": 1,
    "wartime_train": 1,
    "sp_armored_engineer_tech": 1,
    "sp_helicopter_artillery_observers_tech": 1,
}

EGYPT_STATES = [
    "446-Cairo.txt", "447-Alexandria.txt", "452-Marsa Matruh.txt",
    "453-Sinai.txt", "456-Luxor.txt", "457-Aswan.txt",
    "552-Western Egypt.txt", "907-Cairo.txt",
]
RESOURCE_TOTALS = {
    "steel": 752, "tungsten": 300, "rubber": 50, "chromium": 210,
    "coal": 300, "aluminium": 200, "oil": 320,
}
BUILD_EXPECT = {
    "446-Cairo.txt":         (5, 6, 3),
    "447-Alexandria.txt":    (5, 6, 3),
    "452-Marsa Matruh.txt":  (4, 7, 3),
    "453-Sinai.txt":         (4, 7, 3),
    "456-Luxor.txt":         (9, 0, 5),
    "457-Aswan.txt":         (5, 6, 3),
    "552-Western Egypt.txt": (9, 0, 5),
    "907-Cairo.txt":         (4, 7, 3),
}
INLAND_STATES = {"456-Luxor.txt", "552-Western Egypt.txt"}
BUILD_KEYS = ("arms_factory", "dockyard", "industrial_complex")

NEW_STATES = [
    "549-Sudan.txt", "551-Khartoum.txt", "767-North Darfur.txt",
    "883-Kassala.txt", "884-Upper Nile.txt", "885-Bahr al Ghazal.txt",
    "886-Blue Nile.txt", "887-South Darfur.txt",
    "455-Jordan.txt", "454-Israel.txt", "553-Lebanon.txt",
]
NEW_BUILD_EXPECT = {
    "883-Kassala.txt": (2, 5, 2), "455-Jordan.txt": (2, 5, 2),
    "454-Israel.txt": (1, 5, 3), "553-Lebanon.txt": (1, 5, 3),
    "549-Sudan.txt": (4, 0, 5), "551-Khartoum.txt": (4, 0, 5),
    "767-North Darfur.txt": (4, 0, 5), "884-Upper Nile.txt": (3, 0, 6),
    "885-Bahr al Ghazal.txt": (3, 0, 6), "886-Blue Nile.txt": (3, 0, 6),
    "887-South Darfur.txt": (3, 0, 6),
}
NEW_INLAND = set(NEW_STATES) - {"883-Kassala.txt", "455-Jordan.txt",
                                "454-Israel.txt", "553-Lebanon.txt"}

errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


check(not os.path.exists(os.path.join(MOD, "map")),
      "folder map/ masih ada (harus dihapus agar error map hilang)")

# --- state ---
totals = defaultdict(int)
for fn in EGYPT_STATES:
    p = os.path.join(MOD, "history", "states", fn)
    check(os.path.isfile(p), "state hilang: %s" % fn)
    if not os.path.isfile(p):
        continue
    txt = open(p, encoding="utf-8-sig", errors="replace").read()
    check(re.search(r"owner\s*=\s*EGY", txt) is not None,
          "%s: owner bukan EGY" % fn)
    check(re.search(r"owner\s*=\s*ENG", txt) is None,
          "%s: masih ada owner = ENG" % fn)
    check(re.search(r"state_category\s*=\s*megalopolis", txt) is not None,
          "%s: state_category bukan megalopolis" % fn)
    check(re.search(r"add_core_of\s*=\s*EGY", txt) is not None,
          "%s: tidak punya core EGY" % fn)
    m = re.search(r"resources\s*=\s*\{([^}]*)\}", txt, re.S)
    check(m is not None, "%s: blok resources hilang" % fn)
    if m:
        for k in RESOURCE_TOTALS:
            mm = re.search(r"\b%s\s*=\s*(\d+)" % k, m.group(1))
            check(mm is not None, "%s: resource %s hilang" % (fn, k))
            if mm:
                totals[k] += int(mm.group(1))

for k, v in RESOURCE_TOTALS.items():
    check(totals[k] == v,
          "total %s = %d (harap %d)" % (k, totals[k], v))

# --- building slots (3 tab = level atas blok buildings) ---
b_total = defaultdict(int)
for fn in EGYPT_STATES:
    p = os.path.join(MOD, "history", "states", fn)
    if not os.path.isfile(p):
        continue
    txt = open(p, encoding="utf-8-sig", errors="replace").read()
    vals = {}
    for b in BUILD_KEYS:
        mm = re.search(r"^\t\t\t%s = (\d+)$" % b, txt, re.M)
        vals[b] = int(mm.group(1)) if mm else 0
        b_total[b] += vals[b]
    got = tuple(vals[b] for b in BUILD_KEYS)
    check(got == BUILD_EXPECT[fn],
          "%s: building %s (harap %s)" % (fn, got, BUILD_EXPECT[fn]))
    check(sum(got) == 14,
          "%s: total shared building %d (harap 14)" % (fn, sum(got)))
    if fn in INLAND_STATES:
        check(vals["dockyard"] == 0,
              "%s: dockyard di state pedalaman (only_costal)" % fn)

check(b_total["arms_factory"] == 45,
      "total arms_factory = %d (harap 45)" % b_total["arms_factory"])
check(b_total["dockyard"] == 39,
      "total dockyard = %d (harap 39)" % b_total["dockyard"])
check(b_total["industrial_complex"] == 28,
      "total industrial_complex = %d (harap 28)" % b_total["industrial_complex"])
check(sum(b_total.values()) == 112,
      "total slot = %d (harap 112)" % sum(b_total.values()))

# --- wilayah baru: SUD / JOR / ISR / LEB ---
n_total = defaultdict(int)
for fn in NEW_STATES:
    p = os.path.join(MOD, "history", "states", fn)
    check(os.path.isfile(p), "state baru hilang: %s" % fn)
    if not os.path.isfile(p):
        continue
    txt = open(p, encoding="utf-8-sig", errors="replace").read()
    check(re.search(r"owner\s*=\s*EGY", txt) is not None,
          "%s: owner bukan EGY" % fn)
    for old in ("ENG", "PAL", "JOR", "LEB"):
        check(re.search(r"owner\s*=\s*%s\b" % old, txt) is None,
              "%s: masih owner = %s" % (fn, old))
    check(re.search(r"add_core_of\s*=\s*EGY", txt) is not None,
          "%s: tidak punya core EGY" % fn)
    check(re.search(r"state_category\s*=\s*large_city", txt) is not None,
          "%s: state_category bukan large_city" % fn)
    vals = {}
    for b in BUILD_KEYS:
        mm = re.search(r"^\t\t\t%s = (\d+)$" % b, txt, re.M)
        vals[b] = int(mm.group(1)) if mm else 0
        n_total[b] += vals[b]
    got = tuple(vals[b] for b in BUILD_KEYS)
    check(got == NEW_BUILD_EXPECT[fn],
          "%s: building %s (harap %s)" % (fn, got, NEW_BUILD_EXPECT[fn]))
    check(sum(got) == 9,
          "%s: total shared building %d (harap 9)" % (fn, sum(got)))
    if fn in NEW_INLAND:
        check(vals["dockyard"] == 0,
              "%s: dockyard di state pedalaman (only_costal)" % fn)

check(n_total["arms_factory"] == 30,
      "total arms_factory baru = %d (harap 30)" % n_total["arms_factory"])
check(n_total["dockyard"] == 20,
      "total dockyard baru = %d (harap 20)" % n_total["dockyard"])
check(n_total["industrial_complex"] == 49,
      "total industrial_complex baru = %d (harap 49)" %
      n_total["industrial_complex"])
check(sum(n_total.values()) == 99,
      "total slot baru = %d (harap 99)" % sum(n_total.values()))

# --- country & leader ---
hist = os.path.join(MOD, "history", "countries", "EGY - Egypt.txt")
check(os.path.isfile(hist), "history country EGY hilang")
if os.path.isfile(hist):
    t = open(hist, encoding="utf-8-sig", errors="replace").read()
    check("capital = 907" in t, "capital bukan 907")
    check('set_oob = "EGY_1936"' in t, "set_oob EGY_1936 hilang")
    check("create_country_leader" in t, "create_country_leader hilang")
    check("Khalifah Harun al-Rashid" in t, "nama khalifah salah")
    check("ideology = despotism" in t, "ideology leader bukan despotism")
    check("set_research_slots = 4" in t, "set_research_slots = 4 hilang")
    check(t.count("set_grand_doctrine = ") == 1,
          "grand doctrine lebih dari 1 (harap seperti awal)")
    check("set_grand_doctrine = grand_battleplan" in t,
          "grand doctrine grand_battleplan hilang")

    lm = re.search(r"create_country_leader\s*=\s*\{(.*?)\n\}", t, re.S)
    check(lm is not None, "blok create_country_leader tidak ditemukan")
    if lm:
        for trait in LEADER_TRAITS:
            check(re.search(r"(?m)^\t\t%s[ \t]*$" % trait, lm.group(1))
                  is not None, "trait khalifah %s hilang" % trait)

    tm = re.search(r"set_technology\s*=\s*\{(.*?)\n\}", t, re.S)
    check(tm is not None, "blok set_technology tidak ditemukan")
    if tm:
        body = tm.group(1)
        have = {}
        for m in re.finditer(r"(?m)^\t([A-Za-z0-9_]+) = (\d+)[ \t]*$", body):
            have[m.group(1)] = int(m.group(2))
        expected = EXPECTED_TECHS
        kurang = sorted(set(expected) - set(have))
        lebih = sorted(set(have) - set(expected))
        beda_level = sorted(k for k in set(expected) & set(have)
                            if expected[k] != have[k])
        check(not kurang and not lebih and not beda_level,
              "set_technology tidak cocok dengan 200 tech save 1941.12.1: "
              "kurang %s / lebih %s / level beda %s" %
              (kurang, lebih, beda_level))

oob = os.path.join(MOD, "history", "units", "EGY_1936.txt")
check(os.path.isfile(oob), "OOB EGY_1936 hilang")
if os.path.isfile(oob):
    t = open(oob, encoding="utf-8-sig", errors="replace").read()
    check(t.count("division={") == 4, "OOB bukan 4 divisi")
    for name in DIVISION_NAMES:
        check('name="%s"' % name in t, "nama divisi hilang: %s" % name)
    reg = re.search(r"regiments\s*=\s*\{([^}]*)\}", t, re.S)
    sup = re.search(r"support\s*=\s*\{([^}]*)\}", t, re.S)
    check(reg is not None and "artillery" not in reg.group(1),
          "artillery tidak boleh di regiments (support type)")
    check(sup is not None and "artillery" in sup.group(1),
          "artillery harus di support division template")

# --- perwira ---
chars = os.path.join(MOD, "common", "characters", "EGY.txt")
check(os.path.isfile(chars), "common/characters/EGY.txt hilang")
if os.path.isfile(chars):
    t = open(chars, encoding="utf-8-sig", errors="replace").read()
    check(t.count("field_marshal = {") == 3,
          "field marshal = %d (harap 3)" % t.count("field_marshal = {"))
    check(t.count("corps_commander = {") == 12,
          "corps commander = %d (harap 12)" % t.count("corps_commander = {"))
    check(t.count("navy_leader = {") == 5,
          "navy leader = %d (harap 5)" % t.count("navy_leader = {"))
    stat_vals = [int(x) for x in re.findall(
        r"\b(?:skill|attack_skill|defense_skill|planning_skill|logistics_skill|"
        r"maneuvering_skill|coordination_skill) = (\d+)", t)]
    check(len(stat_vals) == 100, "jumlah field stat = %d (harap 100)" % len(stat_vals))
    check(all(v >= 3 for v in stat_vals),
          "ada stat < 3: %s" % sorted(set(v for v in stat_vals if v < 3)))
    check(all(v <= 9 for v in stat_vals),
          "ada stat > 9: %s" % sorted(set(v for v in stat_vals if v > 9)))

    LAND = {"brilliant_strategist", "brave", "career_officer",
            "engineer_officer", "infantry_officer", "old_guard", "motivated",
            "harsh_leader", "armor_officer", "cavalry_officer",
            "trait_cautious", "trait_reckless"}
    FM_ONLY = {"aggressive_assaulter", "defensive_doctrine",
               "expert_delegator", "fast_planner", "inspirational_leader",
               "logistics_wizard", "offensive_doctrine",
               "organisational_leader", "thorough_planner",
               "unyielding_defender"}
    GEN_ONLY = {"adaptable", "ambusher", "camouflage_expert",
                "combined_arms_expert", "desert_fox", "expert_improviser",
                "fortress_buster", "guerilla_fighter", "hill_fighter",
                "infantry_expert", "infantry_leader", "jungle_rat",
                "organizer", "paratrooper", "ranger", "skirmisher",
                "swamp_fox", "trait_engineer", "trait_mountaineer",
                "trickster", "urban_assault_specialist", "winter_expert"}
    CONFLICT = {
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
    KHALID = {"skill": 7, "attack_skill": 8, "defense_skill": 4,
              "planning_skill": 6, "logistics_skill": 6}

    NAVY = {"destroyer_officer", "fleet_protector", "destroyer_leader",
            "smoke_screen_expert", "submarine_officer", "seawolf",
            "silent_hunter", "hunter_killer", "lone_wolf", "torpedo_expert",
            "search_pattern_expert", "carrier_officer", "aviation_enthusiast",
            "air_controller", "flight_deck_manager", "battleship_adherent",
            "heavy_ship_officer", "ironside", "big_guns_expert",
            "chief_engineer", "safety_first", "navy_career_officer",
            "loading_drill_master"}
    ADMIRAL_FOCUS = {
        "EGY_admiral_abu_al_fath": "submarine",
        "EGY_admiral_uthman_al_ghazi": "submarine",
        "EGY_admiral_khalil_al_bahri": "surface",
        "EGY_admiral_nur_al_din": "surface",
        "EGY_admiral_ishaq_al_muhandis": "management",
    }
    #Tiap grup harus terwakili minimal satu trait
    FOCUS_GROUPS = {
        "submarine": [{"submarine_officer", "seawolf"}],
        "surface": [{"destroyer_officer", "destroyer_leader"},
                    {"battleship_adherent", "heavy_ship_officer", "ironside"},
                    {"carrier_officer", "aviation_enthusiast", "air_controller"}],
        "management": [{"chief_engineer", "navy_career_officer"}],
    }
    PRIMARY_NAVY_STATS = {
        "submarine": ("attack_skill", "maneuvering_skill"),
        "surface": ("attack_skill", "defense_skill"),
        "management": ("coordination_skill", "skill"),
    }
    NAVY_CONFLICT = {
        "silent_hunter": {"lancer"}, "lancer": {"silent_hunter"},
        "fighter_director": {"dive_bomber", "torpedo_bomber"},
        "dive_bomber": {"fighter_director", "torpedo_bomber"},
        "torpedo_bomber": {"fighter_director", "dive_bomber"},
        "concealment_expert": {"lone_wolf"},
        "lone_wolf": {"concealment_expert"},
    }

    chars_hist = open(
        os.path.join(MOD, "history", "countries", "EGY - Egypt.txt"),
        encoding="utf-8-sig", errors="replace").read()
    n_char = 0
    for m in re.finditer(r"^\t(EGY_[a-z_]+) = \{(.*?)^\t\}", t, re.M | re.S):
        tok, body = m.group(1), m.group(2)
        n_char += 1
        check("recruit_character = %s" % tok in chars_hist,
              "%s tidak di-recruit di history" % tok)
        is_navy = "navy_leader = {" in body
        is_fm = "field_marshal = {" in body
        kind = "navy_leader" if is_navy else (
            "field_marshal" if is_fm else "corps_commander")
        if is_navy:
            allowed, forbidden = NAVY, LAND | FM_ONLY | GEN_ONLY
        else:
            allowed = LAND | (FM_ONLY if is_fm else GEN_ONLY)
            forbidden = (GEN_ONLY if is_fm else FM_ONLY) | {
                "superior_tactician", "demoted", "sick", "wounded"}
        conflicts = NAVY_CONFLICT if is_navy else CONFLICT
        tm = re.search(r"traits = \{ (.*?) \}", body)
        traits = tm.group(1).split() if tm else []
        lo, hi = (3, 6) if is_navy else (1, 3)
        check(bool(tm) and lo <= len(traits) <= hi,
              "%s: jumlah trait %d (harap %d-%d)" % (tok, len(traits), lo, hi))
        check(all(x in allowed for x in traits),
              "%s: trait tidak cocok untuk %s: %s" %
              (tok, kind, [x for x in traits if x not in allowed]))
        check(all(x not in forbidden for x in traits),
              "%s: trait terlarang untuk %s: %s" %
              (tok, kind, [x for x in traits if x in forbidden]))
        check(not any(b in conflicts.get(a, ()) for a in traits
                      for b in traits if a != b),
              "%s: trait saling mutually_exclusive: %s" % (tok, traits))

        if is_navy:
            keys = ("skill", "attack_skill", "defense_skill",
                    "maneuvering_skill", "coordination_skill")
            focus = ADMIRAL_FOCUS.get(tok)
            check(focus is not None, "%s: fokus admiral tidak dikenal" % tok)
            if focus:
                for group in FOCUS_GROUPS[focus]:
                    check(bool(group.intersection(traits)),
                          "%s: fokus %s kurang trait dari %s" %
                          (tok, focus, sorted(group)))
        else:
            keys = ("skill", "attack_skill", "defense_skill",
                    "planning_skill", "logistics_skill")
        st = {k: int(v) for k, v in re.findall(
            r"\b(%s) = (\d+)" % "|".join(keys), body)}
        if tok == "EGY_khalid_ibn_al_walid":
            check(st == KHALID,
                  "Khalid stat %s (harap %s)" % (st, KHALID))
        else:
            low, high = (3, 5) if is_navy else (4, 5)
            check(all(low <= v <= high for v in st.values()),
                  "%s: stat di luar %d-%d: %s" % (tok, low, high, st))
            if is_navy and focus:
                for k in PRIMARY_NAVY_STATS[focus]:
                    check(st.get(k) == 5,
                          "%s: stat utama %s = %s (harap 5)" % (tok, k, st.get(k)))
    check(n_char == 20, "jumlah karakter = %d (harap 20)" % n_char)

# --- idea & focus ---
idea = os.path.join(MOD, "common", "ideas", "EGY_ideas.txt")
check(os.path.isfile(idea), "common/ideas/EGY_ideas.txt hilang")
if os.path.isfile(idea):
    t = open(idea, encoding="utf-8-sig", errors="replace").read()
    check("gsm_scientific_industry = {" in t, "idea gsm_scientific_industry hilang")
    check("original_tag = EGY" in t, "idea tidak dibatasi untuk EGY")
    check("gsm_caliphate_legacy = {" in t, "idea gsm_caliphate_legacy hilang")
    for mod in ("war_support_factor = 0.1",
                "stability_factor = 0.15",
                "conscription_factor = 0.01"):
        check(mod in t, "modifier buff kekhalifahan hilang: %s" % mod)
    check("industrial_capacity_dockyard = 0.1" in t,
          "modifier dockyard output +10% hilang")
    for mod in ("weekly_manpower = 2500", "conscription_factor = 0.1",
                "stability_factor = 0.05", "research_speed_factor",
                "production_speed_industrial_complex_factor",
                "production_speed_arms_factory_factor",
                "production_speed_dockyard_factor"):
        check(mod not in t, "modifier idea lama masih ada: %s" % mod)
    legacy = t.split("gsm_caliphate_legacy = {")[-1]
    mm = re.search(r"modifier\s*=\s*\{([^}]*)\}", legacy, re.S)
    n = len(re.findall(r"[a-z_]+\s*=", mm.group(1))) if mm else -1
    check(n == 3, "gsm_caliphate_legacy punya %d modifier (harap 3)" % n)

trait_file = os.path.join(MOD, "common", "country_leader", "EGY_traits.txt")
check(os.path.isfile(trait_file), "common/country_leader/EGY_traits.txt hilang")
if os.path.isfile(trait_file):
    t = open(trait_file, encoding="utf-8-sig", errors="replace").read()
    check("gsm_stability = {" in t, "trait awal gsm_stability hilang")
    check("gsm_caliph = {" in t, "trait gsm_caliph hilang")
    caliph = t.split("gsm_caliph = {")[-1]
    for mod in ("stability_factor", "war_support_factor", "weekly_manpower",
                "mobilization_speed", "conscription_factor"):
        check(mod not in caliph,
              "trait gsm_caliph harus kosmetik, modifier lama masih ada: %s" % mod)

focus = os.path.join(MOD, "common", "national_focus", "EGY.txt")
check(os.path.isfile(focus), "common/national_focus/EGY.txt hilang")
if os.path.isfile(focus):
    t = open(focus, encoding="utf-8-sig", errors="replace").read()
    check("id = egy_tree" in t, "id focus_tree salah")
    check("default = no" in t, "focus_tree harus default = no (tag EGY yang memilih)")
    check("tag = EGY" in t, "focus_tree tidak menarget EGY")
    check("id = EGY_scientific_industrial_renaissance" in t,
          "focus EGY_scientific_industrial_renaissance hilang")
    check("id = EGY_islamic_unity" in t, "focus EGY_islamic_unity hilang")
    for pre in ("EGY_scientific_industrial_renaissance", "EGY_islamic_unity"):
        check(re.search(r"prerequisite\s*=\s*\{[^}]*focus\s*=\s*%s" % pre,
                        t, re.S) is not None,
              "focus setelah %s tidak punya prerequisite" % pre)
    check("require = {" not in t,
          "keyword 'require' tidak valid di focus (pakai 'prerequisite')")
    check("id = EGY_proclaim_caliphate" in t, "focus EGY_proclaim_caliphate hilang")
    check("country_event = { id = gsm_caliphate.1 days = 1 }" in t,
          "focus proklamasi tidak memicu event gsm_caliphate.1")
    check("add_ideas = gsm_scientific_industry" in t,
          "reward focus tidak membuka idea gsm_scientific_industry")

# idea produksi kapal harus sudah aktif sejak 1936 lewat history
hist = os.path.join(MOD, "history", "countries", "EGY - Egypt.txt")
if os.path.isfile(hist):
    t = open(hist, encoding="utf-8-sig", errors="replace").read()
    check("add_ideas = gsm_scientific_industry" in t,
          "national spirit gsm_scientific_industry tidak ada sejak awal")

# --- kekhalifahan ---
decision = os.path.join(MOD, "common", "decisions", "EGY_caliphate.txt")
check(os.path.isfile(decision), "common/decisions/EGY_caliphate.txt hilang")
if os.path.isfile(decision):
    t = open(decision, encoding="utf-8-sig", errors="replace").read()
    check("gsm_caliphate_category = {" in t,
          "decision tidak pakai kategori khusus gsm_caliphate_category")
    check("gsm_proclaim_caliphate = {" in t, "decision proklamasi hilang")
    for tag in ("TUR", "IRQ", "SAU", "ISR", "LEB", "JOR"):
        check("%s = { is_subject_of = EGY }" % tag in t,
              "syarat vassal %s hilang" % tag)
    check("country_event = { id = gsm_caliphate.1" in t,
          "decision tidak memicu event gsm_caliphate.1")

event = os.path.join(MOD, "events", "EGY_caliphate.txt")
check(os.path.isfile(event), "events/EGY_caliphate.txt hilang")
if os.path.isfile(event):
    t = open(event, encoding="utf-8-sig", errors="replace").read()
    check("id = gsm_caliphate.1" in t, "id event kekhalifahan salah")
    check("set_cosmetic_tag = CAL" in t, "event tidak mengubah cosmetic tag")
    check("add_manpower = 25000" in t, "event tidak menambah manpower")
    check("add_ideas = gsm_caliphate_legacy" in t, "event tidak memberi national spirit")
    check("remove_country_leader_trait = gsm_stability" in t,
          "event tidak menghapus trait awal")
    check("add_country_leader_trait = gsm_caliph" in t,
          "event tidak memberi trait gsm_caliph")

cal = os.path.join(MOD, "common", "countries", "CAL.txt")
check(os.path.isfile(cal), "common/countries/CAL.txt hilang")
if os.path.isfile(cal):
    t = open(cal, encoding="utf-8-sig", errors="replace").read()
    check("color = { 30 120 65 }" in t, "warna cosmetic tag CAL salah")
flag = os.path.join(MOD, "gfx", "flags", "CAL.tga")
check(os.path.isfile(flag), "flag CAL.tga hilang")

# --- localisation ---
loc = os.path.join(MOD, "localisation", "english", "GSM_l_english.yml")
check(os.path.isfile(loc), "file lokalisasi GSM_l_english.yml hilang")
if os.path.isfile(loc):
    raw = open(loc, "rb").read()
    check(raw.startswith(b"\xef\xbb\xbf"), "lokalisasi tidak punya BOM")
    t = raw.decode("utf-8-sig", errors="replace")
    required = [
        'EGY: "Grand Sultanate of Al-Muhit"',
        'EGY_neutrality: "Grand Sultanate of Al-Muhit"',
        'EGY_neutrality_DEF: "the Grand Sultanate of Al-Muhit"',
        'EGY_brit_puppet: "Grand Sultanate of Al-Muhit"',
        'STATE_907: "Dar al-Khilafah"',
        'VICTORY_POINTS_7011: "Dar al-Khilafah"',
        'VICTORY_POINTS_907: "Dar al-Khilafah"',
        'gsm_caliphate_legacy_desc: "By the Caliph\'s decree: +10% war support, +15% stability and +1% recruitable population."',
        'EGY_khalid_ibn_al_walid: "Khalid ibn al-Walid"',
        'EGY_admiral_khalil_al_bahri: "Khalil al-Bahri"',
        'EGY_admiral_abu_al_fath: "Abu al-Fath"',
        'EGY_admiral_uthman_al_ghazi: "Uthman al-Ghazi"',
        'EGY_admiral_nur_al_din: "Nur al-Din"',
        'EGY_admiral_ishaq_al_muhandis: "Ishaq al-Muhandis"',
        'gsm_scientific_industry: "Scientific & Industrial Renaissance"',
        'gsm_stability: "Steadfast Caliph"',
        'gsm_caliph: "Caliph of the Faithful"',
        'gsm_caliphate_category: "The Caliphate"',
        'gsm_caliphate_legacy: "Legacy of the Caliphate"',
        'gsm_proclaim_caliphate: "Proclaim the Caliphate"',
        'EGY_islamic_unity: "Islamic Unity"',
        'EGY_proclaim_caliphate: "Proclaim the Caliphate"',
        'gsm_caliphate.1.t: "The Grand Islamic Caliphate"',
        'CAL: "Grand Islamic Caliphate"',
        'CAL_DEF: "the Grand Islamic Caliphate"',
        'EGY_scientific_industrial_renaissance: "Scientific & Industrial Renaissance"',
        'EGY_scientific_industrial_renaissance_desc: "Empower our shipyards to forge a new fleet for the Grand Sultanate."',
    ]
    for line in required:
        check(line in t, "lokalisasi hilang: %s" % line)

# --- colors / country definition ---
cd = os.path.join(MOD, "common", "countries", "Egypt.txt")
check(os.path.isfile(cd), "country definition Egypt.txt hilang")
colors = os.path.join(MOD, "common", "countries", "colors.txt")
check(os.path.isfile(colors), "colors.txt hilang")
if os.path.isfile(colors):
    t = open(colors, encoding="utf-8-sig", errors="replace").read()
    m = re.search(r"EGY\s*=\s*\{(.*?)\n\}", t, re.S)
    check(m is not None, "colors.txt tidak punya blok EGY")
    if m:
        check("212 175 55" in m.group(1), "warna EGY belum emas Al-Muhit")
        check("255 215 100" in m.group(1), "color_ui EGY belum emas terang")
    check("24 122 74" not in m.group(1),
          "masih ada warna hijau lama di blok EGY")
    check("230 230 70" not in t,
          "masih ada warna EGY lama (230 230 70) -> blok rusak")

# --- flags ---
for folder, fsize in (("", (82, 52)), ("medium", (41, 26)), ("small", (10, 7))):
    for fn in ("EGY.tga", "EGY_neutrality.tga", "EGY_fascism.tga",
               "EGY_communism.tga", "EGY_democratic.tga"):
        p = os.path.join(MOD, "gfx", "flags", folder, fn)
        check(os.path.isfile(p), "flag %s/%s hilang" % (folder, fn))
        if os.path.isfile(p):
            try:
                im = Image.open(p)
                check(im.size == fsize,
                      "flag %s/%s size %s" % (folder, fn, im.size))
                if folder == "" and fn == "EGY.tga" and im.size == (82, 52):
                    rgba = im.convert("RGBA")
                    check(rgba.getpixel((5, 5)) == (212, 175, 55, 255),
                          "warna dasar bendera EGY bukan emas")
                    check(rgba.getpixel((0, 0)) == (255, 215, 100, 255),
                          "pinggir bendera EGY bukan emas terang")
                    check(rgba.getpixel((30, 26)) == (96, 68, 16, 255),
                          "lambang bendera EGY bukan perunggu")
                    rgba.close()
                im.close()
            except Exception as e:
                errors.append("flag %s/%s: %s" % (folder, fn, e))

# --- descriptors ---
for p in (DESCRIPTOR, os.path.join(MOD, "descriptor.mod")):
    check(os.path.isfile(p), "descriptor hilang: %s" % p)
    if os.path.isfile(p):
        t = open(p, encoding="utf-8-sig", errors="replace").read()
        check('version="1.20.0.0"' in t, "descriptor version salah: %s" % p)
        check('supported_version="1.20.*"' in t,
              "descriptor supported_version salah: %s" % p)
        check('path="mod/Al-Muhit"' in t, "descriptor path salah: %s" % p)

if errors:
    print("VALIDASI GAGAL:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("VALIDASI OK: Mesir 112 slot + 11 state baru 99 slot, tanpa override peta.")
