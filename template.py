import os
from pathlib import Path

project_name = "src"

list_of_files = [
    f"{project_name}/backend/__init__.py",
    f"{project_name}/backend/main.py",
    f"{project_name}/backend/chatbot.py",
    f"{project_name}/backend/data_analysis.py",
    f"{project_name}/backend/mongo_utils.py",
    f"{project_name}/backend/document_handler.py",
    f"{project_name}/backend/config.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/frontend/__init__.py",
    f"{project_name}/frontend/app.py",
    f"{project_name}/frontend/components/__init__.py",
    f"{project_name}/frontend/assets/__init__.py",

    f"{project_name}/models/__init__.py",
    f"{project_name}/models/embeddings.pkl",

    f"{project_name}/data/__init__.py",
    f"{project_name}/data/sample_orders.csv",

    f"{project_name}/notebooks/__init__.py",
    f"{project_name}/notebooks/explore_data.ipynb",

    f"docs/architecture.png",

    f".env",
    f"requirements.txt",
    f"Dockerfile",
    f".dockerignore",
    f"setup.sh",
    f"README.md"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print(f"✅ File already exists: {filepath}")

print("\n📦 BizBuddy AI project structure created successfully!")
