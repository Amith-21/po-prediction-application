import streamlit as st
import json
import pandas as pd
from classifier import classify_po

# 1. Page Configuration
st.set_page_config(page_title="PO Intelligence", page_icon="📦", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# 2. Sidebar Inputs
with st.sidebar:
    st.header("Input Data")
    po_description = st.text_area("PO Description", height=150, placeholder="e.g., Annual subscription for cloud services")
    supplier = st.text_input("Supplier (Optional)", placeholder="e.g., Microsoft")
    
    classify_btn = st.button("🚀 Classify PO")
    st.divider()
    st.caption("v1.2 | Procurement Taxonomy Engine")

# 3. Main Interface
st.title("📦 PO L1-L2-L3 Classifier")

if classify_btn:
    if not po_description.strip():
        st.error("Please enter a description in the sidebar.")
    else:
        with st.spinner("Analyzing taxonomy..."):
            result = classify_po(po_description, supplier)
            
            try:
                # Parse JSON result
                data = json.loads(result)
                
                # Feature 1: Visual Metric Cards
                col1, col2, col3 = st.columns(3)
                col1.metric("Level 1 (Category)", data.get("L1", "N/A"))
                col2.metric("Level 2 (Sub-Cat)", data.get("L2", "N/A"))
                col3.metric("Level 3 (Commodity)", data.get("L3", "N/A"))
                
                st.divider()
                
                # Feature 2: Tabbed Results
                tab1, tab2 = st.tabs(["📊 Table View", "💻 Developer JSON"])
                
                with tab1:
                    df = pd.DataFrame([data])
                    st.dataframe(df, use_container_width=True)
                    
                    # Feature 3: Export to CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Result as CSV",
                        data=csv,
                        file_name="classification_result.csv",
                        mime="text/csv",
                    )
                
                with tab2:
                    st.json(data)
                    
            except Exception:
                st.error("Model returned an invalid format. See raw output below:")
                st.info(result)
else:
    st.info("Fill out the PO details in the left sidebar and click 'Classify' to see the taxonomy mapping.")
