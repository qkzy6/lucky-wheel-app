# streamlit_app.py
# (版本 6 - 真正的"无限循环"动画 + "平滑停止")

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
    # (为了让"滚筒"更长，我们复制 *至少* 5 次)
    # (更长的列表能保证"减速"阶段不会看到末尾)
    items_list = items_config * 5 
    labels = [item[0] for item in items_list]
    weights = [item[1] for item in items_list]
    n_items = len(items_list) 
    base_len = len(items_config) # 单个循环的长度

    # --- 视觉参数 ---
    item_height_px = 70  # 每个奖品的高度 (像素)
    font_size_px = 30  # 奖品的字体大小 (像素)
    visible_items = 3  # 我们希望同时显示3个
    container_height = item_height_px * visible_items # 容器总高度
    
    # (Python) 计算单个循环的高度 (用于 CSS @keyframes)
    one_loop_height = base_len * item_height_px

    # --- Streamlit 交互 ---
    if st.button("开始抽奖!", type="primary", use_container_width=True):
        
        # --- (Python) 抽奖逻辑 ---
        chosen_base_index = random.choices(list(range(base_len)), weights=[w[1] for w in items_config], k=1)[0]
        result = items_config[chosen_base_index][0]
        
        # 我们让它停在第 3 个重复列表的对应位置
        stop_index = (base_len * 2) + chosen_base_index
        
        # (Python) 计算 JS 最终需要停止的位置 (居中)
        centering_offset = (item_height_px * (visible_items - 1) / 2)
        final_position = -((stop_index * item_height_px) - centering_offset)

        # --- HTML/CSS/JS ---
        reel_items_html = ""
        for label in labels:
            reel_items_html += f'<div class="item">{label}</div>'

        slot_machine_html = f"""
        <style>
            .slot-container {{
                width: 100%; 
                height: {container_height}px;
                overflow: hidden; 
                border: 2px solid #444; 
                border-radius: 5px;
                background: #f9f9f9; 
                box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
            }}
            .reel {{ 
                /* 默认无动画，JS会添加 */
            }}
            .item {{
                height: {item_height_px}px; 
                line-height: {item_height_px}px;
                font-size: {font_size_px}px; 
                font-weight: bold; 
                text-align: center;
                border-bottom: 1px dashed #ccc;
            }}
            
            /* 🔴 改动点 1: 
               定义一个"无限循环"的动画
               它从 0 滚动到 -one_loop_height
            */
            @keyframes spin {{
                0% {{
                    transform: translateY(0);
                }}
                100% {{
                    transform: translateY(-{one_loop_height}px);
                }}
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

            const finalPosition = {final_position};

            /* 🔴 改动点 2: (阶段 1: 立即开始无限循环) */
            // 0.5s 滚一个循环，非常快 (制造模糊感)
            // 'linear' 保证匀速
            // 'infinite' 保证无限循环 (解决"白屏")
            reel.style.animation = 'spin 0.5s linear infinite';

            /* 🔴 改动点 3: (阶段 2: 2.5秒后, 准备停止) */
            setTimeout(() => {{
                // (关键步骤 1: 抓住当前位置)
                // 我们需要"抓住"滚筒在动画中的确切位置
                const containerTop = reel.parentElement.getBoundingClientRect().top;
                const reelTop = reel.getBoundingClientRect().top;
                const currentY = reelTop - containerTop;

                // (关键步骤 2: 无缝切换)
                reel.style.animation = 'none'; // 停止无限循环
                reel.style.transition = 'none'; // 确保下一步"设置"是瞬时的
                
                // 立即将滚筒的"物理"位置设置为我们"抓住"的位置
                reel.style.transform = `translateY(${{currentY}}px)`;

                // (关键步骤 3: 强制浏览器"刷新")
                // 这是一个小技巧，强制浏览器在应用"减速"动画前
                // 先"承认"上面的 `transform` 更改
                reel.offsetHeight; 

                // (关键步骤 4: 应用减速)
                reel.style.transition = 'transform 3s ease-out'; // 3秒减速
                reel.style.transform = `translateY(${{finalPosition}}px)`; // 滚向最终位置
            }}, 2500); // 2.5秒后执行"停止"
        }};
        </script>
        """

        # 4. (Streamlit) 渲染这个HTML组件
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
