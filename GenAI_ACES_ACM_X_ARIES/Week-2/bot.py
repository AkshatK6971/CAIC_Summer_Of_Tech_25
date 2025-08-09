from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import pprint
import os

load_dotenv()
groq_key = os.getenv("GROQ_KEY")

llm=ChatGroq(
    groq_api_key=groq_key,
    model="llama-3.3-70b-versatile",
    temperature=0.7
)

# class Product(BaseModel):
#     product_description : str = Field(description="The generated product description")

# content_template="""
# # CONTEXT #
# I want to advertise for my company's duty free product catalogue. The SKU Name of the product is {sku_name}, brand of the product is {brand_name} and its category is : {sub_category}.

# # OBJECTIVE #
# Create new product description for the above product based on the following existing description: {description}. Extract all key points and features from the existing description and write a new description from them. The word count should be similar to the original description.

# # STYLE #
# The writing style needs focus on the unique aspects of the product - its ingredients, its process, its history. Use descriptive language to evoke sensory experience - taste, smell, touch. Be precise and concise when writing. The content needs to be simple enough for the common man to understand it.
# Following words are BLACKLISTED from appearing in the response: 'transformative','tapestry','like',';','-'.
# REPLACE the following words with a more descriptive and specific response: 'foster','fostering','all about','is about','think of','like','but also'.

# # TONE #
# Simple, clear and elegant.

# # AUDIENCE #
# My company's audience profile is the common man who likes to indulge in the finer things in life every once in a while.

# {format_instructions}
# """

# parser = PydanticOutputParser(pydantic_object=Product)
# output_fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
# content_prompt = PromptTemplate(input_variables=["sku_name","brand_name","sub_category","description"],template=content_template,partial_variables={"format_instructions":parser.get_format_instructions()})
# content_runnable = content_prompt | llm  | output_fixing_parser

# user_input={
#     "brand_name":"Chloe",
#     "sku_name":"CHLOÉ Atelier des Fleurs Magnolia Alba Eau de Parfum 150ml",
#     "sub_category":"Perfumes",
#     "description":"The House of Chloé unveils a collection of nine exclusive Eau de Parfum fragrances for woman: Atelier des Fleurs.\nMagnolia Alba transcribes the smooth, plump and slightly lemony notes of magnolia blossoms in spring."
# }

# result=content_runnable.invoke(user_input)
# print(result.product_description)

class Query(BaseModel):
    query_category : str = Field(description="The query category to be classified") 

query_classifier_template="""
Your job is to classify user queries into payment issues, delivery issues and product issues. 

Do NOT respond with more than 1 word.

Query: {query}

{format_instructions}
"""

query_parser = PydanticOutputParser(pydantic_object=Query)
query_output_fixing_parser = OutputFixingParser.from_llm(parser=query_parser,llm=llm)

query_classifier_prompt = PromptTemplate(input_variables=["query"],template=query_classifier_template,partial_variables={"format_instructions":query_parser.get_format_instructions()})
query_classifier_runnable = query_classifier_prompt | llm  | query_output_fixing_parser

class Response(BaseModel):
    response : str = Field(description="Response provided as a response to the query")

payment_issues_template="""
You are a PayTM customer service representative. Introduce yourself first. Your job is to address the queries related to payment issues. Help the user out in 2 sentences. 

Query is {query}

{format_instructions}
"""

delivery_issues_template="""
You are a Delhivery customer service representative. Introduce yourself first. Your job is to address the queries related to delivery issues. Help the user out in 2 sentences. 

Query is {query}

{format_instructions}
"""

product_issues_template="""
You are an Amazon customer service representative. Introduce yourself first. Your job is to address the queries related to product issues. Help the user out in 2 sentences. 

Query is {query}

{format_instructions}
"""

response_parser = PydanticOutputParser(pydantic_object=Response)
response_output_fixing_parser = OutputFixingParser.from_llm(parser=response_parser,llm=llm)

payment_issues_prompt = PromptTemplate(input_variables=["query"],template=payment_issues_template,partial_variables={"format_instructions":response_parser.get_format_instructions()})
payment_issues_runnable = payment_issues_prompt | llm  | response_output_fixing_parser

delivery_issues_prompt = PromptTemplate(input_variables=["query"],template=delivery_issues_template,partial_variables={"format_instructions":response_parser.get_format_instructions()})
delivery_issues_runnable = delivery_issues_prompt | llm | response_output_fixing_parser

product_issues_prompt = PromptTemplate(input_variables=["query"],template=product_issues_template,partial_variables={"format_instructions":response_parser.get_format_instructions()})
product_issues_runnable = product_issues_prompt | llm | response_output_fixing_parser

def logic(category):
    if "payment" in category['info'].query_category.lower():
        return payment_issues_runnable
    elif "delivery" in category['info'].query_category.lower():
        return delivery_issues_runnable
    else:
        return product_issues_runnable

complete_classification_pipeline = {
    "query": lambda x: x["query"], 
    "info": query_classifier_runnable
} | RunnableLambda(logic)

result=complete_classification_pipeline.invoke({"query":"Your payment gateway crashed midway through payment and it withdrew money from my bank account without giving me the subscription. What can i do?"})
print(result.response)
result=complete_classification_pipeline.invoke({"query":"The delivery driver hasn't arrived yet. What do I do?"})
print(result.response)
result=complete_classification_pipeline.invoke({"query":"The headphones arrived faulty. What should I do?"})
print(result.response)