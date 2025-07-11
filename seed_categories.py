from db import SessionLocal, Base, engine
from models import Category

Base.metadata.create_all(bind=engine)

def seed_categories():
    session = SessionLocal()
    categories = [
        ('Tests', 'IREG'), ('Tests', 'Post Launch Outbound'), ('Tests', 'Post Launch Inbound'),
        ('Tests', 'Troubleshooting'), ('Tests', 'Emergency'),
        ('Work Orders', 'Company A'), ('Work Orders', 'Company B'),
        ('Tickets', 'Customer'), ('Tickets', 'Internal')
    ]
    for main, sub in categories:
        exists = session.query(Category).filter_by(main_category=main, sub_category=sub).first()
        if not exists:
            session.add(Category(main_category=main, sub_category=sub))
    session.commit()
    session.close()
    print("✅ Categories seeded.")

if __name__ == '__main__':
    seed_categories()
