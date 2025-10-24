from fastapi import FastAPI

app = FastAPI(title='MedCOCO-Search API')

@app.get('/')
def root():
    return {'message': 'Welcome to MedCOCO-Search API'}

