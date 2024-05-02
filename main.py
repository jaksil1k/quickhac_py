import time
from typing import Annotated

from fastapi import FastAPI, UploadFile, File

from file_gpt import upload_file, delete_file, upload_vs, delete_vs, get_assistant_id, create_thread, update_run, client
from config import THREAD_ID


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/file")
async def upload_file_endpoint(file_id):
    # upload_vs(file_id)

    thread_message = client.beta.threads.messages.create(
        THREAD_ID,
        role="user",
        content="{'doc_type': 'IDCard'}",
        attachments=[
            {"file_id": file_id, "tools": [{"type": 'file_search'}]}
        ],
    )
    print(thread_message.id)
    run = client.beta.threads.runs.create_and_poll(
        thread_id=THREAD_ID, assistant_id=get_assistant_id()
    )

    messages = list(client.beta.threads.messages.list(thread_id=THREAD_ID, run_id=run.id))

    message_content = messages[0].content[0].text
    # annotations = message_content.annotations
    # citations = []
    # for index, annotation in enumerate(annotations):
    #     message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
    #     if file_citation := getattr(annotation, "file_citation", None):
    #         cited_file = client.files.retrieve(file_citation.file_id)
    #         citations.append(f"[{index}] {cited_file.filename}")

    # print(message_content)
    return parse(message_content.value)

def parse(res: str):
    j = len(res) - 1
    while (res[j] != '}'):
        j -= 1
    ans = ''
    i = 0
    while (i <= j):
        ans += res[i]
        i += 1
    return ans




@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
