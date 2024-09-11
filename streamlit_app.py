import streamlit as st
import pyshorteners
import qrcode
from io import BytesIO
from PIL import Image

# Streamlit 애플리케이션
st.title("URL 단축기 및 QR 코드 생성기")

# 사용자로부터 URL 입력 받기
original_url = st.text_input("단축할 URL을 입력하세요:")

# 단축 서비스 선택
service = st.selectbox("URL 단축 서비스 선택", ["TinyURL", "Bitly", "Is.gd"])

if st.button("단축하기"):
    if original_url:
        # pyshorteners 초기화
        s = pyshorteners.Shortener()

        try:
            # 선택한 서비스에 따라 URL 단축
            if service == "TinyURL":
                shortened_url = s.tinyurl.short(original_url)
            elif service == "Bitly":
                # Bitly의 경우 API 토큰이 필요합니다. 환경 변수나 설정 파일을 통해 설정할 수 있습니다.
                # 예를 들어, s.bitly.token = 'your_token_here'로 설정해야 합니다.
                s.bitly.token = 'your_bitly_access_token'  # 여기에서 실제 토큰으로 교체해야 합니다.
                shortened_url = s.bitly.short(original_url)
            elif service == "Is.gd":
                shortened_url = s.isgd.short(original_url)
            else:
                st.error("지원하지 않는 서비스입니다.")
                shortened_url = None

            if shortened_url:
                st.write(f"단축된 URL: {shortened_url}")

                # QR 코드 생성
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(shortened_url)
                qr.make(fit=True)

                # QR 이미지를 메모리 버퍼에 저장
                img = qr.make_image(fill='black', back_color='white')
                buf = BytesIO()
                img.save(buf)
                buf.seek(0)

                # Streamlit에서 이미지 표시
                st.image(buf, caption="단축된 URL의 QR 코드")

                # QR 코드 다운로드 링크 제공
                st.download_button(
                    label="QR 코드 다운로드",
                    data=buf,
                    file_name="qrcode.png",
                    mime="image/png"
                )

        except Exception as e:
            st.error(f"URL 단축 중 오류 발생: {e}")

    else:
        st.error("URL을 입력해 주세요.")
