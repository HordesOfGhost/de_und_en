# from fastapi import APIRouter, Depends, HTTPException, Query, Path, Form
# from sqlalchemy.orm import Session
# from services.db.models import get_db
# from services.db.utils import get_model
# from services.db.crud_for_records import (
#     create_record as create_db_record,
#     get_records as get_all_db_records,
#     get_record as get_single_db_record,
#     update_record as update_db_record,
#     delete_record as delete_db_record,
# )
# from schemas.enums import TableName


# router = APIRouter()

# @router.post("/records", tags=['crud'])
# def create_record(
#     table_name: TableName = Query(..., description="Choose 'conversations' or 'translations'"),
#     english: str = Form(...),
#     german: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     Model = get_model(table_name)
#     record = create_db_record(db, Model, english, german)
#     return {"message": "Record created", "record": {
#         "id": record.id,
#         "english": record.english,
#         "german": record.german
#     }}

# @router.get("/records", tags=['crud'])
# def read_records(
#     table_name: TableName = Query(..., description="Choose 'conversations' or 'translations'"),
#     db: Session = Depends(get_db)
# ):
#     Model = get_model(table_name)
#     records = get_all_db_records(db, Model)
#     return [
#         {"id": r.id, "english": r.english, "german": r.german}
#         for r in records
#     ]

# @router.get("/records/{record_id}", tags=['crud'])
# def read_single_record(
#     record_id: int,
#     table_name: TableName = Query(..., description="Choose 'conversations' or 'translations'"),
#     db: Session = Depends(get_db)
# ):
#     Model = get_model(table_name)
#     record = get_single_db_record(db, Model, record_id )
#     if not record:
#         raise HTTPException(status_code=404, detail="Record not found")
#     return {"id": record.id, "english": record.english, "german": record.german}

# @router.put("/records/{record_id}", tags=['crud'])
# def update_record(
#     record_id: int = Path(...),
#     table_name: TableName = Query(..., description="Choose 'conversations' or 'translations'"),
#     english: str = Form(...),
#     german: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     Model = get_model(table_name)
#     record = get_single_db_record(db, Model, record_id)
#     if not record:
#         raise HTTPException(status_code=404, detail="Record not found")
#     update_db_record(db, Model, record_id, english, german)
#     return {"message": f"Record {record_id} updated", "record": {
#         "id": record.id,
#         "english": record.english,
#         "german": record.german
#     }}

# @router.delete("/records/{record_id}", tags=['crud'])
# def delete_record(
#     record_id: int,
#     table_name: TableName = Query(..., description="Choose 'conversations' or 'translations'"),
#     db: Session = Depends(get_db)
# ):
#     Model = get_model(table_name)
#     record = get_single_db_record(db, Model, record_id)
#     if not record:
#         raise HTTPException(status_code=404, detail="Record not found")

#     delete_db_record(db, Model, record_id)
#     return {"message": f"Deleted record {record_id} from {table_name}"}
