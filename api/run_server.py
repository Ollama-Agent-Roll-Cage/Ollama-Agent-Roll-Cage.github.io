import uvicorn
import os
from dotenv import load_dotenv
from pathlib import Path

# Ensure we're in the correct directory
os.chdir(Path(__file__).parent)

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    # Verify GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY"):
        env_file = Path(".env")
        if not env_file.exists():
            # Create .env file if it doesn't exist
            with open(env_file, "w") as f:
                f.write("GROQ_API_KEY=\n")
            print("Error: GROQ_API_KEY not set")
            print("A .env file has been created. Please add your Groq API key to it:")
            print("GROQ_API_KEY=your_api_key_here")
            exit(1)
        else:
            print("Error: GROQ_API_KEY not found in .env file")
            print("Please add your Groq API key to the .env file:")
            print("GROQ_API_KEY=your_api_key_here")
            exit(1)

    # Run the server
    uvicorn.run(
        "chat_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )