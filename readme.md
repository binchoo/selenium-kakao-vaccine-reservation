# selenium-kakao-vaccine-reservation

## 개요

카카오 계정으로 로그인하고

카카오 맵에서 접종 지역을 선택하면

여분의 코로나 백신을 찾아 접종을 예약합니다. 

앱 실행은 접종 신청이 될 때까지 유지됩니다.

## 실행 방법

### python 3.7 이상

```
pip install -r requirements.txt
python main.py
```

## 진행 순서

1. ### 카카오 계정에 로그인 하기

   앱 실행시 인터넷 브라우저가 실행되어(크롬) 카카오 로그인 페이지가 보입니다. 

   자신의 카카오 계정에 로그인하세요. 로그인이 완료되면 브라우저가 자동으로 닫힙니다.

   로그인 정보는 앱이 백신 접종을 신청하기 위한 필수 정보입니다.

2. ### 유저 정보 검증 절차

   입력하신 유저 정보를 앱이 검증합니다: 계정은 백신 예약 서비스에 *정보이용제공동의*가 되어 있어야 합니다.

   앱을 사용하기 이전에, 카카오톡> 백신예약> 아무 병원 선택> 백신 알림 신청하여 정보이용제공동의에 수락하시길 바랍니다.

3. ### 접종 지역 선택하기

   이상이 없는 카카오 계정이라면, 다음 순서 '접종 지역 선택하기'로 진행할 수 있습니다.

   앱은 다시 한 번 브라우저를 띄워 카카오 맵을 보여줍니다.

   카카오 맵을 조작하면 앱의 커맨드 창에 아래와 같이 글씨가 올라옵니다.

   ```
   현재 보고있는 영역:
            좌상 [127.1170, 37.5543] 우하 [127.0603, 37.5992]
            CMD 창에서 Ctrl + C하면 이 영역을 백신 검색에 사용합니다.
   ```

   접종을 원하시는 지역이 보이도록 맵을 조정하세요. 그리고 앱의 커맨드에서 `콘트롤 + C` 버튼을 누르면 지역 설정이 완료됩니다!

4. ### 백신 유형 선택하기

   로그인 정보와 접종 지역 설정까지 마쳤다면, 마지막으로 백신 제작사를 선택합니다. 유저는 5가지 선택지를 보고 백신 코드를 입력하시면 됩니다.  `ANY`를 입력할 경우 어떤 백신이든 여분이 생기면 신청합니다.

   ```
        <백신 코드 일람>
   화이자         : VEN00013
   모더나         : VEN00014
   아스크라제네카   : VEN00015
   얀센          : VEN00016
   아무거나       : ANY
   ```

5. ### 백신 접종 예약이 신청될 때까지 기다리기

   설정을 모두 마쳤습니다. 이제부터 앱은 

   유저가 고른 지역에서, 선택한 유형의 백신 여분이 발견될 때까지 계속해서 탐색합니다.

   여분의 백신이 발견되면 당신을 대신하여 접종을 신청을 진행합니다.
   
## 권장 릴리스

https://github.com/binchoo/selenium-kakao-vaccine-reservation/releases/tag/Release1.0.1

## 코드 의존성

- [SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium/blob/trunk/LICENSE) Apache License 2.0
- [wkeeling/selenium-wire ](https://github.com/wkeeling/selenium-wire/blob/master/LICENSE) MIT License
- [SJang1/korea-covid-19-remaining-vaccine-macro](https://github.com/SJang1/korea-covid-19-remaining-vaccine-macro/blob/main/LICENSE) MIT License
- [SergeyPirogov/webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager/blob/master/LICENSE.txt) Apache License 2.0

## 라이센스

[MIT License](https://github.com/binchoo/selenium-kakao-vaccine-reservation/blob/master/LICENSE)
