# selenium-kakao-vaccine-reservation

## 개요

카카오 계정으로 로그인하고

카카오 맵에서 접종 지역을 선택하면

여분의 코로나 백신을 찾아 접종을 예약합니다. 

앱 실행은 접종 신청이 될 때까지 유지됩니다.

## 권장 릴리스

https://github.com/binchoo/selenium-kakao-vaccine-reservation/releases/tag/1.1

## 실행 방법
릴리스에 업로드한 실행 파일을 실행하거나, 소스 코드를 내려받아 파이썬으로 실행합니다.

### 실행 파일을 사용시
  - `qtmain.exe` - 윈도우용 실행파일 
  - 맥OS용 실행파일은 아직 지원하지 않습니다. 이미 내장된 파이썬을 이용해 보십시오.

### python 3.7 이상을 사용시
GUI 애플리케이션
```bash
pip install -r requirements.txt
python qtmain.py
```

## 진행 순서

1. ### 카카오 계정에 로그인 하기

   `브라우저로 로그인` 버튼을 눌러서 브라우저를 엽니다. 가장 최초에 브라우저를 열 때 필요한 설치 몇 가지가 진행되어 속도가 더딜 수 있습니다.

   자신의 카카오 계정에 로그인하세요. 로그인이 완료되면 브라우저가 자동으로 닫힙니다.

   로그인 정보는 앱이 백신 접종을 신청하기 위한 필수 정보입니다.
   
   ![login_button](https://user-images.githubusercontent.com/15683098/128219902-8748b2b8-b8cd-4ea5-af23-ae9521a0f59c.gif)

2. ### 유저 정보 검증 절차

   입력하신 유저 정보를 앱이 검증합니다: 계정은 백신 예약 서비스에 *정보이용제공동의*가 되어 있어야 합니다.

   앱을 사용하기 이전에, 카카오톡> 백신예약> 아무 병원 선택> 백신 알림 신청하여 정보이용제공동의에 수락하시길 바랍니다.
   
   ![image](https://user-images.githubusercontent.com/15683098/128220027-5d182dfb-8cf7-461c-ab69-a15d1c62eafe.png)

3. ### 접종 지역 선택하기

   `브라우저로 탐지` 버튼을 눌러 다시 브라우저를 띄웁니다.

   나타난 카카오 맵을 조작하면 앱의 커맨드 창에 아래와 같이 글씨가 올라옵니다. 이 값은 GUI에도 업데이트 됩니다.

   ```
   현재 보고있는 영역:
            좌상 [127.1170, 37.5543] 우하 [127.0603, 37.5992]
            브라우저를 닫으면 이 영역을 백신 검색에 사용합니다.
   ```

   접종을 원하시는 지역이 보이도록 맵을 조정하세요. **브라우저를 닫거나** CMD에서 `콘트롤 + C` 버튼을 누르면 지역 설정이 완료됩니다!
   
   ![region_button](https://user-images.githubusercontent.com/15683098/128219908-b9e2a935-9307-43e5-a47d-77d2e86c2de6.gif)

4. ### 백신 유형 선택하기

   ![image](https://user-images.githubusercontent.com/15683098/128715052-21067835-da7a-45f6-a63b-df9af2fedb0c.png)
   
   기본값은 화이자/모더나 백신입니다. 원하는 유형의 백신을 선택하십시오. 앱은 해당하는 백신에 대해서만 예약을 신청합니다.

5. ### 백신 접종 예약이 신청될 때까지 기다리기

   설정을 모두 마쳤다면, 매크로 수행 버튼이 활성화됩니다.

   매크로는 유저가 고른 지역에서, 선택한 백신 여분이 발견될 때까지 계속해서 탐색하고

   여분의 백신이 발견되면 당신을 대신하여 접종을 신청을 진행합니다.
   
   ![image](https://user-images.githubusercontent.com/15683098/128220071-76dd55cc-0adb-4159-9985-9b120013bb4a.png)
   
   ![GIF 2021-08-05 오후 7-34-37](https://user-images.githubusercontent.com/15683098/128337800-a8dd6b91-05ab-4587-9197-3610524acf99.gif)

## 코드 의존성

- [SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium/blob/trunk/LICENSE) Apache License 2.0
- [wkeeling/selenium-wire ](https://github.com/wkeeling/selenium-wire/blob/master/LICENSE) MIT License
- [SJang1/korea-covid-19-remaining-vaccine-macro](https://github.com/SJang1/korea-covid-19-remaining-vaccine-macro/blob/main/LICENSE) MIT License
- [SergeyPirogov/webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager/blob/master/LICENSE.txt) Apache License 2.0
- [PyQt5](https://www.riverbankcomputing.com/static/Docs/PyQt5/introduction.html#license) Riverbank Commercial License && GPLv3

## 라이센스

[GPLv3](LICENSE) 
