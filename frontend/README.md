# Legal AI Client - Frontend

Modern React web application for the AdvocaDabra Legal AI System.

## Tech Stack
- **React 19** - Latest React with modern hooks
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API communication
- **React Router** - Client-side routing
- **React Dropzone** - Drag-drop file uploads

## Features
- 🔐 **JWT Authentication** - Secure login/signup system
- 📤 **File Upload** - Drag-drop interface with progress tracking
- 🔍 **SCR Analysis** - Similar Case Retrieval interface
- 📚 **PCR Analysis** - Precedent Case Retrieval interface
- 📱 **Responsive Design** - Mobile-friendly interface
- ⚡ **Real-time Updates** - Live progress and status indicators

## Development

### Setup
```bash
npm install
```

### Development Server
```bash
npm run dev
```
Runs on: http://localhost:5173

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

## Project Structure

```
src/
├── App.jsx              # Main application component
├── main.jsx             # React entry point
├── index.css            # Global styles
├── components/          # Reusable UI components
│   ├── Navbar.jsx       # Navigation header
│   └── ProtectedRoute.jsx # Authentication guard
├── hooks/               # React custom hooks
│   └── useAuth.jsx      # Authentication context
├── lib/                 # Utilities and services
│   └── api.js           # API client with interceptors
├── routes/              # Page components
│   ├── Dashboard.jsx    # Main analysis dashboard
│   ├── Landing.jsx      # Homepage/welcome page
│   ├── Login.jsx        # User login form
│   └── Signup.jsx       # User registration form
└── styles/              # Additional stylesheets
    └── tailwind.css     # Tailwind directives
```

## API Integration

The frontend communicates with the Flask backend through:
- **Base URL**: `http://localhost:8000/api`
- **Authentication**: JWT tokens stored in localStorage
- **Interceptors**: Automatic token injection and error handling
- **File Uploads**: FormData with progress tracking

## Key Components

### Dashboard
- Integrated SCR/PCR analysis tabs
- Embedded file upload with drag-drop
- Real-time results display
- File management interface

### Authentication
- JWT-based authentication
- Persistent login sessions
- Protected route guards
- Automatic token refresh handling

### File Upload
- Multi-format support (PDF, TXT, JSON, CSV, Excel, Word)
- Progress tracking with visual feedback
- Success/error notifications
- File selection interface

## Environment Configuration

Default configuration works out of the box. To customize:

Create `.env.local`:
```
VITE_API_URL=http://localhost:8000/api
```

## Dependencies

### Production
- `react` - Core React library
- `react-dom` - React DOM rendering
- `react-router-dom` - Client-side routing
- `axios` - HTTP client
- `react-dropzone` - File upload component
- `lucide-react` - Icon library

### Development
- `@vitejs/plugin-react` - React support for Vite
- `tailwindcss` - CSS framework
- `autoprefixer` - CSS post-processor
- `eslint` - Code linting
- `vite` - Build tool and dev server
