# 🎨 위작 검증 서비스

**ResNet 기반 전이 학습 모델을 사용한 AI 미술품 진위 검증 시스템**

## 📋 프로젝트 개요

이 프로젝트는 고가의 미술품이 진품인지 위작인지를 검증하는 AI 서비스입니다.

### 주요 특징
- ✅ **높은 신뢰도**: 80% 이상의 신뢰도로만 진품 판정
- 🎯 **명확한 결과**: "진품 확실" 또는 "진품임을 확신하지 못함" 두 가지만 제시
- 🚀 **빠른 분석**: ResNet 기반 심층 신경망으로 실시간 검증
- 🎨 **직관적 UI**: Streamlit 기반 사용하기 쉬운 인터페이스

## 🏗️ 기술 스택

- **모델**: ResNet50 Transfer Learning (ImageNet 사전학습)
- **프레임워크**: PyTorch
- **웹 프레임워크**: Streamlit
- **언어**: Python 3.8+

## 📁 프로젝트 구조

```
artwork-verifier/
├── app.py              # Streamlit 메인 애플리케이션
├── model.py            # ResNet 기반 검증 모델
├── config.py           # 설정 파일
├── requirements.txt    # 의존성
├── README.md          # 이 파일
└── .gitignore         # Git 무시 파일
```

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/toolofuture/sure.git
cd sure
```

### 2. 가상 환경 생성
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate     # Windows
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 로컬 실행
```bash
streamlit run app.py
```

### 5. 웹 브라우저 접속
```
http://localhost:8501
```

## 🌐 Streamlit Cloud 배포

### 1. GitHub 저장소에 푸시
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Streamlit Cloud 연결
1. [Streamlit Cloud](https://streamlit.io/cloud)에 접속
2. GitHub 계정으로 로그인
3. "New app" 선택
4. 저장소와 파일 설정

### 3. Secrets 설정 (필요시)
1. Streamlit Cloud 앱 설정에서 "Secrets" 선택
2. OpenAI API 키 추가 (선택사항):
```toml
OPENAI_API_KEY = "sk-..."
```

## 🤖 모델 상세 정보

### ResNet50 Transfer Learning
- **입력 크기**: 224x224 픽셀
- **출력**: 진품 vs 불확실 (2개 클래스)
- **신뢰도 임계값**: 80% (CONFIDENCE_THRESHOLD)

### 모델 아키텍처
```
ResNet50 (사전학습)
  ├── Conv 레이어들 (Frozen)
  └── 커스텀 분류 헤드 (학습 가능)
      ├── Linear(2048 → 512)
      ├── ReLU + Dropout(0.5)
      ├── Linear(512 → 256)
      ├── ReLU + Dropout(0.3)
      └── Linear(256 → 2)
```

## 📊 사용 예시

### 웹 UI 사용
1. 이미지 업로드 페이지에서 미술품 사진 선택
2. "위작 검증 시작" 버튼 클릭
3. 결과 확인:
   - 진품 확실 ✅ (초록색)
   - 진품임을 확신하지 못함 ❌ (빨간색)

### Python 코드 사용
```python
from model import create_verifier
from PIL import Image

# 검증기 생성
verifier = create_verifier()

# 이미지 로드
image = Image.open("artwork.jpg")

# 검증
result = verifier.verify(image)
print(result)
# {
#   "result": "진품 확실 ✅",
#   "confidence": "92.3%",
#   "color": "green",
#   "authentic_probability": 0.923,
#   "uncertain_probability": 0.077
# }
```

## ⚙️ 설정 커스터마이징

`config.py`에서 다음을 수정할 수 있습니다:

```python
# 신뢰도 임계값 (낮출수록 더 쉽게 진품 판정)
CONFIDENCE_THRESHOLD = 0.8

# 이미지 크기
IMAGE_SIZE = 224

# 모델 종류
MODEL_NAME = "resnet50"  # resnet34, resnet101도 가능
```

## 📈 성능

- **처리 시간**: ~1-2초 (GPU 환경)
- **정확도**: ResNet50 기반 높은 인식률
- **메모리**: ~2GB RAM (모델 로드 시)

## 🔐 보안 고려사항

- API 키는 Streamlit Secrets에 저장
- 업로드된 이미지는 임시로만 처리됨
- 개인 정보는 저장하지 않음

## 🤝 기여

이슈 및 풀 요청을 환영합니다!

## 📄 라이선스

MIT License

## 📞 문의

문제가 발생하면 GitHub Issues를 통해 보고해주세요.

---

**Last Updated**: 2025-10-24
**Version**: 1.0.0
