import os
from langchain_community.llms import OpenAI                         # To call OpenAI API
from langchain_groq import ChatGroq              # To call OpenAI Chat API
from langchain.prompts import PromptTemplate              # To create prompt templates
from langchain.chains import LLMChain                     # To create chains of calls to LLMs
from langchain.chains import SequentialChain
# from langchain.callbacks import get_openai_callback       # To track token usage
import os
import json
import pandas as pd
import traceback                                          # For error handling
from dotenv import load_dotenv                            # For storing environment variables in local workspace
import PyPDF2

load_dotenv(dotenv_path="C:\\Users\\hp\\Desktop\\Projects\\MCQ Generator\\experiment\\.env") # Load environment variables from .env file

key=os.getenv("GROQ_API_KEY")



llm = ChatGroq(
    groq_api_key=key,
    model_name="llama-3.1-8b-instant",   # or "mixtral-8x7b-32768"
    temperature=0.7
)



# with open("Response.json","r") as f:
#     RESPONSE_JSON=json.load(f)

# print(RESPONSE_JSON)


TEMPLATE = """
Text: {text}

You are an expert MCQ maker. 
Create exactly {number} multiple choice questions for {subject} students in {tone} tone. 

⚠️ Rules:
- Output MUST be valid JSON.
- Follow the structure in RESPONSE_JSON exactly.
- Do not add Python-style dicts, only JSON (keys/strings in double quotes).
- Ensure all {number} questions are unique and relevant to the text.


### RESPONSE_JSON (example format)
{RESPONSE_JSON}
"""


quiz_generation_prompt=PromptTemplate(
    input_variables=["text","number","subject","tone","RESPONSE_JSON"],
    template=TEMPLATE
)


quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz",verbose=True)


TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""



quiz_evaluation_prompt=PromptTemplate(
    input_variables=["text","number","subject","tone","RESPONSE_JSON"],
    template=TEMPLATE2
)



review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review",verbose=True)



generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "RESPONSE_JSON"],
    output_variables=["quiz", "review"],
    verbose=True,
)

# PATH="data.txt"

# with open(PATH, "r") as file:
#     TEXT=file.read()

# print(TEXT)

# generate_evaluate_chain

# TEXT
# NUMBER=5
# SUBJECT='GENAI'
# TONE='SIMPLE'
# RESPONSE_JSON=RESPONSE_JSON

# RESPONSE_JSON

# json.dumps(RESPONSE_JSON)     # To convert Python dictionary to JSON string

# response=generate_evaluate_chain(
#     {

#     "text":TEXT,
#     "number": NUMBER,
#     "subject": SUBJECT,
#     "tone": TONE,
#     "RESPONSE_JSON":json.dumps(RESPONSE_JSON, indent=2)
#     }
# )

# response

# quiz=response.get("quiz")

# quiz=json.loads(quiz)

# quiz

# quiz_table_data = []
# for key, value in quiz.items():
#     mcq = value["mcq"]
#     options = " | ".join(
#         [
#             f"{option}: {option_value}"
#             for option, option_value in value["options"].items()
#             ]
#         )
#     correct = value["correct"]
#     quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

# quiz_table_data

# quiz=pd.DataFrame(quiz_table_data)

# quiz.to_csv("genai.csv", index=False)