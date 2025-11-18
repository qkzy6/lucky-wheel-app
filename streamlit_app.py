# streamlit_app.py
# (版本 2 - 带老虎机滚动效果)

import streamlit as st
import random
import streamlit.components.v1 as components  # <-- 导入新组件


def create_wheel_app():
    st.title("🎉 幸运大转盘 (网页版) 🎉")

    # ========== 配置 ==========
    # 注意：为了让滚动效果更好看，我把列表复制了2遍
    items_config = [
        ("谢谢参与", 50),
        ("10积分", 15),
        ("20积分", 10),
        ("50积分", 10),
        ("100积分", 5),
        ("神秘大奖", 3),
    ]
    # (为了让"滚筒"更长，我们复制几次)
    items_list = items_config * 5  # 列表 x 5

    # 提取标签和权重 (这部分逻辑和您原来的一样)
    labels = [item[0] for item in items_list]
    weights = [item[1] for item in items_list]
    n_items = len(items_list)

    # --- Streamlit 交互 ---
    if st.button("开始抽奖!", type="primary", use_container_width=True):

        # 1. (Python) 核心抽奖逻辑 (不变)
        # 我们在[中间]的重复列表里抽取一个
        base_len = len(items_config)
        # 抽取一个 0 到 base_len-1 的索引
        chosen_base_index = random.choices(list(range(base_len)), weights=[w[1] for w in items_config], k=1)[0]
        result = items_config[chosen_base_index][0]

        # 2. (JS) 计算 JS 应该停在哪个索引上
        # 我们让它停在第 3 个重复列表的对应位置
        stop_index = (base_len * 2) + chosen_base_index
        item_height_px = 50  # 每一项的高度 (像素)

        # 3. (HTML/CSS/JS) 动态生成"老虎机"组件
        # 这段代码会发送到浏览器并在那里执行

        # (CSS 样式)
        reel_items_html = ""
        for label in labels:
            reel_items_html += f'<div class="item">{label}</div>'

        slot_machine_html = f"""
        <style>
            .slot-container {{
                width: 100%;
                height: {item_height_px}px; /* 只显示一个奖品的高度 */
                overflow: hidden;
                border: 2px solid #444;
                border-radius: 5px;
                background: #f9f9f9;
                box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
            }}
            .reel {{
                /* JS会改变这里的 transform 和 transition */
                transition: none; /* 默认无动画 */
                transform: translateY(0);
            }}
            .item {{
                height: {item_height_px}px;
                line-height: {item_height_px}px;
                font-size: 20px; /* 字体调小一点 */
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
        (function() {{
            const reel = document.getElementById('reel');
            const stopIndex = {stop_index};
            const itemHeight = {item_height_px};

            // 1. (模糊/加速)
            // 立即开始一个"模糊"的快速滚动
            // 我们通过 CSS @keyframes 来实现 (比 JS 更流畅)

            // (动态创建 @keyframes 动画)
            const styleSheet = document.createElement("style");
            const randomSpin = -(Math.random() * 10000 + 10000); // 随机滚动位置
            styleSheet.innerHTML = `
                @keyframes spin-fast {{
                    0% {{ transform: translateY(0); }}
                    100% {{ transform: translateY(${randomSpin}px); }}
                }}
            `;
            document.head.appendChild(styleSheet);

            // 应用这个快速模糊的动画
            reel.style.animation = 'spin-fast 1.5s linear infinite';

            // 2. (等待) 
            // 让它"模糊"地转 2.5 秒钟
            setTimeout(() => {{
                // 3. (停止) 
                // 移除"模糊"动画，并计算最终停止位置
                reel.style.animation = 'none'; // 停止无限滚动

                // 计算最终停止位置 (居中)
                const finalPosition = -(stopIndex * itemHeight);

                // 4. (缓动) 
                // 应用一个 CSS 'ease-out' 动画，让它平滑地停下
                reel.style.transition = 'transform 3s ease-out'; // 3秒钟缓动停止
                reel.style.transform = `translateY(${finalPosition}px)`;

            }}, 2500); // 2.5秒后开始执行"停止"

        }})();
        </script>
        """

        # 4. (Streamlit) 渲染这个HTML组件
        components.html(slot_machine_html, height=item_height_px + 10)  # 增加一点高度

        # 5. (Streamlit) 在组件下方显示最终结果 (使用 st.empty 延迟显示)
        result_placeholder = st.empty()

        # 6. (关键) 等待动画播完再显示文字
        # 我们必须用 time.sleep 来"等待"前端动画播完 (2.5秒 + 3秒 = 5.5秒)
        time.sleep(5.5)

        result_placeholder.success(f"恭喜！您抽中了： {result}")

        if "谢" not in result and "无" not in result:
            st.balloons()

    else:
        # 默认显示
        st.info("请点击上面的按钮开始抽奖")


# --- 程序入口 ---
if __name__ == "__main__":
    create_wheel_app()