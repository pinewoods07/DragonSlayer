import streamlit as st
import random
import time

# ============================================
#  🏰 드래곤 슬레이어 v2
# ============================================

st.set_page_config(page_title="🏰 드래곤 슬레이어", page_icon="⚔️", layout="centered")

# ── CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #0a0a1a 0%, #1a0a2e 100%);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .title-box {
        text-align: center;
        padding: 20px 0 10px;
    }
    .title-box h1 {
        font-size: 2.2em;
        background: linear-gradient(90deg, #ffd700, #ff8c00, #ffd700);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
    }
    @keyframes shimmer {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    .title-box .sub {
        color: #667;
        font-size: 0.85em;
    }
    
    .box {
        background: linear-gradient(135deg, #161633, #1e1e44);
        border: 1px solid #2e2e5e;
        border-radius: 14px;
        padding: 18px;
        margin: 8px 0;
    }
    .box-red {
        background: linear-gradient(135deg, #2a1010, #3a1515);
        border: 1px solid #5a2a2a;
        border-radius: 14px;
        padding: 18px;
        margin: 8px 0;
        text-align: center;
    }
    .box-green {
        background: linear-gradient(135deg, #102a10, #153a15);
        border: 1px solid #2a5a2a;
        border-radius: 14px;
        padding: 18px;
        margin: 8px 0;
        text-align: center;
    }
    
    .bar-bg {
        background: #0a0a15;
        border-radius: 8px;
        height: 22px;
        overflow: hidden;
        border: 1px solid #222;
        margin: 4px 0;
    }
    .bar-fill {
        height: 100%;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75em;
        font-weight: bold;
        color: white;
        text-shadow: 1px 1px 2px #000;
        transition: width 0.5s ease;
    }
    
    .log-box {
        background: #08081a;
        border: 1px solid #1e1e3e;
        border-radius: 10px;
        padding: 12px;
        font-size: 0.82em;
        line-height: 1.8;
        max-height: 250px;
        overflow-y: auto;
        color: #aaa;
    }
    .log-box .dmg { color: #ff6666; }
    .log-box .heal { color: #66ff66; }
    .log-box .skill { color: #ffaa00; }
    .log-box .info { color: #6699ff; }
    
    .stat-row {
        display: flex;
        justify-content: space-around;
        margin-top: 10px;
        font-size: 0.85em;
        color: #999;
    }
    
    .big-emoji {
        font-size: 4em;
        text-align: center;
        animation: bounce 0.6s ease;
    }
    @keyframes bounce {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .shake {
        animation: shake 0.4s ease;
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-8px); }
        75% { transform: translateX(8px); }
    }
    
    .flash-red {
        animation: flashR 0.5s ease;
    }
    @keyframes flashR {
        0% { background: #ff000033; }
        100% { background: transparent; }
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .victory-text {
        text-align: center;
        font-size: 1.8em;
        font-weight: 900;
        color: #ffd700;
        text-shadow: 0 0 20px #ffd70066;
        animation: glow 1.5s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 5px #ffd700; }
        to { text-shadow: 0 0 30px #ffd700, 0 0 60px #ff8c00; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
#  게임 데이터
# ============================================

JOBS = {
    "⚔️ 전사": {
        "emoji": "⚔️", "hp": 130, "atk": 16, "def": 12, "spd": 5,
        "skill": "파워 슬래시", "skill_desc": "공격력 2.2배 강타",
        "skill_type": "power", "skill_mult": 2.2, "sp_cost": 100,
    },
    "🧙 마법사": {
        "emoji": "🧙", "hp": 85, "atk": 24, "def": 5, "spd": 8,
        "skill": "파이어볼", "skill_desc": "공격력 2.5배 + 화상(3턴간 피해)",
        "skill_type": "magic_burn", "skill_mult": 2.5, "sp_cost": 100,
    },
    "🏹 궁수": {
        "emoji": "🏹", "hp": 95, "atk": 19, "def": 7, "spd": 15,
        "skill": "속사", "skill_desc": "3~5회 연속 공격",
        "skill_type": "multi", "skill_mult": 1.0, "sp_cost": 100,
    },
    "🛡️ 성기사": {
        "emoji": "🛡️", "hp": 160, "atk": 12, "def": 16, "spd": 3,
        "skill": "성스러운 빛", "skill_desc": "HP 35% 회복 + 공격력 1.5배 공격",
        "skill_type": "heal_atk", "skill_mult": 1.5, "sp_cost": 100,
    },
}

AREAS = {
    "🌲 수풀 숲": {
        "level_req": 1,
        "monsters": [
            {"name": "슬라임", "emoji": "🟢", "hp": 50, "atk": 10, "def": 3,
             "exp": 20, "gold": 8, "skill": None},
            {"name": "고블린", "emoji": "👺", "hp": 70, "atk": 14, "def": 5,
             "exp": 30, "gold": 12, "skill": "독 칼날", "s_mult": 1.5, "s_chance": 20},
            {"name": "늑대", "emoji": "🐺", "hp": 55, "atk": 16, "def": 3,
             "exp": 25, "gold": 10, "skill": "급소 물기", "s_mult": 2.0, "s_chance": 15},
        ]
    },
    "🏔️ 바위 산": {
        "level_req": 3,
        "monsters": [
            {"name": "오크 전사", "emoji": "👹", "hp": 120, "atk": 20, "def": 10,
             "exp": 55, "gold": 28, "skill": "분노의 일격", "s_mult": 1.8, "s_chance": 25},
            {"name": "하피", "emoji": "🦅", "hp": 80, "atk": 24, "def": 5,
             "exp": 50, "gold": 24, "skill": "음파 공격", "s_mult": 2.0, "s_chance": 20},
            {"name": "골렘", "emoji": "🗿", "hp": 180, "atk": 15, "def": 20,
             "exp": 65, "gold": 35, "skill": None},
        ]
    },
    "🌋 화염 동굴": {
        "level_req": 5,
        "monsters": [
            {"name": "화염 정령", "emoji": "🔥", "hp": 140, "atk": 28, "def": 10,
             "exp": 90, "gold": 45, "skill": "폭염", "s_mult": 2.2, "s_chance": 30},
            {"name": "다크나이트", "emoji": "🖤", "hp": 200, "atk": 26, "def": 18,
             "exp": 110, "gold": 60, "skill": "암흑 베기", "s_mult": 2.0, "s_chance": 25},
            {"name": "서큐버스", "emoji": "😈", "hp": 110, "atk": 35, "def": 8,
             "exp": 100, "gold": 55, "skill": "생명 흡수", "s_mult": 1.8, "s_chance": 30},
        ]
    },
    "🐉 드래곤 둥지": {
        "level_req": 8,
        "monsters": [
            {"name": "와이번", "emoji": "🦎", "hp": 250, "atk": 32, "def": 15,
             "exp": 160, "gold": 85, "skill": "급강하", "s_mult": 2.2, "s_chance": 25},
            {"name": "드래곤 가드", "emoji": "🐲", "hp": 300, "atk": 36, "def": 20,
             "exp": 220, "gold": 110, "skill": "화염 브레스", "s_mult": 2.5, "s_chance": 30},
        ]
    }
}

DRAGON_BOSS = {
    "name": "고대 드래곤 이그니스", "emoji": "🐉",
    "hp": 700, "atk": 45, "def": 25, "exp": 0, "gold": 999,
    "skill": "멸망의 브레스", "s_mult": 2.8, "s_chance": 35,
}

SHOP_ITEMS = {
    "🧪 HP 포션 (소)": {"type": "potion", "heal": 40, "price": 20, "desc": "HP 40 회복"},
    "🧪 HP 포션 (대)": {"type": "potion", "heal": 100, "price": 55, "desc": "HP 100 회복"},
    "💙 SP 포션": {"type": "sp_potion", "value": 50, "price": 30, "desc": "SP 50 회복"},
    "⚔️ 강화석": {"type": "atk_boost", "value": 3, "price": 60, "desc": "공격력 +3 영구"},
    "🛡️ 방어 부적": {"type": "def_boost", "value": 3, "price": 60, "desc": "방어력 +3 영구"},
    "💎 생명의 반지": {"type": "hp_boost", "value": 25, "price": 70, "desc": "최대HP +25 영구"},
}

def exp_needed(level):
    return int(level * 45 * (1 + level * 0.1))

# ============================================
#  세션 초기화
# ============================================

DEFAULTS = {
    "scene": "intro", "player": None, "battle_log": [],
    "current_monster": None, "monster_hp": 0, "monster_max_hp": 0,
    "turn": 0, "inventory": [], "kill_count": 0,
    "boss_defeated": False, "burn_turns": 0,
    "last_action": "", "sp": 0, "max_sp": 100,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================
#  유틸리티
# ============================================

def make_bar(current, maximum, color_high="#00cc44", color_mid="#ffaa00", color_low="#ff3333", label=""):
    pct = max(0, min(100, (current / max(1, maximum)) * 100))
    if pct > 50: c = color_high
    elif pct > 25: c = color_mid
    else: c = color_low
    display = label if label else f"{current}/{maximum}"
    return f'<div class="bar-bg"><div class="bar-fill" style="width:{pct}%;background:linear-gradient(90deg,{c},{c}88);">{display}</div></div>'

def add_log(msg, cls=""):
    tag = f'<span class="{cls}">{msg}</span>' if cls else msg
    st.session_state.battle_log.append(tag)
    if len(st.session_state.battle_log) > 25:
        st.session_state.battle_log.pop(0)

def calc_damage(atk, defn):
    base = max(1, atk - defn // 2)
    return max(1, base + random.randint(-3, 5))

def check_level_up():
    p = st.session_state.player
    msgs = []
    while p["exp"] >= exp_needed(p["level"]):
        p["exp"] -= exp_needed(p["level"])
        p["level"] += 1
        p["max_hp"] += 12
        p["hp"] = p["max_hp"]
        p["atk"] += 3
        p["def"] += 2
        p["spd"] += 1
        st.session_state.max_sp = min(150, st.session_state.max_sp + 5)
        msgs.append(f"🎉 레벨 {p['level']} 달성! 능력치 상승! HP 전회복!")
    return msgs

# ============================================
#  전투 로직
# ============================================

def enemy_turn():
    p = st.session_state.player
    m = st.session_state.current_monster

    # 몬스터 스킬 사용 판정
    use_skill = False
    if m.get("skill") and random.randint(1, 100) <= m.get("s_chance", 0):
        use_skill = True

    if use_skill:
        dmg = calc_damage(int(m["atk"] * m["s_mult"]), p["def"])
        add_log(f"💥 {m['emoji']} {m['name']}의 <b>{m['skill']}</b>! → <b>{dmg}</b> 데미지!", "dmg")
        # 서큐버스 생명흡수
        if m.get("skill") == "생명 흡수":
            heal = dmg // 3
            st.session_state.monster_hp = min(st.session_state.monster_max_hp, st.session_state.monster_hp + heal)
            add_log(f"💜 {m['name']}이 {heal} HP를 흡수했다!", "heal")
    else:
        is_crit = random.randint(1, 100) <= 8
        dmg = calc_damage(m["atk"], p["def"])
        if is_crit:
            dmg = int(dmg * 1.7)
            add_log(f"💥 {m['emoji']} {m['name']}의 크리티컬! → <b>{dmg}</b> 데미지!", "dmg")
        else:
            add_log(f"👊 {m['emoji']} {m['name']}의 공격 → <b>{dmg}</b> 데미지", "dmg")

    p["hp"] = max(0, p["hp"] - dmg)
    st.session_state.last_action = "enemy_hit"

    if p["hp"] <= 0:
        add_log("💀 당신은 쓰러졌다...", "dmg")
        st.session_state.scene = "game_over"


def process_burn():
    """화상 데미지 처리"""
    if st.session_state.burn_turns > 0:
        burn_dmg = random.randint(8, 15)
        st.session_state.monster_hp = max(0, st.session_state.monster_hp - burn_dmg)
        st.session_state.burn_turns -= 1
        add_log(f"🔥 화상! {burn_dmg} 추가 데미지! (남은 {st.session_state.burn_turns}턴)", "skill")
        if st.session_state.monster_hp <= 0:
            return True
    return False


def battle_victory():
    p = st.session_state.player
    m = st.session_state.current_monster
    st.session_state.monster_hp = 0
    st.session_state.burn_turns = 0

    is_boss = "이그니스" in m.get("name", "")
    if is_boss:
        st.session_state.boss_defeated = True
        st.session_state.scene = "victory"
        return

    exp_gain = m.get("exp", 0)
    gold_gain = m.get("gold", 0) + random.randint(0, m.get("gold", 0) // 3)
    p["exp"] += exp_gain
    p["gold"] += gold_gain
    st.session_state.kill_count += 1

    add_log(f"━━━━━━━━━━━━━━━━━━", "info")
    add_log(f"🏆 <b>{m['name']}</b> 처치! +{exp_gain}EXP +{gold_gain}G", "info")

    for msg in check_level_up():
        add_log(msg, "skill")

    if random.randint(1, 100) <= 18:
        drop = random.choice(["🧪 HP 포션 (소)", "🧪 HP 포션 (대)", "💙 SP 포션"])
        st.session_state.inventory.append(drop)
        add_log(f"📦 <b>{drop}</b> 획득!", "info")

    st.session_state.scene = "battle_result"


# ============================================
#  씬: 인트로
# ============================================

def scene_intro():
    st.markdown("""
    <div class="title-box">
        <div style="font-size:3em; animation:bounce 0.8s ease;">🏰</div>
        <h1>드래곤 슬레이어</h1>
        <p class="sub">고대 드래곤 이그니스를 처치하라</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    > *천 년간 왕국을 공포에 떨게 한 고대 드래곤 이그니스.*  
    > *수많은 영웅이 도전했지만, 아무도 돌아오지 못했다.*  
    > *왕은 마지막 희망을 걸고 새로운 모험가를 찾고 있다...*
    """)

    if st.button("⚔️ 모험을 시작하다", use_container_width=True, type="primary"):
        st.session_state.scene = "create"
        st.rerun()

    st.markdown("""
    <div style="text-align:center; color:#445; font-size:0.8em; margin-top:30px;">
        ⚔️ 턴제 전투 · 📊 SP 게이지 스킬 · 🛒 상점 · 🐉 보스전
    </div>
    """, unsafe_allow_html=True)


# ============================================
#  씬: 캐릭터 생성
# ============================================

def scene_create():
    st.markdown("""
    <div class="title-box">
        <h1>👤 캐릭터 생성</h1>
        <p class="sub">당신의 영웅을 만드세요</p>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("🏷️ 영웅의 이름", placeholder="이름을 입력하세요")

    st.markdown("### 직업 선택")

    for job_name, j in JOBS.items():
        st.markdown(f"""
        <div class="box">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:2em;">{j['emoji']}</span>
                <div>
                    <div style="color:#ffd700; font-weight:bold; font-size:1.1em;">{job_name}</div>
                    <div style="color:#999; font-size:0.82em;">
                        ❤️{j['hp']} ⚔️{j['atk']} 🛡️{j['def']} 💨{j['spd']}
                    </div>
                    <div style="color:#ffaa00; font-size:0.82em;">
                        ✨ {j['skill']} — {j['skill_desc']} (SP {j['sp_cost']})
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    job = st.selectbox("직업 선택", list(JOBS.keys()))

    if st.button("🎮 게임 시작!", use_container_width=True, type="primary"):
        if not name.strip():
            st.warning("이름을 입력해주세요!")
        else:
            j = JOBS[job]
            st.session_state.player = {
                "name": name.strip(), "job": job, "emoji": j["emoji"],
                "level": 1, "exp": 0,
                "hp": j["hp"], "max_hp": j["hp"],
                "atk": j["atk"], "def": j["def"], "spd": j["spd"],
                "gold": 30,
                "skill": j["skill"], "skill_desc": j["skill_desc"],
                "skill_type": j["skill_type"], "skill_mult": j["skill_mult"],
                "sp_cost": j["sp_cost"],
            }
            st.session_state.sp = 0
            st.session_state.max_sp = 100
            st.session_state.inventory = ["🧪 HP 포션 (소)"] * 2
            st.session_state.scene = "town"
            st.rerun()


# ============================================
#  씬: 마을
# ============================================

def scene_town():
    p = st.session_state.player

    st.markdown("""
    <div class="title-box">
        <h1>🏘️ 평화로운 마을</h1>
        <p class="sub">모험을 준비하세요</p>
    </div>
    """, unsafe_allow_html=True)

    # 캐릭터 상태
    st.markdown(f"""
    <div class="box fade-in">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:1.4em;">{p['emoji']}</span>
                <b style="color:#ffd700; font-size:1.1em;">{p['name']}</b>
                <span style="color:#778;"> {p['job']}</span>
            </div>
            <div style="color:#aaa; font-size:0.9em;">
                Lv.{p['level']} · 💰{p['gold']}G
            </div>
        </div>
        <div style="margin-top:8px;">
            <div style="font-size:0.75em; color:#888;">❤️ HP</div>
            {make_bar(p['hp'], p['max_hp'])}
        </div>
        <div style="margin-top:6px;">
            <div style="font-size:0.75em; color:#888;">✨ SP</div>
            {make_bar(st.session_state.sp, st.session_state.max_sp, '#3399ff', '#3399ff', '#3399ff')}
        </div>
        <div class="stat-row">
            <span>⚔️ 공격 {p['atk']}</span>
            <span>🛡️ 방어 {p['def']}</span>
            <span>💨 속도 {p['spd']}</span>
            <span>📊 EXP {p['exp']}/{exp_needed(p['level'])}</span>
        </div>
        <div style="margin-top:8px; font-size:0.78em; color:#556;">
            🎒 인벤토리: {len(st.session_state.inventory)}개 · 💀 처치: {st.session_state.kill_count}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⚔️ 던전 탐험", use_container_width=True, type="primary"):
            st.session_state.scene = "area_select"
            st.rerun()
    with col2:
        if st.button("🛒 상점", use_container_width=True):
            st.session_state.scene = "shop"
            st.rerun()
    with col3:
        if st.button("💤 휴식 (10G)", use_container_width=True):
            if p["gold"] >= 10:
                p["gold"] -= 10
                p["hp"] = p["max_hp"]
                st.session_state.sp = st.session_state.max_sp
                st.toast("💤 푹 쉬었다! HP·SP 전회복!", icon="😴")
                time.sleep(0.5)
                st.rerun()
            else:
                st.toast("💰 골드가 부족합니다!", icon="❌")

    st.markdown("---")

    if p["level"] >= 8:
        st.markdown("""
        <div style="text-align:center; color:#ff4444; font-size:0.9em; margin-bottom:8px;">
            🐉 드래곤 둥지에서 거대한 기운이 느껴진다...
        </div>
        """, unsafe_allow_html=True)
        if st.button("🐉 최종 보스에게 도전!", use_container_width=True, type="primary"):
            m = DRAGON_BOSS.copy()
            st.session_state.current_monster = m
            st.session_state.monster_hp = m["hp"]
            st.session_state.monster_max_hp = m["hp"]
            st.session_state.battle_log = ["🐉 고대 드래곤 이그니스가 포효한다!!! 대지가 흔들린다!"]
            st.session_state.turn = 0
            st.session_state.burn_turns = 0
            st.session_state.scene = "battle"
            st.rerun()
    else:
        st.markdown(f"""
        <div style="text-align:center; color:#445; font-size:0.82em;">
            🔒 드래곤 도전: Lv.8 필요 (현재 Lv.{p['level']})
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.inventory:
        with st.expander("🎒 인벤토리 확인"):
            counts = {}
            for item in st.session_state.inventory:
                counts[item] = counts.get(item, 0) + 1
            for item, cnt in counts.items():
                st.write(f"{item} ×{cnt}")

# ============================================
#  씬: 상점
# ============================================

def scene_shop():
    p = st.session_state.player

    st.markdown("""
    <div class="title-box">
        <h1>🛒 마을 상점</h1>
        <p class="sub">현명한 투자가 생존을 결정합니다</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="box" style="text-align:center;">
        <span style="font-size:1.3em;">💰</span>
        <b style="color:#ffd700; font-size:1.3em;">{p['gold']}G</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    for item_name, data in SHOP_ITEMS.items():
        col1, col2 = st.columns([4, 1])
        with col1:
            affordable = "color:#ddd;" if p["gold"] >= data["price"] else "color:#555;"
            st.markdown(f"""
            <div class="box" style="padding:12px; {affordable}">
                <b>{item_name}</b>
                <span style="color:#888; font-size:0.85em;"> — {data['desc']}</span>
                <span style="float:right; color:#ffd700;">💰{data['price']}G</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("구매", key=f"buy_{item_name}", use_container_width=True):
                if p["gold"] >= data["price"]:
                    p["gold"] -= data["price"]
                    if data["type"] == "potion":
                        st.session_state.inventory.append(item_name)
                        st.toast(f"✅ {item_name} 구매!", icon="🧪")
                    elif data["type"] == "sp_potion":
                        st.session_state.inventory.append(item_name)
                        st.toast(f"✅ {item_name} 구매!", icon="💙")
                    elif data["type"] == "atk_boost":
                        p["atk"] += data["value"]
                        st.toast(f"⚔️ 공격력 +{data['value']}! (현재 {p['atk']})", icon="⚔️")
                    elif data["type"] == "def_boost":
                        p["def"] += data["value"]
                        st.toast(f"🛡️ 방어력 +{data['value']}! (현재 {p['def']})", icon="🛡️")
                    elif data["type"] == "hp_boost":
                        p["max_hp"] += data["value"]
                        p["hp"] += data["value"]
                        st.toast(f"❤️ 최대HP +{data['value']}! (현재 {p['max_hp']})", icon="💎")
                    time.sleep(0.3)
                    st.rerun()
                else:
                    st.toast("골드가 부족합니다!", icon="❌")

    st.markdown("---")
    if st.button("🏘️ 마을로 돌아가기", use_container_width=True):
        st.session_state.scene = "town"
        st.rerun()


# ============================================
#  씬: 지역 선택
# ============================================

def scene_area_select():
    p = st.session_state.player

    st.markdown("""
    <div class="title-box">
        <h1>🗺️ 던전 선택</h1>
        <p class="sub">어디로 떠날 것인가?</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="box" style="text-align:center; padding:10px;">
        {p['emoji']} <b>{p['name']}</b> Lv.{p['level']}
        · ❤️{p['hp']}/{p['max_hp']}
        · ✨SP {st.session_state.sp}/{st.session_state.max_sp}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    for area_name, area in AREAS.items():
        locked = p["level"] < area["level_req"]
        names = " ".join([f"{m['emoji']}{m['name']}" for m in area["monsters"]])

        if locked:
            st.markdown(f"""
            <div class="box" style="opacity:0.35;">
                <b>{area_name}</b> 🔒 Lv.{area['level_req']} 필요<br>
                <span style="font-size:0.8em; color:#445;">{names}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="box">
                <b style="color:#ffd700;">{area_name}</b>
                <span style="color:#667;"> 권장 Lv.{area['level_req']}+</span><br>
                <span style="font-size:0.82em; color:#999;">출현: {names}</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"➡️ {area_name} 탐험", key=f"go_{area_name}", use_container_width=True):
                m = random.choice(area["monsters"]).copy()
                st.session_state.current_monster = m
                st.session_state.monster_hp = m["hp"]
                st.session_state.monster_max_hp = m["hp"]
                st.session_state.battle_log = [f"⚠️ {m['emoji']} <b>{m['name']}</b>이(가) 나타났다!"]
                st.session_state.turn = 0
                st.session_state.burn_turns = 0
                st.session_state.last_action = ""
                st.session_state.scene = "battle"
                st.rerun()

    st.markdown("---")
    if st.button("🏘️ 마을로 돌아가기", use_container_width=True):
        st.session_state.scene = "town"
        st.rerun()


# ============================================
#  씬: 전투
# ============================================

def scene_battle():
    p = st.session_state.player
    m = st.session_state.current_monster
    m_hp = st.session_state.monster_hp
    m_max = st.session_state.monster_max_hp
    sp = st.session_state.sp
    max_sp = st.session_state.max_sp

    is_boss = "이그니스" in m.get("name", "")

    # 제목
    if is_boss:
        st.markdown("""
        <div class="title-box">
            <h1>🐉 최종 보스전</h1>
            <p class="sub" style="color:#ff4444;">고대 드래곤 이그니스</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="title-box">
            <h1>⚔️ 전투</h1>
            <p class="sub">Turn {st.session_state.turn}</p>
        </div>
        """, unsafe_allow_html=True)

    # 피격 애니메이션 클래스
    m_anim = "shake" if st.session_state.last_action == "player_hit" else ""
    p_anim = "flash-red" if st.session_state.last_action == "enemy_hit" else ""

    # 몬스터 카드
    burn_text = f"<span style='color:#ff6600; font-size:0.8em;'>🔥 화상 {st.session_state.burn_turns}턴</span>" if st.session_state.burn_turns > 0 else ""
    st.markdown(f"""
    <div class="box-red {m_anim}">
        <div class="big-emoji">{m['emoji']}</div>
        <div style="font-size:1.2em; font-weight:bold; color:#ff6666; margin:6px 0;">
            {m['name']}
        </div>
        <div style="font-size:0.8em; color:#777; margin-bottom:6px;">
            ⚔️{m['atk']} 🛡️{m['def']}
            {(' · ✨' + m.get('skill','')) if m.get('skill') else ''}
            {burn_text}
        </div>
        {make_bar(m_hp, m_max, '#cc3333', '#cc6600', '#cc3333')}
    </div>
    """, unsafe_allow_html=True)

    # VS
    st.markdown("<div style='text-align:center; font-size:1.5em; margin:5px 0;'>⚡</div>", unsafe_allow_html=True)

    # 플레이어 카드
    st.markdown(f"""
    <div class="box {p_anim}">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <span style="font-size:1.3em;">{p['emoji']}</span>
                <b style="color:#ffd700;">{p['name']}</b>
                <span style="color:#667;"> Lv.{p['level']}</span>
            </div>
            <div style="color:#888; font-size:0.85em;">
                ⚔️{p['atk']} 🛡️{p['def']}
            </div>
        </div>
        <div style="margin-top:8px;">
            <span style="font-size:0.72em; color:#888;">❤️ HP</span>
            {make_bar(p['hp'], p['max_hp'])}
        </div>
        <div style="margin-top:4px;">
            <span style="font-size:0.72em; color:#888;">✨ SP</span>
            {make_bar(sp, max_sp, '#3399ff', '#3399ff', '#336699', f'{sp}/{max_sp}')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # ── 행동 버튼 ──
    can_skill = sp >= p["sp_cost"]
    potions = [i for i in st.session_state.inventory if "HP 포션" in i]
    sp_potions = [i for i in st.session_state.inventory if "SP 포션" in i]

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        btn_atk = st.button("⚔️ 공격\n(SP+25)", use_container_width=True, type="primary")
    with col2:
        skill_label = f"✨ {p['skill']}\n(SP {p['sp_cost']})" if can_skill else f"🚫 {p['skill']}\n(SP 부족)"
        btn_skill = st.button(skill_label, use_container_width=True, disabled=not can_skill)
    with col3:
        btn_pot = st.button(f"🧪 HP포션 ({len(potions)})", use_container_width=True, disabled=len(potions) == 0)
    with col4:
        if is_boss:
            btn_flee = st.button("🏃 도망 (불가)", use_container_width=True, disabled=True)
        else:
            btn_flee = st.button("🏃 도망", use_container_width=True)

    # SP 포션 (별도)
    if sp_potions:
        if st.button(f"💙 SP포션 사용 ({len(sp_potions)})", use_container_width=True):
            used = sp_potions[0]
            st.session_state.inventory.remove(used)
            recover = 50
            st.session_state.sp = min(max_sp, sp + recover)
            add_log(f"💙 SP포션 사용! SP +{recover}", "heal")
            enemy_turn()
            st.rerun()

    # ── 공격 ──
    if btn_atk:
        st.session_state.turn += 1
        dmg = calc_damage(p["atk"], m["def"])
        st.session_state.monster_hp -= dmg
        st.session_state.sp = min(max_sp, sp + 25)
        add_log(f"⚔️ {p['name']}의 공격! → <b>{dmg}</b> 데미지 (SP+25)", "info")
        st.session_state.last_action = "player_hit"

        # 화상 처리
        if st.session_state.monster_hp > 0:
            if process_burn():
                battle_victory()
                st.rerun()
            else:
                enemy_turn()
        else:
            battle_victory()
        st.rerun()

    # ── 스킬 ──
    if btn_skill:
        st.session_state.turn += 1
        st.session_state.sp -= p["sp_cost"]
        st.session_state.last_action = "player_hit"

        stype = p["skill_type"]

        if stype == "power":
            dmg = calc_damage(int(p["atk"] * p["skill_mult"]), m["def"])
            st.session_state.monster_hp -= dmg
            add_log(f"✨ <b>{p['skill']}!</b> → <b>{dmg}</b> 데미지!", "skill")

        elif stype == "magic_burn":
            dmg = calc_damage(int(p["atk"] * p["skill_mult"]), m["def"])
            st.session_state.monster_hp -= dmg
            st.session_state.burn_turns = 3
            add_log(f"🔥 <b>{p['skill']}!</b> → <b>{dmg}</b> 데미지 + 화상 3턴!", "skill")

        elif stype == "multi":
            hits = random.randint(3, 5)
            total = 0
            for _ in range(hits):
                d = calc_damage(p["atk"], m["def"])
                total += d
            st.session_state.monster_hp -= total
            add_log(f"🏹 <b>{p['skill']}!</b> {hits}연속! → 총 <b>{total}</b> 데미지!", "skill")

        elif stype == "heal_atk":
            heal = int(p["max_hp"] * 0.35)
            p["hp"] = min(p["max_hp"], p["hp"] + heal)
            dmg = calc_damage(int(p["atk"] * p["skill_mult"]), m["def"])
            st.session_state.monster_hp -= dmg
            add_log(f"✨ <b>{p['skill']}!</b> HP+{heal} & {dmg} 데미지!", "skill")

        if st.session_state.monster_hp > 0:
            if process_burn():
                battle_victory()
                st.rerun()
            else:
                enemy_turn()
        else:
            battle_victory()
        st.rerun()

    # ── HP 포션 ──
    if btn_pot:
        st.session_state.turn += 1
        used = potions[0]
        st.session_state.inventory.remove(used)
        heal = SHOP_ITEMS[used]["heal"]
        old = p["hp"]
        p["hp"] = min(p["max_hp"], p["hp"] + heal)
        actual = p["hp"] - old
        add_log(f"🧪 {used} 사용! HP +<b>{actual}</b> 회복", "heal")
        st.session_state.last_action = ""
        enemy_turn()
        st.rerun()

    # ── 도망 ──
    if btn_flee and not is_boss:
        chance = 45 + p["spd"] * 2
        if random.randint(1, 100) <= chance:
            add_log("🏃 도망에 성공!", "info")
            st.session_state.scene = "town"
            st.session_state.burn_turns = 0
        else:
            add_log("🏃 도망 실패!", "dmg")
            st.session_state.last_action = ""
            enemy_turn()
        st.rerun()

    # ── 전투 로그 ──
    if st.session_state.battle_log:
        st.markdown("#### 📜 전투 로그")
        log_html = "<br>".join(reversed(st.session_state.battle_log))
        st.markdown(f'<div class="log-box">{log_html}</div>', unsafe_allow_html=True)


# ============================================
#  씬: 전투 결과
# ============================================

def scene_battle_result():
    p = st.session_state.player
    m = st.session_state.current_monster

    st.markdown(f"""
    <div class="box-green fade-in">
        <div style="font-size:2.5em;">🏆</div>
        <div style="font-size:1.3em; font-weight:bold; color:#ffd700; margin:8px 0;">
            승리!
        </div>
        <div style="color:#aaa;">
            {m['emoji']} {m['name']} 처치
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 최근 로그
    if st.session_state.battle_log:
        recent = [l for l in st.session_state.battle_log[-6:]]
        log_html = "<br>".join(recent)
        st.markdown(f'<div class="log-box">{log_html}</div>', unsafe_allow_html=True)

    # 현재 상태
    st.markdown(f"""
    <div class="box" style="font-size:0.85em; color:#999;">
        ❤️ HP {p['hp']}/{p['max_hp']} · ✨ SP {st.session_state.sp}/{st.session_state.max_sp}
        · 📊 EXP {p['exp']}/{exp_needed(p['level'])} · 💰 {p['gold']}G
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚔️ 계속 탐험", use_container_width=True, type="primary"):
            st.session_state.battle_log = []
            st.session_state.scene = "area_select"
            st.rerun()
    with col2:
        if st.button("🏘️ 마을로", use_container_width=True):
            st.session_state.battle_log = []
            st.session_state.scene = "town"
            st.rerun()


# ============================================
#  씬: 게임 오버
# ============================================

def scene_game_over():
    p = st.session_state.player

    st.markdown(f"""
    <div class="box-red fade-in" style="padding:30px;">
        <div style="font-size:3.5em;">💀</div>
        <div style="font-size:1.8em; font-weight:bold; color:#ff4444; margin:10px 0;">
            패배...
        </div>
        <div style="color:#888; font-size:0.9em;">
            {p['emoji']} {p['name']} Lv.{p['level']}<br>
            처치 수: {st.session_state.kill_count}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏘️ 마을 부활 (골드 절반 잃음)", use_container_width=True):
            p["hp"] = p["max_hp"] // 2
            p["gold"] = p["gold"] // 2
            st.session_state.sp = 0
            st.session_state.burn_turns = 0
            st.session_state.battle_log = []
            st.session_state.scene = "town"
            st.rerun()
    with col2:
        if st.button("🔄 처음부터", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()


# ============================================
#  씬: 엔딩
# ============================================

def scene_victory():
    p = st.session_state.player

    st.balloons()

    st.markdown(f"""
    <div class="box fade-in" style="text-align:center; padding:30px; border-color:#ffd70044;">
        <div style="font-size:4em;">👑</div>
        <div class="victory-text">
            드래곤 슬레이어!
        </div>
        <div style="color:#aaa; margin:15px 0; font-size:0.95em;">
            <em>고대 드래곤 이그니스가 쓰러졌다.<br>
            왕국에 다시 평화가 찾아왔다...</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="box" style="text-align:center;">
        <div style="font-size:1.2em; color:#ffd700; margin-bottom:15px;">
            🏆 최종 기록 🏆
        </div>
        <div style="display:flex; justify-content:space-around; margin:15px 0;">
            <div>
                <div style="font-size:1.8em; color:#ffd700;">Lv.{p['level']}</div>
                <div style="font-size:0.75em; color:#667;">최종 레벨</div>
            </div>
            <div>
                <div style="font-size:1.8em; color:#ff6666;">💀 {st.session_state.kill_count}</div>
                <div style="font-size:0.75em; color:#667;">총 처치</div>
            </div>
            <div>
                <div style="font-size:1.8em; color:#ffaa00;">💰 {p['gold']}</div>
                <div style="font-size:0.75em; color:#667;">보유 골드</div>
            </div>
        </div>
        <div style="color:#556; margin-top:10px; font-size:0.85em;">
            {p['emoji']} {p['name']} · {p['job']}<br>
            ⚔️{p['atk']} 🛡️{p['def']} ❤️{p['max_hp']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    if st.button("🔄 새 게임", use_container_width=True, type="primary"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ============================================
#  메인 라우터
# ============================================

SCENES = {
    "intro": scene_intro,
    "create": scene_create,
    "town": scene_town,
    "shop": scene_shop,
    "area_select": scene_area_select,
    "battle": scene_battle,
    "battle_result": scene_battle_result,
    "game_over": scene_game_over,
    "victory": scene_victory,
}

current = st.session_state.scene
if current in SCENES:
    SCENES[current]()
else:
    st.session_state.scene = "intro"
    st.rerun()
