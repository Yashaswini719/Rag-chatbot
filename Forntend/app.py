import uuid

import requests
import streamlit as st


BACKEND_URL = "http://localhost:8000"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Local RAG",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

    /* ---------- Global ---------- */

    .stApp {
        background: #0b0d12;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }

    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background: #10131a;
        border-right: 1px solid #242832;
    }

    section[data-testid="stSidebar"] .block-container {
        padding: 2rem 1.2rem;
    }

    .sidebar-brand {
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }

    .sidebar-subtitle {
        color: #8b93a5;
        font-size: 0.82rem;
        margin-bottom: 1.5rem;
    }

    .section-label {
        color: #8b93a5;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 1.3rem;
        margin-bottom: 0.7rem;
    }

    /* ---------- Main Header ---------- */

    .hero {
        padding: 0.5rem 0 1.5rem 0;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 750;
        letter-spacing: -0.045em;
        margin: 0;
        color: #f5f7fb;
    }

    .hero-subtitle {
        color: #8f97a8;
        font-size: 1rem;
        margin-top: 0.45rem;
    }

    .status-row {
        display: flex;
        gap: 0.55rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.38rem 0.7rem;
        border-radius: 999px;
        background: #151922;
        border: 1px solid #292e39;
        color: #b8c0cf;
        font-size: 0.75rem;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #55d98a;
    }

    /* ---------- Welcome ---------- */

    .welcome-card {
        border: 1px solid #292e39;
        background: #11151d;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
    }

    .welcome-title {
        font-size: 1.25rem;
        font-weight: 650;
        color: #f2f4f8;
        margin-bottom: 0.4rem;
    }

    .welcome-text {
        color: #9098a8;
        font-size: 0.92rem;
        margin-bottom: 1.2rem;
    }

    .suggestion {
        display: inline-block;
        padding: 0.55rem 0.8rem;
        margin: 0.25rem 0.25rem 0.25rem 0;
        border: 1px solid #2b303b;
        border-radius: 10px;
        color: #bfc6d3;
        background: #151922;
        font-size: 0.82rem;
    }

    /* ---------- Document cards ---------- */

    .document-card {
        background: #151820;
        border: 1px solid #282d37;
        border-radius: 12px;
        padding: 0.8rem;
        margin-bottom: 0.6rem;
    }

    .document-name {
        color: #e8ebf0;
        font-size: 0.83rem;
        font-weight: 600;
        word-break: break-word;
    }

    .document-meta {
        color: #7f8797;
        font-size: 0.72rem;
        margin-top: 0.2rem;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid #303641;
        background: #171b24;
        color: #e7eaf0;
        font-weight: 600;
        transition: 0.15s ease;
    }

    .stButton > button:hover {
        border-color: #596274;
        background: #1d222d;
        color: white;
    }

    /* ---------- File uploader ---------- */

    [data-testid="stFileUploader"] {
        background: #141821;
        border: 1px dashed #343b49;
        border-radius: 12px;
        padding: 0.3rem;
    }

    /* ---------- Chat ---------- */

    [data-testid="stChatMessage"] {
        border: 1px solid #242934;
        border-radius: 14px;
        margin-bottom: 0.8rem;
        padding: 0.2rem 0.4rem;
        background: #11151c;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: #151922;
    }

    /* ---------- Source ---------- */

    .source-header {
        color: #8d96a7;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.8rem;
    }

    /* ---------- Footer ---------- */

    .footer {
        text-align: center;
        color: #626a79;
        font-size: 0.72rem;
        padding: 1.5rem 0 0.5rem;
    }

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

def initialize_state():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "documents" not in st.session_state:
        st.session_state.documents = []

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())


# =========================================================
# BACKEND - DOCUMENTS
# =========================================================

def load_documents():

    try:

        response = requests.get(
            f"{BACKEND_URL}/documents",
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):
            return data.get("documents", [])

        if isinstance(data, list):
            return data

        return []

    except requests.RequestException as error:

        st.error(f"Could not load documents: {error}")

        return []


# =========================================================
# BACKEND - UPLOAD
# =========================================================

