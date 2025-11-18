# streamlit_app.py

import streamlit as st
import random
import time  # <-- 我们需要导入 time 模块


def create_wheel_app():
    st.title("🎉 幸运大转盘 (网页版) 🎉")

    items = [
        ("谢谢参与", 50),  # 扇区0
        ("10积分", 15),  # 扇区1
        ("20积分", 10),  # 扇区2
        ("50积分", 10),  # 扇区3
        ("100积分", 5),  # 扇区4
        ("神秘大奖", 3),  # 扇区5
    ]
    labels = [item[0] for item in items]
    weights = [item[1] for item in items]

    # --- 交互核心 ---
    if st.button("开始抽奖!", type="primary", use_container_width=True):

        # (关键!) st.spinner 会显示一个加载动画
        with st.spinner("转盘正在...转动... 🌀"):

            # 1. (核心逻辑) 抽奖结果其实是立刻算出来的
            chosen_index = random.choices(list(range(len(labels))), weights=weights, k=1)[0]
            result = labels[chosen_index]

            # 2. (模拟转动) 故意暂停 3 秒钟，让用户等待，增加期待感
            time.sleep(3)

        # 3. 暂停结束后，spinner 自动消失，显示结果
        st.success(f"恭喜！您抽中了： {result}")

        # 4. 放气球庆祝
        if "谢" not in result and "无" not in result:
            st.balloons()

    else:
        st.info("请点击上面的按钮开始抽奖")


# --- 程序入口 ---
if __name__ == "__main__":
    create_wheel_app()