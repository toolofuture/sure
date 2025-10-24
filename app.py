import streamlit as st
from PIL import Image
import io
import os
from model import create_verifier

# Page configuration
st.set_page_config(
    page_title="위작 검증 서비스",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .big-font {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
    }
    .result-container {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
    .authentic-result {
        background-color: #d4edda;
        border: 2px solid #28a745;
        color: #155724;
    }
    .uncertain-result {
        background-color: #f8d7da;
        border: 2px solid #dc3545;
        color: #721c24;
    }
    .confidence-text {
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'verifier' not in st.session_state:
    st.session_state.verifier = create_verifier()

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<div class='big-font'>🎨 위작 검증 서비스</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
### 📋 서비스 설명
- **진품 검증 AI 모델**: ResNet 기반 전이 학습 모델
- **판정 결과**: 진품 확실 ✅ 또는 진품임을 확신하지 못함 ❌
- **신뢰도**: 80% 이상의 신뢰도일 때만 진품이라고 판정합니다
""")

st.markdown("---")

# Main content
st.subheader("📸 이미지 업로드")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "이미지를 업로드하세요 (JPG, PNG, BMP)",
        type=["jpg", "jpeg", "png", "bmp"],
        help="검증할 미술품 이미지를 업로드하세요"
    )

with col2:
    st.info("💡 **팁**: 고해상도 이미지가 더 정확한 결과를 제공합니다.")

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_container_width=True)
    
    st.markdown("---")
    
    # Verify button
    if st.button("🔍 위작 검증 시작", use_container_width=True, type="primary"):
        with st.spinner("AI 모델이 분석 중입니다..."):
            try:
                # Get verification result
                result = st.session_state.verifier.verify(image)
                
                # Display result with color coding
                st.markdown("---")
                st.subheader("✨ 검증 결과")
                
                if "확실" in result["result"]:  # 진품 확실
                    result_html = f"""
                    <div class='result-container authentic-result'>
                        <div style='font-size: 48px;'>✅</div>
                        <div class='confidence-text'>{result['result']}</div>
                        <div style='font-size: 18px; margin: 10px 0;'>신뢰도: {result['confidence']}</div>
                    </div>
                    """
                else:  # 진품임을 확신하지 못함
                    result_html = f"""
                    <div class='result-container uncertain-result'>
                        <div style='font-size: 48px;'>❌</div>
                        <div class='confidence-text'>{result['result']}</div>
                        <div style='font-size: 18px; margin: 10px 0;'>신뢰도: {result['confidence']}</div>
                    </div>
                    """
                
                st.markdown(result_html, unsafe_allow_html=True)
                
                # Additional analysis info
                st.markdown("---")
                st.subheader("📊 상세 분석")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("진품 확률", f"{result['authentic_probability']*100:.1f}%")
                with col2:
                    st.metric("불확실 확률", f"{result['uncertain_probability']*100:.1f}%")
                
                st.info("""
                **분석 기준:**
                - ResNet50 기반 심층 신경망을 사용합니다
                - 80% 이상의 신뢰도로만 진품으로 판정합니다
                - 미세한 차이와 패턴을 감지합니다
                """)
                
            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
else:
    st.info("👆 위에서 이미지를 업로드하여 시작하세요.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    🎨 Artwork Verification Service | Powered by ResNet Transfer Learning
</div>
""", unsafe_allow_html=True)
