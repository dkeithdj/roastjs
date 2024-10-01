import os
from datetime import datetime, timedelta

import google.generativeai as genai
from dotenv import load_dotenv
from fasthtml.common import (
    H1,
    A,
    Body,
    Button,
    Container,
    Div,
    FastHTML,
    Form,
    Grid,
    Link,
    Nav,
    P,
    Script,
    Title,
    add_toast,
    picolink,
    serve,
    setup_toasts,
    FileResponse
)
from lucide_fasthtml import Lucide

load_dotenv()

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

# Set up the app, including daisyui and tailwind for the chat component
tlink = (Script(src="https://cdn.tailwindcss.com"),)
dlink = Link(
    rel="stylesheet",
    href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css",
)
favicon = Link(rel="icon", type="image/x-icon", href="favicon.ico")

app = FastHTML(hdrs=(tlink, dlink, picolink, favicon))

setup_toasts(app)

# Set up a chat model (https://claudette.answer.ai/)
# cli = Client(models[0])
sp = """You are a helpful and concise assistant."""
rate_limit_duration = timedelta(seconds=5)
last_message_time = None  # Track when the last message was sent


def ChatMessage(msg):
    return Div(
        Div(
            P(msg, id="chat-message", cls="text-primary-content"),
            Div(
                Button(
                    "Copy",
                    cls="btn",
                    hx_on_click='navigator.clipboard.writeText(document.querySelector("#chat-message").innerText).then(() => alert("Copied to clipboard!"), (e) => console.error(e))',
                ),
                cls="card-actions justify-end",
            ),
            cls="card-body",
        ),
        cls="card bg-primary shadow-xl",
    )


# The input field for the user message. Also used to clear the
# input field after sending a message via an OOB swap
def ChatButton():
    return Button(
        "Roast it!",
        type="submit",
        name="msg",
        id="msg-input",
        cls="btn btn-primary",
        hx_swap_oob="true",
    )


def Footer():
    return Container(
        Div(
            # Navigation Links
            Nav(
                Grid(
                    A(
                        "denreikeith.me",
                        href="https://denreikeith.me",
                        target="_blank",
                        cls="link link-hover",
                    ),
                    cls="grid-flow-col gap-4",
                )
            ),
            # Social Media Icons
            Nav(
                A(
                    Lucide("github", cls="fill-current"),
                    href="https://github.com/dkeithdj/roastjs",
                    target="_blank",
                ),
                A(
                    Lucide("linkedin", cls="fill-current"),
                    href="https://www.linkedin.com/in/denreikeith/",
                    target="_blank",
                ),
                A(
                    Lucide("twitter", cls="fill-current"),
                    href="https://www.x.com/_denreikeith/",
                    target="_blank",
                ),
                cls="flex",
            ),
            # Copyright Notice
            Div(
                P(
                    f"Copyright © {datetime.now().year} - All rights reserved by denreikeith."
                )
            ),
            cls="footer footer-center bg-base-200 text-base-content rounded p-10",
        )
    )

@app.route("/{fname:path}.{ext:static}")
def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

# The main screen
@app.route("/")
def get():
    page = Body(
        H1("Roast JS 🔥", cls="text-center text-3xl font-bold mt-4 mb-2"),
        H1("100% JS-less, 100% Python", cls="text-center italic"),
        Div(
            "Made with ",
            A(
                "FastHTML",
                href="https://fastht.ml",
                target="_blank",
                cls="link link-hover mt-4",
            ),
            cls="text-center text-sm mt-2 mb-2",
        ),
        Div(id="chatlist", cls=""),
        Form(
            ChatButton(),
            hx_post="/post",
            hx_target="#chatlist",
            cls="flex space-x-2 mt-2",
        ),
        Footer(),
        cls="p-4 max-w-lg mx-auto",
    )

    return Title("RoastJS"), page


# Handle the form submission
@app.route("/post")
def post(session):
    global last_message_time
    now = datetime.now()

    # Check rate limit
    if last_message_time and now - last_message_time < rate_limit_duration:
        Div(
            add_toast(
                session,
                "Rate limit exceeded. Please wait before sending another message.",
                "error",
            )
        )
        return Div(
            hx_out="outerHTML",
        )

    last_message_time = now  # Update last message time

    try:
        response = model.generate_content(
            "You are a witty assistant asked to create a light-hearted roast. tell me a roast about javascript, make it comedic. 2 sentences. be a bit harsh, make it unique"
        )

        if not response.text:
            return Div(
                add_toast(session, "An error occurred. Please try again later.", "warn")
            )
        return (ChatMessage(response.text),)  # The chatbot's response
    except Exception as e:
        return Div(
            add_toast(session, "An error occurred. Please try again later.", "error")
    )


serve()
