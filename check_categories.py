from db import SessionLocal
from models import Category

session = SessionLocal()
categories = session.query(Category).all()
if not categories:
    print("🚫 No categories found in the database.")
else:
    print("✅ Categories in DB:")
    for c in categories:
        print(f"{c.id}: {c.main_category} > {c.sub_category}")
session.close()
