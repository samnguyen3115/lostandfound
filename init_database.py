#!/usr/bin/env python3
"""
Database initialization script for Lost and Found application.
Run this script once to set up your database with default data.

Usage:
    python init_database.py
    
Or using Flask CLI:
    flask init-db
"""

from lostandfound import app, initialize_database

if __name__ == "__main__":
    print("Initializing database...")
    initialize_database()
    print("Database initialization complete!")
