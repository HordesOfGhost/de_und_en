from sqlalchemy.orm import Session

def create_record(db: Session, model, english: str, german: str):
    record = model(english=english, german=german)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_records(db: Session, model):
    return db.query(model).all()

def get_record(db: Session, model, record_id: int):
    return db.query(model).get(record_id)

def update_record(db: Session, model, record_id: int, english: str, german: str):
    record = db.query(model).get(record_id)
    if not record:
        return None
    record.english = english
    record.german = german
    db.commit()
    db.refresh(record)
    return record

def delete_record(db: Session, model, record_id: int):
    record = db.query(model).get(record_id)
    if not record:
        return None
    db.delete(record)
    db.commit()
    return record
