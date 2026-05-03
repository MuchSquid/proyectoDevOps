from fastapi import FastAPI

app = FastAPI(title="Biblioteca Reservas API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Biblioteca Reservas API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
