import fitz
import streamlit as st
from groq import Groq

# Cấu hình trang web (Tự động ẩn Sidebar)
st.set_page_config(
    page_title="INFORME",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🔑 Groq API Key của bạn
GROQ_API_KEY ="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"

# Custom CSS giao diện Ombre
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none; }
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .title-text { 
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900; font-size: 2.8rem; margin-bottom: 0.5rem; text-align: center;
    }
    .subtitle-text { color: #4b5563; font-size: 1.1rem; margin-bottom: 2rem; text-align: center; }
    .stTextArea textarea { 
        border-radius: 12px; border: 2px solid #e2e8f0; 
        background-color: rgba(255, 255, 255, 0.8); 
    }
    .stButton>button {
        background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%);
        color: white; font-weight: bold; border: none; border-radius: 8px; padding: 0.5rem 1rem;
    }
    .result-card { 
        background: rgba(255, 255, 255, 0.95); padding: 1.8rem; border-radius: 16px; 
        border-left: 6px solid #4f46e5; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); margin-top: 1rem; 
    }
    </style>
""", unsafe_allow_html=True)

# Giao diện chính
st.markdown('<div class="title-text">⚖️ INFORME - Trợ Lý Tinh Gọn Văn Bản Hành Chính</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Chuyển đổi văn bản pháp lý phức tạp thành ngôn ngữ dễ hiểu chỉ trong vài giây</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📂 Tải lên văn bản hành chính (PDF)", type=["pdf"])

if uploaded_file:
    # Đọc PDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = "".join([page.get_text() for page in doc])

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("📄 Văn bản gốc")
        st.text_area("", text, height=500)

    with col2:
        st.subheader("⚡ Kết quả tinh gọn")
        if st.button("🚀 Bắt đầu phân tích & Tóm tắt", type="primary", use_container_width=True):
            with st.spinner("🔍 AI đang đọc và tinh gọn văn bản..."):
                try:
                    client = Groq(api_key=GROQ_API_KEY)
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
                    completion = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3
                    )
                    st.markdown(f'<div class="result-card">{completion.choices[0].message.content}</div>', unsafe_allow_html=True)
                    st.toast("Đã tóm tắt xong!", icon="🎉")
                except Exception as e:
                    st.error(f"Lỗi xử lý AI: {e}")
