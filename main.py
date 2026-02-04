import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post, edit_post


# Options for length and language
length_options = ["Short", "Medium", "Long"]
# Display labels include flags for clarity. We'll map them to canonical language names below.
language_options = [
    "English 🇬🇧",
    "Hinglish",
    "Chinese (中文) 🇨🇳",
    "Spanish (Español) 🇪🇸",
    "German (Deutsch) 🇩🇪",
    "French (Français) 🇫🇷",
]

# Map display label -> canonical language name used by generator
language_map = {
    "English 🇬🇧": "English",
    "Hinglish": "Hinglish",
    "Chinese (中文) 🇨🇳": "Chinese",
    "Spanish (Español) 🇪🇸": "Spanish",
    "German (Deutsch) 🇩🇪": "German",
    "French (Français) 🇫🇷": "French",
}


# Main app layout
def main():
    # Page configuration
    st.set_page_config(page_title="LinkedIn Post Generator", layout="wide")
    
    st.title("🚀 LinkedIn Post Generator with GenAI")
    st.markdown("---")

    # Initialize session state
    if 'current_post' not in st.session_state:
        st.session_state.current_post = None
    if 'generated_post' not in st.session_state:
        st.session_state.generated_post = None

    # Sidebar: Input Controls
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.markdown("Set your post parameters below")
        st.markdown("---")

        fs = FewShotPosts()
        tags = fs.get_tags()

        # Topic input
        selected_tag = st.text_input(
            "📝 Topic",
            value="",
            placeholder="Type a topic (e.g. Job Search, Motivation)"
        )

        # Length selection
        selected_length = st.selectbox(
            "📏 Post Length",
            options=length_options,
            index=1  # Default to Medium
        )

        # Language selection
        selected_language = st.selectbox(
            "🌐 Language",
            options=language_options,
            index=0  # Default to English
        )

        st.markdown("---")

        # Generate button
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            generate_clicked = st.button("✨ Generate", use_container_width=True)
        with col_btn2:
            clear_clicked = st.button("🔄 Clear", use_container_width=True)

        if clear_clicked:
            st.session_state.current_post = None
            st.session_state.generated_post = None
            st.success("Post cleared!")

        if generate_clicked:
            if not selected_tag or not selected_tag.strip():
                st.warning("⚠️ Please enter a topic first!")
            else:
                with st.spinner("✍️ Generating your post..."):
                    canonical_language = language_map.get(selected_language, selected_language)
                    post = generate_post(selected_length, canonical_language, selected_tag)
                    st.session_state.generated_post = post
                    st.session_state.current_post = post
                st.success("✅ Post generated successfully!")

    # Main content area
    if st.session_state.current_post:
        # Two-column layout: Preview + Editor
        col_preview, col_editor = st.columns([1, 1], gap="large")

        with col_preview:
            st.subheader("📱 Preview")
            st.markdown("---")
            # Display the current post in a nice box
            st.markdown(
                f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 4px solid #0066cc;">
                    {st.session_state.current_post}
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("")
            # Copy button
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.info("Post copied! (You can use Ctrl+C in the preview)")

        with col_editor:
            st.subheader("✏️ Edit & Refine")
            st.markdown("---")
            
            # Direct edit area
            st.session_state.current_post = st.text_area(
                "Edit your post directly:",
                value=st.session_state.current_post,
                height=200,
                label_visibility="collapsed"
            )

            st.markdown("**💬 Or ask the AI to refine it:**")
            edit_instruction = st.text_area(
                "Edit instruction",
                placeholder="E.g. Make it shorter, add emojis, make it more professional, add a CTA...",
                height=80,
                label_visibility="collapsed"
            )

            # Action buttons
            btn_col1, btn_col2 = st.columns(2, gap="small")
            with btn_col1:
                apply_edit = st.button("🤖 Apply Edit", use_container_width=True)
            with btn_col2:
                regenerate = st.button("🔄 Regenerate", use_container_width=True)

            if apply_edit:
                if not edit_instruction or not edit_instruction.strip():
                    st.warning("⚠️ Please enter edit instructions!")
                else:
                    with st.spinner("🤔 Refining your post..."):
                        canonical_language = language_map.get(selected_language, selected_language)
                        original_post_text = st.session_state.get('current_post', '') or ''
                        edited = edit_post(original_post_text, edit_instruction, length=selected_length, language=canonical_language, tag=selected_tag)
                        st.session_state.current_post = edited
                    st.success("✅ Post refined!")

            if regenerate:
                if not selected_tag or not selected_tag.strip():
                    st.warning("⚠️ Please enter a topic first!")
                else:
                    with st.spinner("✍️ Generating a new post..."):
                        canonical_language = language_map.get(selected_language, selected_language)
                        post = generate_post(selected_length, canonical_language, selected_tag)
                        st.session_state.current_post = post
                        st.session_state.generated_post = post
                    st.success("✅ New post generated!")

        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; color: #888; font-size: 12px; margin-top: 20px;">
            💡 Tip: You can manually edit the post or use AI-powered refinement. Generated posts are cached in your session.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        # Initial state: empty screen with tips
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px;">
            <h2>👋 Welcome to LinkedIn Post Generator</h2>
            <p style="font-size: 18px; color: #888;">
            Generate engaging LinkedIn posts tailored to your topic, language, and tone.
            </p>
            <hr>
            <p><strong>✨ Get started:</strong></p>
            <ol style="text-align: left; display: inline-block;">
                <li>Enter your topic in the sidebar</li>
                <li>Choose post length and language</li>
                <li>Click <strong>Generate</strong> to create your post</li>
                <li>Refine using direct edits or AI assistance</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)


# Run the app
if __name__ == "__main__":
    main()
