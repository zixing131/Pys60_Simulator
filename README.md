# Pys60_Simulator

桌面 PyS60 模拟器，对照 `pys60-1.4.5_src` 的 Python 包装层、C/C++ 参数解析和 SDK 颜色转换语义实现。

已接入图形、UI、活动对象、音频、数据库，以及摄像头、通讯录、日历、电话、短信、收件箱、日志、GPS、传感器、OpenGL 和虚拟蓝牙/OBEX。桌面显示与截图共用画布和控件渲染。支持范围与剩余差异见 [兼容说明](docs/API_COMPATIBILITY.md)。这不是完整的 Symbian 操作系统模拟。

## 运行

使用带 Tk 的 **Python 3.10+**：

```sh
python -m pip install -r requirements.txt
python examples/api_demo.py
python examples/extensions_demo.py
python run_pys60.py path/to/application.py
```

扩展示例有摄像头、OpenGL、数据三个标签。默认相机画面是明确配置的彩条测试图，GPS 是注入位置；菜单可以注入短信。电话和短信操作只作用于本地模拟设备。

显式选择宿主摄像头或视频：

```sh
python examples/extensions_demo.py --camera 0
python examples/extensions_demo.py --camera path/to/video.mp4
```

Q / F1 打开菜单，W / F2 退出；文本编辑器中使用 F1 / F2，避免占用字母输入。运行自己的脚本建议使用 `run_pys60.py`，它安装 S60 socket 扩展，并确保标准库同名 `calendar` 不会遮住 S60 日历 API。

旧游戏与第三方应用仍可能含 Python 2 语法，需要先迁移后再使用当前运行时；本次没有批量转换它们，也不再宣称当前新增后端支持 Python 2。

## 配置模拟设备

数据默认保存在 `~/.pys60-simulator`；设置 `PYS60_DATA_DIR` 可隔离不同应用或测试。通讯录和日历复用原版公开包装层，下层用 SQLite 持久化。设备注入示例：

```python
import simulator
simulator.set_camera_source('frame.jpg')  # 图片、图片序列、视频路径、PIL 图像、函数或摄像头编号
simulator.set_position(31.2304, 121.4737, altitude=12.5)
simulator.set_gsm_location(460, 0, 12, 34)
simulator.receive_sms('5550100', '测试消息')
simulator.receive_call('5550100')
simulator.emit_sensor(1, 0, 300, 0)
```

应用仍通过 `camera`、`positioning`、`telephone` 等原版 API 访问设备。没有配置相机或 GPS 时会报告不可用，不返回伪造的成功结果。

OpenGL 使用桌面兼容上下文和真实离屏 framebuffer：macOS 默认 CGL，其他平台使用 SDL2；每个 GLCanvas 的状态独立。需要宿主可用的 OpenGL 2.1 兼容驱动。`PYS60_GL_BACKEND=sdl` 可选择 SDL 后端，必要时用 `PYS60_SDL_LIBRARY` 指定 SDL2 动态库。`PYS60_FONT` 可指定用于桌面绘制的 TTF 字体。

## 验证

```sh
python -m unittest discover -s tests -v
python tests/gui_smoke.py
python examples/extensions_demo.py --smoke
```

单元测试使用无 Tk 窗口模式；OpenGL 测试仍创建原生 GL 上下文。GUI smoke 会短暂打开窗口，对比实际 Tk PhotoImage 与截图中的像素。扩展测试覆盖 SQLite 重开、事务/回滚、回调顺序/取消、录像解码、GPS 数据、蓝牙收发与 OpenGL 读回。API 表面检查读取本地 `pys60-1.4.5_src`，该目录不存在时仅跳过源码表面检查。

`PYS60_HEADLESS=1` 可禁用 Tk 窗口。此时对话框默认取消，不会自动确认或选择第一项。异步回调在创建线程进入 `e32.ao_yield()`、`ao_sleep()`、`Ao_lock.wait()` 或 Tk 事件循环时执行。

已在 macOS arm64 / Python 3.10 上验证 CGL、SDL 和 Tk。Windows/Linux 的实际驱动、字体及摄像头尚未实机验证。第三方来源见 [版权说明](docs/THIRD_PARTY_NOTICES.md)。
