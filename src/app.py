"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from pymongo import MongoClient
from typing import Dict, List, Any

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# MongoDB connection
def get_db():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['school_activities_db']
    try:
        yield db
    finally:
        client.close()

# Helper function to convert MongoDB document to dictionary format
def format_activities_for_frontend(activities_from_db: List[Dict[str, Any]]) -> Dict[str, Any]:
    activities_dict = {}
    for activity in activities_from_db:
        activity_name = activity['name']
        activities_dict[activity_name] = {
            "description": activity['description'],
            "schedule": activity['schedule'],
            "max_participants": activity['max_participants'],
            "participants": activity['participants']
        }
    return activities_dict


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
async def get_activities(db=Depends(get_db)):
    """Get all activities"""
    activities_cursor = db.activities.find()
    activities_list = list(activities_cursor)
    return format_activities_for_frontend(activities_list)


@app.post("/activities/{activity_name}/signup")
async def signup_for_activity(activity_name: str, email: str, db=Depends(get_db)):
    """Sign up a student for an activity"""
    # Validate activity exists
    activity = db.activities.find_one({"name": activity_name})
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")
    
    # Add student to the activity
    result = db.activities.update_one(
        {"name": activity_name},
        {"$push": {"participants": email}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to sign up student")
        
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
async def unregister_from_activity(activity_name: str, email: str, db=Depends(get_db)):
    """Unregister a student from an activity"""
    # Validate activity exists
    activity = db.activities.find_one({"name": activity_name})
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")
    
    # Remove student from the activity
    result = db.activities.update_one(
        {"name": activity_name},
        {"$pull": {"participants": email}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to unregister student")
        
    return {"message": f"Unregistered {email} from {activity_name}"}