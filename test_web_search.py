from chatbot.web_search import search_web_knowledge

while True:

    question = input("\nAsk: ")

    result = search_web_knowledge(question)

    if result:

        college, title, content, url = result

        print("\nCollege:", college)
        print("Title:", title)
        print("URL:", url)
        print("\nAnswer:\n")
        print(content[:1000])

    else:

        print("No result found.")