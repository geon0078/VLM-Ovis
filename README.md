# VLM-Ovis: Vision Language Model Web Interface

Ovis Vision Language Model을 위한 사용하기 쉬운 웹 인터페이스입니다. Gradio를 사용하여 구축되었으며, 이미지 분석과 설명 생성을 위한 직관적인 UI를 제공합니다.

## 주요 기능

- 이미지 업로드 및 AI 분석
- 다국어 텍스트 프롬프트 지원
- 고급 생성 파라미터 조정 (Temperature, Top-p, Max tokens)
- 실시간 성능 모니터링 (토큰 처리 속도, 메모리 사용량)
- 예시 이미지 제공
- 시스템 정보 표시

## 설치 및 실행

### 1. 필요 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 모델 다운로드
Hugging Face에서 Ovis 모델을 다운로드하거나, 기존 캐시를 사용하세요.

### 3. 애플리케이션 실행
```bash
python app.py
```

웹 브라우저에서 `http://localhost:7860`으로 접속하세요.

## 프로젝트 구조

```
.
├── app.py              # 메인 애플리케이션
├── model.py            # 모델 로딩 및 추론 로직
├── ui_components.py    # UI 구성 요소들
├── styles.py          # CSS 스타일 및 테마
├── requirements.txt    # 필요 패키지 목록
└── README.md          # 프로젝트 문서
```

## 파일별 설명

### app.py
- 메인 실행 파일
- Gradio 인터페이스 초기화 및 실행
- 이벤트 핸들러 연결

### model.py
- OvisModel 클래스 정의
- 모델 로딩 및 추론 로직
- 성능 통계 수집 및 계산

### ui_components.py
- Gradio UI 구성 요소들
- 입력/출력 섹션, 헤더, 푸터 생성
- 예시 이미지 관리

### styles.py
- 커스텀 CSS 스타일
- Gradio 테마 설정

## 사용 방법

1. **이미지 업로드**: 분석하고 싶은 이미지를 업로드하세요
2. **프롬프트 입력**: 이미지에 대한 질문이나 요청사항을 입력하세요
3. **고급 설정** (선택사항): 생성 파라미터를 조정하세요
4. **분석 실행**: "이미지 분석하기" 버튼을 클릭하세요
5. **결과 확인**: AI가 생성한 분석 결과와 성능 통계를 확인하세요

## 성능 모니터링

애플리케이션은 다음과 같은 성능 지표를 제공합니다:

- 처리 시간
- 입력/출력 토큰 수
- 토큰 생성 속도 (tokens/sec)
- GPU 메모리 사용량
- 시스템 정보 (CPU, GPU, RAM)

## 요구사항

- Python 3.8+
- CUDA 지원 GPU (권장)
- 최소 8GB RAM
- Ovis 모델 파일

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여

버그 리포트, 기능 요청, 풀 리퀘스트를 환영합니다!
