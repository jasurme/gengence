from fastapi import FastAPI

app = FastAPI(title="get time")

@app.post("/get_time")
def get_time(format: str):
    from datetime import datetime
    return datetime.now().strftime(format)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7717)