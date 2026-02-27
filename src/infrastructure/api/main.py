from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.api.routers import tracking, users
from infrastructure.cache import get_redis
from infrastructure.config.settings import settings
from src.infrastructure.persistence.database.connection import get_db

app = FastAPI(title=settings.PROJECT_NAME, docs_url=None, redoc_url="/redocs", openapi_url="/openapi.json")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return HTMLResponse(
        content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{app.title} - Swagger UI</title>
            <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
            <style>
                body {{
                    background-color: #1e1e1e !important;
                    color: #fff !important;
                    margin: 0;
                }}
                .swagger-ui .topbar {{
                    background-color: #2d2d2d !important;
                    display: none;
                }}
                .swagger-ui .scheme-container {{
                    background: #2d2d2d !important;
                    box-shadow: none !important;
                }}
                .swagger-ui {{
                    background: #1e1e1e !important;
                }}
                .swagger-ui .opblock-tag {{
                    background: rgba(0,0,0,0.1) !important;
                    color: #fff !important;
                }}
                .swagger-ui .opblock {{
                    background: #2d2d2d !important;
                    border-color: #3d3d3d !important;
                }}
                .swagger-ui .opblock-summary {{
                    border-color: #3d3d3d !important;
                }}
                .swagger-ui table thead tr td,
                .swagger-ui table thead tr th {{
                    background: #2d2d2d !important;
                    color: #fff !important;
                    border-color: #3d3d3d !important;
                }}
                .swagger-ui table tbody tr td {{
                    background: transparent !important;
                    color: #fff !important;
                    border-color: #3d3d3d !important;
                }}
                .swagger-ui .parameter__name {{
                    color: #fff !important;
                }}
                .swagger-ui .parameter__type {{
                    color: #aaa !important;
                }}
                .swagger-ui .btn {{
                    background: #3d3d3d !important;
                    color: #fff !important;
                    border-color: #4d4d4d !important;
                }}
                .swagger-ui .execute {{
                    background: #4CAF50 !important;
                    color: #fff !important;
                }}
                .swagger-ui .try-out__btn {{
                    background: #3d3d3d !important;
                    color: #fff !important;
                }}
            </style>
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
            <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
            <script>
                window.onload = function() {{
                    window.ui = SwaggerUIBundle({{
                        url: "{app.openapi_url}",
                        dom_id: '#swagger-ui',
                        deepLinking: true,
                        presets: [
                            SwaggerUIBundle.presets.apis,
                            SwaggerUIStandalonePreset
                        ],
                        plugins: [
                            SwaggerUIBundle.plugins.DownloadUrl
                        ],
                        layout: "StandaloneLayout",
                        defaultModelsExpandDepth: -1,
                        displayRequestDuration: true
                    }});
                }};
            </script>
        </body>
        </html>
        """,
        status_code=200,
        media_type="text/html",
    )


app.include_router(users.router)
app.include_router(tracking.router)


@app.get("/")
def root():
    return {"message": "Server is running!"}


@app.get("/health", tags=["Health"])
async def health_check(
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
):
    """
    Verifica a conectividade com o Banco de Dados e o Redis.
    """
    await db.execute(text("SELECT 1"))
    await redis_client.ping()  # type: ignore

    return {
        "status": "ok",
        "database": "connected",
        "redis": "connected",
    }
