from langchain_classic.chains import RetrievalQA



from langchain_core.prompts import PromptTemplate

from app.components.llm import load_llm
from app.components.vector_store import load_vector_store

from app.config.config import HUGGINGFACE_REPO_ID,HF_TOKEN
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


logger = get_logger(__name__)

CUSTOM_PROMPT_TEMPLATE = """
You are a medical question-answering assistant using retrieved documents.

Rules:
- Use ONLY information from the Context that is directly relevant to the Question.
- Ignore any sentences in the Context that are unrelated to the Question.
- Do NOT add external knowledge or assumptions.
- Do NOT mention the Context, retrieval, citations, or what is/ isn't mentioned.
- If the Context does not contain enough relevant information to answer, reply exactly:
The information is not available in the provided context.

Output style:
- 2–3 short sentences max.
- Neutral, factual, medically accurate.

Context:
{context}

Question:
{question}

Answer:
"""



def set_custom_prompt():
    return PromptTemplate(template=CUSTOM_PROMPT_TEMPLATE,input_variables=["context" , "question"])

def create_qa_chain():
    try:
        logger.info("Loading vector store for context")
        db = load_vector_store()

        if db is None:
            return None, "Vector store not present or empty. Please ensure you have processed your PDFs."

        llm = load_llm()

        if llm is None:
            return None, "LLM not loaded. Please check if your HUGGINGFACEHUB_API_TOKEN is correct in the .env file."

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_kwargs={'k': 4}),
            return_source_documents=False,
            chain_type_kwargs={'prompt': set_custom_prompt()}
        )

        logger.info("Successfully created the QA chain")
        return qa_chain, None

    except Exception as e:
        error_message = CustomException("Failed to make a QA chain", e)
        logger.error(str(error_message))
        return None, str(error_message)