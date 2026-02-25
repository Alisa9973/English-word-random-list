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
        jp = str(item.get("日本語訳", "")).strip()  # ★追加
        if ex:
            DATA.append({"番号": no, "例文": ex, "日本語訳": jp})  # ★追加
    except:
        pass

# ===== state =====
if "wrong_list" not in st.session_state:
    st.session_state.wrong_list = []

if "review_mode" not in st.session_state:
    st.session_state.review_mode = False

if "show_jp" not in st.session_state:
    st.session_state.show_jp = False

# ===== テスト生成 =====
def new_test():
    st.session_state.test_set = random.sample(DATA, 10)
    st.session_state.index = 0
    st.session_state.review_mode = False
    st.session_state.show_jp = False

def review_wrong():
    if len(st.session_state.wrong_list) == 0:
        st.warning("まだ×はありません")
        return
    st.session_state.test_set = st.session_state.wrong_list.copy()
    st.session_state.index = 0
    st.session_state.review_mode = True
    st.session_state.show_jp = False

# ===== ボタン =====
col1, col2 = st.columns(2)

with col1:
    if st.button("🎯 新しく10問"):
        new_test()

with col2:
    if st.button("📚 ×だけ復習"):
        review_wrong()

if "test_set" not in st.session_state:
    st.stop()

current = st.session_state.test_set[st.session_state.index]

st.markdown(f"""
### Q{st.session_state.index + 1}

**[{current['番号']}]**  
{current['例文']}
""")

# ===== 日本語訳（クリック/タップ） =====
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
    if st.button("⭕ 正解"):
        st.session_state.index += 1
        st.session_state.show_jp = False  # 次の問題で閉じる

with colB:
    if st.button("❌ 不正解"):
        if current not in st.session_state.wrong_list:
            st.session_state.wrong_list.append(current)
        st.session_state.index += 1
        st.session_state.show_jp = False  # 次の問題で閉じる

# ===== 次の問題 =====
if st.session_state.index >= len(st.session_state.test_set):
    st.success("🎉 終了！")
    st.write(f"❌ 記録された問題数: {len(st.session_state.wrong_list)}")
    st.stop()