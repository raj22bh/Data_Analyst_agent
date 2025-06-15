import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import re
import io
import base64
from typing import Dict, List, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# File processing imports
try:
    from docx import Document
    import PyPDF2
    from PIL import Image
    import pytesseract
    import together
    from wordcloud import WordCloud
    import textstat
    from collections import Counter
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
except ImportError as e:
    st.error(f"Missing required package: {e}. Please install all dependencies.")

class DataAnalystAgent:
    def __init__(self, together_api_key: str):
        """Initialize the Data Analyst Agent with Together AI API key"""
        self.together_client = together.Together(api_key=together_api_key)
        self.model_name = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8"
        self.conversation_history = []
        self.current_data = None
        self.data_summary = None
        self.file_type = None
    
    def process_csv_file(self, file_content) -> Dict[str, Any]:
        """Process CSV file"""
        try:
            df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
            self.current_data = df
            self.file_type = "csv"
            
            summary = {
                "shape": df.shape,
                "columns": list(df.columns),
                "dtypes": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "numeric_columns": list(df.select_dtypes(include=[np.number]).columns),
                "categorical_columns": list(df.select_dtypes(include=['object']).columns),
                "sample_data": df.head().to_dict()
            }
            
            # Basic statistics for numeric columns
            if summary["numeric_columns"]:
                summary["statistics"] = df.describe().to_dict()
            
            self.data_summary = summary
            return {"status": "success", "summary": summary}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def process_excel_file(self, file_content) -> Dict[str, Any]:
        """Process Excel file"""
        try:
            df = pd.read_excel(io.BytesIO(file_content))
            self.current_data = df
            self.file_type = "excel"
            
            summary = {
                "shape": df.shape,
                "columns": list(df.columns),
                "dtypes": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "numeric_columns": list(df.select_dtypes(include=[np.number]).columns),
                "categorical_columns": list(df.select_dtypes(include=['object']).columns),
                "sample_data": df.head().to_dict()
            }
            
            if summary["numeric_columns"]:
                summary["statistics"] = df.describe().to_dict()
            
            self.data_summary = summary
            return {"status": "success", "summary": summary}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def process_text_file(self, file_content) -> Dict[str, Any]:
        """Process text file"""
        try:
            text = file_content.decode('utf-8')
            self.current_data = text
            self.file_type = "text"
            
            # Text analysis
            words = text.split()
            sentences = text.split('.')
            paragraphs = text.split('\\n\\n')
            
            summary = {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "paragraph_count": len(paragraphs),
                "character_count": len(text),
                "readability_score": textstat.flesch_reading_ease(text),
                "most_common_words": Counter(words).most_common(10),
                "preview": text[:500] + "..." if len(text) > 500 else text
            }
            
            self.data_summary = summary
            return {"status": "success", "summary": summary}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def process_docx_file(self, file_content) -> Dict[str, Any]:
        """Process DOCX file"""
        try:
            doc = Document(io.BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\\n"
            
            self.current_data = text
            self.file_type = "docx"
            
            words = text.split()
            sentences = text.split('.')
            paragraphs = text.split('\\n')
            
            summary = {
                "word_count": len(words),
                "sentence_count": len(sentences),
                "paragraph_count": len([p for p in paragraphs if p.strip()]),
                "character_count": len(text),
                "readability_score": textstat.flesch_reading_ease(text) if text.strip() else 0,
                "most_common_words": Counter(words).most_common(10) if words else [],
                "preview": text[:500] + "..." if len(text) > 500 else text
            }
            
            self.data_summary = summary
            return {"status": "success", "summary": summary}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def process_pdf_file(self, file_content) -> Dict[str, Any]:
        """Process PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\\n"
            
            self.current_data = text
            self.file_type = "pdf"
            
            words = text.split()
            sentences = text.split('.')
            
            summary = {
                "page_count": len(pdf_reader.pages),
                "word_count": len(words),
                "sentence_count": len(sentences),
                "character_count": len(text),
                "readability_score": textstat.flesch_reading_ease(text) if text.strip() else 0,
                "most_common_words": Counter(words).most_common(10) if words else [],
                "preview": text[:500] + "..." if len(text) > 500 else text
            }
            
            self.data_summary = summary
            return {"status": "success", "summary": summary}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def process_image_file(self, file_content) -> Dict[str, Any]:
        """Process image file using OCR"""
        try:
            image = Image.open(io.BytesIO(file_content))
            text = pytesseract.image_to_string(image)
            
            self.current_data = text
            self.file_type = "image"
            
            summary = {
                "image_size": image.size,
                "image_mode": image.mode,
                "extracted_text_length": len(text),
                "word_count": len(text.split()) if text.strip() else 0,
                "extracted_text": text[:500] + "..." if len(text) > 500 else text
            }
            
            self.data_summary = summary
            return {"status": "success", "summary": summary}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def upload_and_process_file(self, uploaded_file) -> Dict[str, Any]:
        """Process uploaded file based on its extension"""
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            file_content = uploaded_file.read()
            
            if file_extension == 'csv':
                return self.process_csv_file(file_content)
            elif file_extension in ['xlsx', 'xls']:
                return self.process_excel_file(file_content)
            elif file_extension == 'txt':
                return self.process_text_file(file_content)
            elif file_extension == 'docx':
                return self.process_docx_file(file_content)
            elif file_extension == 'pdf':
                return self.process_pdf_file(file_content)
            elif file_extension in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
                return self.process_image_file(file_content)
            else:
                return {"status": "error", "message": f"Unsupported file type: {file_extension}"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def query_llama(self, question: str, context: str = "") -> str:
        """Query the Llama model with context about the data"""
        try:
            # Prepare context
            if self.data_summary:
                context_text = f"Data Summary: {json.dumps(self.data_summary, indent=2, default=str)}\\n\\n"
            else:
                context_text = ""
            
            if context:
                context_text += f"Additional Context: {context}\\n\\n"
            
            # Add conversation history
            conversation_context = ""
            if self.conversation_history:
                conversation_context = "Previous conversation:\\n"
                for item in self.conversation_history[-3:]:  # Last 3 exchanges
                    conversation_context += f"Q: {item['question']}\\nA: {item['answer']}\\n\\n"
            
            prompt = f"""You are a data analyst assistant. Analyze the provided data and answer the user's question comprehensively.

{context_text}{conversation_context}

User Question: {question}

Please provide a detailed, accurate analysis based on the data. If you need to make calculations or observations, be specific and cite the data when possible."""

            response = self.together_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an expert data analyst. Provide clear, accurate, and detailed analysis based on the provided data."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            answer = response.choices[0].message.content
            
            # Store in conversation history
            self.conversation_history.append({
                "question": question,
                "answer": answer
            })
            
            return answer
            
        except Exception as e:
            return f"Error querying model: {str(e)}"
    
    def create_visualizations(self) -> List[Dict[str, Any]]:
        """Create appropriate visualizations based on data type"""
        visualizations = []
        
        try:
            if self.file_type in ['csv', 'excel'] and self.current_data is not None:
                df = self.current_data
                
                # Numeric columns visualization
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    # Correlation heatmap
                    if len(numeric_cols) > 1:
                        fig_corr = px.imshow(
                            df[numeric_cols].corr(),
                            title="Correlation Heatmap",
                            color_continuous_scale="RdBu"
                        )
                        visualizations.append({
                            "title": "Correlation Heatmap",
                            "type": "plotly",
                            "figure": fig_corr
                        })
                    
                    # Distribution plots
                    for col in numeric_cols[:3]:  # Limit to first 3 columns
                        fig_hist = px.histogram(
                            df, 
                            x=col, 
                            title=f"Distribution of {col}",
                            marginal="box"
                        )
                        visualizations.append({
                            "title": f"Distribution of {col}",
                            "type": "plotly",
                            "figure": fig_hist
                        })
                
                # Categorical columns visualization
                cat_cols = df.select_dtypes(include=['object']).columns
                for col in cat_cols[:2]:  # Limit to first 2 columns
                    value_counts = df[col].value_counts().head(10)
                    fig_bar = px.bar(
                        x=value_counts.index,
                        y=value_counts.values,
                        title=f"Top 10 Values in {col}"
                    )
                    visualizations.append({
                        "title": f"Top 10 Values in {col}",
                        "type": "plotly",
                        "figure": fig_bar
                    })
            
            elif self.file_type in ['text', 'docx', 'pdf'] and self.current_data:
                # Word cloud
                if len(self.current_data.strip()) > 0:
                    wordcloud = WordCloud(
                        width=800, 
                        height=400, 
                        background_color='white'
                    ).generate(self.current_data)
                    
                    fig_wc, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    ax.set_title('Word Cloud')
                    
                    visualizations.append({
                        "title": "Word Cloud",
                        "type": "matplotlib",
                        "figure": fig_wc
                    })
                    
                    # Word frequency chart
                    words = self.current_data.split()
                    word_freq = Counter(words).most_common(10)
                    
                    fig_freq = px.bar(
                        x=[item[1] for item in word_freq],
                        y=[item[0] for item in word_freq],
                        orientation='h',
                        title="Top 10 Most Frequent Words"
                    )
                    fig_freq.update_layout(xaxis_title="Frequency", yaxis_title="Words")
                    
                    visualizations.append({
                        "title": "Word Frequency",
                        "type": "plotly",
                        "figure": fig_freq
                    })
            
        except Exception as e:
            st.error(f"Error creating visualizations: {str(e)}")
        
        return visualizations

def main():
    st.set_page_config(
        page_title="Data Analyst Agent",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("🤖 Data Analyst Agent")
    st.markdown("### Upload any document and get AI-powered analysis with visualizations")
    
    # Sidebar for API key and file upload
    with st.sidebar:
        st.header("Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Enter your Together AI API Key:",
            type="password",
            help="Get your API key from Together AI platform"
        )
        
        if not api_key:
            st.warning("Please enter your Together AI API key to proceed.")
            st.stop()
        
        st.header("File Upload")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls', 'txt', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'],
            help="Supported formats: CSV, Excel, Text, Word, PDF, Images"
        )
    
    # Initialize session state
    if 'agent' not in st.session_state:
        try:
            st.session_state.agent = DataAnalystAgent(api_key)
        except Exception as e:
            st.error(f"Error initializing agent: {str(e)}")
            st.stop()
    
    if 'file_processed' not in st.session_state:
        st.session_state.file_processed = False
    
    if 'visualizations' not in st.session_state:
        st.session_state.visualizations = []
    
    # Main content area
    if uploaded_file is not None:
        if not st.session_state.file_processed or st.session_state.get('last_file') != uploaded_file.name:
            with st.spinner("Processing file..."):
                result = st.session_state.agent.upload_and_process_file(uploaded_file)
                
                if result["status"] == "success":
                    st.session_state.file_processed = True
                    st.session_state.last_file = uploaded_file.name
                    st.success(f"File '{uploaded_file.name}' processed successfully!")
                    
                    # Generate visualizations
                    with st.spinner("Creating visualizations..."):
                        st.session_state.visualizations = st.session_state.agent.create_visualizations()
                    
                else:
                    st.error(f"Error processing file: {result['message']}")
                    st.stop()
        
        # Display file summary
        if st.session_state.agent.data_summary:
            st.header("📋 Data Summary")
            
            # Create columns for summary display
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Basic Information")
                summary = st.session_state.agent.data_summary
                
                if st.session_state.agent.file_type in ['csv', 'excel']:
                    st.write(f"**Shape:** {summary['shape'][0]} rows × {summary['shape'][1]} columns")
                    st.write(f"**Columns:** {', '.join(summary['columns'][:5])}{'...' if len(summary['columns']) > 5 else ''}")
                    st.write(f"**Numeric Columns:** {len(summary['numeric_columns'])}")
                    st.write(f"**Categorical Columns:** {len(summary['categorical_columns'])}")
                
                elif st.session_state.agent.file_type in ['text', 'docx', 'pdf']:
                    st.write(f"**Word Count:** {summary['word_count']}")
                    st.write(f"**Character Count:** {summary['character_count']}")
                    if 'readability_score' in summary:
                        st.write(f"**Readability Score:** {summary['readability_score']:.1f}")
                
                elif st.session_state.agent.file_type == 'image':
                    st.write(f"**Image Size:** {summary['image_size']}")
                    st.write(f"**Extracted Text Length:** {summary['extracted_text_length']}")
            
            with col2:
                st.subheader("Preview")
                if st.session_state.agent.file_type in ['csv', 'excel']:
                    if 'sample_data' in summary and summary['sample_data']:
                        st.dataframe(pd.DataFrame(summary['sample_data']).head())
                else:
                    preview_text = summary.get('preview', summary.get('extracted_text', ''))
                    if preview_text:
                        st.text_area("Content Preview", preview_text, height=200, disabled=True)
        
        # Visualizations
        if st.session_state.visualizations:
            st.header("📊 Visualizations")
            
            for viz in st.session_state.visualizations:
                st.subheader(viz['title'])
                
                if viz['type'] == 'plotly':
                    st.plotly_chart(viz['figure'], use_container_width=True)
                elif viz['type'] == 'matplotlib':
                    st.pyplot(viz['figure'])
        
        # Chat interface
        st.header("💬 Ask Questions About Your Data")
        
        # Display conversation history
        if st.session_state.agent.conversation_history:
            st.subheader("Conversation History")
            for i, item in enumerate(st.session_state.agent.conversation_history):
                with st.expander(f"Q{i+1}: {item['question'][:50]}..."):
                    st.write(f"**Question:** {item['question']}")
                    st.write(f"**Answer:** {item['answer']}")
        
        # Question input
        question = st.text_input(
            "Ask a question about your data:",
            placeholder="e.g., What are the main trends in this data? Can you summarize the key findings?"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            ask_button = st.button("Ask Question", type="primary")
        
        if ask_button and question:
            with st.spinner("Analyzing and generating response..."):
                answer = st.session_state.agent.query_llama(question)
                
                st.subheader("Answer:")
                st.write(answer)
        
        # Sample questions
        st.subheader("💡 Sample Questions")
        sample_questions = [
            "What are the key insights from this data?",
            "Can you identify any patterns or trends?",
            "What recommendations would you make based on this analysis?",
            "Are there any outliers or anomalies in the data?",
            "What's the statistical summary of the numeric columns?"
        ]
        
        for sq in sample_questions:
            if st.button(sq, key=f"sample_{sq}"):
                with st.spinner("Analyzing..."):
                    answer = st.session_state.agent.query_llama(sq)
                    st.subheader("Answer:")
                    st.write(answer)
    
    else:
        st.info("👆 Please upload a file using the sidebar to begin analysis.")
        
        # Show supported file types
        st.markdown("""
        ### Supported File Types:
        - **CSV/Excel Files**: Statistical analysis, correlations, distributions
        - **Text Files**: Word frequency, readability analysis, content extraction
        - **PDF Documents**: Text extraction and analysis
        - **Word Documents**: Content analysis and text processing
        - **Images**: OCR text extraction and analysis
        
        ### Features:
        - 🤖 AI-powered analysis using Llama-4-Maverick
        - 📊 Automatic visualization generation
        - 💬 Interactive Q&A about your data
        - 📈 Statistical summaries and insights
        - 🔍 Pattern recognition and trend analysis
        """)

if __name__ == "__main__":
    main()