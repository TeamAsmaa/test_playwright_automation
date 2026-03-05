# Codingville AI Labs – UI Automation Framework

📌 **Overview**

This project is a professional UI Test Automation Framework built using:

- Python 3.12
- Pytest
- Playwright (Sync API)
- Page Object Model (POM)
- Parametrized Test Execution
- Automatic Video Recording
- Playwright Trace Collection

🏗 **Architecture & Design**

This framework follows modern automation best practices:

✔ **Page Object Model (POM)**  
All UI interactions are abstracted inside page classes to ensure:

- Clean separation of concerns
- Maintainability
- Reusability
- Scalability

Example structure:
```bash
pages/
 ├── login_page.py
 └── Mission_Page.py
```
✔ **Pytest Fixtures**  
Shared setup and configuration logic is handled through pytest fixtures inside conftest.py

Fixtures are used for:

- Browser setup
- Page initialization
- Shared test configuration

✔ **Parametrized Execution**  
Multiple mission URLs are executed dynamically using Pytest parametrization.

## 🧪 Test Coverage

### 🔐 Login Test

Validates teacher authentication.

Steps:
- Navigate to login page
- Enter teacher credentials
- Submit login form
- Verify redirect to `/teacher/dashboard`

Test file:
tests/test_login.py

---

### 🧠 Mission Automation

Automates the full AI Lab mission workflow.

Steps:
- Login as teacher
- Open mission URL
- Wait for "Mission Instructions"
- Start mission and dismiss overlays
- Open settings and view model answer
- Run AI generation
- Validate successful backend request (HTTP 200–299)
- Continue mission actions until completion

Test file:
tests/test_missions.py

🎥 **Debugging & Artifacts**

For each executed test:

-  Browser session is recorded
-  Playwright trace file is generated

To inspect a trace:

```bash
playwright show-trace trace.zip
```
## 📂 Project Structure
```
pages/
 ├── login_page.py
 └── Mission_Page.py

tests/
 ├── test_login.py
 └── test_missions.py

conftest.py
pytest.ini
requirements.txt
README.md
```

## ⚙️ **Environment Setup**

### **Python Version & Virtual Environment**

This project is tested and supported on Python 3.12

**Create a virtual environment using Python 3.12:**
```bash
# Windows
py -3.12 -m venv venv
```

Activate the environment:
```bash
# Windows
venv\Scripts\activate
```
📦 **Install Dependencies**
```bash
# Windows
pip install -r requirements.txt
```
🌐 **Install Playwright Browsers**
```bash
playwright install
```
▶️**Running Tests**

Run Login Test
```bash
pytest tests/test_login.py -s
```
Run Mission Tests
```bash
pytest tests/test_missions.py -s
```
Run Mission Tests
```bash
pytest -s
```