from typing import Union # 테스트용
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import json,os,uuid
from ocr import do_ocr

# uvicorn main:app --reload 
app = FastAPI()

# Server Health Check
@app.get("/")
def read_root():
    return "FastAPI Server On!!"

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
        # LangChain의 프롬프트 사용해서 gpt api를 통한 노트 탬플릿 생성 수행
    except Exception as e:
        print(f"Error saving image: {e}")

    return genPageFail # 실패시 리턴

# 문제 1개 생성
'''
- 노트 한 페이지에 대한 텍스트 전달받기
- 전달받은 텍스트 바탕으로 퀴즈 생성하여 반환
'''
@app.get("/gen-problem")
def generateProblem():
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