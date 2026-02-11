import json
import random
import streamlit as st

st.set_page_config(page_title="例文ランダム表示", page_icon="🎲")
st.header("🎲 例文ランダムテスト（10問）")

# ===== JSON読み込み =====
with open("data.json", encoding="utf-8") as f:
    DATA = json.load(f)

if len(DATA) < 10:
    st.error("データが10件未満です")
    st.stop()

# ===== テスト初期化 =====
def new_test():
    st.session_state.test_set = random.sample(DATA, 10)
    st.session_state.index = 0

if "test_set" not in st.session_state:
    new_test()

# ===== 現在の問題 =====
current = st.session_state.test_set[st.session_state.index]

st.markdown(
    f"""
    <div style="font-size:1.4em; line-height:1.7;
                padding:16px; border-radius:12px;
                background:#f6f7f9;">
      <b>Q{st.session_state.index + 1} / 10</b><br><br>
      <b>[{current['番号']}]</b> {current['例文']}
    </div>
    """,
    unsafe_allow_html=True
)

# ===== ボタン処理 =====
col1, col2 = st.columns(2)

with col1:
    if st.session_state.index < 9:
        if st.button("次へ ▶"):
            st.session_state.index += 1
    else:
        st.success("🎉 テスト終了！")

with col2:
    if st.button("🔄 新しい10問"):
        new_test()
