# Library Management System

[![GitHub branch](https://img.shields.io/badge/branch-main-blue)](https://github.com/chrispl89/library_management_system/tree/main)
[![GitHub branch](https://img.shields.io/badge/branch-frontend-green)](https://github.com/chrispl89/library_management_system/tree/frontend)

A modern library management system with separated backend and frontend architecture.

## 📦 Branches Overview

### `main` branch
- **Backend-only** version
- Contains complete REST API with:
  - User authentication/authorization
  - Book management system
  - Email activation flow
  - Database models and migrations
- Stable version ready for production deployments

### `frontend` branch (**new!** 🎉) `WIP: developement phase`
- **Full-stack** version with Node.js frontend
- Includes all backend features from `main` branch plus:
  - User interface for library management
  - Login/registration forms
  - Interactive book dashboard
  - Role-based UI components
  
## 🚀 Getting Started

### For backend-only use (main branch):
```bash
git clone https://github.com/chrispl89/library_management_system.git
cd library_management_system
# Follow backend setup instructions in /django/README.md
```
### To work with frontend:
```bash
git clone https://github.com/chrispl89/library_management_system.git
cd library_management_system
git checkout frontend

# Install dependencies
cd frontend
npm install

# Start development server
npm start
```
### 🔄 Branch Workflow

- All frontend development happens in frontend branch

- Backend improvements are first merged to main, then propagated to frontend

- To contribute to frontend:
```bash
git checkout frontend
git checkout -b feature/your-feature-name
```

## Project Structure
```bash
📦library_management_system
├── 📂django # Django backend + web interface 
│ ├── README.md # Detailed Django setup/docs
│ └── ... # Django project files
├── 📂gui # Desktop GUI version (WIP)
│ ├── README.md # GUI-specific documentation
│ └── ... # GUI source files
├──📂frontend # Node.js frontend (WIP)
│ ├── README.md # frontend + web interface
│ └── ... # NODE.js project files
└── README.md # This file (project overview)

```

## Components

### 1. Django Web Version
Web-based solution with full library management capabilities.

**Features**:
- Book/member management
- Borrowing system
- Admin dashboard

📚 [See Django Documentation →](/django/README.md)

### 2. Desktop GUI (Work in Progress)
Experimental desktop interface for local management.

⚠️ **Status**: Early development phase

🖥️ [GUI Documentation →](/gui/README.md)


### 3. Frontend (Work in Progress)
web-based solution with UI

⚠️ **Status**: Early development phase

📚 [See Node.js Documentation →](https://github.com/chrispl89/library_management_system/blob/frontend/frontend/README.md)


## Contributing
Contributions welcome! Please follow:

Component-specific guidelines in each subfolder's README


## Note:
Current focus is frontend. GUI components are experimental, but will probably be developed in the future.