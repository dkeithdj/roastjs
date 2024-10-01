import os

import google.generativeai as genai

# from claudette import Client, models, contents
import uvicorn
from dotenv import load_dotenv
from fasthtml.common import (
    H1,
    Body,
    Button,
    Div,
    FastHTML,
    Form,
    Group,
    Input,
    Link,
    Script,
    Title,
    picolink,
    serve,
    Container,
    Socials,
    Card,
    P, A, Titled
)

load_dotenv()

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# Set up the app, including daisyui and tailwind for the chat component
tlink = (Script(src="https://cdn.tailwindcss.com"),)
dlink = Link(
    rel="stylesheet",
    href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css",
)
app = FastHTML(hdrs=(tlink, dlink, picolink))

# Set up a chat model (https://claudette.answer.ai/)
# cli = Client(models[0])
sp = """You are a helpful and concise assistant."""
messages = []


# Chat message component (renders a chat bubble)
def ChatMessage(msg):
    bubble_class = (
        "chat-bubble-primary" if msg["role"] == "user" else "chat-bubble-secondary"
    )
    chat_class = "chat-end" if msg["role"] == "user" else "chat-start"
    return Div(
        Div(msg["role"], cls="chat-header"),
        Div(msg["content"], cls=f"chat-bubble {bubble_class}"),
        cls=f"chat {chat_class}",
    )


# The input field for the user message. Also used to clear the
# input field after sending a message via an OOB swap
def ChatInput():
    return Input(
        type="text",
        name="msg",
        id="msg-input",
        placeholder="Type a message",
        cls="input input-bordered w-full",
        hx_swap_oob="true",
    )

# The main screen
@app.route("/")
def get():
    page = Body(
        H1("Roast JS 🔥", cls="text-center text-3xl font-bold mt-4 mb-2"),
        Div(
            *[ChatMessage(msg) for msg in messages],
            id="chatlist",
            cls="chat-box h-[73vh] overflow-y-auto",
        ),
        Form(
            Group(ChatInput(), Button("Send", cls="btn btn-primary")),
            hx_post="/",
            hx_target="#chatlist",
            hx_swap="beforeend",
            cls="flex space-x-2 mt-2",
        ),
        cls="p-4 max-w-lg mx-auto",
    )
    return Title("Chatbot Demo"), page

# Handle the form submission
@app.route("/")
def post(msg: str):
    print(msg)
    messages.append({"role": "user", "content": msg})
    response = model.generate_content(
        "You are a witty assistant asked to create a light-hearted roast. tell me a roast about javascript, make it comedic. 2 sentences. be a bit harsh"
    )
    print(response.text)
    # r = cli(messages, sp=sp)  # get response from chat model
    messages.append({"role": "assistant", "content": response.text})
    return (
        # ChatMessage(messages[-2]),  # The user's message
        ChatMessage(messages[-1]),  # The chatbot's response
        # ChatInput(),
    )  # And clear the input field via an OOB swap

serve()

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
