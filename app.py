import fitz
import streamlit as st
from google import genai

st.set_page_config(page_title="Tinh Gọn Văn Bản", layout="wide")
st.title("📄 Trợ Lý Tinh Gọn Văn Bản Hành Chính")

api_key = st.sidebar.text_input("Nhập API Key:", type="password")
uploaded_file = st.file_uploader("Tải PDF", type=["pdf"])

if uploaded_file and api_key:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "".join([page.get_text() for page in doc])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📌 Văn bản gốc")
        st.text_area("Nội dung", text, height=400)

    with col2:
        st.subheader("⚡ Bản tóm tắt")
        if st.button("Tóm tắt", type="primary"):
            with st.spinner("Đang xử lý..."):
                client = genai.Client(api_key=api_key)
                prompt = f"Hãy tóm tắt văn bản hành chính sau thành dạng gạch đầu dòng dễ hiểu, nêu rõ: Đối tượng áp dụng, Thủ tục cần làm, Mốc thời gian:\n\n{text}"
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                st.markdown(response.text)