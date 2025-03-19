import dotenv

dotenv.load_dotenv()
import pandas as pd
from api.database import get_db
import api.db_models as db_models
import os

df = pd.read_csv("imagedata.csv")

with next(get_db()) as db:
    for index, row in df.iterrows():
        existing_image = (db.query(db_models.Image).filter(db_models.Image.image_id_drive == row["image_id"]).first())

        if not existing_image:
            image = db_models.Image(image_name=row["image_name"], image_id_drive=row["image_id"], event_id=row["event_id"])
            db.add(image)
            print(f"Added image {row['image_name']} to the database.")
        else:
            print(f"Image {row['image_name']} already exists in the database.")

    db.commit()
    print("Images added to the database.")

events = os.listdir("faiss_indexes")

with next(get_db()) as db:
    for event in events:
        existing_event = (db.query(db_models.Event).filter(db_models.Event.event_name == event).first())

        if not existing_event:
            event = db_models.Event(event_name=event)
            db.add(event)
            print(f"Added event {event.event_name} to the database.")
        else:
            print(f"Event {event} already exists in the database.")

    db.commit()
    print("Events added to the database.")