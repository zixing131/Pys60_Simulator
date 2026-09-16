# PyS60 1.4.5 兼容范围

基准为本仓库提供的 `pys60-1.4.5_src`，目标设备档案为 S60 3.0。优先级为实际 Python 包装代码、C/C++ 参数解析与实现、随附文档。SDK 提供而此源码未定义的枚举另核对 Symbian SDK 头文件。

“接口存在”与“行为完全一致”分开验证：`tests/test_api_surface.py` 从原版方法表/包装层提取公开名字；`tests/test_contract.py` 和 `tests/test_extensions.py` 验证关键数据、像素和事件语义；`tests/gui_smoke.py` 核对实际 Tk 显示与截图。接口检查通过不表示全部硬件能力已实现。

## 已对齐的核心行为

- `graphics`：五种模式名称、只读 size/mode、twipsize；新图像式 resize/transpose；旋转常量 1–5；多点 getpixel 返回 RGB 三元组列表；弧度制 arc/pieslice；裁剪源区域、缩放和灰度 mask；矩形右/下边界不包含；绘图参数与颜色校验；load 尺寸限制、save 格式/压缩参数；异步返回值及 stop；文字测量同时使用 maxwidth/maxadvance；Draw 共享目标。
- `appuifw`：Canvas 的三类按键事件、bind 清除、重绘矩形和 resize 回调；Text 的内容、光标和编辑方法；Listbox 的数据格式、当前项、回调和绑定；Form 的字段验证、序列操作与 save_hook；对话框的取消与结果类型；Application 的 screen/orientation、layout 返回结构、标题、菜单、用户标签切换；InfoPopup 的显示、隐藏和定时。
- `e32`：创建线程执行回调的活动对象调度；异步和同步 sleep/timer；pending timer 校验和取消；锁的预先 signal、单等待者及线程约束；跨线程 callgate；`file_copy(target, source)`；版本字段、进程启动、闲置计时与错误类型。导入不创建 Tk 窗口，也不再替换进程的 `os.abort`。
- `audio`：真实 pygame 文件加载、独立文件缓冲、单活动播放器、状态转换、重复与间隔、音量、位置及微秒时长；播放开始/自然结束回调。
- `sysinfo`：补齐原版公开函数；IMEI、电池、信号和软件版本采用原版模拟器约定，屏幕随方向变化；内存与磁盘容量查询宿主机。
- `e32db`：Dbms 创建/打开、事务、SQL 修改计数；Db_view 的准备、逐行访问、1 基列编号、类型、NULL、raw 与日期读取；SQLite 持久化。
- `e32dbm`：字符串键值、r/w/c/n、fast 缓存、sync、close、reorganize、迭代和映射操作。移除了读取文件时执行 `eval` 的旧行为。
- `topwindow`：位置/大小、图像列表、增删、可见性与实际 Tk 浮窗；保留旧 `TopWindow` 导入别名。`globalui` 提供带超时的查询。`keycapture` 提供窗口内捕获、forwarding、start/stop/last_key。socket 接入点提供 start/stop/ip、选择与默认对象校验。`appuifw2` 共享同一实现及 app 实例。

## 新增设备与 OpenGL 后端

