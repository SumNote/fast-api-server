from typing import Union # 테스트용
from fastapi import FastAPI
import json

app = FastAPI()

# Server Health Check
@app.get("/")
def read_root():
    return "FastAPI Server On!!"

# 이미지 multipart로 전달 받아서 텍스트 추출
'''
- multipart로 노트 이미지 전달받기
- 이미지 ocr 실시
- ocr 결과물 바탕으로 노트 한 페이지 생성
'''
@app.get("/image-to-text")
def imageToText():
    return genPageFail

# 문제 1개 생성
'''
- 노트 한 페이지에 대한 텍스트 전달받기
- 전달받은 텍스트 바탕으로 퀴즈 생성하여 반환
'''
@app.get("/gen-problem")
def generateProblem():
    return genQuizFail




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