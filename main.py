import streamlit as st
import random

# ============================================
#  🏰 중세 판타지 RPG - 드래곤을 처치하라!
# ============================================

# ── 페이지 설정 ──
st.set_page_config(
    page_title="🏰 드래곤 슬레이어",
    page_icon="⚔️",
    layout="centered"
)

# ── CSS 스타일 ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');

    .stApp {
        background: linear-gradient(180deg, #0a0a1a 0%, #1a0a2e 100%);
        color: #ddd;
    }

    .game-title {
        text-align: center;
        padding: 20px 0;
    }
    .game-title h1 {
        font-size: 2.5em;
        background: linear-gradient(90deg, #ffd700, #ff8c00, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    .game-title p {
        color: #666;
        font-size: 0.9em;
    }

    .status-box {
        background: linear-gradient(135deg, #1a1a3e, #2a1a4e);
        border: 1px solid #3a2a6e;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
    }

    .hp-bar-bg {
        background: #1a0a0a;
        border-radius: 10px;
        height: 25px;
        overflow: hidden;
        border: 1px solid #333;
    }
    .hp-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8em;
        font-weight: bold;
        color: white;
        text-shadow: 1px 1px 2px black;
    }

    .monster-card {
        background: linear-gradient(135deg, #2a0a0a, #3a1a1a);
        border: 1px solid #5a2a2a;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }

    .battle-log {
        background: #0a0a1a;
        border: 1px solid #2a2a4e;
        border-radius: 10px;
        padding: 15px;
        max-height: 200px;
        overflow-y: auto;
        font-family: monospace;
        font-size: 0.85em;
    }

    .victory {
        text-align: center;
        font-size: 1.5em;
        color: #ffd700;
        padding: 20px;
        animation: glow 1s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 5px #ffd700; }
        to { text-shadow: 0 0 20px #ffd700, 0 0 40px #ff8c00; }
    }

    .defeat {
        text-align: center;
        font-size: 1.5em;
        color: #ff4444;
        padding: 20px;
    }

    .loot-box {
        background: linear-gradient(135deg, #1a2a1a, #1a3a2a);
        border: 1px solid #2a5a3a;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        color: #aaa !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
#  게임 데이터 정의
# ============================================

# 직업 데이터
JOBS = {
    "⚔️ 전사": {
        "emoji": "⚔️",
        "hp": 120, "max_hp": 120,
        "atk": 15, "def": 10, "spd": 5,
        "skill": "파워 슬래시",
        "skill_desc": "공격력 2배의 강력한 일격",
        "skill_mult": 2.0,
    },
    "🧙 마법사": {
        "emoji": "🧙",
        "hp": 80, "max_hp": 80,
        "atk": 22, "def": 4, "spd": 8,
        "skill": "파이어볼",
        "skill_desc": "공격력 2.5배 마법 공격",
        "skill_mult": 2.5,
    },
    "🏹 궁수": {
        "emoji": "🏹",
        "hp": 90, "max_hp": 90,
        "atk": 18, "def": 6, "spd": 14,
        "skill": "속사",
        "skill_desc": "2~4회 연속 공격",
        "skill_mult": 1.0,  # 특수 처리
    },
    "🛡️ 성기사": {
        "emoji": "🛡️",
        "hp": 150, "max_hp": 150,
        "atk": 10, "def": 15, "spd": 3,
        "skill": "성스러운 빛",
        "skill_desc": "HP 30% 회복 + 공격",
        "skill_mult": 1.5,
    },
}

# 몬스터 데이터 (지역별)
AREAS = {
    "🌲 수풀 숲": {
        "level_req": 1,
        "monsters": [
            {"name": "슬라임", "emoji": "🟢", "hp": 30, "atk": 5, "def": 2, "exp": 15, "gold": 5},
            {"name": "고블린", "emoji": "👺", "hp": 45, "atk": 8, "def": 3, "exp": 25, "gold": 10},
            {"name": "늑대", "emoji": "🐺", "hp": 40, "atk": 10, "def": 2, "exp": 20, "gold": 8},
        ]
    },
    "🏔️ 바위 산": {
        "level_req": 3,
        "monsters": [
            {"name": "오크", "emoji": "👹", "hp": 80, "atk": 14, "def": 8, "exp": 50, "gold": 25},
            {"name": "하피", "emoji": "🦅", "hp": 60, "atk": 18, "def": 4, "exp": 45, "gold": 20},
            {"name": "골렘", "emoji": "🗿", "hp": 120, "atk": 10, "def": 15, "exp": 60, "gold": 30},
        ]
    },
    "🌋 화염 동굴": {
        "level_req": 5,
        "monsters": [
            {"name": "화염 정령", "emoji": "🔥", "hp": 100, "atk": 22, "def": 8, "exp": 80, "gold": 40},
            {"name": "다크나이트", "emoji": "🖤", "hp": 140, "atk": 20, "def": 14, "exp": 100, "gold": 55},
            {"name": "서큐버스", "emoji": "😈", "hp": 90, "atk": 28, "def": 6, "exp": 90, "gold": 50},
        ]
    },
    "🐉 드래곤 둥지": {
        "level_req": 8,
        "monsters": [
            {"name": "와이번", "emoji": "🦎", "hp": 180, "atk": 25, "def": 12, "exp": 150, "gold": 80},
            {"name": "드래곤 가드", "emoji": "🐲", "hp": 220, "atk": 30, "def": 16, "exp": 200, "gold": 100},
        ]
    }
}

# 최종 보스
DRAGON_BOSS = {
    "name": "🐉 고대 드래곤 이그니스",
    "emoji": "🐉",
    "hp": 500,
    "atk": 40,
    "def": 20,
    "exp": 0,
    "gold": 999,
}

# 상점 아이템 (2단계)
SHOP_ITEMS = {
    "🧪 HP 포션 (소)": {"type": "potion", "heal": 30, "price": 15, "desc": "HP 30 회복"},
    "🧪 HP 포션 (대)": {"type": "potion", "heal": 80, "price": 40, "desc": "HP 80 회복"},
    "⚔️ 강화석": {"type": "atk_boost", "value": 3, "price": 50, "desc": "공격력 +3 (영구)"},
    "🛡️ 방어 부적": {"type": "def_boost", "value": 3, "price": 50, "desc": "방어력 +3 (영구)"},
    "💎 생명의 반지": {"type": "hp_boost", "value": 20, "price": 60, "desc": "최대 HP +20 (영구)"},
}

# 레벨업 경험치 테이블
def exp_needed(level):
    return level * 40

# ============================================
#  세션 상태 초기화
# ============================================

def init_session():
    defaults = {
        "scene": "intro",          # intro, create, town, area_select, battle, boss_battle, victory, game_over
        "player": None,
        "battle_log": [],
        "current_monster": None,
        "monster_hp": 0,
        "turn": 0,
        "inventory": [],
        "kill_count": 0,
        "boss_defeated": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# ============================================
#  유틸리티 함수
# ============================================

def hp_bar(current, maximum, color="#00cc44"):
    """HP 바 HTML 생성"""
    pct = max(0, min(100, (current / maximum) * 100))
    if pct > 50:
        bar_color = "#00cc44"
    elif pct > 25:
        bar_color = "#ffaa00"
    else:
        bar_color = "#ff3333"
    return f"""
    <div class="hp-bar-bg">
        <div class="hp-bar-fill" style="width:{pct}%; background:linear-gradient(90deg, {bar_color}, {bar_color}88);">
            {current}/{maximum}
        </div>
    </div>
    """

def add_log(msg):
    st.session_state.battle_log.append(msg)
    if len(st.session_state.battle_log) > 20:
        st.session_state.battle_log.pop(0)

def check_level_up():
    """레벨업 체크 및 처리"""
    p = st.session_state.player
    messages = []
    while p["exp"] >= exp_needed(p["level"]):
        p["exp"] -= exp_needed(p["level"])
        p["level"] += 1
        # 스탯 증가
        p["max_hp"] += 10
        p["hp"] = p["max_hp"]  # 레벨업 시 풀회복
        p["atk"] += 2
        p["def"] += 1
        p["spd"] += 1
        messages.append(f"🎉 레벨 {p['level']} 달성! 스탯이 올랐습니다!")
    return messages

def calc_damage(attacker_atk, defender_def):
    """데미지 계산 (랜덤 요소 포함)"""
    base = max(1, attacker_atk - defender_def // 2)
    variation = random.randint(-2, 4)
    return max(1, base + variation)

# ============================================
#  화면 렌더링 함수들
# ============================================

# ── 인트로 화면 ──
def scene_intro():
    st.markdown("""
    <div class="game-title">
        <h1>🏰 드래곤 슬레이어</h1>
        <p>고대 드래곤 이그니스를 처치하라!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        > *오랜 세월 왕국을 공포에 떨게 한 고대 드래곤 이그니스...*
        > *왕은 용감한 모험가를 찾고 있다.*
        > *당신이 그 영웅이 될 수 있을 것인가?*
        """)

        st.markdown("")

        if st.button("⚔️ 모험 시작", use_container_width=True, type="primary"):
            st.session_state.scene = "create"
            st.rerun()

        st.markdown("")
        st.markdown("""
        <div style='text-align:center; color:#555; font-size:0.8em;'>
            🎮 턴제 RPG | 📈 레벨업 & 성장 | 🛒 상점 | 🐉 보스전
        </div>
        """, unsafe_allow_html=True)


# ── 캐릭터 생성 ──
def scene_create():
    st.markdown("""
    <div class="game-title">
        <h1>👤 캐릭터 생성</h1>
        <p>당신의 영웅을 만드세요</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    name = st.text_input("🏷️ 영웅의 이름", placeholder="이름을 입력하세요")

    st.markdown("### 직업 선택")

    # 직업 정보 표시
    cols = st.columns(2)
    for i, (job_name, job_data) in enumerate(JOBS.items()):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="status-box">
                <div style="font-size:2em; text-align:center;">{job_data['emoji']}</div>
                <div style="text-align:center; font-weight:bold; font-size:1.1em; color:#ffd700;">{job_name}</div>
                <div style="font-size:0.85em; margin-top:8px; color:#aaa;">
                    ❤️ HP: {job_data['hp']} &nbsp;
                    ⚔️ 공격: {job_data['atk']} &nbsp;
                    🛡️ 방어: {job_data['def']} &nbsp;
                    💨 속도: {job_data['spd']}<br>
                    ✨ 스킬: {job_data['skill']}<br>
                    <span style="color:#888;">{job_data['skill_desc']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    job = st.selectbox("직업을 선택하세요", list(JOBS.keys()))

    st.markdown("")
    if st.button("🎮 게임 시작!", use_container_width=True, type="primary"):
        if not name.strip():
            st.warning("이름을 입력해주세요!")
        else:
            job_data = JOBS[job].copy()
            st.session_state.player = {
                "name": name.strip(),
                "job": job,
                "emoji": job_data["emoji"],
                "level": 1,
                "exp": 0,
                "hp": job_data["hp"],
                "max_hp": job_data["max_hp"],
                "atk": job_data["atk"],
                "def": job_data["def"],
                "spd": job_data["spd"],
                "gold": 30,
                "skill": job_data["skill"],
                "skill_desc": job_data["skill_desc"],
                "skill_mult": job_data["skill_mult"],
            }
            st.session_state.inventory = ["🧪 HP 포션 (소)"] * 3
            st.session_state.scene = "town"
            st.rerun()


# ── 마을 화면 ──
def scene_town():
    p = st.session_state.player

    st.markdown("""
    <div class="game-title">
        <h1>🏘️ 평화로운 마을</h1>
        <p>모험을 준비하세요</p>
    </div>
    """, unsafe_allow_html=True)

    # 캐릭터 상태
    st.markdown(f"""
    <div class="status-box">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div>
                <span style="font-size:1.5em;">{p['emoji']}</span>
                <strong style="color:#ffd700; font-size:1.2em;"> {p['name']}</strong>
                <span style="color:#888;"> {p['job']}</span>
            </div>
            <div style="color:#aaa;">
                Lv.{p['level']} &nbsp; 💰 {p['gold']}G
            </div>
        </div>
        {hp_bar(p['hp'], p['max_hp'])}
        <div style="display:flex; justify-content:space-around; margin-top:12px; font-size:0.85em; color:#aaa;">
            <span>⚔️ 공격 {p['atk']}</span>
            <span>🛡️ 방어 {p['def']}</span>
            <span>💨 속도 {p['spd']}</span>
            <span>📊 EXP {p['exp']}/{exp_needed(p['level'])}</span>
        </div>
        <div style="margin-top:8px; font-size:0.8em; color:#666;">
            🎒 인벤토리: {len(st.session_state.inventory)}개 &nbsp;|&nbsp;
            💀 처치 수: {st.session_state.kill_count}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

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
        if st.button("💤 휴식 (풀회복)", use_container_width=True):
            p["hp"] = p["max_hp"]
            st.success("💤 편안한 휴식... HP가 완전히 회복되었습니다!")
            st.rerun()

    # 보스전 버튼 (레벨 8 이상)
    st.markdown("---")
    if p["level"] >= 8:
        st.markdown("""
        <div style="text-align:center; color:#ff4444; font-size:0.9em; margin-bottom:10px;">
            🐉 드래곤 둥지에서 강대한 기운이 느껴진다...
        </div>
        """, unsafe_allow_html=True)
        if st.button("🐉 최종 보스: 고대 드래곤에게 도전!", use_container_width=True, type="primary"):
            st.session_state.current_monster = DRAGON_BOSS.copy()
            st.session_state.monster_hp = DRAGON_BOSS["hp"]
            st.session_state.battle_log = ["🐉 고대 드래곤 이그니스가 포효한다!"]
            st.session_state.turn = 0
            st.session_state.scene = "battle"
            st.rerun()
    else:
        st.markdown(f"""
        <div style="text-align:center; color:#555; font-size:0.85em;">
            🔒 드래곤에게 도전하려면 Lv.8 이상이 필요합니다 (현재 Lv.{p['level']})
        </div>
        """, unsafe_allow_html=True)

    # 인벤토리
    if st.session_state.inventory:
        with st.expander("🎒 인벤토리"):
            items_count = {}
            for item in st.session_state.inventory:
                items_count[item] = items_count.get(item, 0) + 1
            for item_name, count in items_count.items():
                st.write(f"{item_name} x{count}")


# ── 상점 ──
def scene_shop():
    p = st.session_state.player

    st.markdown("""
    <div class="game-title">
        <h1>🛒 마을 상점</h1>
        <p>장비와 물약을 구매하세요</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**💰 보유 골드: {p['gold']}G**")
    st.markdown("---")

    for item_name, item_data in SHOP_ITEMS.items():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{item_name}** — {item_data['desc']}")
        with col2:
            st.markdown(f"💰 {item_data['price']}G")
        with col3:
            if st.button("구매", key=f"buy_{item_name}"):
                if p["gold"] >= item_data["price"]:
                    p["gold"] -= item_data["price"]

                    if item_data["type"] == "potion":
                        st.session_state.inventory.append(item_name)
                        st.success(f"{item_name} 구매 완료! 인벤토리에 추가됨")
                    elif item_data["type"] == "atk_boost":
                        p["atk"] += item_data["value"]
                        st.success(f"⚔️ 공격력 +{item_data['value']}! (현재: {p['atk']})")
                    elif item_data["type"] == "def_boost":
                        p["def"] += item_data["value"]
                        st.success(f"🛡️ 방어력 +{item_data['value']}! (현재: {p['def']})")
                    elif item_data["type"] == "hp_boost":
                        p["max_hp"] += item_data["value"]
                        p["hp"] += item_data["value"]
                        st.success(f"❤️ 최대 HP +{item_data['value']}! (현재: {p['max_hp']})")
                    st.rerun()
                else:
                    st.error("골드가 부족합니다!")

    st.markdown("---")
    if st.button("🏘️ 마을로 돌아가기", use_container_width=True):
        st.session_state.scene = "town"
        st.rerun()


# ── 지역 선택 ──
def scene_area_select():
    p = st.session_state.player

    st.markdown("""
    <div class="game-title">
        <h1>🗺️ 던전 선택</h1>
        <p>어디로 모험을 떠날까요?</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    for area_name, area_data in AREAS.items():
        locked = p["level"] < area_data["level_req"]
        monster_names = ", ".join([m["emoji"] + m["name"] for m in area_data["monsters"]])

        if locked:
            st.markdown(f"""
            <div class="status-box" style="opacity:0.4;">
                <strong>{area_name}</strong> 🔒 Lv.{area_data['level_req']} 필요<br>
                <span style="font-size:0.8em; color:#555;">{monster_names}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="status-box">
                <strong style="color:#ffd700;">{area_name}</strong>
                <span style="color:#888;"> (권장 Lv.{area_data['level_req']}+)</span><br>
                <span style="font-size:0.85em; color:#aaa;">출현: {monster_names}</span>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"{area_name} 탐험!", key=f"area_{area_name}", use_container_width=True):
                # 랜덤 몬스터 선택
                monster = random.choice(area_data["monsters"]).copy()
                st.session_state.current_monster = monster
                st.session_state.monster_hp = monster["hp"]
                st.session_state.battle_log = [f"{monster['emoji']} {monster['name']}이(가) 나타났다!"]
                st.session_state.turn = 0
                st.session_state.scene = "battle"
                st.rerun()

    st.markdown("---")
    if st.button("🏘️ 마을로 돌아가기", use_container_width=True):
        st.session_state.scene = "town"
        st.rerun()


# ── 전투 화면 ──
def scene_battle():
    p = st.session_state.player
    m = st.session_state.current_monster
    m_hp = st.session_state.monster_hp

    is_boss = m["name"] == "🐉 고대 드래곤 이그니스" or "드래곤 이그니스" in m.get("name", "")

    # 제목
    if is_boss:
        st.markdown("""
        <div class="game-title">
            <h1>🐉 최종 보스전!</h1>
            <p>고대 드래곤 이그니스</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="game-title">
            <h1>⚔️ 전투!</h1>
            <p>Turn {st.session_state.turn}</p>
        </div>
        """, unsafe_allow_html=True)

    # 몬스터 정보
    st.markdown(f"""
    <div class="monster-card">
        <div style="font-size:3em;">{m['emoji']}</div>
        <div style="font-size:1.3em; font-weight:bold; color:#ff6666; margin:8px 0;">{m['name']}</div>
        <div style="font-size:0.85em; color:#888; margin-bottom:8px;">
            ⚔️ {m['atk']} &nbsp; 🛡️ {m['def']}
        </div>
        {hp_bar(m_hp, m['hp'], '#ff3333')}
    </div>
    """, unsafe_allow_html=True)

    # 플레이어 상태
    st.markdown(f"""
    <div class="status-box">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span>{p['emoji']} <strong>{p['name']}</strong> Lv.{p['level']}</span>
            <span style="color:#888;">⚔️{p['atk']} 🛡️{p['def']}</span>
        </div>
        <div style="margin-top:8px;">
            {hp_bar(p['hp'], p['max_hp'])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 행동 선택
    st.markdown("### 🎯 행동 선택")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        btn_attack = st.button("⚔️ 공격", use_container_width=True)
    with col2:
        btn_skill = st.button(f"✨ {p['skill']}", use_container_width=True)
    with col3:
        # 포션 개수 확인
        potions = [i for i in st.session_state.inventory if "포션" in i]
        btn_potion = st.button(f"🧪 포션 ({len(potions)})", use_container_width=True)
    with col4:
        btn_flee = st.button("🏃 도망", use_container_width=True)

    # ── 공격 처리 ──
    if btn_attack:
        st.session_state.turn += 1
        dmg = calc_damage(p["atk"], m["def"])
        st.session_state.monster_hp -= dmg
        add_log(f"⚔️ {p['name']}의 공격! → {dmg} 데미지")

        if st.session_state.monster_hp <= 0:
            battle_victory()
            st.rerun()
        else:
            enemy_turn()
            st.rerun()

    # ── 스킬 처리 ──
    if btn_skill:
        st.session_state.turn += 1

        if p["job"] == "🏹 궁수":
            # 궁수: 2~4회 연속공격
            hits = random.randint(2, 4)
            total = 0
            for i in range(hits):
                dmg = calc_damage(p["atk"], m["def"])
                total += dmg
            st.session_state.monster_hp -= total
            add_log(f"🏹 {p['skill']}! {hits}연속! → 총 {total} 데미지")

        elif p["job"] == "🛡️ 성기사":
            # 성기사: 회복 + 공격
            heal = int(p["max_hp"] * 0.3)
            p["hp"] = min(p["max_hp"], p["hp"] + heal)
            dmg = calc_damage(int(p["atk"] * p["skill_mult"]), m["def"])
            st.session_state.monster_hp -= dmg
            add_log(f"✨ {p['skill']}! HP +{heal} 회복 & {dmg} 데미지")

        else:
            # 전사, 마법사: 배율 공격
            dmg = calc_damage(int(p["atk"] * p["skill_mult"]), m["def"])
            st.session_state.monster_hp -= dmg
            add_log(f"✨ {p['skill']}! → {dmg} 데미지!")

        if st.session_state.monster_hp <= 0:
            battle_victory()
            st.rerun()
        else:
            enemy_turn()
            st.rerun()

    # ── 포션 사용 ──
    if btn_potion:
        if not potions:
            add_log("❌ 포션이 없습니다!")
            st.rerun()
        else:
            # 가장 작은 포션부터 사용
            used = potions[0]
            st.session_state.inventory.remove(used)
            item_data = SHOP_ITEMS[used]
            heal = item_data["heal"]
            old_hp = p["hp"]
            p["hp"] = min(p["max_hp"], p["hp"] + heal)
            actual_heal = p["hp"] - old_hp
            add_log(f"🧪 {used} 사용! HP +{actual_heal} 회복")

            enemy_turn()
            st.rerun()

    # ── 도망 ──
    if btn_flee:
        if is_boss:
            add_log("🐉 드래곤에게서는 도망칠 수 없다!")
            enemy_turn()
            st.rerun()
        else:
            flee_chance = 50 + p["spd"] * 3
            if random.randint(1, 100) <= flee_chance:
                add_log("🏃 도망에 성공했다!")
                st.session_state.scene = "town"
                st.rerun()
            else:
                add_log("🏃 도망에 실패했다!")
                enemy_turn()
                st.rerun()

    # ── 전투 로그 표시 ──
    if st.session_state.battle_log:
        st.markdown("### 📜 전투 로그")
        log_text = ""
        for log in reversed(st.session_state.battle_log):
            log_text += log + "\n"
        st.markdown(f"""
        <div class="battle-log">{log_text}</div>
        """, unsafe_allow_html=True)


# ── 적 턴 처리 ──
def enemy_turn():
    p = st.session_state.player
    m = st.session_state.current_monster
    m_hp = st.session_state.monster_hp

    # 크리티컬 확률 10%
    is_crit = random.randint(1, 100) <= 10
    dmg = calc_damage(m["atk"], p["def"])
    if is_crit:
        dmg = int(dmg * 1.8)
        add_log(f"💥 {m['name']}의 크리티컬! → {dmg} 데미지!")
    else:
        add_log(f"👹 {m['name']}의 공격! → {dmg} 데미지")

    p["hp"] -= dmg

    if p["hp"] <= 0:
        p["hp"] = 0
        add_log("💀 쓰러졌다...")
        st.session_state.scene = "game_over"


# ── 전투 승리 처리 ──
def battle_victory():
    p = st.session_state.player
    m = st.session_state.current_monster
    st.session_state.monster_hp = 0

    is_boss = "이그니스" in m.get("name", "")

    if is_boss:
        st.session_state.boss_defeated = True
        st.session_state.scene = "victory"
        return

    # 경험치 & 골드
    exp_gain = m.get("exp", 0)
    gold_gain = m.get("gold", 0)
    # 랜덤 보너스
    gold_gain += random.randint(0, gold_gain // 2)

    p["exp"] += exp_gain
    p["gold"] += gold_gain
    st.session_state.kill_count += 1

    add_log(f"🎉 {m['name']}을(를) 처치! +{exp_gain}EXP +{gold_gain}G")

    # 레벨업 체크
    lvl_msgs = check_level_up()
    for msg in lvl_msgs:
        add_log(msg)

    # 드랍 아이템 (20% 확률)
    if random.randint(1, 100) <= 20:
        drop = random.choice(["🧪 HP 포션 (소)", "🧪 HP 포션 (대)"])
        st.session_state.inventory.append(drop)
        add_log(f"📦 {drop} 을(를) 발견!")

    st.session_state.scene = "battle_result"


# ── 전투 결과 화면 ──
def scene_battle_result():
    p = st.session_state.player
    m = st.session_state.current_monster

    st.markdown(f"""
    <div class="loot-box">
        <div style="font-size:2em;">🏆</div>
        <div style="font-size:1.3em; font-weight:bold; color:#ffd700; margin:10px 0;">
            승리!
        </div>
        <div style="color:#aaa;">
            {m['emoji']} {m['name']} 처치
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 최근 로그 표시
    if st.session_state.battle_log:
        for log in st.session_state.battle_log[-5:]:
            st.markdown(f"- {log}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚔️ 계속 탐험", use_container_width=True, type="primary"):
            st.session_state.scene = "area_select"
            st.rerun()
    with col2:
        if st.button("🏘️ 마을로", use_container_width=True):
            st.session_state.scene = "town"
            st.rerun()


# ── 게임 오버 ──
def scene_game_over():
    p = st.session_state.player

    st.markdown(f"""
    <div class="defeat">
        <div style="font-size:3em;">💀</div>
        <div>패배...</div>
        <div style="font-size:0.6em; color:#888; margin-top:10px;">
            {p['name']} Lv.{p['level']} | 처치 수: {st.session_state.kill_count}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏘️ 마을에서 부활 (골드 절반 잃음)", use_container_width=True):
            p["hp"] = p["max_hp"]
            p["gold"] = p["gold"] // 2
            st.session_state.scene = "town"
            st.rerun()
    with col2:
        if st.button("🔄 처음부터 다시", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ── 엔딩 (드래곤 처치) ──
def scene_victory():
    p = st.session_state.player

    st.markdown(f"""
    <div class="victory">
        <div style="font-size:4em;">👑</div>
        <div>🐉 고대 드래곤 이그니스를 처치했다!</div>
    </div>
    """, unsafe_allow_html=True)

    st.balloons()

    st.markdown(f"""
    <div class="status-box" style="text-align:center;">
        <div style="font-size:1.5em; color:#ffd700; margin-bottom:15px;">
            🏆 전설의 영웅 🏆
        </div>
        <div style="font-size:1.1em; color:#ddd; margin-bottom:20px;">
            {p['emoji']} <strong>{p['name']}</strong>
        </div>
        <div style="display:flex; justify-content:space-around; color:#aaa;">
            <div>
                <div style="font-size:1.5em; color:#ffd700;">Lv.{p['level']}</div>
                <div style="font-size:0.8em;">최종 레벨</div>
            </div>
            <div>
                <div style="font-size:1.5em; color:#ff6666;">💀 {st.session_state.kill_count}</div>
                <div style="font-size:0.8em;">처치 수</div>
            </div>
            <div>
                <div style="font-size:1.5em; color:#ffaa00;">💰 {p['gold']}</div>
                <div style="font-size:0.8em;">보유 골드</div>
            </div>
        </div>
        <div style="margin-top:20px; color:#888; font-size:0.9em;">
            <em>"왕국에 다시 평화가 찾아왔다..."</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🔄 새 게임 시작", use_container_width=True, type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ============================================
#  메인 라우터
# ============================================

scene = st.session_state.scene

if scene == "intro":
    scene_intro()
elif scene == "create":
    scene_create()
elif scene == "town":
    scene_town()
elif scene == "shop":
    scene_shop()
elif scene == "area_select":
    scene_area_select()
elif scene == "battle":
    scene_battle()
elif scene == "battle_result":
    scene_battle_result()
elif scene == "game_over":
    scene_game_over()
elif scene == "victory":
    scene_victory()
