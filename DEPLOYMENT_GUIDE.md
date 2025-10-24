# 🚀 Streamlit Cloud 배포 가이드

## 단계 1: GitHub 저장소 준비

### 1.1 저장소 생성 및 파일 푸시

```bash
# 저장소 클론 (이미 진행됨)
cd artwork-verifier

# 모든 파일 확인
git status

# 원격 저장소 확인
git remote -v
```

## 단계 2: Streamlit Cloud 배포

### 2.1 Streamlit Cloud 가입
1. https://streamlit.io/cloud 방문
2. GitHub 계정으로 로그인

### 2.2 새 앱 생성
1. "Create app" 버튼 클릭
2. 다음 정보 입력:
   - **Repository**: `toolofuture/sure`
   - **Branch**: `main`
   - **Main file path**: `app.py`

### 2.3 앱 배포 대기
- 배포는 자동으로 시작됨
- 몇 분 정도 소요될 수 있음

## 단계 3: API 키 설정 (Secrets)

### 3.1 Streamlit Cloud에서 Secrets 설정

1. 배포된 앱의 우상단 메뉴 클릭
2. "Settings" → "Secrets" 선택
3. 다음 형식으로 API 키 추가:

```toml
# OpenAI API key (선택사항)
OPENAI_API_KEY = "sk-proj-..."

# 또는 Anthropic API key
ANTHROPIC_API_KEY = "sk-ant-..."
```

**중요**: TOML 형식을 정확히 따르세요. 문자열은 따옴표로 감싸야 합니다.

### 3.2 Secrets 저장
- "Save" 클릭
- 변경사항이 약 1분 내에 반영됨

## 단계 4: 앱 접속 및 테스트

### 4.1 배포된 앱 URL
앱 배포 후 다음 형식으로 접속 가능:
```
https://sure-YOUR_USERNAME.streamlit.app
```

### 4.2 기본 테스트
1. 샘플 이미지 업로드
2. "위작 검증 시작" 버튼 클릭
3. 결과 확인

## 단계 5: 로컬 개발 및 업데이트

### 5.1 로컬 실행
```bash
# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py
```

### 5.2 변경사항 배포
```bash
# 변경사항 커밋
git add .
git commit -m "update: 설명"

# GitHub에 푸시
git push origin main

# Streamlit Cloud가 자동으로 새 버전 배포
```

## 문제 해결

### 문제: "This file does not exist"
- 해결: `app.py`가 저장소 최상위에 있는지 확인

### 문제: "ModuleNotFoundError: No module named 'torch'"
- 해결: `requirements.txt` 확인 및 Streamlit이 의존성 재설치 대기

### 문제: TOML 형식 오류
- 해결: Secrets 입력 시 따옴표 사용 확인
  ```toml
  # 올바른 형식
  OPENAI_API_KEY = "sk-proj-..."
  
  # 틀린 형식
  OPENAI_API_KEY = sk-proj-...
  ```

### 문제: 앱 로딩이 느린 경우
- 모델 초기화에 시간 소요 (처음 실행 시)
- CPU 환경에서는 더 오래 걸릴 수 있음
- 보통 30초 이상 기다리세요

## 모니터링 및 로그

### Streamlit Cloud 로그 확인
1. 앱 URL 방문
2. 우상단 메뉴 → "View logs"
3. 에러 메시지 확인

## 보안 권장사항

1. **API 키 보호**
   - 절대 코드에 직접 입력하지 말 것
   - 항상 Streamlit Secrets 사용

2. **저장소 설정**
   - `.gitignore`에 민감한 파일 추가
   - `.env` 파일은 커밋하지 말 것

3. **업로드 파일 처리**
   - 업로드된 이미지는 메모리에서만 처리됨
   - 서버에 저장되지 않음

## 다음 단계

1. ✅ 앱 배포 완료
2. 📊 사용자 피드백 수집
3. 🔄 모델 성능 개선
4. 📈 추가 기능 개발

---

**배포 완료 체크리스트:**
- [ ] GitHub 저장소에 코드 푸시
- [ ] Streamlit Cloud에 앱 배포
- [ ] Secrets에 API 키 설정
- [ ] 앱 접속 확인
- [ ] 기본 테스트 완료
