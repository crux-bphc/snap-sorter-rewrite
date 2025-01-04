# Snap Sorter Setup

Simple guide to get this project up and running.

## Step 1: Set Up a Virtual Environment

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **On macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

## Step 2: Install Dependencies

Once the virtual environment is activated, install the required packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Step 3: Download the Data

Download the dataset from the following link:

https://drive.google.com/file/d/1l3PhT_iwu7gKe7Vyen-EISPFDhlzZtjq/view?usp=sharing

Unzip the downloaded file.

## Step 4: Organize the Dataset

1. **Place the folders:**
   - Move the extracted `data` folder into the working directory.
   - Move the `clusters` folder into the working directory as well.

The structure should look like this:
```
backend/
│
├── data/
├── clusters/
├── venv/
├── requirements.txt
└── (other project files)
```

## Step 5: Set Up Postgres

1. Install PostgreSQL and set up the database.
2. Create a database and a user with appropriate permissions.
3. Note down the database name, username, and password for the `.env` file.

## Step 6: Set Up the `.env` File

Create a `.env` file in the root directory and populate it with the following keys:

```
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
SESSION_SECRET_KEY=
FRONTEND_REDIRECT_URI=http://localhost:8080/#/upload
IMAGES_BASE_URL=http://127.0.0.1:8000/images
STATIC_BASE_URL=http://127.0.0.1:8000/static
OAUTH2_SECRET_KEY=
OAUTH2_ALGORITHM=HS256
OAUTH2_EXPIRATION_MINUTES=30
DB_NAME=
DB_USER=
DB_PASS=
```

Fill in the missing values with your specific credentials and settings. You can change the `FRONTEND_REDIRECT_URI` as needed.

## Step 7: Run the Application

Run the FastAPI server using the following command:

```bash
fastapi dev main.py
```

On running this for the first time, tables in the database will be automatically created and setup. To populate the database, run the following script:

```
python db_populator.py
```

## Step 8: Check Out the Documentation

Once the server is running, access the API documentation at the following URL:

```
http://127.0.0.1:8000/docs
```

API documentation can be found here.
