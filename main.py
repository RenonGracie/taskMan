from fasthtml.common import *

app, rt = fast_app()

@rt('/')
async def get():
    styles = Style("""
        body, .container {
            font-family: Arial, sans-serif;
            background-color: #333;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .content {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        h1 {
            color: #3b82f6;
            font-size: 4rem;
            margin-bottom: 20px;
        }
        #user-input {
            background-color: #444;
            color: #ccc;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            margin-bottom: 20px;
            width: 300px;
            text-align: center;
        }
        #my-button {
            background-color: #2563eb;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            width: 300px;
            text-align: center;
        }
        #my-button:hover {
            background-color: #1d4ed8;
        }
    """)

    # Create a text input for the user name
    user_input = Input(type='text', placeholder='name', id='user-input')

    # Create a button
    button = Button('Login', id='my-button', onclick='goToNextPage()')

    # JavaScript to handle button click and redirect
    script = Script("""
        function goToNextPage() {
            const userName = document.getElementById('user-input').value;
            if (userName) {
                window.location.href = `/welcome?name=${encodeURIComponent(userName)}`;
            } else {
                alert('Please enter your name.');
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            const userInput = document.getElementById('user-input');
            userInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    goToNextPage();
                }
            });
        });
    """)

    # Wrap the title, input, and button in a Div with class 'content'
    content = Div(H1('taskMan 🤷‍♂️'), user_input, button, cls='content')

    # Return the styled page with the script
    return Titled( styles, content, script, id='login-title')

