import streamlit as st
import asyncio
from dotenv import load_dotenv
from research_manager import ResearchManager



# 设置页面标题
st.title("Deep Research")

# 初始化 session state
if "report_content" not in st.session_state:
    st.session_state.report_content = ""
if "query" not in st.session_state:
    st.session_state.query = ""
if "running" not in st.session_state:
    st.session_state.running = False
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# 创建表单处理回车键提交
with st.form("research_form"):
    # 创建查询输入框
    query = st.text_input(
        "What topic would you like to research?",
        value=st.session_state.query,
        key="form_query",
    )

    # 创建运行按钮
    run_button = st.form_submit_button("Run", type="primary")

# 创建报告区域
report_area = st.empty()
report_area.markdown(st.session_state.report_content)


async def run_research(query: str):
    """异步执行研究并生成报告"""
    st.session_state.running = True
    st.session_state.report_content = ""
    st.session_state.last_query = query

    # 初始清空报告区域
    report_area.markdown(st.session_state.report_content)

    try:
        # 创建 ResearchManager 实例
        manager = ResearchManager()

        # 处理每个生成的 chunk
        async for chunk in manager.run(query):
            # 确保 chunk 是字符串
            if not isinstance(chunk, str):
                chunk = str(chunk)

            # 处理换行：确保 Markdown 格式的换行
            chunk = chunk.replace("\n", "  \n")  # 添加两个空格确保 Markdown 换行

            # 追加到报告内容
            st.session_state.report_content += chunk + "\n\n"

            # 更新报告区域
            report_area.markdown(st.session_state.report_content)

            # 添加轻微延迟以确保 UI 更新
            await asyncio.sleep(0.01)

    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
    finally:
        st.session_state.running = False


# 处理表单提交
if run_button:
    if query:
        # 如果正在运行但查询已更改，则中断当前任务并启动新任务
        if st.session_state.running and query != st.session_state.last_query:
            # 这里可以添加中断当前研究的逻辑（如果有）
            st.warning("Interrupting current research to start new one")
            st.session_state.running = False

        # 启动或重启研究
        if not st.session_state.running:
            st.session_state.query = query
            asyncio.run(run_research(query))
        else:
            st.info("Research is already running. Please wait...")
    else:
        st.warning("Please enter a research topic")
