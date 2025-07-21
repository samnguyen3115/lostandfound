from sqlite3 import IntegrityError
import os
from flask import json
from config import Config
from app import create_app, db
from app.main.models import Post, Tag, Building
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db, 'Post': Post, 'Tag': Tag, 'Building': Building}

# Color and building data for initialization
color_tags = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown', 'black', 'white', 'gray']
building_tags = [
    'alden_memorial', 
    'atwater_ken_lab', 
    'fuller_lab', 
    'gordon_library', 
    'goddard_hall', 
    'higgins_lab', 
    'kaven_hall', 
    'olin_hall', 
    'campus_center', 
    'salisbury_lab', 
    'stratton_lab', 
    'innovation_studio', 
    'morgan_dining_hall', 
    'sports_recreation_center', 
    'harrington_auditorium', 
    'unity_hall', 
    'bartlett_center'
]

def initialize_database():
    """Initialize database with default data. Should be run once during setup."""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Add default tags if they don't exist
        add_default_tags()
        
        # Load and add building data
        data_file = "app/static/building_database/building.json"
        if os.path.exists(data_file):
            try:
                data = load_json_data(data_file)
                for building_data in data:
                    add_or_update_building(building_data)
                print("Database initialized successfully!")
            except Exception as e:
                print(f"Error loading building data: {e}")
        else:
            print(f"Warning: Building data file not found at {data_file}")

def add_default_tags():
    # Check if there are any tags in the database
    existing_tags = db.session.scalars(sqla.select(Tag)).all()
    existing_tag_names = {tag.name for tag in existing_tags} 

    # Add color tags
    for tag_name in color_tags:
        if tag_name not in existing_tag_names:
            db.session.add(Tag(name=tag_name, category="color"))
            print(f"Added color tag: {tag_name}")

    # Add building tags
    for tag_name in building_tags:
        if tag_name not in existing_tag_names:
            db.session.add(Tag(name=tag_name, category="building"))
            print(f"Added building tag: {tag_name}")

    # Commit changes to the database
    try:
        db.session.commit()
        print("Default tags added successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding default tags: {e}")

DATA_FILE = "app/static/building_database/building.json"


def load_json_data(file_path):
    """Load JSON data from file with error handling."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from {file_path}: {e}")
        return []

def add_or_update_building(json_data):
    with app.app_context():
        # Check if the record exists
        existing_building = Building.query.filter_by(building_id=json_data.get('building_id')).first()
        
        if existing_building:
            # Update existing record
            existing_building.name = json_data.get('name', existing_building.name)
            existing_building.count = json_data.get('count', existing_building.count)
            existing_building.title = json_data.get('title', existing_building.title)
            existing_building.body = json_data.get('body', existing_building.body)
            existing_building.theme_image_link = json_data.get('theme_image_link', existing_building.theme_image_link)
            existing_building.image_link = json_data.get('image_link', existing_building.image_link)
        else:
            # Create a new record
            new_building = Building(
                building_id=json_data.get('building_id'),
                name=json_data.get('name'),
                count=json_data.get('count'),
                title=json_data.get('title'),
                body=json_data.get('body'),
                theme_image_link=json_data.get('theme_image_link'),
                image_link=json_data.get('image_link')
            )
            db.session.add(new_building)
        
        # Commit the changes to the database
        try:
            db.session.commit()
            print(f"Building {json_data.get('name', 'Unknown')} added/updated successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding/updating building: {e}")

# Command to initialize database (run this once during setup)
@app.cli.command()
def init_db():
    """Initialize the database with default data."""
    initialize_database()

if __name__ == "__main__":
    app.run(debug=True)

