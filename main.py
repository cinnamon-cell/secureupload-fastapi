from fastapi import FastAPI, File, UploadFile, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

# Enable CORS for POST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 80 * 1024  # 80KB
VALID_EXTENSIONS = [".csv", ".json", ".txt"]
REQUIRED_TOKEN = "x4fzhu4jftnilsig"

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_8182: str = Header(None)
):
    # 1️⃣ Authentication
    if x_upload_token_8182 != REQUIRED_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 2️⃣ File type validation
    if not any(file.filename.endswith(ext) for ext in VALID_EXTENSIONS):
        raise HTTPException(status_code=400, detail="Invalid file type")

    # 3️⃣ Read file content
    contents = await file.read()

    # 4️⃣ File size validation
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # 5️⃣ If CSV → analyze
    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(contents))

        rows = len(df)
        columns = df.columns.tolist()

        total_value = round(float(df["value"].sum()), 2)

        category_counts = (
            df["category"]
            .value_counts()
            .to_dict()
        )

        return {
            "email": "23f3003410@ds.study.iitm.ac.in",
            "filename": file.filename,
            "rows": rows,
            "columns": columns,
            "totalValue": total_value,
            "categoryCounts": category_counts
        }

    return {"message": "File accepted but not processed"}