url = {
    'kakao': {
        'login_page': "https://accounts.kakao.com/login?continue=https%3A%2F%2Fcs.kakao.com%2F",
        'continue_page': "https://cs.kakao.com/",
        'map_page': "https://vaccine-map.kakao.com/map2?v=1",
        'user_info_api': "https://vaccine.kakao.com/api/v1/user",
        'left_by_coords': "https://vaccine-map.kakao.com/api/v3/vaccine/left_count_by_coords",
        'org_inventory': 'https://vaccine.kakao.com/api/v2/org/org_code/{}',
        'reservation': 'https://vaccine.kakao.com/api/v2/reservation'
    }
}

header = {
    'kakao': {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=utf-8',
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; SM-G977N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.164 Mobile Safari/537.36;KAKAOTALK 2309420",
        'Origin': 'https://vaccine.kakao.com',
        'Connection': 'Keep-Alive',
        'Keep-Alive': 'timeout=5, max=1000'
    }
}

CONTEXT_PATH = 'context.json'
APP_VERSION = 1.1
APP_NAME = f'COVID-19 Vaccine Auto Reservation v{APP_VERSION}'
QAPP_STYLE = 'Fusion'

USER_VALIDITY_TEXT = {
    "E_RESPONSE": """
        사용자 정보를 불러오는데 실패하였습니다. 
        Chrome 브라우저에서 카카오에 제대로 로그인되어있는지 확인해주세요.
        로그인이 되어 있는데도 안된다면, 카카오톡에 들어가서 잔여백신 알림 신청을 한번 해보세요. 정보제공 동의가 나온다면 동의 후 다시 시도해주세요.""",
    "E_INVALID_STATUS": "사용자의 상태를 조회할 수 없었습니다.",
    "E_ALREDY_RESERVED": "이미 접종이 완료되었거나 예약이 완료된 사용자입니다.",
    "OK": "사용자 정보를 불러오는데 성공했습니다."
}

USER_VALIDITY_TO_VIEW_VALIDITY = {
    "E_RESPONSE": "expired",
    "E_INVALID_STATUS": "expired",
    "E_ALREADY_RESERVED": "expired",
    "OK": "ok"
}