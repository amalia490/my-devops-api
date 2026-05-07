from fastapi import FastAPI

#initializare aplicatie 
app = FastAPI()

#ruta de baza
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Hello DevOps! Aplicatia functioneaza."}