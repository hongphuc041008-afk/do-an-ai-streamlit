import fitz
import streamlit as st
from google import genai

# Cấu hình trang web
st.set_page_config(
    page_title="Trợ Lý Pháp Lý AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thêm CSS tùy chỉnh để làm đẹp giao diện
st.markdown("""
    <style>
    /* Đổi phông chữ và màu nền chính */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Làm đẹp tiêu đề */
    .title-text {
        color: #1e3a8a;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    .subtitle-text {
        color: #4b5563;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Bo tròn các khung nội dung */
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
    }
    
    /* Thiết kế thẻ chứa kết quả AI */
    .result-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #2563eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Thanh bên (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=70)
    st.title("⚙️ Cấu hình")
    api_key = AQ.Ab8RN6KURfJs4xwcrFTXtX3J3-9_lEAl-Zbj-FnUUk9HRMAqUQ
    st.markdown("---")
    st.info("💡 **Mẹo:** Tải lên văn bản PDF dạng Nghị định, Thông tư hoặc Quyết định để AI phân tích tốt nhất.")

# Header chính
st.markdown('<div class="title-text">⚖️ Trợ Lý Tinh Gọn Văn Bản Hành Chính</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Chuyển đổi văn bản pháp lý phức tạp thành ngôn ngữ dễ hiểu chỉ trong vài giây</div>', unsafe_allow_html=True)

# Tải file PDF
uploaded_file = st.file_uploader("📂 Tải lên văn bản hành chính (PDF)", type=["pdf"])

if uploaded_file:
    # Đọc PDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "".join([page.get_text() for page in doc])

    # Chia cột giao diện
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.subheader("📄 Văn bản gốc")
        st.text_area("", text, height=450)

    with col2:
        st.subheader("⚡ Kết quả tinh gọn")
        if st.button("🚀 Bắt đầu phân tích & Tóm tắt", type="primary", use_container_width=True):
            with st.spinner("🔍 AI đang đọc và tinh gọn văn bản..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    Bạn là một chuyên gia pháp lý. Hãy tóm tắt văn bản hành chính sau thành dạng ngôn ngữ phổ thông dễ hiểu.
                    
                    Yêu cầu trình bày:
                    1. 🎯 **Tóm tắt ngắn gọn (TL;DR):** 2-3 câu tổng quan.
                    2. 👤 **Đối tượng áp dụng:** Ai là người bị ảnh hưởng/cần thực hiện?
                    3. 📋 **Các bước / Thủ tục cần làm:** Liệt kê gạch đầu dòng rõ ràng.
                    4. ⏰ **Mốc thời gian / Hạn chót (nếu có):** Nêu rõ thời gian cụ thể.
                    
                    Nội dung văn bản:
                    {text}
                    """
                    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                    
                    # Hiển thị kết quả trong khung đẹp
                    st.markdown(f'<div class="result-card">{response.text}</div>', unsafe_allow_html=True)
                    st.toast("Đã tóm tắt xong!", icon="🎉")
                except Exception as e:
                    st.error(f"Lỗi: {e}")
