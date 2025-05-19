import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
import uvicorn
from src.utils import save_user_to_database, hash_password, verify_password
from utils import send_mail, save_to_database, read_from_database, get_user_from_database
from fastapi.middleware.cors import CORSMiddleware

email_has_been_send = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InnerData(BaseModel):
    tds: int = Field(alias="TDS")
    time: datetime
    temperature : float
    cycle : int
    # expects ISO 8601 format (e.g., "2025-05-04T15:00:00Z")

class signup_data(BaseModel):
    email: str
    username: str
    password: str

class DataPayload(BaseModel):
    data: InnerData

class LoginData(BaseModel):
    username: str
    password: str


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

@app.post("/signup")
async def signup(userdata: signup_data):
    print("Received signup data:", userdata)
    email = userdata.email
    username = userdata.username
    hashed = hash_password(userdata.password)

    print(f"Received signup data: email_address={email}, username={username}, password={hashed}")

    incoming_data = {
        "message": "User signed up successfully",
        "email_address": email,
        "username": username,
        "password": hashed
    }

    saved_success = save_user_to_database(incoming_data)
    if not saved_success:
        raise HTTPException(status_code=500, detail="Failed to save user data")

    print(json.dumps(incoming_data, indent=4))

    return {"message": "User signed up successfully"}

@app.post("/login")
async def login(logindata: LoginData):
    print("Received login data:", logindata)

    username = logindata.username
    password = logindata.password

    user = get_user_from_database(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed = user.get('password')
    verified_password = verify_password(password, hashed)

    if not verified_password:
        raise HTTPException(status_code=404, detail="Password is incorrect")

    return {"message": "Login successful"}



@app.get("/monitoring_data")
async def monitoring_data():
    print("Reading data from database")
    data = read_from_database()
    return data

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)