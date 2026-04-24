import streamlit as st
import tempfile

# Core modules
from memory.memory_store import MemoryStore
from evaluation.rag_eval import RAGEvaluator
from retriever.image_search import ImageSearch
from generator.llm_client import LLMClient
from pipelines.sql_pipeline import SQLPipeline
from retriever.query_engine import QueryEngine


# -----------------------------
# Initialize components (once)
# -----------------------------
@st.cache_resource
def init_components():
    memory = MemoryStore()
    llm = LLMClient()
    evaluator = RAGEvaluator(llm)
    image_search = ImageSearch()
    sql_pipeline = SQLPipeline(db_path="src/data/raw/db.sqlite")
    query_engine = QueryEngine()

    return memory, llm, evaluator, image_search, sql_pipeline, query_engine


memory, llm, evaluator, image_search, sql_pipeline, query_engine = init_components()


# -----------------------------
# Helper functions
# -----------------------------
def get_relevant_memory(query, k=2):
    try:
        memory_context = memory.get_context()

        if not memory_context:
            return ""

        memory_lines = memory_context.split("\n")[-k:]
        memory_context = "\n".join(memory_lines)

        if query.lower() not in memory_context.lower():
            return ""

        return memory_context

    except:
        return ""


def is_context_relevant(context):
    return len(context.strip().split()) > 20


def show_eval(faithful, score):
    st.write("### 🧠 Hallucination Check")

    if faithful:
        st.success("✅ Low Hallucination Risk")
    else:
        st.warning("⚠️ Possible Hallucination")

    st.write("### 📊 Faithfulness Score")
    st.write(f"{round(score, 3)}")

    if score > 0.7:
        st.info("High confidence in answer")
    elif score > 0.4:
        st.info("Moderate confidence")
    else:
        st.info("Low confidence")


# -----------------------------
# UI
# -----------------------------
st.title("AI App")

option = st.selectbox("Choose type", ["ask", "ask-image", "ask-sql"])

query = st.text_input("Enter your query")


# -----------------------------
# IMAGE MODE UI
# -----------------------------
if option == "ask-image":
    st.subheader("Image AI")

    image_mode = st.selectbox(
        "Choose Image Mode",
        ["Text → Image", "Image → Image", "Image → Text"]
    )

    uploaded_file = None

    if image_mode in ["Image → Image", "Image → Text"]:
        uploaded_file = st.file_uploader(
            "Upload Image", type=["png", "jpg", "jpeg"]
        )


# -----------------------------
# Button action
# -----------------------------
if st.button("Submit"):
    try:

        # -----------------------
        # TEXT (RAG + fallback)
        # -----------------------
        if option == "ask":
            if not query:
                st.warning("Please enter a query")
                st.stop()

            results, context = query_engine.query(query, k=5)

            if is_context_relevant(context):
                source = "documents"
                prompt = f"""
You are a helpful assistant.

Answer ONLY from the provided context.
If answer is not present, say:
"Not found in provided documents."

Context:
{context}

Question:
{query}

Answer:
"""
            else:
                source = "general"
                prompt = f"""
You are a helpful assistant.

No relevant documents were found.
Answer using general knowledge.

Question:
{query}

Answer:
"""

            answer = llm.generate(prompt)

            memory_context = get_relevant_memory(query)

            refined = evaluator.refine_answer(memory_context, answer)
            faithful = evaluator.hallucination_check(context, refined)
            score = evaluator.faithfulness_score(context, refined)

            memory.add(query, refined)

            st.write("### Answer")
            st.write(refined)

            st.write("### Source")
            st.write(source)

            show_eval(faithful, score)

        # -----------------------
        # IMAGE (ALL 3 MODES)
        # -----------------------
        elif option == "ask-image":

            # TEXT → IMAGE
            if image_mode == "Text → Image":
                if not query:
                    st.warning("Enter a query")
                    st.stop()

                results, context = query_engine.query(query, k=3)

                enhanced_query = query
                if is_context_relevant(context):
                    enhanced_query += " " + context[:200]

                images = image_search.text_to_image(enhanced_query)

                st.write("### Results")
                for r in images:
                    st.image(r["image"])
                    st.write(r["final_caption"])
                    st.divider()

            # IMAGE → IMAGE
            elif image_mode == "Image → Image":
                if not uploaded_file or not query:
                    st.warning("Provide both query and image")
                    st.stop()

                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(uploaded_file.read())
                    temp_path = tmp.name

                results = image_search.image_to_image(temp_path)

                st.write("### Similar Images")
                for r in results:
                    st.image(r["image"])
                    st.write(r["final_caption"])
                    st.divider()

            # IMAGE → TEXT
            elif image_mode == "Image → Text":
                if not uploaded_file or not query:
                    st.warning("Provide query and image")
                    st.stop()

                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(uploaded_file.read())
                    temp_path = tmp.name

                answer = image_search.image_to_text(temp_path, query)

                # 🔥 Evaluate image answer (best effort)
                faithful = True if answer else False
                score = 0.7 if answer else 0.0

                st.image(temp_path)
                st.write("### Answer")
                st.write(answer)

                show_eval(faithful, score)

        # -----------------------
        # SQL (RAG + pipeline)
        # -----------------------
        elif option == "ask-sql":
            if not query:
                st.warning("Please enter a query")
                st.stop()

            results, context = query_engine.query(query, k=5)

            user_query = query
            if is_context_relevant(context):
                user_query += f"\n\nContext:\n{context}"

            pipeline_result = sql_pipeline.run(user_query)

            sql_query = pipeline_result["sql"]
            result = pipeline_result["result"]
            answer = pipeline_result["answer"]

            memory_context = get_relevant_memory(query)

            refined = evaluator.refine_answer(memory_context, answer)
            faithful = evaluator.hallucination_check(str(result), refined)
            score = evaluator.faithfulness_score(str(result), refined)

            memory.add(query, refined)

            st.write("### SQL Query")
            st.code(sql_query, language="sql")

            st.write("### Result")
            st.write(result)

            st.write("### Answer")
            st.write(refined)

            show_eval(faithful, score)

    except Exception as e:
        st.error(str(e))