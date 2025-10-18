# Library Management System - Frontend

React frontend application for the Library Management System, fully integrated with Django REST API backend.

## Features

- **Authentication**: JWT-based login and registration
- **Book Management**: Browse, search, and manage books (librarians only)
- **Loan System**: Borrow books and track active loans
- **Reservations**: Reserve books that are currently unavailable
- **Reviews**: Rate and review books
- **User Dashboard**: View personal activity, loans, reservations, and reviews
- **Google Books Integration**: Search and import books from Google Books API

## Tech Stack

- React 19
- React Router DOM for navigation
- Axios for API calls
- Bootstrap for styling
- Lucide React for icons
- JWT Decode for token management

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Django backend running on `http://127.0.0.1:8000`

## Installation

1. Install dependencies:
```bash
npm install
```

2. Make sure the Django backend is running on port 8000

3. Start the development server:
```bash
npm start
```

The application will open at [http://localhost:3000](http://localhost:3000)

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout.js          # Main layout with navigation
│   ├── context/
│   │   └── AuthContext.js     # Authentication context
│   ├── pages/
│   │   ├── Home.js            # Landing page
│   │   ├── Login.js           # Login page
│   │   ├── Register.js        # Registration page
│   │   ├── Books.js           # Books management
│   │   ├── Loans.js           # Loans management
│   │   ├── Reservations.js    # Reservations management
│   │   ├── Reviews.js         # Reviews management
│   │   └── Dashboard.js       # User dashboard
│   ├── services/
│   │   └── api.js             # API service layer
│   ├── App.js                 # Main app component
│   └── index.js               # Entry point
└── package.json
```

## API Integration

The frontend communicates with the Django backend through the following endpoints:

- **Authentication**: `/api/token/`, `/api/register/`
- **Books**: `/api/books/`
- **Loans**: `/api/loans/`
- **Reservations**: `/api/reservations/`
- **Reviews**: `/api/reviews/`
- **Dashboard**: `/api/dashboard/`
- **Google Books**: `/api/google-books/`

## User Roles

- **Reader**: Can browse books, borrow, reserve, and review
- **Librarian**: Can manage books (add, edit, delete) + all reader permissions
- **Admin**: Full system access including user management

## Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
