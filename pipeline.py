# Website Summarizer: 
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.prompts import PromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.schema import Document
from typing import List, Tuple

### Setting my environment variables:
import os
import dotenv

dotenv.load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

### My constants:
MODEL_NAME = "meta/llama3-70b-instruct" #Context length: 8k token
# Load the data:
# Load the data from the given URL using WebBaseLoader
def load_data(url:str) -> List[Document]:
    loader = WebBaseLoader(
        web_path=url,
        default_parser="lxml",
        bs_get_text_kwargs={
            'separator': "\n\n",
            'strip': True
        }
    )
    return loader.load()


## Split documents:
def split_documents(
        docs : List[Document],
        separators: List[str] = ["\n\n", "\n"], 
        chunk_size: int = 1500, 
        chunk_overlap: int = 200, 
        length_function=len
    ) -> List[Document]:
    return RecursiveCharacterTextSplitter(
        separators=separators,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function
    ).create_documents([docs[0].page_content], [docs[0].metadata])

## Create Prompts:
def get_prompts_for_map_reduce() -> Tuple[PromptTemplate]:
    map_prompt = """
    Write a concise summary of the following text between (""):
    "{text}"
    CONCISE SUMMARY:
    """
    map_prompt_template = PromptTemplate(
        input_variables=['text'],
        template=map_prompt
    )

    combine_prompt = """
    Write a concise and cohesive summary of the following text (only the main topic on them) delimited by triple backquotes.
    Return your response in bullet points which covers the key points of the text.
    ```{text}```
    BULLET POINT SUMMARY:
    """
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])

    return map_prompt_template, combine_prompt_template
## Build Summary chain:

def create_chain(
        llm=None,
        chain_type='map_reduce',
        map_prompt_template=None,
        combine_prompt_template=None,
        verbose=False
    ) -> BaseCombineDocumentsChain:
    return load_summarize_chain(
        llm=llm, 
        chain_type=chain_type, 
        map_prompt=map_prompt_template, 
        combine_prompt=combine_prompt_template, 
        verbose=verbose
    )

## Build a Pipeline:
def summary_pipeline(url, chain_type='map_reduce', api_key=None) -> str:
    docs = load_data(url=url)
    chunks = split_documents(docs=docs)
    llm = ChatNVIDIA(model=MODEL_NAME, api_key=api_key)
    map_prompt_template, combine_prompt_template = get_prompts_for_map_reduce()
    chain = create_chain(llm=llm, map_prompt_template=map_prompt_template, combine_prompt_template=combine_prompt_template, chain_type=chain_type)    
    summary = chain.run(chunks)
    return summary

