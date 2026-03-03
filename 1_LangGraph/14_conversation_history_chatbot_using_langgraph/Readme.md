## Conversation_History Chatbot using Streamlit

## Step 1: Add a Sidebar with Title
- Create a sidebar component with a suitable title.
  
### 1.1 Generate Dynamic `thread_id`
- Generate a dynamic `thread_id`.
- Add the generated `thread_id` to the session.

### 1.2 Display `thread_id` in Sidebar
- Display the current `thread_id` inside the sidebar.

---

## Step 2: Add a "New Chat" Button

- Add a **New Chat** button to the interface.

### On Click of "New Chat" Button:

#### 2.1 Open a New Chat Window
- Open a fresh chat window.

#### 2.2 Generate a New `thread_id`
- Create a new dynamic `thread_id`.

#### 2.3 Save `thread_id` in Session
- Store the newly generated `thread_id` in the session.

#### 2.4 Reset Message History
- Clear the previous conversation history.

---

## Step 3: Create a List to Store All `thread_id`s
- Maintain a list to store all generated `thread_id`s.

---

## Step 4: Load All `thread_id`s in the Sidebar
- Display all stored `thread_id`s in the sidebar.

---

## Step 5: Convert Sidebar Items to Clickable Buttons
- Make each `thread_id` in the sidebar clickable.

---

## Step 6: Load Conversation on Click
- On clicking a particular `thread_id`, load the corresponding conversation history.

