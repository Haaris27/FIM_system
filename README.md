# File Integrity Monitoring (FIM) System
A comprehensive solution for monitoring and maintaining file integrity across your systems. This project combines a Python backend for file monitoring and a Next.js frontend for visualization and management.

# 🚀 Features
Real-time file integrity monitoring
Change detection and alerting
User-friendly dashboard interface
Detailed reporting and analytics
Secure authentication system


# 🏗️ Project Structure
FIM_system/
├── fim/                  # Python virtual environment
├── frontend/             # Next.js frontend application
│   ├── components/       # React components
│   ├── pages/            # Next.js pages
│   ├── public/           # Static assets
│   ├── styles/           # CSS/SCSS styles
│   └── package.json      # Frontend dependencies
├── backend/              # Python backend code
│   ├── models/           # Data models
│   ├── routes/           # API endpoints
│   ├── utils/            # Utility functions
│   └── app.py            # Main application entry point
└── README.md             # Project documentation


# 🛠️ Installation
Prerequisites
Python 3.8+
Node.js 14+
npm or yarn



# Backend Setup
git clone https://github.com/Haaris27/FIM_system.git
cd FIM_system


# Set up Python virtual environment
python -m venv fim
fim/scripts/activate  # On Windows
 #source fim/bin/activate  # On Unix/MacOS

# Install Python dependencies
pip install -r requirements.txt

# Configure the application
Edit configuration files as needed


# Frontend Setup
Navigate to the frontend directory
cd frontend

# Install dependencies
npm i / npm install

# Build the application
npm run build



# 🚀 Running the Application

# Start the Backend
cd FIM_system
fim/scripts/activate
python app.py  # or the main Python file

# Start the Frontend
cd frontend
npm run build  # Only needed first time or after changes
npm start      # For production
npm run dev    # For development

# Access the application at http://localhost:3000
