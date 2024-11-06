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

Download and unzip the data

## Step 4: Organize the Dataset

1. **Place the folders**:
   - Move the extracted `data` folder into the working directory.
   - Move the `clusters` folder into the working directory as well.

The structure should look like this:
```
snap-sorter-rewrite/
│
├── data/
├── clusters/
├── venv/
├── requirements.txt
└── (other project files)
```

## Step 5: Run it

```
streamlit run app_st.py
```