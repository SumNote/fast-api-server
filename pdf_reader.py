import PyPDF2 # pip install PyPDF2
import os
# pdf에서 글자 추출
# 라이브러리 사용 예정
def pdf_to_text(file_path):
    text = ""  # pdf 파일의 텍스트 정보 저장용
    # title = author = None  # 문서 정보를 저장할 변수 초기화
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            # 페이지 수 얻기
            # num_pages = len(reader.pages)
            
            # 모든 페이지의 텍스트 추출
            for page in reader.pages:
                text += page.extract_text() + "\n"  # 각 페이지의 텍스트를 추가

            # 문서 정보 접근(pdf 파일 메타데이터, 파일 제목, 저자)
            # info = reader.document_info
            # title = info.title if info.title else "No Title"
            # author = info.author if info.author else "No Author"
    except FileNotFoundError as e: # 파일이 존재하지 않을 경우
        print("The file was not found:", e)
        return False
    except Exception as e:
        print("An error occurred:", e)
        return False
    return text # 우선 텍스트만 리턴