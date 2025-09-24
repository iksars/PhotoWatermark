# Photo Watermark CLI

这是一个命令行工具，用于自动为图片添加拍摄日期水印。程序会读取图片的 EXIF 信息来获取拍摄日期，并将其作为水印添加到图片上。

## ✨ 功能

-   **自动提取日期**：从图片的 EXIF 信息中智能提取原始拍摄日期（`DateTimeOriginal`）。
-   **自定义水印**：可以自由设置水印的字体大小、颜色和位置（左上角、居中、右下角）。
-   **自定义字体**：支持使用自己的字体文件（`.ttf` 或 `.otf`），默认使用项目自带的 `Roboto-Regular` 字体。
-   **自动处理方向**：能够自动读取并修正因手机拍摄导致的照片旋转问题，确保输出图片方向正常。
-   **批量处理**：一次性处理指定目录下的所有图片（`.jpg`, `.jpeg`, `.png`）。
-   **安全输出**：处理后的图片会保存在一个新的子目录（`原目录名_watermark`）中，不会覆盖原始文件。

## 🚀 安装

1.  **克隆仓库**
    ```bash
    git clone https://github.com/iksars/PhotoWatermark.git
    cd PhotoWatermark
    ```

2.  **创建并激活 Python 虚拟环境**
    ```bash
    # 创建虚拟环境
    python3 -m venv .venv

    # 激活虚拟环境 (Linux/macOS)
    source .venv/bin/activate
    ```

3.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

## 💡 使用方法

基本命令格式如下：

```bash
python watermark.py <图片目录> [可选参数]
```

---

### 示例

假设你的图片都存放在一个名为 `my_trip_photos` 的文件夹中。

1.  **使用默认设置**
    （字体大小: 50, 颜色: 白色, 位置: 右下角）
    ```bash
    python watermark.py my_trip_photos
    ```

2.  **自定义水印**
    -   设置字体大小为 `100`
    -   颜色为 `red` (红色)
    -   位置在 `top-left` (左上角)
    ```bash
    python watermark.py my_trip_photos --font-size 100 --color red --position top-left
    ```

3.  **使用自定义字体**
    如果你有一个名为 `my-font.ttf` 的字体文件，可以这样使用：
    ```bash
    python watermark.py my_trip_photos --font-path /path/to/my-font.ttf --font-size 120
    ```

### 所有可用参数

-   `image_dir`: (必需) 包含图片的目录路径。
-   `--font-size`: (可选) 水印的字体大小。默认为 `50`。
-   `--color`: (可选) 水印的颜色，可以是颜色名（如 `white`, `black`, `red`）或十六进制代码（如 `#FFFFFF`）。默认为 `white`。
-   `--position`: (可选) 水印在图片上的位置。可选值为 `top-left`, `center`, `bottom-right`。默认为 `bottom-right`。
-   `--font-path`: (可选) 指定一个 `.ttf` 或 `.otf` 字体文件的路径。如果未提供，则使用项目 `fonts` 目录下的 `Roboto-Regular.ttf`。

## 📁 项目结构

```
.
├── fonts/
│   └── Roboto-Regular.ttf   # 默认字体
├── .gitignore             # Git 忽略配置
├── LICENSE                # 项目许可证
├── README.md              # 项目说明文档
├── requirements.txt       # Python 依赖包
└── watermark.py           # 主程序脚本
```