- `contacts`、`calendar`：沿用 1.4.5 / S60 3rd Edition 的 Python 包装层，后端用 SQLite；支持 ID、字段 schema、分组、检索、自动提交、begin/commit/rollback、事件类型、闹钟属性、完成状态与重复实例查询。日期规则支持 daily、weekly、monthly_by_dates、monthly_by_days、yearly_by_date、yearly_by_day 和 exceptions。`calendar` 同时保留宿主标准库函数；启动入口处理已经加载标准库 calendar 的情况。
- `messaging`、`inbox`、`telephone`、`logs`：共享持久化消息/日志。短信正常回调为 0→1→2→3→4；有 callback 时等待首次事件后返回，无 callback 时等待终态。电话状态回调收到 `(status, incoming_number)`；来电/短信可经 `simulator` 注入。Inbox 通知异步执行，解绑后不会收到队列中旧通知。
- `camera`：图片/序列、视频文件、PIL 图像、可调用帧提供者或显式选择的 OpenCV 摄像头。RGB/RGB12/RGB16 返回 graphics.Image，JPEG 模式返回字节；finder 输出图像帧。录制生成实际 AVI/MP4/MOV 文件，回调保留 `(error, event)` 与 0xFA0–0xFA2 常量。
- `positioning`、`location`：线程内同步/异步定位请求、微秒间隔、深拷贝位置/速度/卫星字段、最后位置、模块信息和 GSM 四元组。必须设置 requestors 和位置源；未配置的设备报告不可用。`sensor` 沿用原版方向过滤逻辑、0.1 秒稳定定时和 RotSensor 映射，后台事件在连接线程投递。
- `gles`、`glcanvas`：从方法表登记 179 个入口、385 个 GL 常量和 58 个 EGL 常量。桌面 OpenGL 实际处理矩阵、光照、纹理、客户端数组、VBO、索引绘制、状态查询和像素读回；16.16 定点数转换为浮点调用。GLCanvas 独立上下文，redraw 收到帧号，resize 收到 None；输出进入同一桌面画布/截图。数组长度校验避免宿主驱动越界读取。
- socket 虚拟蓝牙：AF_BT 使用仅监听 loopback 的 TCP；支持通道分配、服务发现/广告、异步 accept/recv、实际字节收发，以及等待中的接收端之间的文件传输。服务注册限同一模拟器进程，设备地址为 `02:00:00:00:00:01`。Internet socket 继续使用宿主实现。
- 桌面绘制：RGB12/RGB16 使用 SDK TRgb 截断与位扩展；L/1 使用 `(2R+5G+B)>>3`。写入、blit、加载、缩放、相机帧使用统一转换。pattern 白区使用 fill、黑区保留底图；字体 flags 校验，支持粗体、斜体、上下标和抗锯齿开关。Canvas 按 EMainPane 放置，标题/标签/软键区、Text、Listbox 的显示和截图使用同一软件绘制结果。

## 源码与文档冲突时的选择

- `graphics.blit` 的实际 C++ 位置参数顺序是 `(image, source, target, scale, mask)`，文档将 target 写在 source 前。本项目采用 C++ 顺序，调用方最好使用关键字。非缩放时，C++ 的 BitBlt 不使用 target 的右下角限制源矩形。
- resize/transpose 在提供 callback 时立即返回 None，成功回调收到新 Image、失败收到 None；save/load 回调收到错误码。这按 `ext/graphics/graphics.py` 实现，而非文档概述中的统一错误码描述。
- `point` 按 `graphicsmodule.cpp` 中的实际实现只绘制坐标序列第一点。
- `audio` 的 C++ PlayL 没有重置 SetPosition，因此保留显式设置或 stop 后的位置。
- `e32dbm` 原版 `_query` 实际将持久化结果编码为 latin-1，而文档称结果为 Unicode。本项目持久化读取使用字节串；Python 3 的 str 输入按 latin-1 编码。非 latin-1 Unicode 以及 fast 模式临时值的 Unicode/bytes 混用尚未完全复刻原版，当前输入会更早报编码异常。

关键来源：

