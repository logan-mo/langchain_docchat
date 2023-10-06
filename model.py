from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


import random
import glob
import os

import pandas as pd
from pandasai import SmartDataframe

DOC_DIR = "documents"


class Model:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            openai_api_key=api_key, model_name="gpt-4", temperature=0.5
        )
        self.smart_dataframes = {}
        for user_id in os.listdir(DOC_DIR):
            doc_path = glob.glob(os.path.join(DOC_DIR, user_id, "*.csv"))[0]
            df = pd.read_csv(doc_path)
            self.smart_dataframes[user_id] = SmartDataframe(
                df, config={"verbose": False, "llm": self.llm}
            )

    def generate(self, prompt: str, user_id: str):
        smart_df = self.smart_dataframes[user_id]
        response = smart_df.chat(prompt)
        return response
