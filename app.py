import random
import pandas as pd
import streamlit as st

st.set_page_config(page_title="例文ランダム表示", page_icon="🎲")
st.title("🎲 例文ランダム表示")

ID_COL = "番号"
TEXT_COL = "例文"

uploaded = st.file_uploader("Excelファイル（.xlsx）をアップロード", type=["xlsx"])

if uploaded is None:
    st.info("Excelをアップロードしてね。")
    st.stop()

df = pd.read_excel(uploaded)

missing = [c for c in (ID_COL, TEXT_COL) if c not in df.columns]
if missing:
    st.error(f"必要な列が見つかりません: {missing}\n列一覧: {list(df.columns)}")
    st.stop()

sub = df[[ID_COL, TEXT_COL]].dropna().copy()
sub[TEXT_COL] = sub[TEXT_COL].astype(str).str.strip()

sub = sub[sub[TEXT_COL] != ""]

if sub.empty:
    st.error("表示できるデータがありません（例文が空かも）。")
    st.stop()

records = sub.to_dict(orient="records")

# 1周かぶらないランダム
if "pool" not in st.session_state or st.session_state.get("n") != len(records):
    st.session_state.pool = list(range(len(records)))
    random.shuffle(st.session_state.pool)
    st.session_state.pos = 0
    st.session_state.current = None
    st.session_state.n = len(records)

def pick_next():
    if st.session_state.pos >= len(st.session_state.pool):
        random.shuffle(st.session_state.pool)
        st.session_state.pos = 0
    i = st.session_state.pool[st.session_state.pos]
    st.session_state.pos += 1
    st.session_state.current = records[i]

# 起動時に自動で1つ表示
if st.session_state.current is None:
    pick_next()

if st.button("次を表示 ▶", use_container_width=True):
    pick_next()

cur = st.session_state.current
st.markdown("### ✅ 表示")
st.markdown(
    f"""
    <div style="font-size:1.35em; line-height:1.7; padding:16px; border-radius:12px; background:#f6f7f9;">
      <b>[{cur[ID_COL]}]</b> {cur[TEXT_COL]}
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(f"読み込み件数: {len(records)} 件")
