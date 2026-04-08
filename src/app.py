"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Train for competitive soccer matches and learn teamwork on the field",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Practice swimming techniques, drills, and endurance in the school pool",
        "schedule": "Tuesdays and Fridays, 4:00 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["maya@mergington.edu", "liam@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and digital art in a creative studio setting",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "noah@mergington.edu"]
    },
    "Drama Club": {
        "description": "Develop acting, stagecraft, and production skills for school performances",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
    },
    "Debate Society": {
        "description": "Research current issues and practice persuasive speaking in team debates",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["ryan@mergington.edu", "zoe@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Build problem-solving skills through science challenges and competitions",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["chloe@mergington.edu", "ethan@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
   """Sign up a student for an activity"""
   # Validate activity exists
   if activity_name not in activities:
      raise HTTPException(status_code=404, detail="Activity not found")

   # Get the activity
   activity = activities[activity_name]

   # Validate student is not already signed up
   if email in activity["participants"]:
     raise HTTPException(status_code=400, detail="Student is already signed up")

   # Add student
   activity["participants"].append(email)
   return {"message": f"Signed up {email} for {activity_name}"}