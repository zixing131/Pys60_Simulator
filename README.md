# Pys60_Simulator

桌面 PyS60 模拟器，对照 `pys60-1.4.5_src` 的 Python 包装层、C/C++ 参数解析和 SDK 颜色转换语义实现。

已接入图形、UI、活动对象、音频、数据库，以及摄像头、通讯录、日历、电话、短信、收件箱、日志、GPS、传感器、OpenGL 和虚拟蓝牙/OBEX。桌面显示与截图共用画布和控件渲染。支持范围与剩余差异见 [兼容说明](docs/API_COMPATIBILITY.md)。这不是完整的 Symbian 操作系统模拟。

## 运行

项目以带 Tk 的 **Python 2.7** 为主运行环境，兼容 Python 3.10+。`requirements.txt` 会按解释器选择依赖版本；Python 2.7 使用 Pillow 6.2.2、pygame 2.0.3、NumPy 1.16.6、PyOpenGL 3.1.5 和 OpenCV 4.1.2.30：

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

仓库内的老程序可继续使用 Python 2.7，无需先迁移 Python 3。例如从任意工作目录执行：

```sh
python /path/to/Pys60_Simulator/run_pys60.py /path/to/Pys60_Simulator/Pys60_Simulator/games/flappybird.PY
```

已回归 Flappy Bird、`2048正式版v1.3.py`、推箱子、`softwares/qqui.py`、`softwares/wsg/demo6.py` 和 `softwares/qq_for_symbian/main.py`。这些程序的资源按文件位置定位，存档写入 `~/.pys60-simulator/examples`（或 `PYS60_DATA_DIR`），不依赖 IDE 的工作目录。推箱子首次运行会将仓库中旧文本格式的关卡/记录导入用户目录的 SQLite，原资源不变。其他第三方程序仍需逐个回归。

## 配置模拟设备

数据默认保存在 `~/.pys60-simulator`；设置 `PYS60_DATA_DIR` 可隔离不同应用或测试。通讯录和日历复用原版公开包装层，下层用 SQLite 持久化。设备注入示例：

```python
import simulator
simulator.set_camera_source('frame.jpg')  # 图片、图片序列、视频路径、PIL 图像、函数或摄像头编号
simulator.set_position(31.2304, 121.4737, altitude=12.5)
simulator.set_gsm_location(460, 0, 12, 34)
simulator.receive_sms('5550100', u'测试消息')
simulator.receive_call('5550100')
simulator.emit_sensor(1, 0, 300, 0)
```

应用仍通过 `camera`、`positioning`、`telephone` 等原版 API 访问设备。没有配置相机或 GPS 时会报告不可用，不返回伪造的成功结果。

OpenGL 使用桌面兼容上下文和真实离屏 framebuffer：macOS 默认 CGL，其他平台使用 SDL2；每个 GLCanvas 的状态独立。需要宿主可用的 OpenGL 2.1 兼容驱动。`PYS60_GL_BACKEND=sdl` 可选择 SDL 后端，必要时用 `PYS60_SDL_LIBRARY` 指定 SDL2 动态库。`PYS60_FONT` 可指定用于桌面绘制的 TTF 字体。

## 验证

```sh
python -m unittest discover -s tests -v
python tests/gui_smoke.py
python tests/app_regression.py
python tests/app_regression.py --gui
python examples/extensions_demo.py --smoke
```

单元测试使用无 Tk 窗口模式；OpenGL 测试仍创建原生 GL 上下文。GUI smoke 会短暂打开窗口，对比实际 Tk PhotoImage 与截图中的像素。扩展测试覆盖 SQLite 重开、事务/回滚、回调顺序/取消、录像解码、GPS 数据、蓝牙收发与 OpenGL 读回。API 表面检查读取本地 `pys60-1.4.5_src`，该目录不存在时仅跳过源码表面检查。

`PYS60_HEADLESS=1` 可禁用 Tk 窗口。此时对话框默认取消，不会自动确认或选择第一项。异步回调在创建线程进入 `e32.ao_yield()`、`ao_sleep()`、`Ao_lock.wait()` 或 Tk 事件循环时执行。

已在本机 macOS 的 Python 2.7.14 / Pillow 6.2.2 下验证核心与扩展接口、CGL、Tk 及六个实际程序；Python 3.10 作为兼容回归。Windows/Linux 的实际驱动、字体及摄像头尚未实机验证。第三方来源见 [版权说明](docs/THIRD_PARTY_NOTICES.md)。
