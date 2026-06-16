import streamlit as st
import base64
from io import BytesIO

from services.copyright_service import (
    create_copyright_claim,
    get_user_claims,
    get_copyright_statistics
)

# =====================================================
# LOGIN CHECK
# =====================================================

if not st.session_state.get("logged_in", False):
    st.warning(
        "Please login first."
    )
    st.stop()

# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <h1 class='main-title'>
    © COPYRIGHT MANAGEMENT
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<div class='highlight-mystical'>
Protect your creative works within the Empire of Continuum ecosystem.

Creators can register ownership claims, report disputes, and submit evidence for review by the Continuity Management Team.
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

# =====================================================
# LOAD TESSERACT.JS SCRIPT
# =====================================================

tesseract_script = """
<script src="https://cdn.jsdelivr.net/npm/tesseract.js@v5/dist/tesseract.min.js"></script>
<script>
    window.tesseractReady = false;
    
    async function initTesseract() {
        if (!window.tesseractReady) {
            try {
                const { createScheduler, createWorker } = Tesseract;
                window.tesseractScheduler = createScheduler();
                const worker = createWorker();
                await worker.load();
                window.tesseractScheduler.addWorker(worker);
                window.tesseractReady = true;
            } catch (e) {
                console.error("Tesseract init error:", e);
            }
        }
    }
    
    async function extractText(imageData) {
        await initTesseract();
        try {
            const result = await window.tesseractScheduler.recognize(imageData);
            return result.data.text;
        } catch (e) {
            console.error("OCR error:", e);
            return null;
        }
    }
    
    window.extractTextFromImage = extractText;
</script>
"""

st.markdown(tesseract_script, unsafe_allow_html=True)

# =====================================================
# STATS
# =====================================================

stats = get_copyright_statistics()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"<div class='stMetric'><div style='color: var(--gold-primary); font-weight: bold;'>{stats['total']}</div><div style='font-size: 0.9rem;'>Total Claims</div></div>", unsafe_allow_html=True)

with c2:
    st.markdown(f"<div class='stMetric'><div style='color: #F5C89A; font-weight: bold;'>{stats['pending']}</div><div style='font-size: 0.9rem;'>Pending Review</div></div>", unsafe_allow_html=True)

with c3:
    st.markdown(f"<div class='stMetric'><div style='color: #A8E6A1; font-weight: bold;'>{stats['approved']}</div><div style='font-size: 0.9rem;'>Approved</div></div>", unsafe_allow_html=True)

with c4:
    st.markdown(f"<div class='stMetric'><div style='color: #E8C3FF; font-weight: bold;'>{stats['rejected']}</div><div style='font-size: 0.9rem;'>Rejected</div></div>", unsafe_allow_html=True)

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "📤 Submit Claim",
    "📋 My Claims",
    "🔍 OCR Tool"
])

# =====================================================
# SUBMIT
# =====================================================

with tab1:

    st.subheader("Submit Copyright Claim")

    content_type = st.selectbox(
        "Content Type",
        [
            "Story",
            "Artwork",
            "Wiki Article",
            "Character",
            "Music",
            "Animation",
            "Other"
        ]
    )

    content_id = st.number_input(
        "Content ID (if applicable)",
        min_value=1,
        step=1
    )

    ownership_statement = st.text_area(
        "Ownership Statement",
        height=200,
        placeholder="Describe why you own this work and provide evidence of creation..."
    )

    evidence_path = st.text_input(
        "Evidence File Reference (optional)",
        placeholder="Link to original upload, creation files, etc."
    )

    st.info("💡 Tip: Use the OCR Tool tab to extract text from image evidence automatically!")

    if st.button(
        "📜 Submit Claim",
        use_container_width=True
    ):

        if not ownership_statement.strip():

            st.error(
                "✗ Ownership statement required."
            )

        else:

            try:
                claim_id = create_copyright_claim(
                    claimant_id=st.session_state.user_id,
                    content_type=content_type,
                    content_id=content_id,
                    ownership_statement=ownership_statement,
                    evidence_path=evidence_path
                )

                st.success(f"""
✅ **Claim submitted successfully!**

📝 Claim ID: **{claim_id}**

Your claim has been submitted for review. You will be notified of the status within 3-7 business days.
                """)
                st.balloons()
            except Exception as e:
                st.error(f"Error submitting claim: {str(e)}")

# =====================================================
# USER CLAIMS
# =====================================================

