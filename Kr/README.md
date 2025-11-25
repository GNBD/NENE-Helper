# NENE HELPER / NENE LAUNCHER 🐔
**(네네 헬퍼 / 네네 런처)**

> **마인크래프트 서버 관리를 위한, 꽤 쓸만하고 가벼운 도구입니다.**
> (세상에서 가장 완벽하진 않더라도, 여러분에게 도움이 되길 바랍니다!)

For English Users, please click [here(Click)](https://github.com/GNBD/NENE-Helper).

---

## 🚀 프로젝트 개요 (Project Overview)

**NENE HELPER (또는 NENE LAUNCHER)**는 누구나 마인크래프트 자바 에디션 서버를 쉽고 빠르게 구축하고 관리할 수 있도록 돕는 도구입니다.
PaperMC API(또는 사용자 지정 API)를 통해 최신 서버 코어 파일을 자동으로 가져오며, Python과 HTML/CSS로 제작된 직관적인 웹 GUI를 제공합니다.

### 🚧 개발 진행 중 (Work In Progress)
> **이 프로젝트는 현재 지속적으로 개발 중입니다.**
> 사용 중 버그가 발생하거나 제안 사항이 있다면 언제든지 **[GitHub Issues]** 탭에 남겨주세요. 여러분의 피드백이 이 툴을 더 발전시킵니다!

![스크린샷 2025-11-23 193858](https://github.com/user-attachments/assets/7ffcff58-54e5-4114-921c-e6a18e035c66)

👉 **공식 웹사이트:** [https://nenehelper.netlify.app/](https://nenehelper.netlify.app/)

---

## ✨ 주요 기능 (Key Features)

### ⚡ **서버 관리 (Server Management)**
* **원클릭 서버 생성:** 최신 PaperMC 코어를 다운로드하고 몇 초 만에 서버를 생성합니다.
* **간편한 자바 전환 (Easy Java Switching):** PC에 설치된 모든 Java 버전을 자동으로 감지합니다. 클릭 한 번으로 서버에 사용할 자바 버전(예: Java 8 ↔ Java 21)을 자유롭게 변경할 수 있습니다.
* **서버별 개별 설정:** 서버마다 서로 다른 자바 버전을 지정하여 호환성 문제를 해결할 수 있습니다.
* **수동 경로 지원:** 목록에 없는 경우, 사용자가 직접 자바 실행 경로를 지정할 수도 있습니다.
* **커스텀 API 지원:** 필요에 따라 서버 코어 다운로드 주소(API)를 변경할 수 있습니다.

### 📊 **대시보드 및 모니터링**
* **실시간 모니터링:** 서버 상태, CPU 및 RAM 사용량을 한눈에 확인합니다.
* **웹 기반 UI:** HTML/CSS로 제작되어 깔끔하고 반응이 빠른 인터페이스를 제공합니다.

### 🛠 **필수 관리자 도구**
* **원클릭 명령어:** 복잡한 타이핑 없이 버튼 클릭으로 필수 명령어를 실행합니다:
    * 🌦️ **날씨 및 시간:** 날씨 맑음, 낮/밤 전환 등.
    * ⚙️ **게임 설정:** 난이도 변경, 게임모드 변경 등.
    * 📢 **방송 및 공지:** 화면 중앙 공지(Title), 액션바 메시지, 귓속말 기능.
    * 🛡️ **플레이어 관리:** 관리자 권한(OP) 부여/해제, 추방(Kick), 차단(Ban) 등.

### 🧩 **부가 기능 및 다국어**
* **플러그인 매니저:** 서버 플러그인을 활성화/비활성화하거나 삭제하여 관리할 수 있습니다.
* **다국어 지원:**
    * 🇰🇷 한국어 (Korean) 100%
    * 🇺🇸 영어 (English) 99%
    * 🇯🇵 일본어 (Japanese) 88%
    * 🇨🇳 중국어 (Simplified Chinese) 88%

---

## 🛠️ 기술 스택 (Tech Stack)

* **Backend:** Python (메인 로직), Eel (Python ↔ HTML 연결)
* **Frontend:** HTML, CSS, JavaScript (사용자 인터페이스)

---

## 📦 라이브러리 및 리소스 (Libraries & Resources)

이 프로젝트를 가능하게 해 준 오픈소스 라이브러리와 서비스에 감사드립니다.

### **Backend (Python)**
* **[Eel](https://github.com/python-eel/Eel):** Python으로 간단한 Electron 스타일의 HTML/JS GUI 앱을 만드는 라이브러리.
* **[psutil](https://github.com/giampaolo/psutil):** 시스템 프로세스 및 리소스 사용량(CPU/RAM)을 모니터링하는 크로스 플랫폼 라이브러리.
* **[requests](https://requests.readthedocs.io/):** API 통신 및 파일 다운로드를 위한 간결하고 우아한 HTTP 라이브러리.

### **Frontend (Web)**
* **[Pretendard](https://github.com/orioncactus/pretendard):** UI 전반에 사용된 깔끔하고 현대적인 다중 플랫폼 폰트 (jsDelivr 제공).
* **[Phosphor Icons](https://phosphoricons.com/):** 인터페이스에 사용된 유연하고 직관적인 아이콘 패밀리 (unpkg 제공).

### **APIs & Services**
* **[PaperMC API](https://papermc.io/):** 최신 마인크래프트 서버 빌드 정보를 가져오고 코어 파일을 다운로드하는 데 사용.
* **[Minotar API](https://minotar.net/):** 플레이어 관리 목록에서 사용자 스킨(얼굴) 이미지를 표시하는 데 사용.

> **그리고 여기에 명시적으로 적혀있지 않더라도, 이 프로젝트를 만드는 데 도움을 주신 모든 오픈소스 개발자분들께 진심으로 감사를 전합니다.**

---

## ⚠️ 면책 조항 및 라이선스

* **AI 지원:** 이 프로그램의 일부 기능과 코드 구조는 AI 기술의 도움을 받아 작성되었습니다.
* **책임의 한계:** 이 프로그램 사용으로 인해 발생하는 치명적인 문제에 대해 제작자는 책임을 지지 않으며, 리포지토리는 사전 예고 없이 비공개 전환될 수 있습니다.
* **법적 고지:** 이 앱은 **Mojang AB 또는 Microsoft Corporation과 어떠한 관련도 없습니다.**

❤️ **Created with love by JIN**
