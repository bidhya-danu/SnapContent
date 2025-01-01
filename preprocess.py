import json

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

def process_post(raw_file_path,processed_file_path="data/processed_post.json"):
    enriched_posts=[]
    with open(raw_file_path, encoding='utf-8') as file:
        posts=json.load(file)
        for post in posts:
            metadata=extract_metadata(post['text'])
            post_with_metadata=post | metadata
            enriched_posts.append(post_with_metadata)
    
    for epost in enriched_posts:
        print(epost)
            
    
def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract the number of lines, language of the post, and tags.
    1. Return only a valid JSON, no preamble.
    2. The JSON object should only have 3 keys: line_count, language, and tags.
    3. Tags should be an array of tags, and you should extract a maximum of 2 tags.
    4. Language should be either English or Hinglish (Hinglish means a mix of Hindi and English).
    5. Ensure all tags are identical. If there are similar tags like 'LinkedIn Scams' and 'Job Scams', combine them into a single tag like 'Scams'.
    Here is the actual post on which you need to perform this task:
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post': post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException as e:
        print(f"Error parsing JSON: {e}")
        res = {"line_count": 0, "language": "Unknown", "tags": []}  # Default/fallback response
    
    return res
    
   
if __name__=="__main__":
    process_post("data/raw_post.json","data/processed_post.json")
    