with tab2:

    st.subheader("📋 My Claims")

    try:
        claims = get_user_claims(
            st.session_state.user_id
        )
    except:
        claims = []

    if not claims:

        st.info(
            "📭 No claims submitted yet."
        )

    else:
        for claim in claims:

            status = claim.get("status", "pending")

            if status == "approved":
                badge = "<span class='badge-canon'>🟢 Approved</span>"
            elif status == "rejected":
                badge = "<span class='badge-noncanon'>🔴 Rejected</span>"
            else:
                badge = "<span class='badge-pending'>🟡 Pending</span>"

            st.markdown(f"""
<div class='epic-card'>
<div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;'>
<h4 style='color: var(--gold-light); margin-bottom: 0;'>Claim #{claim.get('id', 'N/A')}</h4>
<div>{badge}</div>
</div>

<div style='display: flex; gap: 20px; margin-bottom: 12px; font-size: 0.9rem;'>
<span style='color: var(--purple-light);'>📝 {claim.get('content_type', 'Unknown')}</span>
<span style='color: var(--gold-primary);'>ID: {claim.get('content_id', 'N/A')}</span>
</div>

<p style='color: #D8D8D8; margin-bottom: 12px;'>{claim.get('ownership_statement', 'No statement')}</p>

<small style='color: #A8A8A8;'>Evidence: {claim.get('evidence_path', 'None provided')}</small>
</div>
            """, unsafe_allow_html=True)

# =====================================================
# OCR TOOL
# =====================================================

with tab3:

    st.subheader("🔍 Image Text Recognition (OCR)")

    st.markdown("""
<div class='highlight-mystical'>
🤖 **Powered by Tesseract.js** - Extract text from images of your creative work as evidence.

This tool runs locally in your browser with no data sent to external servers. Perfect for:
- Extracting text from screenshots
- Reading handwritten notes or signatures
- Recognizing text in artwork
- Capturing evidence of original creation
</div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    # Upload image
    uploaded_file = st.file_uploader(
        "Upload image to extract text from",
        type=["png", "jpg", "jpeg", "gif", "bmp"],
        help="Supports PNG, JPG, GIF, BMP formats"
    )

    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📷 Uploaded Image:**")
            st.image(uploaded_file)

        with col2:
            st.markdown("**📝 Extracted Text:**")
            
            # Prepare image data
            image_bytes = uploaded_file.read()
            
            # Create a simple instruction for OCR
            with st.spinner("🔄 Extracting text using OCR... (This may take 10-30 seconds on first use)"):
                st.info("""
**⚙️ How to use this tool:**

1. The image above has been uploaded
2. Click the button below to start text extraction
3. Processing happens in your browser (no uploads to servers)
4. Extracted text will appear here
5. Copy the text and use it in your copyright claim

**Note:** First-time use will download the OCR model (~50-100MB), which may take longer.
                """)
                
                if st.button("🚀 Extract Text from Image", key="ocr_extract"):
                    st.info("⏳ Processing image... Please wait. This may take 20-60 seconds depending on image size.")
                    
                    try:
                        # Convert image to base64
                        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                        
                        # Create JavaScript code to extract
                        ocr_html = f"""
                        <div id="ocr-result"></div>
                        <script>
                        async function performOCR() {{
                            const imageData = 'data:image/{uploaded_file.type.split("/")[1]};base64,{image_b64}';
                            try {{
                                const {{ Tesseract }} = window;
                                const {{ createWorker }} = Tesseract;
                                
                                const worker = await createWorker('eng');
                                const result = await worker.recognize(imageData);
                                const extractedText = result.data.text;
                                
                                document.getElementById('ocr-result').innerHTML = '<pre style="background: rgba(26,26,46,0.8); padding: 15px; border-radius: 8px; border: 1px solid var(--gold-primary); color: #F5F5F5; max-height: 300px; overflow-y: auto;">' + 
                                    (extractedText || 'No text found in image') + 
                                    '</pre>';
                                
                                await worker.terminate();
                            }} catch (e) {{
                                document.getElementById('ocr-result').innerHTML = '<div style="color: #FF6B6B;">Error: ' + e.message + '</div>';
                            }}
                        }}
                        performOCR();
                        </script>
                        """
                        st.markdown(ocr_html, unsafe_allow_html=True)
                        
                        st.success("✅ OCR extraction initiated! The result appears above.")
                        
                    except Exception as e:
                        st.error(f"❌ Error during OCR processing: {str(e)}")
            
    else:
        st.info("📤 Upload an image file to begin text extraction")

# =====================================================
# FOOTER
# =====================================================

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

st.caption("⚔️ Empire of Continuum • Copyright Management v2.0 • With Tesseract.js OCR")
