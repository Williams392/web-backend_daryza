# backend daryza 2025

## 🛠️ Installation


1. **Create Virtual Environment**
   ```powershell
   # Windows PowerShell
   python -m venv venv
   # macOS/Linux
   python3 -m venv venv
   ```

2. **Activate Virtual Environment**
   ```powershell
   # Windows PowerShell
   .\env\Scripts\activate
   # macOS/Linux
   source venv/Scripts/activate
   ```

3. **Install Dependencies**
   ```powershell
   # Windows PowerShell
   # For development
   pip install -r requirements.txt
   ```

4. **Navigate to the core Directory**
   ```bash
   cd core
   ```

5. **Apply Migrations**
    ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser** (Optional)
   ```powershell
   # Windows PowerShell
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user.


7. **Run Development Server**
   ```powershell
   # Windows PowerShell
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`
