# 🎨 위작 검증 서비스 - 설정 및 배포 가이드

## 📋 프로젝트 개요

**ResNet 기반 AI 미술품 진위 검증 시스템**

### 프로젝트 특징
- ✅ ResNet50 전이 학습 모델
- ✅ 높은 신뢰도: 80% 이상만 "진품 확실" 판정
- ✅ 명확한 결과: "진품 확실" 또는 "진품임을 확신하지 못함"
- ✅ Streamlit 기반 직관적 UI
- ✅ 실시간 이미지 분석

## 🚀 빠른 시작 (로컬)

### 1단계: 저장소 클론
```bash
git clone https://github.com/toolofuture/sure.git
cd sure
```

### 2단계: 가상 환경 설정
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3단계: 의존성 설치
```bash
pip install -r requirements.txt
```

### 4단계: 앱 실행
```bash
streamlit run app.py
```

### 5단계: 브라우저에서 열기
```
http://localhost:8501
```

---

## 🌐 Streamlit Cloud 배포

### 필수 사항
- GitHub 계정 (코드 저장소)
- Streamlit Community Cloud 계정 (무료)

### 배포 단계

#### Step 1: GitHub 저장소 확인
```bash
# 저장소가 이미 준비되어 있습니다
git remote -v
# origin  https://github.com/toolofuture/sure.git
```

#### Step 2: Streamlit Cloud 접속
1. https://streamlit.io/cloud 방문
2. GitHub 계정으로 로그인

#### Step 3: 새 앱 생성
1. **"Create app"** 버튼 클릭
2. 다음 정보 입력:
   - **Repository**: `toolofuture/sure`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. **"Deploy"** 클릭

#### Step 4: 배포 완료 대기
- 자동 배포 시작
- 보통 2-5분 소요
- 첫 실행 시 모델 다운로드 (시간 소요)

#### Step 5: 배포된 앱 접속
```
https://sure-toolofuture.streamlit.app
```
(실제 URL은 배포 후 확인 가능)

---

## 🔐 API 키 설정 (Secrets)

### OpenAI API 키 설정 (선택사항)

#### Streamlit Cloud에서 설정
1. 배포된 앱 우상단 메뉴 클릭
2. **"Settings"** 선택
3. **"Secrets"** 클릭
4. 다음 코드 입력:

```toml
OPENAI_API_KEY = "sk-proj-YOUR_API_KEY_HERE"
```

**⚠️ 중요 사항:**
- 반드시 따옴표 사용
- TOML 형식 정확히 따르기
- 개행 문자 없이 입력

#### 저장
- 우측 **"Save"** 클릭
- 약 1분 내에 반영됨

---

## 📊 기술 상세 정보

### 모델 아키텍처

```
ResNet50 (ImageNet 사전학습)
├── 입력층: 224x224 이미지
├── 백본: Conv 레이어들 (동결됨)
└── 분류 헤드 (학습 가능):
    ├── FC(2048 → 512) + ReLU + Dropout(0.5)
    ├── FC(512 → 256) + ReLU + Dropout(0.3)
    └── FC(256 → 2) [진품/불확실]
```

### 판정 논리

```
진품 신뢰도 >= 80%  →  "진품 확실 ✅" (초록색)
진품 신뢰도 < 80%   →  "진품임을 확신하지 못함 ❌" (빨간색)
```

### 이미지 전처리
- 크기: 224x224 픽셀로 리사이징
- 정규화: ImageNet 평균/표준편차로 정규화
- 형식: RGB 3채널 이미지

---

## 🔧 로컬 테스트

### 테스트 이미지 준비
1. 미술품 이미지 준비 (JPG, PNG, BMP)
2. 앱 실행
3. 이미지 업로드
4. "위작 검증 시작" 클릭

### 예상 실행 시간
- CPU 환경: 2-5초
- GPU 환경: 1-2초

---

## 📁 프로젝트 구조

```
sure/
├── app.py                  # Streamlit 메인 앱
├── model.py                # ResNet 모델 클래스
├── config.py               # 설정 파일
├── requirements.txt        # Python 의존성
├── README.md               # 프로젝트 설명
├── DEPLOYMENT_GUIDE.md     # 배포 상세 가이드
├── SETUP_INSTRUCTIONS.md   # 이 파일
└── .streamlit/
    └── config.toml         # Streamlit 설정
```

---

## 🐛 문제 해결

### 1️⃣ "ModuleNotFoundError: No module named 'torch'"
**해결:**
```bash
pip install torch torchvision
```

### 2️⃣ "This file does not exist" (Streamlit Cloud)
**확인 사항:**
- [ ] `app.py`가 저장소 최상위에 있나?
- [ ] GitHub에 정상 푸시되었나?
- [ ] Branch가 `main`인가?

### 3️⃣ TOML 형식 오류
**올바른 형식:**
```toml
OPENAI_API_KEY = "sk-proj-..."
```
**틀린 형식:**
```toml
OPENAI_API_KEY = sk-proj-...  # 따옴표 없음
```

### 4️⃣ 앱이 느리게 로드됨
- 처음 실행: ResNet50 모델 다운로드 중 (시간 소요)
- 이후 빠른 로딩
- 약 1-2분 기다리세요

### 5️⃣ 이미지 업로드 오류
**지원 형식:** JPG, PNG, BMP
**최대 크기:** 20MB

---

## 📈 배포 후 확인

### ✅ 배포 체크리스트
- [ ] GitHub에 모든 파일 푸시됨
- [ ] Streamlit Cloud 앱 배포 완료
- [ ] 앱 URL로 접속 가능
- [ ] 테스트 이미지로 검증 성공
- [ ] API 키 설정 (필요시)

### 🔗 GitHub 저장소
```
https://github.com/toolofuture/sure
```

---

## 📞 지원

### 문제 발생 시
1. README.md 확인
2. DEPLOYMENT_GUIDE.md 참고
3. Streamlit Cloud 로그 확인
   - 앱 URL 방문 → 우상단 메뉴 → "View logs"

---

## 🎯 다음 단계

1. ✅ 로컬 테스트 완료
2. ✅ Streamlit Cloud 배포
3. 📊 사용자 피드백 수집
4. 🔄 모델 성능 개선
5. 📈 추가 기능 개발
   - 배치 분석
   - 분석 기록 저장
   - 모델 재학습

---

**문서 작성 날짜:** 2025-10-24
**마지막 업데이트:** 2025-10-24
**버전:** 1.0.0
