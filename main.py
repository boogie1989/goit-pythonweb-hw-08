"""
Main application module for Contacts API.
"""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.router import api_router
from app.core.config import API_V1_PREFIX, PROJECT_NAME

# Create FastAPI app instance
app = FastAPI(title=PROJECT_NAME)

# Include API router
app.include_router(api_router, prefix=API_V1_PREFIX)

# Root endpoint
@app.get("/", response_class=RedirectResponse, status_code=302)
def read_root():
    """
    Root endpoint that redirects to API documentation.
    """
    return "/docs"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
