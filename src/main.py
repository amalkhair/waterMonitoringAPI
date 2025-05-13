# main.py
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import uvicorn

from utils import send_mail, save_to_database, read_from_database

email_has_been_send = True

app = FastAPI()

class InnerData(BaseModel):
    tds: int = Field(alias="TDS")
    time: datetime
    temperature : float
    cycle : int
    # expects ISO 8601 format (e.g., "2025-05-04T15:00:00Z")

class DataPayload(BaseModel):
    data: InnerData

@app.post("/upload_data")
async def upload_data(payload: DataPayload):
    print(payload)
    tds = payload.data.tds
    time = payload.data.time
    temperature = payload.data.temperature
    cycle = payload.data.cycle

    print(f"Received TDS={tds}, time={time.isoformat()}, temperature={payload.data.temperature}, cycle={payload.data.cycle}")

    incoming_data = {
        "message": "Data processed successfully",
        "TDS": tds,
        "time": time.isoformat(),
        "temperature": temperature,
        "cycle": cycle
    }

    # Save to database
    save_to_database(incoming_data)

    global email_has_been_send
    if tds < 50 and email_has_been_send:
        print("TDS is less than 50")
        email_has_been_send = False
        # send_mail("TDS reach the Threshold", f"Hi...the TDS is {tds}", "umar.fth@gmail.com")

    print(json.dumps(incoming_data, indent=4))

    return incoming_data

@app.get("/monitoring_data")
async def monitoring_data():
    print("Reading data from database")
    # Implement actual database reading logic here
    data = read_from_database()
    return data

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)