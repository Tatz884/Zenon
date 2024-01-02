from fastapi import FastAPI
from .api.v1 import words as api_words  # Import the 'words' module with an alias
from .cruds import words as crud_words  # Same here

from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "Zenon-backend",
        "description": "All the Zenon backend operations.",
    }
]

app = FastAPI(
    title="Zenon-backend",
    version="0.1.0",
    openapi_tags=tags_metadata
)

origins = [
    "*"
    # "http://localhost*",
    # "https://example.org",
    # "https://tatz884.github.io",
    # "https://tatz884.github.io/*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_words.router, prefix="/api/v1/words", tags=["words"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

# table_names = crud_words.get_table_names()
# for name in table_names:
#     print(name)
#     # 