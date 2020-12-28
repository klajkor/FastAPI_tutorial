from fastapi import FastAPI

app = FastAPI()


@app.get("/")
@app.get("/helloworld")
async def helloworld():
    return {"message": "Hello World, E!"}
