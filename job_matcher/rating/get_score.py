import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
import config
from rating.prompts import system_prompt, get_rating_user_prompt

class rater:
  def __init__(self):
      self.api_key = config.OPENAI_API_KEY

      self.MODEL = config.MODEL_NAME

      self.openai = OpenAI()

  def get_rating(self,data,desc):
      response = self.openai.chat.completions.create(
          model=self.MODEL,
          messages=[
              {"role": "system", "content": system_prompt},
              {"role": "user", "content": get_rating_user_prompt(data,desc)}
        ],
          response_format={"type": "json_object"}
      )
      result = response.choices[0].message.content
      return json.loads(result)