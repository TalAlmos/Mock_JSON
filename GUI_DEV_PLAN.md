# Streamlit GUI Development Plan

This document breaks down the development of a clean, modern Streamlit GUI for the Mock JSON Data Generator into small, actionable tasks.

---

## 1. Project Setup
- [x] Create a new directory for the Streamlit app
- [x] Add/activate a virtual environment
- [x] Install Streamlit and required dependencies (`pip install streamlit`)
- [x] Set up initial `app.py` file
- [x] Add README and requirements.txt for the GUI

---

## 2. Sidebar Navigation
- [x] Design sidebar with menu options:
    - [x] Generate Data
    - [x] List Types
    - [x] Preserve Fields
    - [x] Analyze Data
    - [x] Settings
    - [x] About
- [x] Implement menu selection logic to display the correct panel

---

## 3. Generate Data Panel
- [x] Fetch available insurance types from backend (call backend function)
- [x] Add dropdown for insurance type selection
- [x] Add number input for number of records
- [x] Add checkbox for "Save each record as a separate file"
- [x] Add text input or file picker for output file/directory
- [x] Add "Generate" button
- [x] On generate, call backend logic to generate mock data with selected options
- [x] Receive generated data or confirmation of files written from backend
- [x] Provide download link or file path for generated data (integrate with backend file system)
- [x] Handle and display backend errors (invalid type, generation failure, etc.)
- [x] Display output status, file path, or download link

---

## 4. List Types Panel
- [x] Call backend to fetch and display all supported insurance types
- [x] Show as a clean table or list
- [x] Optionally call backend for type descriptions
- [x] Handle and display backend errors

---

## 5. Preserve Fields Panel
- [x] Call backend to fetch current preserve fields from config
- [x] Display preserve fields as a list
- [x] Add text input and button to add a new field
- [x] On add, call backend to add field to preserve fields and update config.yaml
- [x] Add selection and button to remove a field
- [x] On remove, call backend to remove field from preserve fields and update config.yaml
- [x] Sync changes with config.yaml (backend integration)
- [x] Show confirmation/status messages from backend
- [x] Handle and display backend errors (duplicate field, field not found, etc.)

---

## 6. Analyze Data Panel
- [x] Add button to run example data analysis
- [x] On click, call backend analysis function (e.g., summarize_examples)
- [x] Display insurance types found (list) from backend
- [x] Display unique fields (list) from backend
- [x] Show value distributions (table or chart) from backend
- [x] Add button to export analysis report as JSON (call backend to generate and provide file)
- [x] Provide download link for analysis report (integrate with backend file system)
- [x] Handle and display backend errors

---

## 7. Settings Panel
- [x] Call backend to read current paths and config
- [x] Show current settings and status messages from backend
- [x] Add inputs for Swagger, examples, and output paths
- [x] Add file picker for config.yaml
- [x] Add button to save settings
- [x] On save, call backend to update paths/config and save changes
- [x] Validate paths and config via backend
- [x] Handle and display backend errors

---

## 8. About Panel
- [x] Display project name, version, and author
- [x] Add GitHub/project link
- [x] Add short project description

---

## 9. UI Styling & Theming
- [x] Apply Streamlit theming for a clean, modern look
- [x] Ensure consistent layout and spacing
- [x] Make UI accessible and responsive

---

## 10. Backend Integration (General)
- [x] Connect all panels to backend logic (data generation, config, analysis)
- [x] Ensure all file downloads (mock data, analysis reports) are accessible from frontend
- [x] Handle errors and display user-friendly messages for all backend operations
- [x] Propagate backend confirmations and status updates to the user

---

## 11. Testing & Feedback
- [ ] Test each panel and feature for usability
- [ ] Gather feedback from users
- [ ] Iterate and improve based on feedback 