import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
# from langchain.callbacks import get_openai_callback
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging



def display_mcq(index, question, options, answer):
    with st.container():
        st.markdown(
            f"""
            <div style="
                background-color: #1e1e1e;
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 15px;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
                color: #f0f0f0;
                font-family: 'Segoe UI', sans-serif;
            ">
                <h4 style="color:#00c4ff;">Q{index}. {question}</h4>
                <ul style="list-style-type: none; padding-left: 0; margin: 10px 0;">
                    {''.join([f"<li style='margin:6px 0;'><b style='color:#ffb703;'>{k}.</b> {v}</li>" for k, v in options.items()])}
                </ul>
                <p style="color: #90ee90; font-weight: bold; margin-top: 10px;">
                    ✅ Correct Answer: {answer}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )



st.markdown(
    """
    <style>
    body { background-color: #0e1117; color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #6C63FF, #00C9FF);
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)



#Loading JSON FILE
with open(r'C:\Users\hp\Desktop\Projects\MCQ Generator\experiment\Response.json','r') as file:
    RESPONSE_JSON= json.load(file)


# Creating a title for an app
# st.title("QuizForge – “Where quizzes are forged instantly.”")

st.markdown(
    """
    <h1 style='text-align: center; color: #6C63FF;'>
        ✨ QuizForge ✨
    </h1>
    <h3 style='text-align: center; color: gray;'>
        “Where quizzes are forged instantly.”
    </h3>
    <br>
    """,
    unsafe_allow_html=True
)



with st.form("User Input"):
    uploaded_file=st.file_uploader("Upload a pdf or text file")

    mcq_count=st.number_input("Number of MCQs", min_value=1, max_value=50)

    subject=st.text_input("Insert Subject", max_chars=20)

    tone=st.text_input("Complexity Level of Questions", max_chars=20, placeholder="Simple")

    button=st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text=read_file(uploaded_file)
                response=generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "RESPONSE_JSON": json.dumps(RESPONSE_JSON)
                    }
                )
                #st.write(response)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            
            else:
                if isinstance(response, dict):
                    # Extract quiz data from the response
                    quiz = response.get("quiz", None)
                    if quiz:
                        table_data = get_table_data(quiz)
                        if table_data:
                            # df = pd.DataFrame(table_data)
                            # df.index = df.index + 1
                            # st.table(df)
                            for i, row in enumerate(table_data, start=1):
                                display_mcq(i, row["MCQ"], row["Choices"], row["Correct"])

                            # st.text_area(label="Review", value=response.get("review", ""))
                            st.markdown(
                                f"""
                                <div style="background-color:#1e293b; color:#e2e8f0; padding:15px; border-radius:10px; margin-top:20px;">
                                    <h4>📊 Quiz Review</h4>
                                    <p>{response.get("review", "")}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        else:
                            st.error("Failed to parse quiz data (check PDF content or model output).")
                    else:
                        st.error("No quiz found in response.")



                





