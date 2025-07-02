from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyC79f8bbhGUs3FnKVRxFIdziuZC9kBL8Bg")

def generate_gemini_content(doc_type, sub_category, creativity, prompt):

    system_prompt = (
        "You are an expert content generator. "
        "Based on the provided document type, sub-category, creativity level, and user prompt, "
        "generate high-quality, original content tailored to that context. "
        "Ensure the output is clear, relevant, and fully aligned with the user's intent. "
        "Adapt tone and style based on the category and sub-category, and reflect the creativity level "
        "in the structure and language used."
        "give using some easy word don't use hard words"
        "give more specified and exact information about the prompt given"
    )

    user_prompt = (
        f"Document Type: {doc_type}\n"
        f"Sub-Category: {sub_category}\n"
        f"Creativity Level: {creativity}\n"
        f"Prompt: {prompt}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {"role": "user", "parts": [{"text": system_prompt}]},
                {"role": "user", "parts": [{"text": user_prompt}]},
            ],
            config=types.GenerateContentConfig(
                temperature=float(creativity) / 100
            )
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
