from openai import OpenAI
from config import OPEN_API_KEY, VS_ID, ASST_ID, RUN_ID, THREAD_ID

client = OpenAI()

client.api_key = OPEN_API_KEY


def upload_file(file):
    message_file = client.files.create(
        file=file, purpose="assistants"
    )
    return message_file.id


def delete_file(file_id):
    client.files.delete(file_id)
    print("successfully deleted file")


def upload_to_vs(file_id):
    client.beta.vector_stores.files.create_and_poll(
        vector_store_id=VS_ID,
        file_id=file_id
    )
    print("successfully uploaded file to vs")


def delete_from_vs(file_id):
    client.beta.vector_stores.files.delete(
        vector_store_id=VS_ID,
        file_id=file_id
    )
    print("successfully deleted file from vs")

def create_run():
  run = client.beta.threads.runs.create(
    thread_id=THREAD_ID,
    assistant_id=ASST_ID
  )
  print(run.id, "crated run")

# create_run()
def delete_vs():
    deleted_vector_store = client.beta.vector_stores.delete(
        vector_store_id=VS_ID
    )
    print("successfully deleted file from vs")
# delete_vs()
def create_vs():
  vector_store = client.beta.vector_stores.create(
    name="Document Store"
  )
  print("Created vs", vector_store.id)

# create_vs()

def update_assistant():
    updated_assistant = client.beta.assistants.update(
        ASST_ID,
        instructions="""I need to scan Kazakhstan document ID card.ID Card will contain 2 pages. 
        In ID Card - In front side(where we have human photo) under 'ТУҒАН КҮНІ/ДАТА РОЖДЕНИЯ' will be date in 'dd.MM.yyyy' format mark as birthday, and right to 'ЖСН/ИИН' will be 12 numbers - iin or id of person. Then in back side on the upper-right side 9 numbers, it will be id of card itself mark as card_id, and under 'БЕРІЛГЕН КҮНІ - ҚОЛДАНУ МЕРЗІМІ/ДАТА ВЫДАЧИ - СРОК ДЕЙСТВИЯ' will be two date in 'dd.MM.yyyy' format take it, mark first date as given_date, and second date as expiration_date.
    I will give req in following json: {'doc_type': 'IDCard', 'file_id': 'id of file'}. I will expect answer in json format: {'status': 'success/error', 'data': {'iin' '12 numbers', 'birthday': 'dd.MM.yyyy', 'card_id': '9 numbers', 'given_date': 'dd.MM.yyyy', 'expiration_date': 'dd.MM.yyyy'}} . I need just json response without any explanations and notes and filename. Return success only in case of presence of all fields of document. And you can provide your comment in case of error in field named 'message'.""",
        name="Document scanner",
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [VS_ID]
            }
        },
        model="gpt-4-turbo"
    )
    return updated_assistant.id
# update_assistant()
def create_assistant():
  updated_assistant = client.beta.assistants.create(
    instructions="""Your are document validator. You will answer in json in following format: {"status": "OK/NOT_DOC/FAKE", "message": "your comments"}.
    You will be given set of documents in vector_store that I provided. Firstly check that document is requested type. If not return answer with status 'NOT_DOC'.
    Then compare it with others, If there is no matching, return 'Fake'.Then return 'OK' if all is ok.""",
    name="Document scanner",
    tools=[{"type": "file_search"}],
    tool_resources={
      "file_search": {
        "vector_store_ids": [VS_ID]
      }
    },
    model="gpt-4-turbo"
  )
  print(updated_assistant.id, "created assistant")
  return updated_assistant.id

# create_assistant()
def get_assistant_id():
    return ASST_ID


def update_run(thread_id):
    run = client.beta.threads.runs.update(
        thread_id=thread_id,
        run_id=RUN_ID,
    )
    return run


def create_thread():
    thread = client.beta.threads.create(
        tool_resources={
            "file_search": {
                "vector_store_ids": [VS_ID]
            }
        }
    )
    print ("created thread", thread.id)
    return thread.id
# create_thread()

def delete_thread(thread_id):
    client.beta.threads.delete(thread_id)

# delete_thread("thread_SRs9M6UuJWc2SsxXRBl1LlP7")