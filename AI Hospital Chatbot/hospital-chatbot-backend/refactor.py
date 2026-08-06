import os
import shutil
import re
from pathlib import Path

BASE_DIR = Path("E:/VS_CODE/TechSpire/AI Hospital Chatbot/hospital-chatbot-backend")
APP_DIR = BASE_DIR / "app"

# 1. Moves
MOVES = [
    (APP_DIR / "api/v1/chatbot.py", APP_DIR / "modules/chatbot/api/router.py"),
    (APP_DIR / "models/user.py", APP_DIR / "modules/chatbot/models/user.py"),
    (APP_DIR / "models/conversation.py", APP_DIR / "modules/chatbot/models/conversation.py"),
    (APP_DIR / "models/message.py", APP_DIR / "modules/chatbot/models/message.py"),
    (APP_DIR / "models/__init__.py", APP_DIR / "modules/chatbot/models/__init__.py"),
    
    (APP_DIR / "repositories/base.py", APP_DIR / "modules/chatbot/repositories/base.py"),
    (APP_DIR / "repositories/conversation_repository.py", APP_DIR / "modules/chatbot/repositories/conversation_repository.py"),
    (APP_DIR / "repositories/message_repository.py", APP_DIR / "modules/chatbot/repositories/message_repository.py"),
    (APP_DIR / "repositories/__init__.py", APP_DIR / "modules/chatbot/repositories/__init__.py"),
    
    (APP_DIR / "schemas/chat.py", APP_DIR / "modules/chatbot/schemas/chat.py"),
    (APP_DIR / "schemas/conversation.py", APP_DIR / "modules/chatbot/schemas/conversation.py"),
    (APP_DIR / "schemas/__init__.py", APP_DIR / "modules/chatbot/schemas/__init__.py"),
    
    (APP_DIR / "services/chat_service.py", APP_DIR / "modules/chatbot/services/chat_service.py"),
    (APP_DIR / "services/prompt_service.py", APP_DIR / "modules/chatbot/services/prompt_service.py"),
]

for src, dst in MOVES:
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))

# Delete old provider
old_ai = APP_DIR / "services/ai_provider.py"
if old_ai.exists():
    old_ai.unlink()

# Remove empty old dirs
for d in ["api/v1", "api", "models", "repositories", "schemas"]:
    d_path = APP_DIR / d
    if d_path.exists() and not list(d_path.iterdir()):
        d_path.rmdir()

# 2. Update Imports in all python files
IMPORT_REPLACEMENTS = [
    (r"from app\.models", r"from app.modules.chatbot.models"),
    (r"import app\.models", r"import app.modules.chatbot.models"),
    (r"from app\.schemas", r"from app.modules.chatbot.schemas"),
    (r"from app\.repositories", r"from app.modules.chatbot.repositories"),
    (r"from app\.services\.chat_service", r"from app.modules.chatbot.services.chat_service"),
    (r"from app\.services\.prompt_service", r"from app.modules.chatbot.services.prompt_service"),
    (r"from app\.api\.v1\.chatbot", r"from app.modules.chatbot.api.router"),
    (r"from app\.api\.v1 import api_router", r""),
    (r"app\.include_router\(api_router, prefix=settings\.API_V1_STR\)", r"from app.modules.chatbot.api.router import router\napp.include_router(router, prefix=settings.API_V1_STR + '/chatbot', tags=['Chatbot'])"),
    (r"from app\.services\.ai_provider import BaseAIProvider, get_ai_provider", r"from app.services.ai import BaseBaseAIProvider\nfrom app.services.ai import get_ai_provider"),
    (r"BaseAIProvider", r"BaseBaseAIProvider")
]

for py_file in BASE_DIR.rglob("*.py"):
    if ".venv" in py_file.parts or "alembic" in py_file.parts and py_file.name != "env.py":
        continue
    content = py_file.read_text(encoding="utf-8")
    new_content = content
    for pattern, repl in IMPORT_REPLACEMENTS:
        new_content = re.sub(pattern, repl, new_content)
    
    if new_content != content:
        py_file.write_text(new_content, encoding="utf-8")

# 3. Create stubs
(APP_DIR / "core/security.py").write_text("# Security utilities (JWT, password hashing)\n")
(APP_DIR / "shared/constants.py").write_text("# Global constants\n")
(APP_DIR / "shared/utils.py").write_text("# Global utilities\n")
(APP_DIR / "modules/chatbot/repositories/user_repository.py").write_text("# User repository\n")
(APP_DIR / "modules/chatbot/__init__.py").touch()
(APP_DIR / "services/ai/__init__.py").touch()

print("Refactoring script completed successfully.")
