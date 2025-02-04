from furhat_remote_api import FurhatRemoteAPI
# import numpy as np

from utils import (
    brainstorm,
    search_content,
    open_link,
)

# from joblib import load, dump
# from pathlib import Path


# Connect to Furhat (Ensure Furhat is running on the given IP)
furhat = FurhatRemoteAPI("localhost")

# Main workflow

######### Stage 1: Initiating conversation to know what the user wants assistance with #################

# Initiating a conversation with Furhat
furhat.say(
    text="Hello! I am Furhatos Sama! Your personal research assistant! I am here to help you on your research journey whenever you need me! I can look up videos, articles and publishing venues or simply help you brainstorm!", blocking=True
)

furhat.gesture(name="Smile")
furhat.gesture(name="Blink", blocking=True)
furhat.gesture(name="Blink", blocking=True)
# furhat.gesture(name="Roll")

furhat.say(
    text="How shall I help you today? Feel free to describe your project or idea or anything specific about the assistance you seek from me! Please speak out and say: done speaking, whenever you are finished.",
    blocking=True,
)


# Transcribing user's input and ending when the user says "done speaking" - this is a workaround to block the code till the user is speaking
userInput = ""
while not userInput.endswith("done speaking"):
    userIn = furhat.listen()
    userInput += " " + userIn.message
    print(userInput)

furhat.gesture(name="BrowRaise")

# Finishing the initial conversation
furhat.say(text="Thank you for sharing. Let's proceed.", blocking=True)

furhat.gesture(name="Thoughtful", blocking=True)

furhat.say(text="Hmmm.... Would you like me to fetch relevant content or would you like to brainstorm? Choose between content and brainstorm", blocking=True)

assistanceChoice = ""
assitanceFlags = {
    "content": False,
    "brainstorm": False,
}

while not any(assitanceFlags.values()):
    assistanceCh = furhat.listen()
    assistanceChoice += " " + assistanceCh.message.lower()
    assitanceFlags["content"] = "content" in assistanceChoice
    assitanceFlags["brainstorm"] = "brainstorm" in assistanceChoice
    
    print(assistanceChoice)


if assitanceFlags["content"] is True:

######### Stage 2: Deciding the type of content to look up #################
    furhat.say(
        text="Which kind of content would you like me to look up? Videos or Articles?. Perhaps you would like me to search and find particular venues for publishing? Please choose between Videos, Articles Venues.",
        blocking=True,
    )

    contentChoice = ""

    contentFlags = {
        "video": False,
        "article": False,
        "venue": False,
    }

    while not any(contentFlags.values()):
        contentCh = furhat.listen()
        contentChoice += " " + contentCh.message.lower()
        contentFlags["video"] = "video" in contentChoice
        contentFlags["article"] = "article" in contentChoice
        contentFlags["venue"] = "venue" in contentChoice

        print(contentChoice)
        


######### Stage 2-1: Fetching and showing content suiting user's needs #################
# We use Exa AI for doing an LLM based crawl over the internet

    furhat.say(
        text="Sure! Allow me to search and present the content that suits your need.",
        blocking=True,
    )
    furhat.gesture(name="Smile")

    # Processing user's query and searching relevant content on the internet with LLM
    content_type = list(filter(lambda x: x[1] is True, contentFlags.items()))[0][0]   ### [("video", True), ("article", False), ("venue", False)]
    userInput = userInput.replace("done speaking", "")
    search_results = search_content(userInput, content_type)

    # Display results
    if search_results:
        search_results_str = "\n".join(
            map(lambda x: f"\t --> {x.title}: {x.url}", search_results)
        )
        print(search_results_str)
        titles = ",".join(list(map(lambda x: x.title, search_results)))

        # Make furhat speak the titles of the videos and ask user to choose
        furhat.say(
            text=f"Based on our conversation, I have found some interesting {content_type}s for you!.",
            blocking=True,
        )

        furhat.say(
            text=f"The following are the titles of the {content_type}s I could find: {titles}.",
            blocking=True,
        )

        furhat.gesture(name="Blink")

        furhat.say(text=f"Which one should I open? Please choose between first, second, third or all.", blocking=True)
        conChoice = ""
        choices = {"first": 1, "second": 2, "third": 3}
        choice = 0

        # Processing choices
        while not conChoice.endswith("done speaking"):
            if choice != 0:
                break
            contentCh = furhat.listen()
            conChoice += " " + contentCh.message.lower()
            print(conChoice)

            if "first" in conChoice:
                choice = choices["first"]
                # break
            elif "second" in conChoice:
                choice = choices["second"]
                # break
            elif "third" in conChoice:
                choice = choices["third"]
                # break
            elif "all" in conChoice:
                choice = "all"
            else:
                continue

        print(choice)
        chosen = search_results[choice - 1] if choice != "all" else "all"
        try:
            if chosen == "all":
                for result in search_results:
                    open_link(result.url)
            else:    
                open_link(chosen.url)
        except Exception as e:
            print(f"Couldn't open link because of exception: {e}")


######### Stage 2-2: Interacting and finding some good articles#################
elif assitanceFlags["brainstorm"] is True:
    userQuery = userInput.replace("done speaking", "").lower()
    userInteract = ""
    messages = []
    furhat.say(
        text="Sure! Let's brainstorm! You can end the talk anytime you want by saying 'finish'.",
        blocking=True,
    )
    while not "finish" in userInteract:
        # emotion_capture(duration=5)
        llm_res, fur_res, messages = brainstorm(
            query=userQuery, messages=messages
        )  # Generating LLM Response

        # Responding with Furhat
        furhat.say(text=fur_res, blocking=True, lipsync=True)
        # furhat.say(
        #     text="Should we continue? Please say done whenever you are done speaking",
        #     blocking=True,
        # )
        # furhat.say_stop()
        furhat.gesture(name="Blink")
        while not (
            "done" in userInteract
        ):  # Capturing user's next query
            userQuery = furhat.listen().message.lower()
            userInteract += " " + userQuery

        print(userInteract)
        userInteract = userInteract.replace("done", " ")
        if ("finish" in userInteract):
            break

else:
    print("Not implemented")


######### Stage 3: Ending the interaction #################
furhat.say(
    text="I hope the interaction was helpful! I'll be back whenever you need me! To INFINITY and BEYOND!"
)


