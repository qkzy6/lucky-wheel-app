# streamlit_app.py
# (版本 5 - 放大显示区域, 结果居中, 线性滚动)

import streamlit as st
import random
import streamlit.components.v1 as components
import time

def create_wheel_app():
    st.title("🎉 幸运大转盘 (网页版) 🎉")

    # ========== 配置 ==========
    items_config = [
        ("谢谢参与", 50),   
        ("10积分",   15),   
        ("20积分",   10),   
        ("50积分",   10),   
        ("100积分",   5),   
        ("神秘大奖",  3),   
    ]
    # (为了让"滚筒"更长，我们复制几次)
    items_list = items_config * 5 
    labels = [item[0] for item in items_list]
    weights = [item[1] for item in items_list]
    n_items = len(items_list) 

    # --- 视觉参数 (您可以调整) ---
    item_height_px = 70  # 每个奖品的高度 (像素)
    font_size_px = 30  # 奖品的字体大小 (像素)
    visible_items = 3  # 🔴 改动点 1: 我们希望同时显示3个
    # --- 自动计算 ---
    container_height = item_height_px * visible_items # 容器总高度

    # --- Streamlit 交互 ---
    if st.button("开始抽奖!", type="primary", use_container_width=True):
        
        base_len = len(items_config)
        chosen_base_index = random.choices(list(range(base_len)), weights=[w[1] for w in items_config], k=1)[0]
        result = items_config[chosen_base_index][0]
        
        # 我们让它停在第 3 个重复列表的对应位置
        stop_index = (base_len * 2) + chosen_base_index

        # --- HTML/CSS/JS ---
        reel_items_html = ""
        for label in labels:
            reel_items_html += f'<div class="item">{label}</div>'

        slot_machine_html = f"""
        <style>
            .slot-container {{
                width: 100%; 
                /* 🔴 改动点 1: 容器高度变为 3*item_height */
                height: {container_height}px;
                overflow: hidden; 
                border: 2px solid #444; 
                border-radius: 5px;
                background: #f9f9f9; 
                box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
            }}
            .reel {{ 
                transition: none; 
                transform: translateY(0); 
            }}
            .item {{
                /* 🔴 改动点 1: 应用新的高度和字体 */
                height: {item_height_px}px; 
                line-height: {item_height_px}px;
                font-size: {font_size_px}px; 
                font-weight: bold; 
                text-align: center;
                border-bottom: 1px dashed #ccc;
            }}
        </style>

        <div class="slot-container" id="slot-container">
            <div class="reel" id="reel">
                {reel_items_html}
            </div>
        </div>

        <script>
        window.onload = function() {{
            const reel = document.getElementById('reel');
            if (!reel) {{ return; }} 

            const stopIndex = {stop_index};
            const itemHeight = {item_height_px};
            const nItems = {n_items};
            const visibleItems = {visible_items}; /* 🔴 改动点 2: JS 获知可见数量 */

            // 1. 计算一个随机的"过头"位置
            const randomOvershoot = -(nItems * itemHeight + Math.random() * 4000 + 2000);
            
            // 2. 🔴 改动点 2: 
            // 重新计算最终停止位置，使其"居中"
            // ( (总高度 / 2) - (单个高度 / 2) ) 是为了让它居中
            // ( (itemHeight * visibleItems) / 2 - (itemHeight / 2) ) 
            // 简化: (itemHeight * (visibleItems - 1) / 2)
            const centering_offset = (itemHeight * (visibleItems - 1) / 2);
            const finalPosition = -((stopIndex * itemHeight) - centering_offset);


            // 3. (阶段 1: T=0秒) 
            /* 🔴 改动点 3: 将 'cubic-bezier' (加速模糊) 改为 'linear' (匀速) */
            reel.style.transition = 'transform 2.5s linear'; 
            reel.style.transform = `translateY(${{randomOvershoot}}px)`;

            // 4. (阶段 2: T=2.5秒) 
            setTimeout(() => {{
                reel.style.transition = 'transform 3s ease-out'; /* 3秒减速 */
                reel.style.transform = `translateY(${{finalPosition}}px)`;
            }}, 2500); 
        }};
        </script>
        """

        # 4. (Streamlit) 渲染这个HTML组件
        # 🔴 改动点 1: 匹配新的容器高度
        components.html(slot_machine_html, height=container_height + 10) 
        
        # 5. (Streamlit) 在组件下方显示最终结果
        result_placeholder = st.empty()
        
        # 6. (Python) 等待动画播完 (2.5 + 3 = 5.5秒)
        time.sleep(5.5) 
        
        result_placeholder.success(f"恭喜！您抽中了： {result}")

        if "谢" not in result and "无" not in result:
            st.balloons()
            
    else:
        st.info("请点击上面的按钮开始抽奖")

# --- 程序入口 ---
if __name__ == "__main__":
    create_wheel_app()
