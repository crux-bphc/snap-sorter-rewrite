import dotenv

dotenv.load_dotenv()
import pandas as pd
from api.database import get_db
import api.db_models as db_models

df = pd.read_csv("imagedata.csv")

with next(get_db()) as db:
    for index, row in df.iterrows():
        image = db_models.Image(
            image_name=row["image_name"], image_id_drive=row["image_id"]
        )
        db.add(image)
    db.commit()
    print("Images added to the database.")
