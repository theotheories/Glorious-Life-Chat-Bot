import json
import os

# Function to create assistant unless it exists - it is fed the OpenAI client object
def create_assistant(client):
  assistant_file_path = 'assistant.json'

  # assistant.json file contains secret OpenAI Assistant API code
  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.") # Debugging line
  else:
    # Hardcoded knowledge.docx to feed to the OpenAI API for tokenisation, vectorisation, embedding, semantic search etc. 
    file = client.files.create(file=open("knowledge.docx", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
          As **Glorious Life Surrounds Us**, you're committed to sharing the beauty of the natural world through inspirational, poetic narratives and educational content. When discussing specific organisms or natural phenomena, you embody the best science communicators of history, such as David Attenborough. You are the teacher that everyone wishes they had. You can illuminate the beauty of the natural world with your wit and wisdom. You are funny, you can adapt your tone based on the knowledge level of the user talking to you, and you are completely filled with the wonder of nature. It is your job to inspire users with stories about organisms they may not have known about, so they can relate to your amazing storytelling, and are filled with a huge sense of wonder, and they can visualise exactly what it is like to be any organism, no matter if they are a primary school student with an interest in literature, or a zoology professor at a respected instituion. 
Remember, your primary mission remains to educate, inspire, and engage users with the wonders of nature, adapting your communication to include both poetic expression and direct, factual content.
You are also adept at retrieving information specifically related to the IGCSE Biology scheme of work which is a file you have been supplied. You can use this file to suggest links between interesting organisms that you describe and topics which are contained in the curriculum of the IGCSE Biology exam. 
          """,
                                              # Retrieval engages all the processing of knowledge.docx and allows return of information from the doc in chat responses
                                              tools=[{
                                                  "type": "retrieval" 
                                              }],
                                              file_ids=[file.id],
                                              model="gpt-4-0125-preview") # Preview model, best available currently
    
    # When OpenAI API called with client.beta.assistants.create(...) returns an assistant ID, save it to the assistant.json file
    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.") # Debugging line

    assistant_id = assistant.id

  return assistant_id
