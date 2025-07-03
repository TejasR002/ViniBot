# ViniBot - Multi-Agent Receptionist System

## Overview

**ViniBot** is a Multi-Agent Receptionist system designed to automate and streamline administrative operations in healthcare facilities. Leveraging intelligent agents, ViniBot efficiently manages patient data, schedules appointments, and oversees medical inventory, improving the overall workflow of a healthcare receptionist.

---

## System Architecture

The system consists of **three primary agents** and a **Supervisor Agent** that oversees and coordinates their activities:

### 1. Case Generator Agent
- **Role:** Handles patient information intake and classification.
- **Functions:**
  - Collects patient data including Name, Address, Date, Age, Marital Status, Sex, and Phone Number.
  - Performs Create, Read, Update, and Delete (CRUD) operations on patient records.
  - Identifies whether a patient is a new case or a follow-up.

### 2. Appointment Scheduler Agent
- **Role:** Manages scheduling of patient appointments.
- **Functions:**
  - Checks patient history for previous visits or relevant data.
  - Sends appointment notifications/messages to patients.
  - Finds available time slots and schedules appointments in 20–30 minute intervals.

### 3. Inventory Management (Medicine) Agent
- **Role:** Maintains and manages medical inventory.
- **Functions:**
  - Tracks medicine stock levels in real time.
  - Automatically places orders for medicines when stock is low.

### Supervisor Agent
- **Role:** Central controller and decision-maker.
- **Responsibilities:**
  - Monitors and coordinates all other agents.
  - Delegates tasks and ensures smooth workflow among the Case Generator, Appointment Scheduler, and Inventory Management agents.

---

## Features

- Efficient patient data management and classification.
- Automated appointment scheduling with notification system.
- Real-time medicine inventory tracking and restocking.
- Centralized supervision and coordination for consistent operations.

---

## Installation & Setup

Follow these steps to set up and run ViniBot:

1. **Create a virtual environment:**


   ```bash
   python -m venv venv
   ```
-  On Windows

```bash
 venv\Scripts\activate
```

-  On macOS/Linux

  ```bash
  source venv/bin/activate
  ```
2. **Install the required packages:**

  ```bash
  pip install -r requirements.txt

  ```
3. **Create a `.env` file:**

  - Add your OpenAI API key or modify the model configuration as needed.
  - Example `.env` content:
  ```bash
  OPENAI_API_KEY=your_openai_api_key_here
```
4. **Run the application:**
   ```bash
   streamlit run app.py
   ```
---
## 🐳 Docker Usage

### 📁 Project Structure (Required)

```
vinibot/
├── app.py
├── requirements.txt
├── Dockerfile
├── external.env      # <-- your .env file with secrets (OpenAI key etc.)
```

Your `.env` file (named `external.env`) should look like:

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

### 🔨 Step 1: Build Docker Image

```bash
docker build -t <NAME> .
```

---

### ▶️ Step 2: Run the Container (with external .env)

```bash
docker run -p 8501:8501 \
  -v $(pwd)/external.env:/app/.env \
  <NAME>
```

> 💡 On Windows PowerShell:
```powershell
docker run -p 8501:8501 `
  -v ${PWD}/external.env:/app/.env `
  <NAME>
```

Then open your browser at: [http://localhost:8501](http://localhost:8501)


