from typing import Union # 테스트용
from fastapi import FastAPI,UploadFile, Request
import os,uuid
from ocr import do_ocr
from pdf_reader import pdf_to_text # pdf에서 text추출
from gpt_api import gpt_sum, gpt_pro
import re,difflib

# uvicorn main:app --reload 
app = FastAPI()

# Server Health Check
@app.get("/")
def read_root():
    return "FastAPI Server On!!"


# GPT가 번호를 함께 생성하지 않는 경우 방지용
# 유사도 가장 높은 번호 찾기
def closest_answer(answer, selections):
    max_ratio = -1
    index = -1
    
    for i, sel in enumerate(selections):
        s = difflib.SequenceMatcher(None, answer, sel)
        ratio = s.ratio()
        
        if ratio > max_ratio:
            max_ratio = ratio
            index = i + 1
            
    return str(index)


# 이미지 multipart로 전달 받아서 텍스트 추출
# pip install python-multipart
'''
- multipart로 노트 이미지 전달받기
- 이미지 ocr 실시
- ocr 결과물 바탕으로 노트 한 페이지 생성
'''
# 주의 : 클라이언트에서 image라는 키값으로 이미지를 전송해야함
@app.post("/image-to-text")
async def imageToText(image : UploadFile): 
    UPLOAD_DIR = "./images" # 이미지 저장 경로

    image_content = await image.read()
    filename = f"{str(uuid.uuid4())}.jpg" # 이미지 이름 설정

    try:
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
            fp.write(image_content)  # 서버 로컬 스토리지에 이미지 저장

        image_path = f"{UPLOAD_DIR}/{filename}" # 저장된 이미지 경로

        # OCR
        result,annotation = do_ocr(image_path)
        print("result = ", result) # ocr을 통해 추출한 텍스트
        print("annotaion = ",annotation) # ocr을 통해 추출한 키워드

        # gpt api
        # get_sum에 요약할 내용 입력 + 키워드 전달
        sum_result = gpt_sum(result,annotation)

        # 정규 표현식을 사용하여 제목과 요약 추출
        title_match = re.search(r'\[(.*?)\]', sum_result)

        # title 추출
        title = title_match.group(1) if title_match else ""

        # title 부분을 제거하고 나머지를 summary에 저장
        summary = re.sub(r'\[.*?\]', '', sum_result).strip()

        # 결과 출력
        print("Title:", title)
        print("Summary:", summary)

        # 분류 결과를 스마트폰으로 반환 (JSON 형태로 반환)
        response_data = {
            'text': result,
            'title' : title,
            'summary' : summary,
            'sum_result' : sum_result
        }
        
        return response_data

    except Exception as e:
        print(f"Error saving image: {e}")

    return genPageFail # 실패시 리턴

# 문제 1개 생성
'''
- 노트 한 페이지에 대한 텍스트 전달받기
- 전달받은 텍스트 바탕으로 퀴즈 생성하여 반환
'''
@app.post("/gen-problem")
async def generateProblem(request: Request):
    try:
        # 요청 본문을 바이트 문자열로 읽음
        body_bytes = await request.body()
        # 바이트 문자열을 문자열로 디코딩 (UTF-8 사용)
        content = body_bytes.decode('utf-8')
        
        print("===========content==============")
        print(content)
        
        problem_result = gpt_pro(content)
        
        # 각 질문을 분리하기 위한 패턴
        problems = re.split(r'\n{2,}', problem_result)
        ques, selec, ans, comment = "", "", "", ""

        for i, problem in enumerate(problems):
            print(f"problem #{i + 1}: {problem}")
            pattern = r'&([^&]+)&([\s\S]*?)%([^%]+)%([^@]+)@([\s\S]*)'
            match = re.search(pattern, problem)

            if match:
                question = match.group(1).strip()
                selections = [sel.strip() for sel in match.group(2).split('#') if sel.strip()]
                answer = match.group(3).strip()
                
                # GPT가 번호를 알려주지 않는 상태 방지
                if not answer.isdigit():
                    answer = closest_answer(answer, selections)
                else:
                    answer = re.search(r'(\d+)', answer).group(1)

                commentary = match.group(5).replace('@', '').strip()
                ques += f"[{question}]"
                selec += "[" + "][".join(selections) + "]"
                ans += f"[{answer}]"
                comment += f"[{commentary}]"
        
        response_data = {
            "question": ques,
            "selections": selec,
            "answer": ans,
            "commentary": comment
        }
        
        return response_data
    
    except Exception as e:
        print(f"Error saving image: {e}")
        
    return genQuizFail


# ocr 테스트용 api
@app.get("/ocr-test")
def ocrTest():
    result,annotation = do_ocr("./images/book.jpg")
    print("result : " + result)
    
    response_data = {
        "result" : result
    }
    return response_data


# pdf multipart로 전달 받아서 텍스트 추출
# pip install python-multipart
# 클라이언트로부터 pdf라는 키 값으로 pdf파일을 전달 받아야 한다.
@app.post("/pdf-to-text")
async def pdfToText(pdf : UploadFile): 
    UPLOAD_DIR = "./pdf" # pdf 파일 저장 경로

    pdf_file = await pdf.read()
    filename = f"{str(uuid.uuid4())}.pdf" # pdf 파일 이름 생성

    try:
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
            fp.write(pdf_file)  # 서버 로컬 스토리지에 pdf파일 저장

        file_path = f"{UPLOAD_DIR}/{filename}" # 저장된 pdf파일 경로

        # pdf에서 글자 추출
        result = pdf_to_text(file_path)
        print("result = ", result) # pdf에서 추출한 텍스트들
        
        # gpt api
        # get_sum에 요약할 내용 입력 + 키워드 전달
        sum_result = gpt_sum(result,[]) # pdf로 파일 읽을 경우 annotaion은 없음(빈 배열로 설정)

        # 정규 표현식을 사용하여 제목과 요약 추출
        title_match = re.search(r'\[(.*?)\]', sum_result)

        # title 추출
        title = title_match.group(1) if title_match else ""

        # title 부분을 제거하고 나머지를 summary에 저장
        summary = re.sub(r'\[.*?\]', '', sum_result).strip()

        # 결과 출력
        print("Title:", title)
        print("Summary:", summary)

        # 분류 결과를 스마트폰으로 반환 (JSON 형태로 반환)
        response_data = {
            'text': result,
            'title' : title,
            'summary' : summary,
            'sum_result' : sum_result
        }
    
        return response_data

    except Exception as e:
        print(f"Error saving image: {e}")

    return genPageFail # 실패시 리턴




# 페이지 생성 실패시 반환
genPageFail = {
    'text': "fail",
    'title' : "fail",
    'summary' : "fail",
    'sum_result' : "fail"
}

# 퀴즈 생성 실패시 반환할 json 데이터
genQuizFail = {
    "question": "[fail]",
    "selections": "[fail][fail][fail][fail]",
    "answer": "[fail]",
    "commentary" : "[fail]"
}