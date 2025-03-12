import os
import openai
from serpapi import GoogleSearch

class Agent:
    #initializing the agent
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    #query refiner
    def refine_query(self, query: str) -> str:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""Refine this query for better search results in one sentence: {query}"""
                }
            ],
            max_tokens=100
        )
        return response.choices[0].message.content

    #search engine
    def search(self, query: str) -> list:
        #intentional api key code here i don't know why it's not working
        #with serp api key yet it's working with openai api key
        params = {
            "q": query,
            "engine": "google",
            "api_key": "",
            "num": 5
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        return [
            {
                "title": result["title"],
                "link": result["link"],
                "snippet": result["snippet"]
            } for result in results["organic_results"]
        ]
    
    #run the agent
    def run(self, query: str):
        print("Refinando la consulta...")
        refined_query = self.refine_query(query)
        print(f"Consulta refinada: {refined_query}")
        print("Buscando en la web...")
        search_results = self.search(refined_query)
        print("Resultados de la búsqueda:")
        for result in search_results:
            print(f"Titulo: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Snippet: {result['snippet']}")
            print("\n")

if __name__ == "__main__":
    agent = Agent()
    #we ask the user for a query
    user_query = input("Enter your query: ")
    #we run the agent
    agent.run(user_query)