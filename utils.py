from exa_py import Exa
import webbrowser
from huggingface_hub import InferenceClient
import json

# Keys and inits
with open("_keys.json", 'r') as f:
    keys = json.load(f)  # Loading keys from _keys.json file

EXA_KEY = keys["EXA_KEY"]
HF_KEY = keys["HF_KEY"]
exa = Exa(EXA_KEY)


#### Helper functions
def open_link(link):  # Open video link in a webbrowser
    webbrowser.open(link, new=1)


#### Stage 2-1: Functions for Fetching videos
def search_content(user_input, content_choice):
    num_results = 3
    include_domains = []
    if content_choice == "video":
        query = f"Top videos related to the following: {user_input}. They can be explanations of research papers, concepts, or demonstrations as well. This is to help in a reseach/academic setting."
        include_domains = ["www.youtube.com"]
        
    elif content_choice == "article":
        query = f"Top and recent research articles related to the following: {user_input}. They can be research papers, blogs, or other textual content as well. This is to help in a reseach/academic setting/project."

        include_domains=["scholar.google.com", "www.semanticscholar.org", "www.google.com"]
    
    elif content_choice == "venue":
        query = f"Find the best conferences and journals to publish according to the following user query: {user_input}. The domain of the publishing venue should align with the user query and should have a good ranking."

        include_domains=["www.scimagojr.com", "portal.core.edu.au", "www.google.com", "www.conferenceranks.com"]

    else: 
        raise ValueError(f"Unknown content choice encountered: {content_choice}")
    
    results = exa.search(
        query=query,
        use_autoprompt=True,
        num_results=3,
        include_domains=include_domains,
        type="neural",
        )

    return results.results

#### Stage 2-2: Functions for fetching textual content

# Function to interact with an LLM
def brainstorm(query, messages=[]):

    if len(messages) < 1: # Creating initial prompts to start the brainstorming session
        system_instruction_init = f"""
        You are a helpful AI research assistant named furhatos-sama.
        Your task is to help the user brainstorm creatively through suggesstions, possibilities and discussions. 

        Instructions for response:
        1. Adjust the session according to each new query of the user.
        2. Your aim is to help the user think creatively from different perspectives.
        3. All messages must be short. There should be no pointwise text in the message.
        4. Do not include any kind of special characters.
        5. Each message will be converted to speech using a text to speech synthesizer so the messages must be formatted accordingly.
        6. This will be a conversational flow, so you can ask questions to the user as well.
        7. Always speak with a first person POV.
        """
        user_prompt_init = f"I need help with brainstorming. Following is my query {query}."

        messages = [
            {
                "role": "system",
                "content": system_instruction_init,
            },
            {"role": "user", "content": user_prompt_init},
        ]
    else:  # Continuing conversation 
        messages.append({"role": "user", "content": query})

    # Querying hugging face LLM using an Inference Client
    client = InferenceClient(api_key=HF_KEY, provider="together")
    completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3", messages=messages, max_tokens=500
    )
    # completion = client.chat.completions.create(
    #     model="HuggingFaceH4/zephyr-7b-beta", messages=messages, max_tokens=500
    # )

    # Processing responce for approapriate TTS by furhat
    llm_response = completion.choices[0].message
    fur_response = llm_response.content.lower().replace("furhatos-sama:", " ").replace("\n", ". ")

    print(llm_response)

    # Appending response to messages
    messages.append({"role": "system", "content": fur_response})

    return llm_response, fur_response, messages


