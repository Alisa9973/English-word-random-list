import json
import random
import streamlit as st

st.set_page_config(page_title="例文ランダム表示", page_icon="🎲")
st.header("🎲 例文ランダム表示")

# ===== JSON読み込み =====
with open("data.json", encoding="utf-8") as f:
    DATA = json.load(f)

# ===== 1周かぶらないランダム =====
if "pool" not in st.session_state:
    st.session_state.pool = list(range(len(DATA)))
    random.shuffle(st.session_state.pool)
    st.session_state.pos = 0

def pick_next():
    if st.session_state.pos >= len(st.session_state.pool):
        random.shuffle(st.session_state.pool)
        st.session_state.pos = 0
    i = st.session_state.pool[st.session_state.pos]
    st.session_state.pos += 1
    return DATA[i]

# 起動時に自動表示
if "current" not in st.session_state:
    st.session_state.current = pick_next()

if st.button("次を表示 ▶", use_container_width=True):
    st.session_state.current = pick_next()

cur = st.session_state.current

st.markdown(
    f"""
    <div style="font-size:1.4em; line-height:1.7;
                padding:16px; border-radius:12px;
                background:#f6f7f9;">
      <b>[{cur['番号']}]</b> {cur['例文']}
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(f"全 {len(DATA)} 件")
