#!/usr/bin/env python3
"""
Script to populate MongoDB with initial activity data.
"""

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['school_activities_db']
activities_collection = db['activities']

# Clear existing data if any
activities_collection.delete_many({})

# Initial activities data
activities = {
    "Chess Club": {
        "name": "Chess Club",
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "name": "Programming Class",
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "name": "Gym Class",
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "name": "Basketball Team",
        "description": "Join the school basketball team and compete in local tournaments",
        "schedule": "Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Soccer Club": {
        "name": "Soccer Club",
        "description": "Practice soccer skills and play friendly matches",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Drama Club": {
        "name": "Drama Club",
        "description": "Act, direct, and produce school plays and performances",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Art Workshop": {
        "name": "Art Workshop",
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": []
    },
    "Debate Team": {
        "name": "Debate Team",
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 10,
        "participants": []
    },
    "Math Club": {
        "name": "Math Club",
        "description": "Solve challenging math problems and prepare for competitions",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 12,
        "participants": []
    }
}

# Insert activities as individual documents
for key, activity in activities.items():
    activities_collection.insert_one(activity)

print(f"Successfully populated database with {len(activities)} activities")

# List all collections in the database
print("\nCollections in the database:")
for collection in db.list_collection_names():
    print(f" - {collection}")

# List all activities in the collection
print("\nActivities in the collection:")
for activity in activities_collection.find():
    print(f" - {activity['name']}: {len(activity['participants'])} participants")
