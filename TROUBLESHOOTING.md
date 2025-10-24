# 🔧 문제 해결 가이드

## Requirements 설치 오류 (해결됨)

### 문제
```
Error installing requirements.
Click "Manage App" and consult the terminal for more details.
```

### 원인
- PyTorch 최신 버전(2.1.1)이 Streamlit Cloud의 빌드 환경에서 호환되지 않음
- opencv-python 패키지가 설치 실패 유발

### 해결책 ✅
**Requirements.txt 업데이트됨:**

```
streamlit==1.28.1
torch==2.0.0              # ← 2.1.1에서 2.0.0으로 다운그레이드
torchvision==0.15.1       # ← 0.16.1에서 0.15.1으로 다운그레이드
pillow==10.0.0
numpy==1.24.3
pydantic==2.4.2
python-dotenv==1.0.0
openai==1.3.0
requests==2.31.0
# opencv-python 제거 ✓
# scikit-learn 제거 ✓
```

### Streamlit Cloud 재배포

#### 방법 1: Reboot (빠름)
1. Streamlit Cloud 앱 대시보드 방문
2. "Manage app" 클릭
3. "Reboot app" 버튼 클릭
4. 앱이 자동으로 재시작되고 새로운 requirements 적용

#### 방법 2: 새로 배포 (확실함)
1. 기존 앱 삭제
2. Streamlit Cloud에서 "Create app" 클릭
3. Repository: `toolofuture/sure`
4. Branch: `main`
5. Main file: `app.py`
6. Deploy 클릭

---

## 다른 일반적인 문제들

### 1. "This file does not exist"
**원인**: `app.py`가 저장소 최상위에 없음
**해결**: 파일 위치 확인
```bash
ls -la app.py  # 파일 존재 확인
```

### 2. "ModuleNotFoundError: No module named..."
**원인**: requirements.txt에 누락된 패키지
**해결**: requirements.txt에 패키지 추가 후 재배포
```bash
pip install [패키지명]  # 로컬에서 테스트
```

### 3. 앱 로딩이 매우 느림 (1-2분)
**원인**: PyTorch 모델 첫 로드 시간
**해결**: 정상입니다. 약 1-2분 기다리세요.
- 모델 다운로드 (500MB+)
- 모델 초기화
- 이후 빠른 응답

### 4. TOML 형식 오류 (API 키 설정)
**원인**: Secrets에 잘못된 형식
**올바른 형식**:
```toml
OPENAI_API_KEY = "sk-proj-..."
```
**틀린 형식**:
```toml
OPENAI_API_KEY = sk-proj-...  # 따옴표 없음
OPENAI_API_KEY = 'sk-proj-...' # 작은따옴표
```

### 5. 이미지 업로드 안 됨
**확인사항**:
- [ ] 파일 형식: JPG, PNG, BMP
- [ ] 파일 크기: 20MB 이하
- [ ] 브라우저 캐시 삭제
- [ ] 새 탭에서 다시 접속

---

## 로컬 테스트

문제 발생 시 로컬에서 테스트하면 디버깅이 쉽습니다.

### 1. 가상 환경 설정
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 앱 실행
```bash
streamlit run app.py
```

### 4. 브라우저에서 테스트
```
http://localhost:8501
```

---

## 로그 확인

### Streamlit Cloud 로그
1. 앱 URL 방문
2. 우상단 메뉴 → "Menu"
3. "View logs" 클릭
4. 에러 메시지 확인

### 예상 로그
```
# 정상
Installing dependencies with pip...
Successfully installed torch-2.0.0 torchvision-0.15.1...
App is running at http://...

# 오류
ERROR: Could not find a version that satisfies the requirement torch==2.1.1
```

---

## 도움말

### GitHub Issues
- https://github.com/toolofuture/sure/issues

### Streamlit Community
- https://discuss.streamlit.io

### PyTorch 호환성
- https://pytorch.org/get-started/locally/

---

## 체크리스트

배포 재시도 전 확인:
- [ ] requirements.txt 업데이트됨 (2024-10-24)
- [ ] GitHub에 최신 버전 푸시됨
- [ ] Streamlit Cloud에서 앱 재시작/재배포
- [ ] 로그 확인 (에러 메시지 있는지)
- [ ] 로컬 환경에서 정상 작동
- [ ] Secrets (API 키) 형식 확인

---

**마지막 업데이트**: 2025-10-24
**상태**: ✅ Requirements 호환성 해결됨