def upload_pdf(file):

    files = {
        "file": (
            file.name,
            file.getvalue(),
            "application/pdf",
        )
    }

    response = requests.post(
        f"{BACKEND_URL}/upload/",
        files=files,
        timeout=300,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# BACKEND - DELETE
# =========================================================

def delete_document(document_id):

    response = requests.delete(
        f"{BACKEND_URL}/documents/{document_id}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# BACKEND - CHAT
# =========================================================

def ask_question(question):

    payload = {
        "question": question,
        "session_id": st.session_state.session_id,
    }

    response = requests.post(
        f"{BACKEND_URL}/chat/",
        json=payload,
        timeout=300,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# SIDEBAR
# =========================================================

def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div class="sidebar-brand">◈ Local RAG</div>
            <div class="sidebar-subtitle">
                Private document intelligence
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---------------------------------------------
        # Upload
        # ---------------------------------------------

        st.markdown(
            '<div class="section-label">Add document</div>',
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Choose a PDF",
            type=["pdf"],
            label_visibility="collapsed",
        )

        if uploaded_file is not None:

            if st.button(
                "Upload & index",
                use_container_width=True,
            ):

                with st.spinner("Indexing document..."):

                    try:

                        upload_pdf(uploaded_file)

                        st.session_state.documents = (
                            load_documents()
                        )

                        st.success(
                            f"{uploaded_file.name} indexed"
                        )

                        st.rerun()

                    except requests.RequestException as error:

                        st.error(
                            f"Upload failed: {error}"
                        )

        # ---------------------------------------------
        # Indexed documents
        # ---------------------------------------------

        st.markdown(
            '<div class="section-label">Indexed documents</div>',
            unsafe_allow_html=True,
        )

        if not st.session_state.documents:

            st.caption(
                "No documents yet. Upload a PDF to get started."
            )

        else:

            for doc in st.session_state.documents:

                filename = doc.get(
                    "filename",
                    "Unnamed document",
                )

                chunks = doc.get(
                    "chunks",
                    0,
                )

                document_id = doc.get(
                    "document_id"
                )

                col1, col2 = st.columns(
                    [5, 1],
                    vertical_alignment="center",
                )

                with col1:

                    st.markdown(
                        f"""
                        <div class="document-card">
                            <div class="document-name">
                                📄 {filename}
                            </div>
                            <div class="document-meta">
                                {chunks} chunks
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col2:

                    if st.button(
                        "×",
                        key=f"delete_{document_id}",
                        help="Delete document",
                    ):

                        try:

                            delete_document(
                                document_id
                            )

                            st.session_state.documents = (
                                load_documents()
                            )

                            st.rerun()

                        except requests.RequestException as error:

                            st.error(
                                f"Delete failed: {error}"
                            )

        # ---------------------------------------------
        # New chat
        # ---------------------------------------------

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "＋  New chat",
            use_container_width=True,
        ):

            st.session_state.messages = []

            st.session_state.session_id = (
                str(uuid.uuid4())
            )

            st.rerun()

        # ---------------------------------------------
        # Local status
        # ---------------------------------------------

        st.markdown(
            """
            <div style="
                margin-top: 1.5rem;
                padding-top: 1rem;
                border-top: 1px solid #282d37;
            ">
                <div class="section-label">
                    Runtime
                </div>

                <div style="
                    color:#858d9d;
                    font-size:0.76rem;
                    line-height:1.9;
                ">
                    <span style="color:#55d98a;">●</span>
                    Local processing<br>

                    <span style="color:#55d98a;">●</span>
                    FastAPI backend<br>

                    <span style="color:#55d98a;">●</span>
                    Qdrant vector store<br>

                    <span style="color:#55d98a;">●</span>
                    Ollama LLM
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# MAIN HEADER
# =========================================================

def render_header():

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                Local RAG
            </div>

            <div class="hero-subtitle">
                Ask questions, search context, and chat with your
                documents — locally.
            </div>

            <div class="status-row">

                <div class="status-pill">
                    <span class="status-dot"></span>
                    Local
                </div>

                <div class="status-pill">
                    <span class="status-dot"></span>
                    Ollama
                </div>

                <div class="status-pill">
                    <span class="status-dot"></span>
                    Qdrant
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# WELCOME SCREEN
# =========================================================

def render_welcome():

    st.markdown(
        """
        <div class="welcome-card">

            <div class="welcome-title">
                Ask your documents anything
            </div>

            <div class="welcome-text">
                Upload a PDF from the sidebar, then ask questions
                about its content.
            </div>

            <div>
                <span class="suggestion">
                    What is this document about?
                </span>

                <span class="suggestion">
                    Summarize the key points
                </span>

                <span class="suggestion">
                    What are the main projects?
                </span>
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SOURCES
# =========================================================

def render_sources(sources):

    if not sources:
        return

    st.markdown(
        '<div class="source-header">Retrieved sources</div>',
        unsafe_allow_html=True,
    )

    # Avoid displaying duplicate source chunks
    seen = set()

    for index, source in enumerate(sources):

        filename = source.get(
            "filename",
            "Source",
        )

        chunk_index = source.get(
            "chunk_index",
            index,
        )

        text = source.get(
            "text",
            "",
        )

        source_key = (
            filename,
            chunk_index,
        )

        if source_key in seen:
            continue

        seen.add(source_key)

        label = f"📄 {filename}"

        if chunk_index is not None:
            label += f"  ·  chunk {chunk_index}"

        with st.expander(label):

            st.markdown(text)


# =========================================================
# CHAT
# =========================================================

def render_chat():

    # Header
    render_header()

    # Welcome
    if not st.session_state.messages:
        render_welcome()

    # Existing messages
    for message in st.session_state.messages:

        role = message["role"]

        with st.chat_message(role):

            st.markdown(
                message["content"]
            )

            if (
                role == "assistant"
                and message.get("sources")
            ):

                render_sources(
                    message["sources"]
                )

    # Chat input
    question = st.chat_input(
        "Ask anything about your documents..."
    )

    if not question:
        return

    # ---------------------------------------------
    # User message
    # ---------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # ---------------------------------------------
    # Assistant response
    # ---------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Searching your documents..."):

            try:

                result = ask_question(
                    question
                )

                answer = result.get(
                    "answer",
                    "I couldn't generate an answer.",
                )

                sources = result.get(
                    "sources",
                    [],
                )

            except requests.RequestException as error:

                answer = (
                    "I couldn't connect to the RAG backend. "
                    f"Please make sure FastAPI is running.\n\n"
                    f"`{error}`"
                )

                sources = []

        st.markdown(answer)

        render_sources(
            sources
        )

    # Save response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )


# =========================================================
# MAIN
# =========================================================

def main():

    initialize_state()

    # Load documents
    st.session_state.documents = load_documents()

    render_sidebar()

    render_chat()

    st.markdown(
        """
        <div class="footer">
            Local RAG · Streamlit · FastAPI · Qdrant · Ollama
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()