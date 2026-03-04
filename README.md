# Codingville AI Labs – UI Automation Framework

📌 **Overview**

This project is a professional UI Test Automation Framework built using:

- Python 3.12.x
- Pytest
- Playwright (Sync API)
- Page Object Model (POM)
- Parametrized Test Execution
- Automatic Video Recording
- Playwright Trace Collection

The framework automates AI Lab missions on the Codingville staging platform, validating end-to-end user workflows including mission progression, AI interaction, and final mission completion.

🏗 **Architecture & Design**

This framework follows modern automation best practices:

✔ **Page Object Model (POM)**  
All UI interactions are abstracted inside page classes to ensure:

- Clean separation of concerns
- Maintainability
- Reusability
- Scalability

✔ **Parametrized Execution**  
Multiple mission URLs are executed dynamically using Pytest parametrization.

✔ **Session Reuse**  
Authentication is performed once and reused across test sessions using Playwright storage state.

✔ **Test Isolation**  
Each test run:

- Records a dedicated browser video
- Generates a Playwright trace file
- Stores artifacts separately for debugging

🧪 **Automated Test Coverage**

🔐 **Authentication Setup**

- Logs in using teacher credentials
- Saves authenticated session state
- Enables fast execution of all mission tests

🧠 **AI Predictor Lab Automation**  
End-to-end mission validation including:

1. Navigate to mission URL
2. Close modal dialogs
3. Continue mission steps
4. Open settings & show model answer
5. Execute AI code
6. Handle iframe interactions
7. Complete mission flow
8. Validate success screen

🎨 **AI Image Generator Lab Automation**  
Automates:

- Mission step navigation
- AI level selection
- Image generation
- Iframe handling
- Final mission submission
- Completion validation

🎥 **Debugging & Artifacts**

For each executed test:

- 🎥 Browser session is recorded
- 📦 Playwright trace file is generated

To inspect a trace:

```bash
playwright show-trace trace.zip
```
⚙️ **Environment Setup**

✅ **Python Version & Virtual Environment**
This project is tested and supported on Python 3.12.x

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

Step 1 – Run Authentication Setup
```bash
pytest tests/test_auth_setup.py -s
```
Step 2 – Run All Tests
```bash
pytest -s
```