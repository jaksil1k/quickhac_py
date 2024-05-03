import json

from fastapi import FastAPI

from file_gpt import get_assistant_id, client, upload_to_vs
from util import parse
from config import THREAD_ID

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/file-vs")
async def upload_file_vs(file_id):
    upload_to_vs(file_id)
    return {"status": "OK"}

@app.post("/file")
async def upload_file_endpoint(file_id):
    upload_to_vs(file_id)

    # thread = client.beta.threads.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": "{'doc_type': 'IDCard', 'file_id}: '" + file_id + "'",
    #             # Attach the new file to the message.
    #             "attachments": [
    #                 {"file_id": file_id, "tools": [{"type": "file_search"}]}
    #             ],
    #         }
    #     ]
    # )
    thread_message = client.beta.threads.messages.create(
        THREAD_ID,
        role="user",
        content="{'doc_type': 'IDCard'}",
        attachments=[
            {"file_id": file_id, "tools": [{"type": 'file_search'}]}
        ],
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=THREAD_ID,  assistant_id=get_assistant_id()
    )

    messages = list(client.beta.threads.messages.list(thread_id=THREAD_ID, run_id=run.id))

    # print(messages)
    message_content = messages[0].content[0].text
    # annotations = message_content.annotations
    # citations = []
    # for index, annotation in enumerate(annotations):
    #     message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
    #     if file_citation := getattr(annotation, "file_citation", None):
    #         cited_file = client.files.retrieve(file_citation.file_id)
    #         citations.append(f"[{index}] {cited_file.filename}")

    print(parse(message_content.value))
    return parse(message_content.value)



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
