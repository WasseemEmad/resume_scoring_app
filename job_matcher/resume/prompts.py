system_prompt = """
You are an AI assistant tasked with classifying extracted text data from a resume.

Your job is to:
1. Identify all relevant skills (technical, soft skills, tools, frameworks, etc.)
2. Identify and extract personal details like: name, email, job title, years of experience, phone number.
3. If a field is missing (like name or email), make a **reasonable prediction** based on available data.

You must respond in **valid JSON format** with two top-level keys:
- "Skills": a list of skill objects, each with "type" and "skill".
- "Details": a list of personal information as key-value pairs.

Example response format:
{
  "Skills": [
    {"type": "Programming Language", "skill": "Python"},
    {"type": "Framework", "skill": "TensorFlow"}
  ],
  "Details": [
    {"name": "Tony Emad"},
    {"email": "tony@example.com"},
    {"job": "Machine Learning Engineer"},
    {"experience": "Entry level"},
    {"phone_number": "01220001220"}
  ]
}
Do not add extra text, explanations, or formatting — only output valid JSON.
"""


def get_data_user_prompt(extracted_data):
    user_prompt = (
        f"The following is extracted resume data:\n\n{extracted_data}\n\n"
        "Please classify each item into either a skill or a personal detail, "
        "based on the format and instructions provided earlier. "
        "Return your response strictly in valid JSON."
    )
    return user_prompt