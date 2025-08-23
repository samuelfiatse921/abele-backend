import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
from urllib.request import Request

from fastapi import FastAPI, APIRouter, Depends, Request as FastAPIRequest
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException

from app.deps.auth.deps import get_current_user
from app.deps.db.db import initialize_db
from app.user.web.v1.authenticate import auth_router
from app.user.web.v1.following import following_router
from app.user.web.v1.payment import payment_router
from app.user.web.v1.uploaded_template import template_upload_router
from app.user.web.v1.user import user_router
from app.user.web.v1.user_template import user_template_router
from app.user.web.v1.wallet import wallet_router


# Configure logging
logging.basicConfig(
    level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("SizeMugBackend")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    engine = await initialize_db(app)

    yield

    # Step 4: Dispose engine gracefully
    await engine.dispose()


# Initialize the FastAPI app
app = FastAPI(lifespan=lifespan)


@app.exception_handler(FastAPIHTTPException)
async def custom_http_exception_handler(_: Request, exc: FastAPIHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail if isinstance(exc.detail, dict) else {"detail": exc.detail}
    )

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

base_router = APIRouter()


@app.middleware("http")
async def log_requests(request: FastAPIRequest, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}.")
    return response


@base_router.get("")
async def ping():
    return Response(status_code=200, content="PONG!", media_type="text/html")

# Include API routes
authenticate = Depends(get_current_user)
app.include_router(base_router, prefix="/ping", tags=["base"])
app.include_router(
    auth_router, prefix="/api/v1/authenticate", tags=["authenticate"]
)
app.include_router(
    following_router, prefix="/api/v1/following", tags=["following"], dependencies=[authenticate]
)
app.include_router(
    payment_router, prefix="/api/v1/payment", tags=["payment"], dependencies=[authenticate]
)
app.include_router(
    template_upload_router, prefix="/api/v1/template/upload", tags=["template-upload"]
)
app.include_router(
    user_router, prefix="/api/v1/user", tags=["user"]
)
app.include_router(
    user_template_router, prefix="/api/v1/user/template", tags=["user-template"], dependencies=[authenticate]
)
app.include_router(
    wallet_router, prefix="/api/v1/wallet", tags=["wallet"], dependencies=[authenticate]
)

# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)

