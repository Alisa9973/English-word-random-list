import json
import random
import streamlit as st
from openai import OpenAI
from pathlib import Path
import tempfile

# ===== OpenAIクライアント =====
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="例文ランダム表示", page_icon="🎲")

st.markdown("### 🎲 例文ランダムテスト（10問）")
st.markdown(
    "<div style='font-size:0.9em; color:gray;'>出題範囲を選択</div>",
    unsafe_allow_html=True
)

# ===== JSON読み込み =====
with open("data.json", encoding="utf-8") as f:
    DATA = json.load(f)

# ===== テスト生成関数 =====
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

# ===== TTS関数（安定版）=====
def generate_tts_audio(text: str) -> bytes:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp_path = Path(tmp.name)

    try:
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text,
        )
        tmp_path.write_bytes(response.read())
        return tmp_path.read_bytes()

    finally:
        try:
            tmp_path.unlink()
        except Exception:
            pass

# ===== 出題範囲スライダー =====
max_number = max(int(item["番号"]) for item in DATA)

block_size = 100
max_block = (max_number - 1) // block_size

selected_block = st.slider(
    "出題範囲（100語刻み）",
    min_value=0,
    max_value=max_block,
    value=0
)

start = selected_block * block_size + 1
end = min(start + block_size - 1, max_number)

st.caption(f"現在の範囲：{start}〜{end}")

if st.button("この範囲で開始"):
    new_test(start, end)

# ===== 範囲未選択時 =====
if "test_set" not in st.session_state:
    st.stop()

# ===== 現在の問題 =====
current = st.session_state.test_set[st.session_state.index]

st.markdown(
    f"""
    <div style="font-size:1.25em; line-height:1.7;
                padding:14px; border-radius:10px;
                background:#f6f7f9;">
      <b>{st.session_state.range_label}</b><br>
      <b>Q{st.session_state.index + 1} / 10</b><br>
      <b>[{current['番号']}]</b> {current['例文']}
    </div>
    """,
    unsafe_allow_html=True
)

# ===== 🔊 AI音声再生ボタン =====
if st.button("🔊 ネイティブ音声で再生"):
    with st.spinner("音声生成中..."):
        try:
            audio_bytes = generate_tts_audio(current["例文"])
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.error("音声生成でエラーになりました")
            st.exception(e)

# ===== ナビゲーション =====
colA, colB = st.columns(2)

with colA:
    if st.session_state.index < 9:
        if st.button("次へ ▶", use_container_width=True):
            st.session_state.index += 1
    else:
        st.success("🎉 テスト終了！")

with colB:
    if st.button("🔄 やり直す", use_container_width=True):
        parts = st.session_state.range_label.split("〜")
        new_test(int(parts[0]), int(parts[1]))

st.caption(f"全 {len(DATA)} 件")