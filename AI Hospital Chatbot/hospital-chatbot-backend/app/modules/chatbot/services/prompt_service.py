import os

class PromptService:
    def __init__(self):
        # Dynamically resolve the absolute path to the prompts directory
        self.prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")

    def get_system_prompt(self) -> str:
        prompt_path = os.path.join(self.prompts_dir, "system_prompt.txt")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            # Fallback if the file is somehow missing
            return "You are an AI Hospital Assistant."
            
prompt_service = PromptService()
