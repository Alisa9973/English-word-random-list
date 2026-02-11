import json
import random
import streamlit as st

st.set_page_config(page_title="例文ランダム表示", page_icon="🎲")
st.subheader("🎲 例文ランダムテスト（10問）")

# ===== JSON読み込み =====
with open("data.json", encoding="utf-8") as f:
    DATA = json.load(f)

# ===== テスト生成 =====
def new_test(min_no, max_no):
    filtered = [
        item for item in DATA
        if min_no <= int(item["番号"]) <= max_no
    ]

    if len(filtered) < 10:
        st.error("その範囲には10問未満しかありません")
        return

    st.session_state.test_set = random.sample(filtered, 10)
    st.session_state.index = 0
    st.session_state.range_label = f"{min_no}〜{max_no}"

# ===== 範囲ボタン =====
st.markdown("### 出題範囲を選択")

col1, col2 = st.columns(2)

with col1:
    if st.button("1〜100"):
        new_test(1, 100)

with col2:
    if st.button("101〜200"):
        new_test(101, 200)

# ===== 初期状態 =====
if "test_set" not in st.session_state:
    st.info("範囲を選んでください 👆")
    st.stop()

# ===== 現在の問題 =====
current = st.session_state.test_set[st.session_state.index]

st.markdown(
    f"""
    <div style="font-size:1.3em; line-height:1.7;
                padding:16px; border-radius:12px;
                background:#f6f7f9;">
      <b>{st.session_state.range_label}</b><br><br>
      <b>Q{st.session_state.index + 1} / 10</b><br><br>
      <b>[{current['番号']}]</b> {current['例文']}
    </div>
    """,
    unsafe_allow_html=True
)

# ===== 次へボタン =====
colA, colB = st.columns(2)

with colA:
    if st.session_state.index < 9:
        if st.button("次へ ▶"):
            st.session_state.index += 1
    else:
        st.success("🎉 テスト終了！")

with colB:
    if st.button("🔄 同じ範囲でやり直す"):
        parts = st.session_state.range_label.split("〜")
        new_test(int(parts[0]), int(parts[1]))
