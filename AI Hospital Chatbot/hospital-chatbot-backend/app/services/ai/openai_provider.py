from typing import List, Dict, cast, Iterable
import openai
from openai.types.chat import ChatCompletionMessageParam
from app.services.ai.base_provider import BaseAIProvider

class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: str, base_url: str | None = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model
        
        # Pass base_url only if it is provided
        client_kwargs = {"api_key": self.api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
            
        self.client = openai.OpenAI(**client_kwargs)

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        try:
            openai_messages = cast(Iterable[ChatCompletionMessageParam], messages)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                temperature=0.7,
                max_tokens=500
            )  
            return response.choices[0].message.content or ""
        except openai.RateLimitError as e:
            raise Exception(f"OpenAI Quota Exceeded: Your API key has run out of credits or hit a rate limit. Details: {str(e)}")
        except openai.AuthenticationError as e:
            raise Exception(f"OpenAI Authentication Error: Invalid API key. Details: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenAI API Error: {str(e)}")

    def generate_stream(self, messages: List[Dict[str, str]]):
        try:
            openai_messages = cast(Iterable[ChatCompletionMessageParam], messages)
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                temperature=0.7,
                max_tokens=500,
                stream=True
            )
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f" [Error: {str(e)}]"
