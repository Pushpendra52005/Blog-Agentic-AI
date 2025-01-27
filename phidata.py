import os
from dotenv import load_dotenv

from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.environ['GROQ_API_KEY']

# Define agents
web_search_agent = Agent(
    name="AI News Blogger Agent",
    role="Create a professional blog post about the latest AI developments",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=[
        "Format news as an engaging Google Blogger post.",
        "Include 3-5 key AI news developments.",
        "Write in a professional, yet accessible tone for a general audience.",
        "Use headings, bullet points, and short paragraphs for readability.",
        "Include relevant hashtags for search optimization.",
        "Provide source links for credibility.",
        "Highlight the broader impact of these AI developments.",
        "End with an engaging prompt to invite comments and discussions.",
        "Keep the total post length under 3000 characters."
    ],
    show_tools_calls=True,
    markdown=True
)

news_relevance_agent = Agent(
    name="News Relevance Validator",
    role="Critically evaluate AI news for blog posting",
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=[
        "Carefully assess the generated AI news content for blog suitability.",
        "Determine if the content is suitable for Google Blogger posting.",
        "Check for professionalism, current relevance, potential impact, and absence of controversial content.",
        "Provide a structured evaluation with: \n- Suitability score (0-10) \n- Posting recommendation (Yes/No) \n- Specific reasons for evaluation.",
        "If not suitable, explain specific reasons.",
        "Suggest potential modifications if needed.",
        "Respond with 'NO' in the posting recommendation if content is not suitable."
    ],
    show_tools_calls=True,
    markdown=True
)

# Main function
def main():
    # Generate AI news content
    news_response = web_search_agent.run("5 latest significant AI news developments with sources", stream=False)

    # Validate the generated news content
    validation_response = news_relevance_agent.run(
        f"Evaluate the following AI content for blog posting suitability:\n\n{news_response.content}",
        stream=False
    )

    # Check if validation recommends not posting
    news_content = news_response.content
    if "<function=duckduckgo_news" in validation_response.content:
        news_content = ""
    else:
        news_content = news_response.content

    return {
        "news_content": news_content,
        "validation": validation_response.content
    }

if __name__ == "__main__":
    result = main()
    print("Generated Blog Post")
    print(result["news_content"])
    print("\nValidation Result")
    print(result["validation"])
