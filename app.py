
import sqlite3
from pathlib import Path
from llm_assistant import explain_with_llm
import streamlit as st
from local_assistant import answer_question, debug_labels

# ==========================================
# 1. CONFIGURATION
# ==========================================

DATABASE_PATH = Path("database/floorplans.db")

DATASET_DIR = Path(
    r"C:\Users\Acharya\Downloads\archive\FP_annotation for sell"
)


# ==========================================
# 2. DATABASE FUNCTIONS
# ==========================================

def get_floorplans():
    if not DATABASE_PATH.exists():
        return []

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT floorplan_name
            FROM floorplans
            ORDER BY floorplan_name
        """)
        return [row[0] for row in cursor.fetchall()]


# ==========================================
# 3. FLOOR PLAN IMAGE DISPLAY
# ==========================================

def find_original_image(plan_name):
    for extension in [".png", ".jpg", ".jpeg"]:
        image_path = DATASET_DIR / f"{plan_name}{extension}"

        if image_path.exists():
            return image_path

    return None


def show_floorplan_images(plan_name):
    st.subheader("Floor Plan Visualisation")

    original_path = find_original_image(plan_name)
    overlay_path = DATASET_DIR / f"{plan_name}_overlay.png"

    col1, col2 = st.columns(2)

    with col1:
        st.write("Original Floor Plan")

        if original_path:
            st.image(str(original_path), width="stretch")
        else:
            st.info("Original floor plan image not found.")

    with col2:
        st.write("Annotation Overlay")

        if overlay_path.exists():
            st.image(str(overlay_path), width="stretch")
        else:
            st.info("Annotation overlay not found.")


# ==========================================
# 4. STREAMLIT CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Ask Your Floor Plan",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Ask Your Floor Plan")

st.write(
    "An assistant for exploring building floor plans "
    "and their annotated objects."
)

st.divider()


# ==========================================
# 5. SELECT FLOOR PLAN
# ==========================================

plans = get_floorplans()

if not plans:
    st.error(
        "No floor plans found. Check database/floorplans.db "
        "and make sure it contains floor-plan records."
    )
    st.stop()

selected_plan = st.selectbox(
    "Select a floor plan:",
    plans
)


# ==========================================
# 6. DISPLAY FLOOR PLAN
# ==========================================

show_floorplan_images(selected_plan)

st.divider()


# ==========================================
# 7. QUESTION ANSWERING
# ==========================================


# ==========================================
# 7. QUESTION ANSWERING
# ==========================================

st.subheader("Ask a Question")

question = st.text_input(
    "Enter your question:",
    placeholder="Example: How many doors are there?"
)

if st.button("Get Answer", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            answer, query, parameters = answer_question(
                question,
                selected_plan
            )

            # Verified answer from the SQLite database
            st.subheader("Database Answer")
            st.success(answer)

            # AI explanation using the local Ollama model
            st.subheader("AI Explanation")

            with st.spinner("Generating explanation with local AI..."):
                ai_answer = explain_with_llm(question, answer)

            st.write(ai_answer)

            # Show SQL evidence
            if query:
                with st.expander(
                    "View SQL query and database evidence"
                ):
                    st.write("SQL Query:")
                    st.code(query, language="sql")

                    st.write("Query Parameters:")
                    st.write(parameters)

        except Exception as error:
            st.error(f"Something went wrong: {error}")

# ==========================================
# 8. DEBUG DATABASE LABELS
# ==========================================

with st.expander("Debug: Labels in selected floor plan"):
    try:
        labels = debug_labels(selected_plan)

        if labels:
            st.write("Annotated labels and their counts:")

            for label, count in labels:
                st.write(f"- {label}: {count}")
        else:
            st.info("No annotated objects found.")

    except Exception as error:
        st.error(f"Could not load labels: {error}")


# ==========================================
# 9. FOOTER
# ==========================================

st.divider()

st.caption(
    "Ask Your Floor Plan | "
    "Answers are based on the annotated floor-plan database."
)
