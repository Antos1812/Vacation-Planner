# import gradio as gr
# from openai import OpenAI
# import os
# from dotenv import load_dotenv


# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://openrouter.ai/api/v1")


# def zapytaj_ai(prompt):
#     response = client.chat.completions.create(
#         model="openai/gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content.strip()

# with gr.Blocks() as demo:
#     gr.Markdown("## 🧳 Mini Planer Wakacji (OpenRouter + Gradio)")

#     input_text = gr.Textbox(label="Wpisz pytanie, np. 'Gdzie pojechać na wakacje?'")
#     output_text = gr.Textbox(label="Odpowiedź AI")

#     btn = gr.Button("Wyślij do AI")
#     btn.click(fn=zapytaj_ai, inputs=input_text, outputs=output_text)

# demo.launch()

import gradio as gr
import os
import openai
from dotenv import load_dotenv

load_dotenv() 

apiKey = os.getenv("OPENROUTER_API_KEY")  # Paste there API KEY
 
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=apiKey
)

def ask_travel_destinations(user_input):
    messages = [
        {
            "role": "system",
            "content": (
                "Jesteś asystentem Travel. Na podstawie preferencji użytkownika "
                "zaproponuj tylko JEDNĄ konkretną destynację (kraj). Nie podawaj listy. "
                "Odpowiedz krótko, samą nazwą kraju lub z krótkim uzasadnieniem."
            )
        },
        {"role": "user", "content": user_input}
    ]
    response = client.chat.completions.create(
        model="openai/gpt-4.1-nano",
        messages=messages
    )
    return response.choices[0].message.content.strip()

def create_travel_plan(destinations):
    messages = [
        {"role": "system", "content": "Jesteś agentem. Stwórz plan turystyczny, na podstawie podanych informacji i podanej destynacji."},
        {"role": "user", "content": destinations}
    ]

    response = client.chat.completions.create(
        model="openai/gpt-4.1-nano",
        messages=messages
    )
    return response.choices[0].message.content.strip()

def verify_plan(plan):
    messages = [
        {"role": "system", "content": "Jesteś asystentem weryfikującym. Sprawdź plan i wykonalność tego planu podróży."},
        {"role": "user", "content": plan}
    ]
    response = client.chat.completions.create(
        model="openai/gpt-4.1-nano",
        messages=messages
    )
    return response.choices[0].message.content.strip()

def full_planner(user_question):
    
    dest = ask_travel_destinations(user_question)
    
    
    plan = create_travel_plan(dest)
    
    
    verification = verify_plan(plan)
    
    return dest, plan, verification  

with gr.Blocks() as demo:
    gr.Markdown("## 🧳 Planer Wakacji – 3 Asystentów (Travel, Planner, Verifier) (▀̿Ĺ̯▀̿ ̿)")
    user_input = gr.Textbox(label="Opisz swoje preferencje 🤯🤯👽👽💀🤸‍♂️", placeholder="Jajco")
    btn = gr.Button("✅ZAAAAAACZNIJ✅  ＼(ﾟｰﾟ＼)")
    
    dest_output = gr.Textbox(label="Destynacje")
    plan_output = gr.Textbox(label="Plan podróży")
    verify_output = gr.Textbox(label="Weryfikacja planu")
    
    btn.click(full_planner, inputs=user_input, outputs=[dest_output, plan_output, verify_output])

if __name__ == "__main__":
    demo.launch()