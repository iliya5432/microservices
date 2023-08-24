import json
from fastapi import FastAPI, Response
from pymongo import MongoClient
from bson import ObjectId
import uvicorn

app = FastAPI()

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

    # mongo server
    client = MongoClient("mongodb://localhost:27017/")
    # Database server name
    db = client["carDB"]
    # Collection name
    global car_collection
    car_collection = db["cars"]

@app.get("/", tags=["car-backend"])
async def root():
    return {"message": "Hello World"}

@app.get("/cars")
async def get_cars():
    cars = list(car_collection.find())
    response_content = json.dumps(cars, indent=2, cls=JSONEncoder)  # Use custom JSONEncoder
    return Response(content=response_content, media_type="application/json")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)

