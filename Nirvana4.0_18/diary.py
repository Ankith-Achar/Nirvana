from datetime import datetime, timedelta
from flask import session
from models import db, DiaryEntry, User

def get_all_entries():
    """Get all diary entries for the current logged-in user."""
    if 'user_id' not in session:
        return []
    
    entries = DiaryEntry.query.filter_by(user_id=session['user_id']).order_by(DiaryEntry.timestamp.desc()).all()
    
    # Convert to a format similar to the original (tuple-based) for compatibility
    formatted_entries = []
    for entry in entries:
        formatted_entries.append((
            entry.id,
            entry.title,
            entry.content,
            entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ))
    
    return formatted_entries

def add_entry(title, content):
    """Add a new diary entry for the current logged-in user."""
    if 'user_id' not in session:
        return False
    
    new_entry = DiaryEntry(
        title=title,
        content=content,
        user_id=session['user_id']
    )
    
    db.session.add(new_entry)
    db.session.commit()
    return True

def delete_entry(entry_id):
    """Delete a diary entry by ID, ensuring it belongs to the current user."""
    if 'user_id' not in session:
        return False
    
    entry = DiaryEntry.query.filter_by(id=entry_id, user_id=session['user_id']).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return True
    return False

def search_entries(title='', date=''):
    """Search diary entries of the current user by title and/or date."""
    if 'user_id' not in session:
        return []
    
    query = DiaryEntry.query.filter_by(user_id=session['user_id'])
    
    if title:
        query = query.filter(DiaryEntry.title.like(f'%{title}%'))
    
    if date:
        # Convert date string to datetime for comparison
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        next_day = date_obj + timedelta(days=1)
        query = query.filter(DiaryEntry.timestamp >= date_obj, DiaryEntry.timestamp < next_day)
    
    entries = query.order_by(DiaryEntry.timestamp.desc()).all()
    
    # Convert to a format similar to the original for compatibility
    formatted_entries = []
    for entry in entries:
        formatted_entries.append((
            entry.id,
            entry.title,
            entry.content,
            entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ))
    
    return formatted_entries