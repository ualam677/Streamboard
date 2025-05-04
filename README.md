# Streamboard

Streamboard is a web-based application designed for managing and displaying tournament overlays. It allows users to create, customize, and control stream overlays for tournaments with ease.

## Features

- Create and edit stream overlays with drag-and-drop functionality.
- Customize fields such as player names, scores, and tournament details.
- Upload background images and logos for overlays.
- Dark mode support for better usability.
- Integration with Start.gg for fetching tournament and match data.

---

## Installation

### Backend (Django)

1. **Navigate to the backend directory**:
   ```bash
   cd streamboard_backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

   The backend will be available at `http://127.0.0.1:8000`.

---

### Frontend (Vue.js)

1. **Navigate to the frontend directory**:
   ```bash
   cd streamboard_frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://127.0.0.1:5173`.

---

## Usage

1. **Access the application**:
   - Open the frontend URL in your browser (`http://127.0.0.1:5173`).

2. **Sign up and log in**:
   - Create an account and log in to access the dashboard.

3. **Create a new streamboard**:
   - Navigate to "Create New" and customize your overlay with fields, background images, and logos.

4. **Manage streamboards**:
   - Use the "Manage Boards" section to edit or delete existing streamboards.

5. **Control overlays**:
   - Use the "Controller" to update live overlays during tournaments.

---

## Environment Variables

### Backend
- **`SECRET_KEY`**: Django secret key.
- **`DEBUG`**: Set to `True` for development.
- **`ALLOWED_HOSTS`**: Hosts allowed to access the backend.

### Frontend
- **`VITE_API_BASE_URL`**: Base URL for the backend API.

---

## Testing

### Backend
Run tests using:
```bash
python manage.py test
```


## License

This project is licensed under the MIT License.
