# Streamlit GUI Development Plan

This document breaks down the development of a clean, modern Streamlit GUI for the Mock JSON Data Generator into small, actionable tasks.

---

## 1. Project Setup
- [ ] Create a new directory for the Streamlit app
- [ ] Add/activate a virtual environment
- [ ] Install Streamlit and required dependencies (`pip install streamlit`)
- [ ] Set up initial `app.py` file
- [ ] Add README and requirements.txt for the GUI

---

## 2. Sidebar Navigation
- [ ] Design sidebar with menu options:
    - [ ] Generate Data
    - [ ] List Types
    - [ ] Preserve Fields
    - [ ] Analyze Data
    - [ ] Settings
    - [ ] About
- [ ] Implement menu selection logic to display the correct panel

---

## 3. Generate Data Panel
- [ ] Fetch available insurance types from backend (call backend function)
- [ ] Add dropdown for insurance type selection
- [ ] Add number input for number of records
- [ ] Add checkbox for "Save each record as a separate file"
- [ ] Add text input or file picker for output file/directory
- [ ] Add "Generate" button
- [ ] On generate, call backend logic to generate mock data with selected options
- [ ] Receive generated data or confirmation of files written from backend
- [ ] Provide download link or file path for generated data (integrate with backend file system)
- [ ] Handle and display backend errors (invalid type, generation failure, etc.)
- [ ] Display output status, file path, or download link

---

## 4. List Types Panel
- [ ] Call backend to fetch and display all supported insurance types
- [ ] Show as a clean table or list
- [ ] Optionally call backend for type descriptions
- [ ] Handle and display backend errors

---

## 5. Preserve Fields Panel
- [ ] Call backend to fetch current preserve fields from config
- [ ] Display preserve fields as a list
- [ ] Add text input and button to add a new field
- [ ] On add, call backend to add field to preserve fields and update config.yaml
- [ ] Add selection and button to remove a field
- [ ] On remove, call backend to remove field from preserve fields and update config.yaml
- [ ] Sync changes with config.yaml (backend integration)
- [ ] Show confirmation/status messages from backend
- [ ] Handle and display backend errors (duplicate field, field not found, etc.)

---

## 6. Analyze Data Panel
- [ ] Add button to run example data analysis
- [ ] On click, call backend analysis function (e.g., summarize_examples)
- [ ] Display insurance types found (list) from backend
- [ ] Display unique fields (list) from backend
- [ ] Show value distributions (table or chart) from backend
- [ ] Add button to export analysis report as JSON (call backend to generate and provide file)
- [ ] Provide download link for analysis report (integrate with backend file system)
- [ ] Handle and display backend errors

---

## 7. Settings Panel
- [ ] Call backend to read current paths and config
- [ ] Add inputs for Swagger, examples, and output paths
- [ ] Add file picker for config.yaml
- [ ] Add button to save settings
- [ ] On save, call backend to update paths/config and save changes
- [ ] Validate paths and config via backend
- [ ] Show current settings and status messages from backend
- [ ] Handle and display backend errors

---

## 8. About Panel
- [ ] Display project name, version, and author
- [ ] Add GitHub/project link
- [ ] Add short project description

---

## 9. UI Styling & Theming
- [ ] Apply Streamlit theming for a clean, modern look
- [ ] Ensure consistent layout and spacing
- [ ] Make UI accessible and responsive

---

## 10. Backend Integration (General)
- [ ] Connect all panels to backend logic (data generation, config, analysis)
- [ ] Ensure all file downloads (mock data, analysis reports) are accessible from frontend
- [ ] Handle errors and display user-friendly messages for all backend operations
- [ ] Propagate backend confirmations and status updates to the user

---

## 11. Testing & Feedback
- [ ] Test each panel and feature for usability
- [ ] Gather feedback from users
- [ ] Iterate and improve based on feedback 