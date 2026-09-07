import requests
import streamlit as st


FASTAPI_URL = "http://127.0.0.1:8000"


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="RAG Assistant",
    page_icon="📚",
    layout="wide"
)


# =========================================================
# Session State
# =========================================================

if "projects" not in st.session_state:
    st.session_state.projects = {}

if "current_project_id" not in st.session_state:
    st.session_state.current_project_id = None

if "current_file_id" not in st.session_state:
    st.session_state.current_file_id = None

if "current_file_name" not in st.session_state:
    st.session_state.current_file_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_new_project" not in st.session_state:
    st.session_state.show_new_project = False

# =========================================================
# Load Projects from FastAPI
# =========================================================

if not st.session_state.projects:

    try:

        response = requests.get(
            f"{FASTAPI_URL}/projects/",
            timeout=30
        )

        if response.status_code == 200:

            data = response.json()

            projects = data.get(
                "projects",
                []
            )

            for project in projects:

                project_id = str(
                    project["project_id"]
                )

                file_id = None
                file_name = None

                # =================================================
                # Load Files for This Project
                # =================================================

                files_response = requests.get(
                    f"{FASTAPI_URL}/files/{project_id}",
                    timeout=30
                )

                if files_response.status_code == 200:

                    files_data = files_response.json()

                    files = files_data.get(
                        "files",
                        []
                    )

                    if files:

                        latest_file = files[-1]

                        file_id = latest_file.get(
                            "file_id"
                        )

                        file_name = latest_file.get(
                            "file_name"
                        )

                # =================================================
                # Save Project + File Information
                # =================================================

                st.session_state.projects[
                    project_id
                ] = {
                    "name": project["project_name"],
                    "file_id": file_id,
                    "file_name": file_name
                }

    except requests.exceptions.RequestException:

        pass  


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    .stApp {
        font-size: 20px;
    }

    .stMarkdown {
        font-size: 20px;
    }

    p {
        font-size: 20px;
    }

    h1 {
        font-size: 42px !important;
        font-weight: 700 !important;
    }

    h2 {
        font-size: 32px !important;
        font-weight: 700 !important;
    }

    h3 {
        font-size: 26px !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] {
        font-size: 20px;
    }

    [data-testid="stSidebar"] p {
        font-size: 19px;
    }

    [data-testid="stSidebar"] h1 {
        font-size: 30px !important;
    }

    [data-testid="stSidebar"] h2 {
        font-size: 26px !important;
    }

    [data-testid="stSidebar"] h3 {
        font-size: 23px !important;
    }

    .stButton button {
        font-size: 19px !important;
        font-weight: 600 !important;
        min-height: 48px;
    }

    .stTextInput input {
        font-size: 20px !important;
    }

    .stTextInput label {
        font-size: 19px !important;
    }

    /* =========================
   Chat
   ========================= */

    [data-testid="stChatMessage"] {
        font-size: 24px !important;
    }

    [data-testid="stChatMessage"] p {
        font-size: 24px !important;
        line-height: 1.8 !important;
    }

    [data-testid="stChatMessage"] li {
        font-size: 24px !important;
        line-height: 1.8 !important;
    }

    [data-testid="stChatMessage"] code {
        font-size: 21px !important;
    }

    [data-testid="stChatInput"] textarea {
        font-size: 22px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        font-size: 21px !important;
    }

    [data-testid="stFileUploader"] {
        font-size: 19px;
    }

    [data-testid="stFileUploader"] label {
        font-size: 20px !important;
    }

    [data-testid="stAlert"] {
        font-size: 19px !important;
    }

    [data-testid="stAlert"] p {
        font-size: 19px !important;
    }

    .stCaption {
        font-size: 17px !important;
    }

    hr {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.title("📚 RAG Assistant")

    st.divider()

  



    # =====================================================
    # New Project
    # =====================================================

    if st.button(
        "➕ New Project",
        use_container_width=True
    ):
        st.session_state.show_new_project = True

    # =====================================================
    # Create New Project
    # =====================================================

    if st.session_state.show_new_project:

        st.subheader("Create Project")

        project_name = st.text_input(
            "Project name",
            placeholder="e.g. Python Course"
        )

        col1, col2 = st.columns(2)

        with col1:
            create_project = st.button(
                "Create",
                use_container_width=True
            )

        with col2:
            cancel_project = st.button(
                "Cancel",
                use_container_width=True
            )

        if cancel_project:

            st.session_state.show_new_project = False
            st.rerun()

        if create_project:

            if not project_name.strip():

                st.warning(
                    "Please enter a project name."
                )

            else:

                # Generate project ID
                project_id = len(
                    st.session_state.projects
                ) + 1

                try:

                    # =================================================
                    # Create Project in FastAPI
                    # =================================================

                    response = requests.post(
                        f"{FASTAPI_URL}/projects/",
                        json={
                            "project_id": project_id,
                            "project_name": project_name.strip()
                        },
                        timeout=30
                    )

                    if response.status_code == 201:

                        data = response.json()

                        project = data["project"]

                        created_project_id = str(
                            project["project_id"]
                        )

                        # =================================================
                        # Save Project in Streamlit Session
                        # =================================================

                        st.session_state.projects[
                            created_project_id
                        ] = {
                            "name": project["project_name"],
                            "file_id": None,
                            "file_name": None
                        }

                        # =================================================
                        # Select New Project
                        # =================================================

                        st.session_state.current_project_id = (
                            created_project_id
                        )

                        st.session_state.current_file_id = None

                        st.session_state.current_file_name = None

                        st.session_state.messages = []

                        st.session_state.show_new_project = False

                        st.rerun()

                    else:

                        st.error(
                            "Project creation failed: "
                            f"{response.text}"
                        )

                except requests.exceptions.RequestException as e:

                    st.error(
                        "Could not connect to FastAPI: "
                        f"{e}"
                    )

    st.divider()

    # =====================================================
    # Projects
    # =====================================================

    st.subheader("Projects")

    if not st.session_state.projects:

        st.caption("No projects yet.")

    else:

        for project_id, project in (
            st.session_state.projects.items()
        ):

            is_current = (
                project_id
                == st.session_state.current_project_id
            )

            button_label = (
                f"📂 {project['name']}"
                if is_current
                else f"📁 {project['name']}"
            )

            if st.button(
                button_label,
                key=f"project_{project_id}",
                use_container_width=True
            ):

                st.session_state.current_project_id = (
                    project_id
                )

                st.session_state.current_file_id = (
                    project["file_id"]
                )

                st.session_state.current_file_name = (
                    project["file_name"]
                )

                st.session_state.messages = []

                st.rerun()

    st.divider()

    # =====================================================
    # Clear Chat
    # =====================================================

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# Main Area
# =========================================================

st.title("Document Chat")


# =========================================================
# No Project
# =========================================================

if st.session_state.current_project_id is None:

    st.info(
        "Create a project from the sidebar to get started."
    )

    st.stop()


# =========================================================
# Current Project
# =========================================================

current_project = st.session_state.projects[
    st.session_state.current_project_id
]

st.subheader(
    f"📁 {current_project['name']}"
)


# =========================================================
# File Upload
# =========================================================

uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "txt", "docx"]
)


