from fastapi import FastAPI
from app.api.v1 import employees
from app.core.config import settings

# Initialize the App with Metadata from Config
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise Grade HCM API for ZingHR",
)

# Versioning: Mount the v1 router
app.include_router(
    employees.router,
    prefix="/api/v1/employees",
    tags=["Employees"],
)


@app.get("/health", tags=["System"])
def health_check():
    """Endpoint for monitoring tools to verify the app is alive."""
    return {"status": "operational", "version": settings.VERSION}
