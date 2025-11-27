"""
2025-11-09
File: unittest.py
Author: RuneShell
      dlhj09@naver.com
      https://github.com/RuneShell
Locate: https://github.com/RuneShell/Text_Encryptor
----------------------------------
Brief: Test [CeasorHash.pyd] module using python unittest
"""

import CeasorHash # ★ module built in python 3.10.5

from unittest import main, TestCase, mock
import time


# Result of this file
"""
[Test 1] (Normal Case)

.
[Test 2] (Failure Case)
'[ Aegukga ]\n1. 동해물과 백두산이 마르고 닳도록 하느님이 보우[268 chars]보전하세' != 'x c<?p;_] %\n*@ 떼쾻뢿텍 땂덷펖뿦 챠뢻갠 퓟쯯쮒 틙냙뙉쑠 훣쎴[268 chars]챺얎쫷챤'
- [ Aegukga ]
- 1. 동해물과 백두산이 마르고 닳도록 하느님이 보우하사 우리나라 만세 무궁화 삼천리 화려 강산 대한 사람 대한으로 길이 보전하세
- 2. 남산 위에 저 소나무 철갑을 두른 듯 바람 서리 불변함은 우리 기상일세 무궁화 삼천리 화려 강산 대한 사람 대한으로 길이 보전하세
- 3. 가을 하늘 공활한데 높고 구름 없이 밝은 달은 우리 가슴 일편 단심일세 무궁화 삼천리 화려 강산 대한 사람 대한으로 길이 보전하세
- 4. 이 기상과 이 맘으로 충성을 다하여 괴로우나 즐거우나 나라 사랑하세 무궁화 삼천리 화려 강산 대한 사람 대한으로 길이 보전하세+ x c<?p;_] %
+ *@ 떼쾻뢿텍 땂덷펖뿦 챠뢻갠 퓟쯯쮒 틙냙뙉쑠 훣쎴씽꼎 괨겛쉵뵁 얁뎁 독쩒뗵 옻쳳쐒 뺀덤 꼛쌀 끶캯 뫌뤥 끕꽇댫핒 뜧쮢 씸쁾뮲쮂
+ /Z 즖똏 콭누 윻 텶묆퐓 쏨괱풕 욌뭳 툪 긥춿 벬똜 뼙격쾟뙊 셮갓 꼪떽뻇읞 쬙졀뢪 푫횳틂 뇋돤 툠솳 켚둇 퉁뢡 햲쥺잎뺢 섰뢞 횥쯣펎얒
+ $z 잯렦 픂긳 뤺츙섨핬 꿐쪺 쪲쑕 볋플 붝휽 팈넮 쟣릷 뭛떦 띻선 픙쪌퓈눘 민닶힟 큒굙왃 릱띲 췵쾩 뷷닋 뭦곭 뀦쩞쇻찅 젫뾷 셒룇쟱츿
+ wU 싂 좧좧챔 쫻 촣솮뷅 뚯턠믝 램냕눫 껉괐졯암 떘씊꾙먫 삜닪 뇦뻭꿑퇦 촙쥳컼 룾졨사 껴똘 뾜째 쌖뀆 눖쩩 괯닔댟왚 켆쩧 챺얎쫷챤

.
[Test 3] (Speed Measurement)
Input String Length :  309
Mean time per 1 Encryption & Decryption:  0.06874  ms
Mean time per 1 Encryption & Decryption per 1 letter:  0.00022  ms
.
----------------------------------------------------------------------
Ran 3 tests in 0.073s

OK
"""


class TestCeasorHash(TestCase):
    __ceasorHash = CeasorHash.CeasorHash() 

    __raw_data = """[ Aegukga ]
1. 동해물과 백두산이 마르고 닳도록 하느님이 보우하사 우리나라 만세 무궁화 삼천리 화려 강산 대한 사람 대한으로 길이 보전하세
2. 남산 위에 저 소나무 철갑을 두른 듯 바람 서리 불변함은 우리 기상일세 무궁화 삼천리 화려 강산 대한 사람 대한으로 길이 보전하세
3. 가을 하늘 공활한데 높고 구름 없이 밝은 달은 우리 가슴 일편 단심일세 무궁화 삼천리 화려 강산 대한 사람 대한으로 길이 보전하세
4. 이 기상과 이 맘으로 충성을 다하여 괴로우나 즐거우나 나라 사랑하세 무궁화 삼천리 화려 강산 대한 사람 대한으로 길이 보전하세"""

    __pw = "1234"


    # Test Normal Case
    def test_encryption_1(self):
        print("[Test 1] (Normal Case)")
        
        coded_data = list(self.__raw_data.encode("utf-8"))
        coded_pw = list(self.__pw.encode("utf-8"))

        try:
            encoded_data = self.__ceasorHash.EncryptWithCeasorHash(coded_data, coded_pw, True, 1) # encrypt
            decoded_data = self.__ceasorHash.EncryptWithCeasorHash(encoded_data, coded_pw, False, 1) # decrypt
            decoded_data = bytes(decoded_data).decode("utf-8")

            self.assertEqual(self.__raw_data, decoded_data)

        except AssertionError as e:
            print(e)
        finally:
            print()


    # Test Failure Case
    def test_encryption_2(self):
        print("\n[Test 2] (Failure Case)")
        coded_data = list(self.__raw_data.encode("utf-8"))
        coded_pw = list(self.__pw.encode("utf-8"))

        # Get Wrong password
        mock_obj = mock.Mock()
        mock_obj.toPlainText.return_value = "9876"
        wrong_pw = mock_obj.toPlainText()
        coded_wrong_pw = list(wrong_pw.encode("utf-8"))

        try:
            encoded_data = self.__ceasorHash.EncryptWithCeasorHash(coded_data, coded_pw, True, 1)
            decoded_data = self.__ceasorHash.EncryptWithCeasorHash(encoded_data, coded_wrong_pw, False, 1)
            decoded_data = bytes(decoded_data).decode("utf-8")

            self.assertEqual(self.__raw_data, decoded_data)

        except AssertionError as e:
            print(e)
        finally:
            print()
    

    # Measure Speed
    def test_encryption_3(self):
        print("\n[Test 3] (Speed Measurement)")

        len_raw_data = len(self.__raw_data)
        print("Input String Length : ", len_raw_data)
        coded_data = list(self.__raw_data.encode("utf-8"))
        coded_pw = list(self.__pw.encode("utf-8"))


        start_time = time.perf_counter()

        # Iterate Encryption & Decryption 1000 times
        for i in range(1000):
            encoded_data = self.__ceasorHash.EncryptWithCeasorHash(coded_data, coded_pw, True, 1)
            decoded_data = self.__ceasorHash.EncryptWithCeasorHash(encoded_data, coded_pw, False, 1)

        end_time = time.perf_counter()
        duration = end_time - start_time
        print("Mean time per 1 Encryption & Decryption: ", round(duration, 5), " ms") # (duration * 1000(s -> ms) / 1000(iteration) == duration)
        print("Mean time per 1 Encryption & Decryption per 1 letter: ", round(duration/len_raw_data, 5), " ms")




if(__name__ == "__main__"):
    main()