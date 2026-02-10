from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from app.config.config import HUGGINGFACEHUB_API_TOKEN, HUGGINGFACE_REPO_ID
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_llm(model_id: str = HUGGINGFACE_REPO_ID, hf_token: str = HUGGINGFACEHUB_API_TOKEN):
    try:
        if not hf_token:
            raise CustomException("HUGGINGFACEHUB_API_TOKEN is missing. Please set it in your environment or .env file.")

        logger.info(f"Loading LLM from Hugging Face Hub using model: {model_id}...")

        llm_endpoint = HuggingFaceEndpoint(
            repo_id=model_id,
            huggingfacehub_api_token=hf_token,
            temperature=0.3,
            max_new_tokens=512,
        )
        
        # Wrap the endpoint in ChatHuggingFace to support conversational models
        llm = ChatHuggingFace(llm=llm_endpoint)

        logger.info("LLM loaded successfully as ChatHuggingFace.")
        return llm

    except Exception as e:
        error_message = CustomException("Failed to load an LLM from Hugging Face Hub", e)
        logger.error(str(error_message))
        return None