@rt('/welcome')
async def welcome(name: str):
    styles = Style("""
        body {
            font-family: Arial, sans-serif;
            background-color: #333;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            padding: 0 20px;
        }
        .task {
            background-color: #f3f3f3;
            border-radius: 10px;
            margin-bottom: 10px;
            padding: 10px;
            transition: all 0.3s ease;
            width: 100%;
            box-shadow: 0 0 3px 1px rgba(255, 255, 255, 0.8); /* More intense white box shadow */
        }
        .task-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            cursor: pointer;
        }
        .task.expanded .task-header {
            cursor: default;
        }
        .task.expanded {
            flex-direction: column;
            align-items: flex-start;
        }
        .task-info {
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }
        .task-title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #3b82f6; /* Specific shade of blue */
        }
        .task-creator {
            font-size: 0.6rem;
            color: #555;
        }
        .task-due {
            font-size: 0.9rem;
            color: #555;
            flex-shrink: 0;
            margin-left: 20px;
        }
        .status {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            flex-shrink: 0;
            margin-left: 20px;
        }
        .status-red {
            background-color: #d13939;
        }
        .status-yellow {
            background-color: #d1d039;
        }
        .status-green {
            background-color: #51d139;
        }
        #add-task-button {
            background-color: #3b82f6;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            margin-left: 10px;
        }
        #add-task-button:hover {
            background-color: #1d4ed8;
        }
        .task-details {
            display: none;
            width: 100%;
            padding: 10px;
        }
        .task.expanded .task-details {
            display: flex;
            flex-direction: column;
        }
        .note-input-container {
            display: flex;
            align-items: flex-start; /* Align items to the top */
            width: 100%;
            margin-bottom: 0;
        }
        .note-input {
            flex-grow: 1;
            padding: 0 0.5em;
            border-radius: 0.3em;
            border: 1px solid #ccc;
            margin-right: 0.5em;
            height: 2.5em; /* Set a relative height */
            box-sizing: border-box;
            font-size: .7rem;
        }
        .add-note-button {
            background-color: #3b82f6;
            color: white;
            border: none;
            border-radius: 0.3em;
            cursor: pointer;
            height: 2.5em; /* Match the height of the input */
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 1em;
            white-space: nowrap;
            box-sizing: border-box;
        }
        .add-note-button:hover {
            background-color: #1d4ed8;
        }
        .notes {
            display: flex;
            flex-direction: column; /* Reverse the order */
            max-height: 200px;
            overflow-y: auto;
            width: 100%;
            font-size: .7rem;
        }
        .note {
            background-color: #274786;
            color: #f3f3f3;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 5px;
            display: flex;
            justify-content: space-between;
        }
        .note-timestamp {
            font-size: 0.6rem;
            color: #f3f3f3;
            margin-left: 10px;
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }
        .note-info {
            font-size: 0.6rem;
            color: #f3f3f3;
            display: flex;
            justify-content: flex-end;
            gap: 5px;
        }
        .button-container {
            display: flex;
            justify-content: space-between;
            width: 100%;
        }
        .content {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
        }
        .task-list {
            max-height: calc(6 * 100px); /* Adjust height based on task size */
            overflow-y: auto;
            width: 100%;
            position: relative;
            padding: 0 20px; /* Add padding to the sides */
        }

        .task-list::before,
        .task-list::after {
            content: '';
            position: sticky;
            left: 0;
            right: 0;
            height: 20px;
            pointer-events: none;
            z-index: 1;
        }

        .task-list::before {
            top: 0;
            background: linear-gradient(to bottom, rgba(51, 51, 51, 1), rgba(51, 51, 51, 0));
        }

        .task-list::after {
            bottom: 0;
            background: linear-gradient(to top, rgba(51, 51, 51, 1), rgba(51, 51, 51, 0));
        }

        .task {
            position: relative;
            z-index: 0;
        }
        .info-text {
            text-align: left;
            width: 100%;
            padding: 0 20px;
        }
        .sort-button {
            background-color: #3b82f6;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            margin-left: 10px;
        }

        .sort-button:hover {
            background-color: #1d4ed8;
        }

        .flash-background {
            animation: background-flash 0.25s ease-in-out 0s 2; /* Reduced duration */
        }

        @keyframes background-flash {
            0%, 100% { background-color: #444; }
            50% { background-color: #3b82f6; }
        }

        .priority-container {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            width: 100%;
        }

        .priority-box {
            display: flex;
            align-items: center;
            justify-content: center;
            width: calc(33.33% - 10px); /* Adjust width for spacing */
            height: 50px;
            background-color: #191C23;
            border-radius: 0.3em;
            box-shadow: none;
        }

        .priority-button {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            outline: none;
        }

        #priority-red {
            background-color: #d13939;
        }

        #priority-yellow {
            background-color: #d1d039;
        }

        #priority-green {
            background-color: #51d139;
        }

        .priority-button.selected {
            box-shadow: 0 0 0 3px #0065A0;
        }
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            background-color: #333; /* Match the page background */
            color: #ccc;
            font-size: 0.8rem;
            padding: 10px 0;
        }

        .footer-text {
            margin: 0;
            color: #505050;
        }
    """)

    script = Script(f"""
        let sortMode = 'priority'; // Initial sort mode

        function toggleSortMode() {{
            const sortButton = document.getElementById('sort-button');
            const taskList = document.querySelector('.task-list');
            const tasks = Array.from(taskList.children);

            if (sortMode === 'priority') {{
                sortMode = 'dueDate';
                sortButton.textContent = '⏱️';
                tasks.sort((a, b) => {{
                    const dateA = new Date(a.querySelector('.task-due').textContent.split(': ')[1]);
                    const dateB = new Date(b.querySelector('.task-due').textContent.split(': ')[1]);
                    return dateA - dateB;
                }});
            }} else {{
                sortMode = 'priority';
                sortButton.textContent = '🚦';
                tasks.sort((a, b) => {{
                    const priorityOrder = {{ 'red': 1, 'yellow': 2, 'green': 3 }};
                    const statusA = a.querySelector('.status').classList[1].split('-')[1];
                    const statusB = b.querySelector('.status').classList[1].split('-')[1];
                    return priorityOrder[statusA] - priorityOrder[statusB];
                }});
            }}

            taskList.innerHTML = '';
            tasks.forEach(task => taskList.appendChild(task));
        }}

        function toggleTaskDetails(taskElement) {{
            const notesSection = taskElement.querySelector('.notes');
            const taskDetails = taskElement.querySelector('.task-details');
            if (taskElement.classList.contains('expanded')) {{
                taskElement.classList.remove('expanded');
                notesSection.style.display = 'none';
                taskDetails.style.display = 'none';
            }} else {{
                taskElement.classList.add('expanded');
                notesSection.style.display = 'flex';
                taskDetails.style.display = 'flex';
            }}
        }}

        function addNoteToTask(taskElement) {{
            const noteInput = taskElement.querySelector('.note-input');
            const noteText = noteInput.value;
            if (noteText) {{
                const noteDiv = document.createElement('div');
                noteDiv.className = 'note';
                const timestamp = new Date().toLocaleString();
                noteDiv.innerHTML = `
                    <span>${{noteText}}</span>
                    <div class="note-info">
                        <span class="note-author">{name}</span><span class="note-timestamp">@ ${{timestamp}}</span>
                    </div>
                `;
                taskElement.querySelector('.notes').prepend(noteDiv);
                noteInput.value = '';
            }} else {{
                noteInput.classList.add('flash-background');
                setTimeout(() => noteInput.classList.remove('flash-background'), 1000);
            }}
        }}

        function attachEnterKeyListener(input) {{
            input.addEventListener('keydown', (e) => {{
                if (e.key === 'Enter') {{
                    e.preventDefault();
                    addNoteToTask(input.closest('.task'));
                }}
            }});
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            document.querySelectorAll('.note-input').forEach(attachEnterKeyListener);
        }});

        function showAddTaskModal() {{
            document.getElementById('add-task-modal').style.display = 'flex';
        }}

        function hideAddTaskModal() {{
            document.getElementById('add-task-modal').style.display = 'none';
        }}

        let selectedPriority = 'red'; // Default priority

        function setPriority(priority) {{
            selectedPriority = priority;
            document.querySelectorAll('.priority-button').forEach(button => {{
                button.classList.remove('selected');
            }});
            document.getElementById(`priority-${{priority}}`).classList.add('selected');
        }}

        function addTask() {{
            const taskTitle = document.getElementById('task-title').value;
            const dueDate = document.getElementById('due-date').value;
            const assignedTo = document.getElementById('assigned-to').value;
            if (taskTitle && dueDate && selectedPriority && assignedTo) {{
                const taskDiv = document.createElement('div');
                taskDiv.className = 'task';
                taskDiv.innerHTML = `
                    <div class="task-header" onclick="toggleTaskDetails(this.parentElement)">
                        <div class="task-info">
                            <div class="task-title">${{taskTitle}}</div>
                            <div class="task-creator">created by {name} for ${{assignedTo}}</div>
                        </div>
                        <div class="task-due">due date: ${{new Date(dueDate).toLocaleDateString()}}</div>
                        <div class="status status-${{selectedPriority}}"></div>
                    </div>
                    <div class="task-details">
                        <div class="note-input-container">
                            <input type="text" placeholder="Add a note" class="note-input">
                            <button class="add-note-button" onclick="addNoteToTask(this.parentElement.parentElement.parentElement)">Add Note</button>
                        </div>
                        <div class="notes"></div>
                    </div>
                `;
                document.querySelector('.task-list').appendChild(taskDiv);
                attachEnterKeyListener(taskDiv.querySelector('.note-input')); // Attach listener to new input
                hideAddTaskModal();
            }} else {{
                alert('Please fill in all fields.');
            }}
        }}
    """)

    tasks = [
        Div(
            Div(
                Div(
                    Div("clean house", cls="task-title"),
                    Div("created by john", cls="task-creator"),
                    cls="task-info"
                ),
                Div("due date: 10/19/2024", cls="task-due"),
                Div(cls="status status-red"),
                cls="task-header",
                onclick="toggleTaskDetails(this.parentElement)"
            ),
            Div(
                Div(
                    Input(type='text', placeholder='Add a note', cls='note-input'),
                    Button('Add Note', cls='add-note-button', onclick='addNoteToTask(this.parentElement.parentElement.parentElement)'),
                    cls='note-input-container'
                ),
                Div(
                    Div("<span>Note 1</span><div class='note-info'><span class='note-author'>John</span><span class='note-timestamp'>@ 10/10/23, 10:00 AM</span></div>", cls='note'),
                    Div("<span>Note 2</span><div class='note-info'><span class='note-author'>Jane</span><span class='note-timestamp'>@ 10/11/23, 11:00 AM</span></div>", cls='note'),
                    cls='notes'
                ),
                cls='task-details'
            ),
            cls="task"
        ),
        Div(
            Div(
                Div(
                    Div("wash car", cls="task-title"),
                    Div("created by mike", cls="task-creator"),
                    cls="task-info"
                ),
                Div("due date: 10/12/2025", cls="task-due"),
                Div(cls="status status-yellow"),
                cls="task-header",
                onclick="toggleTaskDetails(this.parentElement)"
            ),
            Div(
                Div(
                    Input(type='text', placeholder='Add a note', cls='note-input'),
                    Button('Add Note', cls='add-note-button', onclick='addNoteToTask(this.parentElement.parentElement.parentElement)'),
                    cls='note-input-container'
                ),
                Div(
                    Div("<span>Note 1</span><div class='note-info'><span class='note-author'>Mike</span><span class='note-timestamp'>@ 10/12/23, 9:00 AM</span></div>", cls='note'),
                    Div("<span>Note 2</span><div class='note-info'><span class='note-author'>Jane</span><span class='note-timestamp'>@ 10/13/23, 2:00 PM</span></div>", cls='note'),
                    cls='notes'
                ),
                cls='task-details'
            ),
            cls="task"
        ),
        Div(
            Div(
                Div(
                    Div("buy house", cls="task-title"),
                    Div("created by alex", cls="task-creator"),
                    cls="task-info"
                ),
                Div("due date: 10/13/2024", cls="task-due"),
                Div(cls="status status-green"),
                cls="task-header",
                onclick="toggleTaskDetails(this.parentElement)"
            ),
            Div(
                Div(
                    Input(type='text', placeholder='Add a note', cls='note-input'),
                    Button('Add Note', cls='add-note-button', onclick='addNoteToTask(this.parentElement.parentElement.parentElement)'),
                    cls='note-input-container'
                ),
                Div(
                    Div("<span>Note 1</span><div class='note-info'><span class='note-author'>Alex</span><span class='note-timestamp'>@ 10/14/23, 1:00 PM</span></div>", cls='note'),
                    Div("<span>Note 2</span><div class='note-info'><span class='note-author'>Jane</span><span class='note-timestamp'>@ 10/15/23, 3:00 PM</span></div>", cls='note'),
                    cls='notes'
                ),
                cls='task-details'
            ),
            cls="task"
        ),
        Div(
            Div(
                Div(
                    Div("grocery shopping", cls="task-title"),
                    Div("created by emma", cls="task-creator"),
                    cls="task-info"
                ),
                Div("due date: 11/01/2024", cls="task-due"),
                Div(cls="status status-yellow"),
                cls="task-header",
                onclick="toggleTaskDetails(this.parentElement)"
            ),
            Div(
                Div(
                    Input(type='text', placeholder='Add a note', cls='note-input'),
                    Button('Add Note', cls='add-note-button', onclick='addNoteToTask(this.parentElement.parentElement.parentElement)'),
                    cls='note-input-container'
                ),
                Div(
                    Div("<span>Note 1</span><div class='note-info'><span class='note-author'>Emma</span><span class='note-timestamp'>@ 10/16/23, 10:00 AM</span></div>", cls='note'),
                    Div("<span>Note 2</span><div class='note-info'><span class='note-author'>Jane</span><span class='note-timestamp'>@ 10/17/23, 11:00 AM</span></div>", cls='note'),
                    cls='notes'
                ),
                cls='task-details'
            ),
            cls="task"
        ),
        Div(
            Div(
                Div(
                    Div("finish project", cls="task-title"),
                    Div("created by liam", cls="task-creator"),
                    cls="task-info"
                ),
                Div("due date: 12/15/2024", cls="task-due"),
                Div(cls="status status-red"),
                cls="task-header",
                onclick="toggleTaskDetails(this.parentElement)"
            ),
            Div(
                Div(
                    Input(type='text', placeholder='Add a note', cls='note-input'),
                    Button('Add Note', cls='add-note-button', onclick='addNoteToTask(this.parentElement.parentElement.parentElement)'),
                    cls='note-input-container'
                ),
                Div(
                    Div("<span>Note 1</span><div class='note-info'><span class='note-author'>Liam</span><span class='note-timestamp'>@ 10/18/23, 10:00 AM</span></div>", cls='note'),
                    Div("<span>Note 2</span><div class='note-info'><span class='note-author'>Jane</span><span class='note-timestamp'>@ 10/19/23, 11:00 AM</span></div>", cls='note'),
                    cls='notes'
                ),
                cls='task-details'
            ),
            cls="task"
        ),
        Div(
            Div(
                Div(
                    Div("plan vacation", cls="task-title"),
                    Div("created by olivia", cls="task-creator"),
                    cls="task-info"
                ),
                Div("due date: 01/20/2025", cls="task-due"),
                Div(cls="status status-green"),
                cls="task-header",
                onclick="toggleTaskDetails(this.parentElement)"
            ),
            Div(
                Div(
                    Input(type='text', placeholder='Add a note', cls='note-input'),
                    Button('Add Note', cls='add-note-button', onclick='addNoteToTask(this.parentElement.parentElement.parentElement)'),
                    cls='note-input-container'
                ),
                Div(
                    Div("<span>Note 1</span><div class='note-info'><span class='note-author'>Olivia</span><span class='note-timestamp'>@ 10/21/23, 10:00 AM</span></div>", cls='note'),
                    Div("<span>Note 2</span><div class='note-info'><span class='note-author'>Jane</span><span class='note-timestamp'>@ 10/22/23, 11:00 AM</span></div>", cls='note'),
                    cls='notes'
                ),
                cls='task-details'
            ),
            cls="task"
        ),
        Div(
            Div(
                Div(
                    Div("read book", cls="task-title"),
                    Div("created by sophia", cls="task-creator"),
                    cls="task-info"
                ),
                Div("due date: 02/10/2025", cls="task-due"),
                Div(cls="status status-yellow"),
                cls="task-header",
                onclick="toggleTaskDetails(this.parentElement)"
            ),
            Div(
                Div(
                    Input(type='text', placeholder='Add a note', cls='note-input'),
                    Button('Add Note', cls='add-note-button', onclick='addNoteToTask(this.parentElement.parentElement.parentElement)'),
                    cls='note-input-container'
                ),
                Div(
                    Div("<span>Note 1</span><div class='note-info'><span class='note-author'>Sophia</span><span class='note-timestamp'>@ 10/23/23, 10:00 AM</span></div>", cls='note'),
                    Div("<span>Note 2</span><div class='note-info'><span class='note-author'>Jane</span><span class='note-timestamp'>@ 10/24/23, 11:00 AM</span></div>", cls='note'),
                    cls='notes'
                ),
                cls='task-details'
            ),
            cls="task"
        ),
        Div(
            Div(
                Div(
                    Div("exercise", cls="task-title"),
                    Div("created by noah", cls="task-creator"),
                    cls="task-info"
                ),
                Div("due date: 03/05/2025", cls="task-due"),
                Div(cls="status status-red"),
                cls="task-header",
                onclick="toggleTaskDetails(this.parentElement)"
            ),
            Div(
                Div(
                    Input(type='text', placeholder='Add a note', cls='note-input'),
                    Button('Add Note', cls='add-note-button', onclick='addNoteToTask(this.parentElement.parentElement.parentElement)'),
                    cls='note-input-container'
                ),
                Div(
                    Div("<span>Note 1</span><div class='note-info'><span class='note-author'>Noah</span><span class='note-timestamp'>@ 10/25/23, 10:00 AM</span></div>", cls='note'),
                    Div("<span>Note 2</span><div class='note-info'><span class='note-author'>Jane</span><span class='note-timestamp'>@ 10/26/23, 11:00 AM</span></div>", cls='note'),
                    cls='notes'
                ),
                cls='task-details'
            ),
            cls="task"
        ),
        Div(
            Div(
                Div(
                    Div("call mom", cls="task-title"),
                    Div("created by ava", cls="task-creator"),
                    cls="task-info"
                ),
                Div("due date: 04/15/2025", cls="task-due"),
                Div(cls="status status-green"),
                cls="task-header",
                onclick="toggleTaskDetails(this.parentElement)"
            ),
            Div(
                Div(
                    Input(type='text', placeholder='Add a note', cls='note-input'),
                    Button('Add Note', cls='add-note-button', onclick='addNoteToTask(this.parentElement.parentElement.parentElement)'),
                    cls='note-input-container'
                ),
                Div(
                    Div("<span>Note 1</span><div class='note-info'><span class='note-author'>Ava</span><span class='note-timestamp'>@ 10/27/23, 10:00 AM</span></div>", cls='note'),
                    Div("<span>Note 2</span><div class='note-info'><span class='note-author'>Jane</span><span class='note-timestamp'>@ 10/28/23, 11:00 AM</span></div>", cls='note'),
                    cls='notes'
                ),
                cls='task-details'
            ),
            cls="task"
        )
    ]

    modal = Div(
        Div(
            Input(type='text', placeholder='Task Title', id='task-title'),
            Input(type='date', id='due-date'),
            Input(type='text', placeholder='Assigned To', id='assigned-to'),
            Div(
                Div(Button('', id='priority-red', cls='priority-button', onclick='setPriority("red")'), cls='priority-box'),
                Div(Button('', id='priority-yellow', cls='priority-button', onclick='setPriority("yellow")'), cls='priority-box'),
                Div(Button('', id='priority-green', cls='priority-button', onclick='setPriority("green")'), cls='priority-box'),
                cls='priority-container'
            ),
            Div(
                Button('Add Task', onclick='addTask()'),
                Button('Cancel', onclick='hideAddTaskModal()'),
                cls='button-container'
            ),
            cls='modal-content'
        ),
        id='add-task-modal',
        cls='modal'
    )

    header = Div(
        H1(f"Welcome, {name.title()}!"),
        Div(
            Button("Add Task", id="add-task-button", onclick="showAddTaskModal()"),
            Button("↕️", id="sort-button", cls="sort-button", onclick="toggleSortMode()"),
            cls='button-group'
        ),
        cls='header'
    )

    task_list = Div(
        *tasks,
        cls='task-list'
    )

    footer = Div(
        P("taskMan version 1.0.1", cls='footer-text'),
        cls='footer'
    )

    content = Div(
        header,
        P("Click on a task to view notes.", cls='info-text'),
        task_list,
        footer,  # Add footer here
        cls='content'
    )

    return Titled(styles, content, modal, script, id='welcome-title')

serve()