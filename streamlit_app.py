# streamlit_app.py
# (版本 4 - 修复 JS 加载顺序和动画逻辑)

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
    n_items = len(items_list) # <-- 获取总长度

    # --- Streamlit 交互 ---
    if st.button("开始抽奖!", type="primary", use_container_width=True):
        
        base_len = len(items_config)
        chosen_base_index = random.choices(list(range(base_len)), weights=[w[1] for w in items_config], k=1)[0]
        result = items_config[chosen_base_index][0]
        
        # 我们让它停在第 3 个重复列表的对应位置
        stop_index = (base_len * 2) + chosen_base_index
        item_height_px = 50 

        # --- HTML/CSS/JS ---
        reel_items_html = ""
        for label in labels:
            reel_items_html += f'<div class="item">{label}</div>'

        slot_machine_html = f"""
        <style>
            .slot-container {{
                width: 100%; height: {item_height_px}px;
                overflow: hidden; border: 2px solid #444; border-radius: 5px;
                background: #f9f9f9; box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
            }}
            .reel {{ 
                /* 默认无动画，JS会添加 */
                transition: none; 
                transform: translateY(0); 
            }}
            .item {{
                height: {item_height_px}px; line-height: {item_height_px}px;
                font-size: 20px; font-weight: bold; text-align: center;
                border-bottom: 1px dashed #ccc;
            }}
        </style>

        <div class="slot-container" id="slot-container">
            <div class="reel" id="reel">
                {reel_items_html}
            </div>
        </div>

        <script>
        /* 🔴 修复点 1：(关键!) 等待所有HTML加载完毕后再运行脚本 */
        window.onload = function() {{
            const reel = document.getElementById('reel');
            if (!reel) {{ return; }} /* 安全检查 */

            const stopIndex = {stop_index};
            const itemHeight = {item_height_px};
            const nItems = {n_items};

            /* 🔴 修复点 2：使用更可靠的"两阶段"动画 */
            
            // 1. 计算一个随机的"过头"位置 (用于模糊滚动)
            const randomOvershoot = -(nItems * itemHeight + Math.random() * 4000 + 2000);
            
            // 2. 计算最终停止位置
            const finalPosition = -(stopIndex * itemHeight);

            // 3. (阶段 1: T=0秒) 
            // 应用一个"加速"的过渡，并让它滚到"过头"位置
            reel.style.transition = 'transform 2.5s cubic-bezier(0.5, 0, 1, 1)'; /* 2.5秒加速 */
            reel.style.transform = `translateY(${{randomOvershoot}}px)`;

            // 4. (阶段 2: T=2.5秒) 
            // 在加速动画快结束时，切换为"减速"过渡，并设置"最终"位置
            setTimeout(() => {{
                reel.style.transition = 'transform 3s ease-out'; /* 3秒减速 */
                reel.style.transform = `translateY(${{finalPosition}}px)`;
            }}, 2500); // 2.5秒后执行
        }};
        </script>
        """

        # 4. (Streamlit) 渲染这个HTML组件
        components.html(slot_machine_html, height=item_height_px + 10)
        
        # 5. (Streamlit) 在组件下方显示最终结果
        result_placeholder = st.empty()
        
        # 6. (Python) 等待 Python，必须和 JS 动画的总时长匹配 (2.5 + 3 = 5.5秒)
        time.sleep(5.5) 
        
        result_placeholder.success(f"恭喜！您抽中了： {result}")

        if "谢" not in result and "无" not in result:
            st.balloons()
            
    else:
        st.info("请点击上面的按钮开始抽奖")

# --- 程序入口 ---
if __name__ == "__main__":
    create_wheel_app()
