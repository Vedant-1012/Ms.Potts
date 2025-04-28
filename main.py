# main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from model_gemini import GeminiModel
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize GeminiModel ONCE
model = GeminiModel()

@app.post("/query")
async def query_endpoint(request: Request):
    try:
        data = await request.json()
        query = data.get("query", "")
        user_context = data.get("context", {}).get("user_profile", {})

        print(f"✅ Received Query: {query}")
        print(f"✅ Received Context: {user_context}")

        response = model.get_response(query, user_context)
        
        print(f"✅ GeminiModel Response: {response}")

        return JSONResponse({
            "final_answer": response.get("final_answer", ""),
            "detected_intent": response.get("detected_intent", ""),
            "reasoning": response.get("reasoning", ""),
        })
    except Exception as e:
        print(f"❌ Exception inside /query: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
