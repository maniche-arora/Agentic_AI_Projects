import streamlit as st
import asyncio
import os
from team.analyzer_gpt import getDataAnalyzerTeam
from config.openai_model_client import get_model_client
from config.docker_utils import getDockerCommandLineCodeExecutor,start_docker_container,stop_docker_container
from config.constants import WORK_DIR_DOCKER
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

st.title("Analyser GPT -  Digital Data Analyzer")
# Upload the file in excel or csv format
uploaded_file = st.file_uploader("Upload your data file (Excel or CSV)", type=["xlsx", "csv"])

task = st.text_input("Enter your analysis task ", value="Can you give me number of columns in my data? ")

async def run_analyzer_gpt(docker, openai_model_client, task):
    try:
        await start_docker_container(docker)
        team = getDataAnalyzerTeam(docker, openai_model_client)

        async for message in team.run_stream(task=task):
            st.write('='*40)
            if isinstance(message, TextMessage):
                print(msg := f"{message.source} said: {message.content}")
               # yield msg
                if msg.startswith("user"):
                    with st.chat_message('user',avatar="https://static.streamlit.io/examples/daniel_avatar.png"):
                        st.markdown(msg)
                elif msg.startswith("data_analyzer_agent"):
                    with st.chat_message('Data analyst',avatar="https://static.streamlit.io/examples/hal_avatar.png"):
                        st.markdown(msg)
                elif msg.startswith("code_executor_agent"):
                    with st.chat_message('Code executor',avatar="https://static.streamlit.io/examples/ava_avatar.png"):
                        st.markdown(msg)

                st.markdown(f"**{message.source} said:** {message.content}")
            
            elif isinstance(message,TaskResult):
                print("Stop Reason: ", message.stop_reason)
              #  yield f"Stop Reason: {message.stop_reason}"
                st.markdown(f"**Stop Reason:** {message.stop_reason}")
            
        return "Analysis completed successfully." 
    
                           

    except Exception as e:
       print('Error: ', e)
       return str(e)
    finally:        
        await stop_docker_container(docker)

    

    

if st.button("Run Analysis"):
    if uploaded_file is not None and task:
        # Use absolute path --updated extra
        work_dir_abs = os.path.abspath(WORK_DIR_DOCKER)
        # Save the uploaded file to a temporary location
        if not os.path.exists(work_dir_abs):
            os.makedirs(work_dir_abs)
        
         # Save file using absolute path --updated extra
        file_path = os.path.join(work_dir_abs, 'data.csv')
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write(f"File '{uploaded_file.name}' uploaded successfully to {file_path}. Running analysis...")

        openai_model_client = get_model_client()
        docker = getDockerCommandLineCodeExecutor()

        error = asyncio.run(run_analyzer_gpt(docker, openai_model_client, task))

        if error != "Analysis completed successfully.":
            st.error(f"Error during analysis: {error}")
        else:
            st.success("Analysis completed successfully.")
            
            # Display generated images
            import glob
            work_dir_abs = os.path.abspath(WORK_DIR_DOCKER)
            
            # Debug: show what files exist
            #st.write(f"Looking for images in: {work_dir_abs}")
            
            if os.path.exists(work_dir_abs):
                all_files = os.listdir(work_dir_abs)
                st.write(f"Files found: {all_files}")
                
                # Find image files more robustly
                image_files = []
                for file in all_files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        image_files.append(os.path.join(work_dir_abs, file))
                
                if image_files:
                    st.subheader("Generated Visualizations")
                    for img_file in sorted(image_files):
                        try:
                            st.image(img_file, caption=os.path.basename(img_file), use_column_width=True)
                        except Exception as e:
                            st.error(f"Could not load image {os.path.basename(img_file)}: {e}")
                else:
                    st.info("No image files (.png, .jpg) found in the output directory.")
            else:
                st.error(f"Output directory not found: {work_dir_abs}")
        

    else:
        st.warning("Please upload a data file before running the analysis.")
