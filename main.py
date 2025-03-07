from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import WorkflowRequest, CodeRequest, PayloadResponse, CodeResponse
from services.payload_generator import PayloadGenerator
from services.code_generator import CodeGenerator

app = FastAPI(title="Workflow Code Generator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
# @app.post("/generate-payload", response_model=PayloadResponse)
# def generate_payload(workflow: WorkflowRequest):
#     try:
#         payload = PayloadGenerator.generate_payload(workflow)
#         return {"payload": payload}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-code", response_model=CodeResponse)
def generate_code(request: CodeRequest):
    try:
        # Generate payload
        payload = PayloadGenerator.generate_payload(request.workflow)

        # Generate code based on language
        code = CodeGenerator.generate_code(
            language=request.language, base_url=request.base_url, payload=payload
        )

        return {"code": code, "payload": payload}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
