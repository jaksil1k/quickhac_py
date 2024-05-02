from openai import OpenAI
from config import OPEN_API_KEY, VS_ID, ASST_ID, RUN_ID

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


def upload_vs(file_id):
  client.beta.vector_stores.files.create(
    vector_store_id=VS_ID,
    file_id=file_id
  )
  print("successfully uploaded file to vs")


def delete_vs(file_id):
  client.beta.vector_stores.files.delete(
    vector_store_id=VS_ID,
    file_id=file_id
  )
  print("successfully deleted file from vs")


def update_assistant():
  updated_assistant = client.beta.assistants.update(
    ASST_ID,
    instructions="""Your are document scanner. I need to scan Kazakhstan document ID card.
    In ID Card - In front side(where we have human photo) under 'ТЕГІ/ФАМИЛИЯ' will be surname, 'АТЫ/ИМЯ' will be name, 'ӘКЕСІНҢ/ОТЕЧЕСТВО' will be middle name mark as middle_name, 'ТУҒАН КҮНІ/ДАТА РОЖДЕНИЯ' will be date in 'dd/MM/yyyy' format mark as birthday, and right to 'ЖСН/ИИН' will be 12 numbers - iin or id of person. 
    In the back side on the upper-right side 9 numbers, it will be id of card itself mark as card_id, and under 'БЕРІЛГЕН КҮНІ - ҚОЛДАНУ МЕРЗІМІ/ДАТА ВЫДАЧИ - СРОК ДЕЙСТВИЯ' will be two date in 'dd/MM/yyyy' format take it, mark first date as given_date, and second date as expiration_date.
    I will give req in following json: {'doc_type': 'IDCard'}. I will expect answer in raw json(which easy to parse) format: {'status': 'success/error', 'data': {'iin' '12 numbers', 'fullname': 'surname name middle_name', 'birthday': 'dd/MM/yyyy', 'card_id': '9 numbers', 'given_date': 'dd/MM/yyyy', 'expiration_date': 'dd/MM/yyyy'}} . I need just json response without any explanations and notes. Return success only in case of presence of all fields of document. In case of error status data will be null.
              """,
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

update_assistant()
def get_assistant_id():
  return ASST_ID


def update_run(thread_id):
  run = client.beta.threads.runs.update(
    thread_id=thread_id,
    run_id=RUN_ID,
  )
  return run


def create_thread(file_id: str, type: str):
  thread = client.beta.threads.create(
    messages=[{
      "role": "user",
      "content": "{'doc_type': '" + type + "'}",
      # Attach the new file to the message.
      "attachments": [
        {"file_id": file_id, "tools": [{"type": 'file_search'}]}
      ],
    }],
    tool_resources={
      "file_search": {
        "vector_store_ids": [VS_ID]
      }
    }
  )
  # update_assistant(vs_id)
  return thread.id


def delete_thread(thread_id):
  client.beta.threads.delete(thread_id)
