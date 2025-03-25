# Before running the backend

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure CSU credentials:
   Open `backend/crawler/run.py` and replace the placeholder credentials with your own:
   ```python
   USERNAME = "ADD_YOUR_CSU_ID_HERE"  # Replace with your CSU student ID
   PASSWORD = "ADD_YOUR_CSU_PASSWORD_HERE"  # Replace with your CSU password
   ```