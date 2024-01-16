from typing import Union # 테스트용
from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 이미지 multipart로 전달 받아서 텍스트 추출
@app.get("/image-to-text")
def imageToText():
    response_data = {
        'text': "fail",
        'title' : "fail",
        'summary' : "fail",
        'sum_result' : "fail"
    }
    return response_data

# 문제 1개 생성
@app.get("/gen-problem")
def generateProblem():
    quiz = {
        "question": "[fail]",
        "selections": "[fail][fail][fail][fail]",
        "answer": "[fail]",
        "commentary" : "[fail]"
    }
    return quiz