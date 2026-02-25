import json
import random
import streamlit as st

st.set_page_config(page_title="例文ランダム表示", page_icon="🎲")
st.markdown("### 🎲 例文ランダムテスト（10問）")

# ===== JSON読み込み =====
with open("data.json", encoding="utf-8") as f:
    RAW = json.load(f)

# ===== データ整形 =====
DATA = []
for item in RAW:
    try:
        no = int(str(item.get("番号", "")).strip())
        ex = str(item.get("例文", "")).strip()
        jp = str(item.get("日本語訳", "")).strip()  # 日本語訳が無ければ空
        if ex:
            DATA.append({"番号": no, "例文": ex, "日本語訳": jp})
    except:
        pass

if not DATA:
    st.error("data.json に有効なデータがありません（番号/例文を確認してね）")
    st.stop()

min_no = min(d["番号"] for d in DATA)
max_no = max(d["番号"] for d in DATA)

# ===== state =====
if "wrong_list" not in st.session_state:
    st.session_state.wrong_list = []
if "review_mode" not in st.session_state:
    st.session_state.review_mode = False
if "show_jp" not in st.session_state:
    st.session_state.show_jp = False
if "test_set" not in st.session_state:
    st.session_state.test_set = None
if "index" not in st.session_state:
    st.session_state.index = 0

# ===== サイドバー：範囲指定 =====
st.sidebar.markdown("## 範囲指定")
start_no = st.sidebar.number_input("開始番号", min_value=min_no, max_value=max_no, value=min_no, step=1)
end_no = st.sidebar.number_input("終了番号", min_value=min_no, max_value=max_no, value=min(max_no, start_no + 99), step=1)

if start_no > end_no:
    st.sidebar.error("開始番号は終了番号以下にしてね")
    st.stop()

def get_pool():
    return [d for d in DATA if start_no <= d["番号"] <= end_no]

# ===== テスト生成 =====
def new_test():
    pool = get_pool()
    if len(pool) == 0:
        st.warning("その範囲にデータがありません")
        return
    k = min(10, len(pool))
    st.session_state.test_set = random.sample(pool, k)
    st.session_state.index = 0
    st.session_state.review_mode = False
    st.session_state.show_jp = False

def review_wrong():
    # 復習は「範囲に関係なく×だけ」でもいいし、「範囲内の×だけ」でもいい
    # ここでは「範囲内の×だけ」にしておく（要望あれば切り替える）
    pool = get_pool()
    pool_set = {(d["番号"], d["例文"]) for d in pool}

    wrong_in_range = [w for w in st.session_state.wrong_list if (w["番号"], w["例文"]) in pool_set]

    if len(wrong_in_range) == 0:
        st.warning("この範囲には×がありません（範囲を広げるか、まず解いてね）")
        return
    st.session_state.test_set = wrong_in_range.copy()
    st.session_state.index = 0
    st.session_state.review_mode = True
    st.session_state.show_jp = False

# ===== ボタン =====
col1, col2 = st.columns(2)

with col1:
    if st.button("🎯 新しく10問", use_container_width=True):
        new_test()

with col2:
    if st.button("📚 ×だけ復習", use_container_width=True):
        review_wrong()

if not st.session_state.test_set:
    st.info("左の範囲を決めて「新しく10問」を押してね")
    st.stop()

# ===== 現在の問題 =====
current = st.session_state.test_set[st.session_state.index]

st.markdown(f"""
### Q{st.session_state.index + 1}

**[{current['番号']}]**  
{current['例文']}
""")

# ===== 日本語訳（タップで表示/非表示） =====
if st.button("🈶 日本語訳を表示 / 非表示", use_container_width=True):
    st.session_state.show_jp = not st.session_state.show_jp

if st.session_state.show_jp:
    jp = current.get("日本語訳", "").strip()
    if jp:
        st.info(jp)
    else:
        st.warning("この問題には日本語訳が入っていません")

# ===== ○ × ボタン =====
colA, colB = st.columns(2)

with colA:
    if st.button("⭕ 正解", use_container_width=True):
        st.session_state.index += 1
        st.session_state.show_jp = False

with colB:
    if st.button("❌ 不正解", use_container_width=True):
        if current not in st.session_state.wrong_list:
            st.session_state.wrong_list.append(current)
        st.session_state.index += 1
        st.session_state.show_jp = False

# ===== 終了 =====
if st.session_state.index >= len(st.session_state.test_set):
    st.success("🎉 終了！")
    st.write(f"❌ 記録された問題数（累計）: {len(st.session_state.wrong_list)}")
    st.stop()