if uploaded_file is not None:

    if st.button(
        "📤 Upload File",
        use_container_width=False
    ):

        try:

            # =================================================
            # 1. Upload File
            # =================================================

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            response = requests.post(
                f"{FASTAPI_URL}/files/upload/"
                f"{st.session_state.current_project_id}",
                files=files,
                timeout=60
            )

            if response.status_code == 201:

                data = response.json()

                file_data = data.get(
                    "file",
                    {}
                )

                file_id = file_data.get(
                    "file_id"
                )

                if not file_id:

                    st.error(
                        "Upload succeeded, "
                        "but file_id was not returned."
                    )

                    st.stop()

                # =================================================
                # 2. Process Document
                # =================================================

                with st.spinner(
                    "Processing document..."
                ):

                    process_response = requests.post(
                        f"{FASTAPI_URL}/documents/process/"
                        f"{st.session_state.current_project_id}/"
                        f"{file_id}",
                        timeout=180
                    )

                if process_response.status_code == 200:

                    # =================================================
                    # 3. Save File Information
                    # =================================================

                    current_project_id = (
                        st.session_state.current_project_id
                    )

                    st.session_state.projects[
                        current_project_id
                    ]["file_id"] = file_id

                    st.session_state.projects[
                        current_project_id
                    ]["file_name"] = uploaded_file.name

                    st.session_state.current_file_id = (
                        file_id
                    )

                    st.session_state.current_file_name = (
                        uploaded_file.name
                    )

                    process_data = (
                        process_response.json()
                    )

                    chunks = process_data.get(
                        "chunks",
                        []
                    )

                    st.success(
                        f"📄 {uploaded_file.name} "
                        "uploaded and processed successfully."
                    )

                    st.info(
                        f"Created {len(chunks)} chunks "
                        "and stored them in Qdrant."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Document processing failed: "
                        f"{process_response.text}"
                    )

            else:

                st.error(
                    f"Upload failed: {response.text}"
                )

        except requests.exceptions.RequestException as e:

            st.error(
                "Could not connect to FastAPI: "
                f"{e}"
            )


# =========================================================
# Current File
# =========================================================

if current_project["file_id"]:

    st.success(
        f"📄 {current_project['file_name']}"
    )

else:

    st.warning(
        "Upload a file before asking questions."
    )


st.divider()


# =========================================================
# Chat History
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# Chat Input
# =========================================================

query = st.chat_input(
    "Ask something about your document..."
)


if query:

    # =====================================================
    # Check File
    # =====================================================

    if not current_project["file_id"]:

        st.warning(
            "Please upload a file first."
        )

        st.stop()

    # =====================================================
    # User Message
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):

        st.markdown(query)

    # =====================================================
    # Assistant Response
    # =====================================================

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            try:

                response = requests.post(
                    f"{FASTAPI_URL}/rag/",
                    json={
                        "query": query,
                        "file_id": current_project["file_id"]
                    },
                    timeout=180
                )

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No answer returned."
                    )

                    st.markdown(answer)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                else:

                    error_message = (
                        "RAG request failed: "
                        f"{response.text}"
                    )

                    st.error(
                        error_message
                    )

            except requests.exceptions.RequestException as e:

                st.error(
                    "Could not connect to FastAPI: "
                    f"{e}"
                )


# =========================================================
# Footer
# =========================================================

st.divider()