- `ext/graphics/graphics.py`；`graphicsmodule.cpp` 的 `Draw_blit`、`Graphics_ParseAndSetParams`、`Draw_point`、`Image_save`、`Image_transpose`。
- `appui/appuifw/appuifwmodule.cpp` 的 Text/Listbox/Form 方法、常量注册；`Doc/lib/libappuifw.tex`。
- `core/Symbian/e32module.cpp` 的 Ao_lock/Ao_timer/Ao_callgate 和模块方法表。
- `ext/recorder/audio.py`、`recordadapter.cpp`；`ext/sysinfo/sysinfo.py`、`Doc/lib/libsysinfo.tex`。
- `ext/e32db/e32dbmodule.cpp`；`core/Lib/e32dbm.py`；`ext/topwindow/topwindow.py`；`ext/keycapture/keycapture.py`。
- SDK 枚举依据：[GULALIGN.H](https://github.com/SymbianSource/oss.FCL.sf.mw.classicui/blob/master/lafagnosticuifoundation/uigraphicsutils/gulinc/GULALIGN.H)、[GDI.H](https://github.com/SymbianSource/oss.FCL.sf.os.graphics/blob/master/graphicsdeviceinterface/gdi/inc/GDI.H)、[AknUtils.h](https://github.com/SymbianSource/oss.FCL.sf.mw.classicui/blob/master/classicui_plat/ui_framework_utilities_api/inc/AknUtils.h)。这些为后续公开 SDK 源码，尚未用 S60 3.0 二进制逐项验证。

- 原版 contacts 新条目 rollback 调用不存在的底层 add_contact，本项目修正为 create_entry；原版 calendar 的 undated todo 路径缺少可用底层实现/自动提交，本项目补上取消日期和持久化。这两项按接口意图修复，不复刻原版缺陷。
- GPS callback 抛异常后仍继续订阅，符合 posdatafetcher.cpp 的 RunL；显式 stop_position 停止请求。calendar 的 begin 是包装层编辑缓冲，不是数据库排他锁；独立条目对象并发提交仍遵循最后写入。
- OpenGL 不复刻原 C 扩展某些查询/像素数组缓冲长度缺陷；多值状态返回完整 tuple，并在输入不足时抛异常。

## 桌面近似与尚未覆盖的行为

以下仍不能宣称与真机完全一致：

- RGB12/RGB16/L/1 的颜色转换已按 SDK 公式验证。字体仍是项目 S60SC.ttf 或 PYS60_FONT，系统字体标签的尺寸为桌面设备档案；合成粗斜体、字形、DPI 与真机字体可能不同。Pillow 的斜线/宽线/椭圆栅格没有经过 Symbian 真机逐像素比较。异步图像计算在下一次调度时执行，计算本身没有后台并行。
- UI 外观、布局尺寸、原生导航/软键区采用桌面近似；Form 使用逐字段对话框，menu、自动增删标签/字段等原生表单交互未完整实现。Listbox 的 MBM/MIF 图标未渲染。Text 字体/样式是插入文本时的近似效果。
- screenshot 包含 Canvas/GLCanvas、软件绘制的 Text/Listbox、标题/标签/软键区和模拟浮窗；不包含宿主窗口边框或外部应用。Text 保留每字符插入样式，但复杂文本选择、IME 标记、双向排版仍依赖桌面近似。TopWindow 原生阴影、圆角、fading 尚未复刻。
- `Image.from_icon`、`from_cfbsbitmap`、`Content_handler.open`（嵌入文档）、录音和修改宿主系统时钟明确报 `SymbianError(-5, ...)`。`open_standalone` 使用宿主默认应用，不提供文档关闭通知。TTS 目前仅使用 macOS `say`。
- pygame 支持的编码格式受本地 SDL_mixer 构建限制。播放完成回调依赖活动调度器。未进行实际扬声器听测或麦克风录音测试。
- 数据库采用 SQLite，不能读取真机 Symbian DBMS 文件。核心 API 不自动转换旧文件；所选示例的 `pys60_examples` 仅在用户目录副本中导入仓库自带的文本 DBM 关卡/记录。SQL 方言、COUNTER 自动递增、范围约束、复杂 SELECT 的声明类型、公元 1 年以前日期等仍有差异。数据库新建/n 模式按原版约定替换目标文件。
- 文件名使用宿主路径，没有全局虚拟 C:/E:/Z: 文件系统；非 Windows 平台 drive_list 的 C: 表示宿主根文件系统。接入点借用现有宿主网络，不能切换蜂窝网络或控制物理适配器。keycapture 只捕获模拟器窗口，不捕获其他宿主应用。
- 电话/短信是本地模拟，未接真实运营商；暂未提供失败状态注入。相机后端仅宣告 none flash / auto exposure / auto white balance，其他设置明确报错；宿主硬件授权和编码器可用性由系统决定。GPS/传感器使用注入数据，未接宿主定位服务/实体传感器。calendar alarm 只保存闹钟信息，不触发桌面系统通知。
- PIM 的 vCard/vCalendar 支持常用文本/时间字段和模拟器完整往返（X-PYS60 扩展字段）；尚未完整实现外部文件的折行/字符集/quoted-printable、全部标准 RRULE/时区与厂商私有字段。不能读取 Symbian 原生二进制数据库。所有模式字段、复杂多日事件/例外实例仍需真机对照。
- GLES 可选 OES palette matrix、draw texture、point-size array、weight/index pointer 入口存在但明确抛 NotImplementedError，CheckExtension 返回 False。桌面内部缓冲精度可能高于请求最小值；不是逐指令 GLES 驱动仿真。`gles_utils` 的数值/向量/定点 camera 辅助函数已修复源码明显错误，原版不完整 lens-flare helper 明确报不支持。
- 蓝牙不连接物理设备，set_security 仅保存模拟安全策略，不能提供实际配对或空口加密；OBEX 是本地文件传递协议，不是完整无线 OBEX 协议栈。Socket 的所有 Symbian 异步/SSL 方言尚未完全移植。
- Python 2.7 为主运行环境，所选六个程序同时保留 Python 3 兼容。未对整个 games/softwares 目录作完整迁移或全量回归；未修改参考源码，也未把其中的 Symbian 构建系统用于宿主环境。

## 后续对齐的验收方式

新增一个模块时，先从它的 Python 包装层与 C++ 方法表登记 API，明确宿主后端或模拟数据模型，再增加独立的参数、返回值、异常、生命周期和异步时序测试。不能仅用空函数或固定成功值通过“接口存在”检查。依赖真机行为的部分需要对应 SDK/emulator 或设备执行原版测试作为对照。

## 本轮验证记录

macOS arm64、Python 3.10、Pillow 11、pygame 2.6.1、PyOpenGL 3.1.10、OpenCV 4.10：67 项 unittest 全部通过。另通过 CGL/SDL 两种后端的 OpenGL 三角形、纹理/VBO 和上下文隔离验证；通过实际 Tk PhotoImage 与截图像素对比及 `extensions_demo.py --smoke`。无 Symbian SDK 二进制/真机对照，因此不能声称整套原生 UI 字形和全部 API 边界已完全相同。

新增依据：`ext/{contacts/eka2,calendar/eka2,camera,gps,sensor,telephone,messaging,inbox,logs,gles,glcanvas,socket}` 的包装层、方法表与实现；颜色公式为 SDK `graphicsdeviceinterface/gdi/inc/GDI.INL` 中的 `TRgb::_Color4K/_Color64K/_Gray256/_Gray2`。移植包装层的版权与修改说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。


## Python 2.7 与真实应用回归

- 文字采用显式 ascent→baseline 换算，兼容 Pillow 6 忽略 `anchor` 的行为；单色字形直接请求字体引擎栅格化，避免对抗锯齿图进行二值化导致断笔。QQ 控件显式选择抗锯齿。GLib 锚点根据实际字形 bbox 计算。
- 多边形使用填充加闭合折线实现宽边框，避免 Pillow 6 不支持 `polygon(width=...)`。弧线补齐旧 Pillow 缺失的端点。`akntextutils` 换行使用绘图相同的字体测量；`txtfield` 延迟创建编辑器，保留 Unicode、长度限制并移除 Tk 哨兵换行。
- 修复 Python 2 的模块加载、目录创建、Unicode 通讯录/消息、日历日期与迭代器、Bluetooth socket 包装、线程标识、OpenGL 框架加载和 Pillow 枚举差异。依赖按解释器版本固定。
- `tests/app_regression.py` 从临时工作目录经真实启动器运行六个程序，用独立存档目录操作 QQ 输入/复选框、Flappy 开始/碰撞/重开/F2 退出取消、2048 合并与持久化、推箱子移动/撤销、WSG 控件/滚动、ZUI 焦点/编辑。`--gui` 另对比 Tk PhotoImage 与应用截图像素，产物默认位于系统临时目录 `pys60-app-regression`。
- `txtfield` 是第三方扩展适配，编辑中的宿主 Text 控件（含 IME/选择）不纳入软件截图；退出编辑后的文字进入统一画布。没有声称所有第三方 API 或真机像素已经完全一致。

最终回归环境：本机 macOS / Python 2.7.14 / Pillow 6.2.2，69 项接口测试；六个实际程序通过独立存档回归和 Tk 帧像素核验，包含嵌套 Tk 回调中等待与唤醒（F2 处理路径）。Python 3.10.9 也通过 69 项接口测试和同六个程序。旧版 Pillow 粗体改用字形掩码横向加粗，WSG 的滚动状态及数值标签重复绘制问题已纳入回归。
