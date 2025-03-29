# DIICSU Room Booking System

This is a comprehensive system for managing room reservations, developed by our team **Return False**. It offers features such as real-time availability checks, conflict detection, and a user-friendly interface for administrators, staff, and students.

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Directory Structure](#directory-structure)  
3. [Getting Started](#getting-started)  
4. [Usage](#usage)  
5. [Contributing](#contributing)  
6. [License](#license)
7. [Note](#note)
8. [Acknowledgements](#acknowledgements)
9. [User Manual (PDF)](#user-manual-pdf)
---

## Project Overview

The Intelligent Room Booking System aims to simplify and streamline the process of reserving rooms for meetings, events, or classes. Our system provides:
- A **web-based frontend** for intuitive interaction.
- A **Python-based backend** for handling reservations, conflicts, and real-time availability.
- Administrative tools for **room management**, **user blacklist management**, **repair handling**, and more.

---

## Directory Structure

Below is a brief description of the main folders and files:

```
INTELLIGENT-ROOM-BOOKING-SYSTEM/
├── .idea/                    // IDE-specific configurations (optional)
├── backend/
│   ├── app/                  // Core application code (e.g., routes, logic)
│   ├── crawler/              // Scripts or modules for CSU timetable scraping/updates
│   ├── README.md             // Additional info about backend usage
│   ├── requirements.txt      // Python dependencies
│   └── run.py                // Main execution script for the backend
│   
├── frontend/
│   ├── .vscode/              // VSCode-specific settings
│   ├── public/               // Static files
│   ├── src/                  // Frontend source code
│   ├── .gitignore            // Git ignore rules for the frontend
│   ├── index.html            // Main HTML file
│   ├── jsconfig.json         // JS/TS config
│   ├── package.json          // NPM dependencies and scripts
│   ├── package-lock.json     // Locked versions of installed packages
│   ├── README.md             // Additional info about frontend usage
│   └── vite.config.js        // Vite configuration
├── .gitignore                // Top-level Git ignore rules
├── User Manual.pdf           // Clickable link in this README points here
└── README.md                 // You are here
```

---

## Getting Started

### Prerequisites

- **Python 3.8+** (or a suitable version to match the `requirements.txt` in `backend/`)
- **Node.js & npm** (for building and running the frontend)
- A virtual environment tool such as **venv** (recommended) for Python dependency management

### Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/eddy-Wang/Intelligent-Room-Booking-System.git
   cd Intelligent-Room-Booking-System
   ```

2. **Backend Setup**  
    First, install dependencies:
   ```bash
   cd backend
   python -m venv venv        # (Optional) Create a virtual environment
   source venv/bin/activate   # On macOS/Linux
   # .\venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

    Then, configure CSU credentials:
   Open `backend/crawler/crawler.py` and replace the placeholder credentials with your own, for auto-crawler to download and fetch CSU timetable.
   ```python
   USERNAME = "ADD_YOUR_CSU_ID_HERE"  # Replace with your CSU student ID
   PASSWORD = "ADD_YOUR_CSU_PASSWORD_HERE"  # Replace with your CSU password
   ```

3. **Frontend Setup**  
   ```bash
   cd ../frontend
   npm install
   ```

---

## Usage

### Running the Backend

From the `backend` directory:
```bash
python run.py
```
- This command will start the backend server (adjust port and settings in the code if needed).
- Alternatively, you can use `python main.py` if that is your primary entry point.

### Running the Frontend

From the `frontend` directory:
```bash
npm run dev
```
- This command will start a local development server (default: http://localhost:3000 or specified by Vite).

### Accessing the Application

Open your web browser and navigate to:
```
http://localhost:5173/
http://127.0.0.1:5173/
```
You should see the login or home page for the Intelligent Room Booking System.

---

## Contributing

We welcome contributions from the community! To get started:

1. Fork this repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes and push them to GitHub:
   ```bash
   git commit -m "Add amazing feature"
   git push origin feature/amazing-feature
   ```
4. Open a pull request describing your changes.

---

## License

This project is licensed under the MIT License. Feel free to use and modify the code for your own projects under the terms of the license.

---
## Note

Our database will expire on 2025.4.6. It will not be available at that time.

---

## Acknowledgements

We, **team Return False**, would like to express our heartfelt gratitude for the passion and effort that each of us—**Tianshuo Wang**, **Jiashuo Chang**, **Yan Chen**, **Qi Xiao**, **Yaxin Huang**, **Hongyun Yu**, **Zekun Li**, and **Yixi Huang**—contributed to developing the DIICSU Room Booking System. Working together on this project has been an incredibly inspiring and rewarding experience.

We also appreciate the valuable feedback and support from the GitHub community. For more details about our project and to follow our progress, please visit our GitHub page:  
[https://github.com/eddy-Wang/Intelligent-Room-Booking-System](https://github.com/eddy-Wang/Intelligent-Room-Booking-System)

Thank you for being a part of this journey with us!

---

## User Manual (PDF)
For a detailed guide on how to use the system—including booking procedures, room management, and administrative functions—please refer to our [User Manual](./User%20Manual.pdf).

