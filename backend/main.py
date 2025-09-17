from fastapi import FastAPI,File , UploadFile,Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
from typing import List
from google.generativeai import types
import google.generativeai as genai
genai.configure(api_key="AIzaSyDHqx-cO7gyMH0JjH8dendrUt_Q5v3m9LY")
model = genai.GenerativeModel("gemini-2.5-flash")

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, set to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"Message":"Work in progress fck uh!"}
@app.get("/data")
def testing():
    return {"Data":[12,12,12]}


@app.post('/uploadimg/')
async def upload_image(file: UploadFile =File(...)):
    if not file.content_type.startswith("image/"):
        return JSONResponse(content={"error:":"only image allowed"}, status_code=400)
    img_bytes=await file.read()
    img=Image.open(io.BytesIO(img_bytes))
    response=model.generate_content(
         [
        "Describe the civic problem in this image in short. give the list of suggestion to explain this problem like this :[Pothhole, big pothhole due to rain , ] , aslo tell which department will help to solve it",
        img  # Directly pass the PIL image
    ]
    )
    return {"respone":response.text}
@app.post('/upload_details/')
async def upload_details (
    file:List[UploadFile]=File(...),
    description: str=Form(...),
    
    date:str=Form(...),
    time:str=Form(...),
    cordinates:str=Form(...),
    location:str=Form(...),
    department:str=Form(...)
):
    
   

    return {
        "description": description,
        "date": date,
        "time": time,
        "location": location,
        "cordinates":cordinates,
        "results": {},
        "department":{department}
    }



