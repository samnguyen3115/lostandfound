#!/usr/bin/env python3
"""
Add email verification columns to User table.
Run this script to update your database schema.
"""

from lostandfound import app
from app import db
from app.main.models import User
import sqlalchemy as sqla

def add_email_verification_columns():
    """Add email verification columns to existing User table."""
    with app.app_context():
        try:
            # Check if columns already exist
            inspector = sqla.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('user')]
            
            columns_to_add = []
            if 'email_verified' not in existing_columns:
                columns_to_add.append('email_verified BOOLEAN DEFAULT FALSE')
            if 'verification_code' not in existing_columns:
                columns_to_add.append('verification_code VARCHAR(5)')
            if 'verification_code_expires' not in existing_columns:
                columns_to_add.append('verification_code_expires TIMESTAMP')
            
            if columns_to_add:
                for column in columns_to_add:
                    sql = f'ALTER TABLE "user" ADD COLUMN {column};'
                    print(f"Executing: {sql}")
                    db.session.execute(sqla.text(sql))
                
                db.session.commit()
                print("Successfully added email verification columns!")
            else:
                print("Email verification columns already exist.")
                
        except Exception as e:
            db.session.rollback()
            print(f"Error adding columns: {e}")

if __name__ == "__main__":
    print("Adding email verification columns to User table...")
    add_email_verification_columns()