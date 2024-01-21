import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# git ignore를 위해 json에서 로드하도록 변경 필요
os.environ['OPENAI_API_KEY'] = 'input your api key'
chatgpt = ChatOpenAI(model_name ="gpt-3.5-turbo")

# answer = chatgpt.predict("why python is the most popular language? answer in Korean")
# print(answer)


summarize_note_template = '''
당신은 노트를 필기하는 학생입니다. 
제공하는 글을 대상으로 제목을 포함하여 노트를 필기하세요. 
요구사항은 아래와 같습니다. 
1. 7줄 이하의 필기노트를 작성하세요. 
2. 핵심 키워드 혹은 핵심 문장은 문자열 가장 마지막줄에 "키워드 : ['사과','아카네'...] 등으로 주어집니다. 핵심 문장을 바탕으로 노트를 작성하세요. 제공되는 키워드가 없을수도 있습니다.
3. 노트의 제목은 []로 표현해야 하고, 마지막 문장을 제외한 각 문장의 끝은 \n\n으로 표기합니다.
4. 노트의 각 문장은 '명사 : 설명' 과 같은 형식으로 작성하도록 합니다. 노트의 문장은 가능한한 짧게 작성합니다.
'''

generate_quiz_template = '''
당신의 역할은 4지선다 객관식 문제를 4개 만드는 것입니다.
아래 규칙을 따라 문제를 만들어주세요.
1. 입력으로 문자열이 주어집니다. 이 문자열을 대상으로 문제를 만들면 됩니다.
2. 문제의 시작과 끝은 &로 감쌉니다. 예를 들어 &다음중 사과의 색이 아닌것을 고르시오& 와 같습니다.
3. 객관식은 #으로 시작하여 #으로 끝납니다. 예를 들어 
#1. 빨간색# 
#2. 노란색# 
#3. 초록색# 
#4. 보라색#
와 같습니다.
4. 문제에 대한 정답 번호를 제공해야합니다. 예를들어 위 문제의 경우 정답은 보라색이므로 정답 번호인 4를 리턴합니다.
정답의 번호는 %로 감싸서 제공합니다. %4%
5. 문제에 대한 해설을 제공해야합니다. 해설은 1줄에서 2줄 사이로 제공합니다. 해설은 @로 감싸서 제공합니다.
@사과는 빨간색,노란색,초록색 등의 색상을 갖는데 보락색은 존재하지 않으므로 정답은 4번입니다.@
'''