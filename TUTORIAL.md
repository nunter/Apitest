# 接口测试小白入门到精通教程

欢迎来到接口测试的世界！本教程将带你从零开始，学习如何进行接口测试。我们将使用 Python 语言，配合 `requests` 库进行 HTTP 请求，并使用 `pytest` 框架来管理和运行测试用例。

## 1. 环境准备

首先，你需要安装 Python。安装完成后，我们需要安装一些必要的第三方库。

在终端（Terminal）或命令行中运行以下命令：

```bash
pip install -r requirements.txt
```

或者单独安装：

```bash
pip install flask requests pytest
```

## 2. 启动演示服务器

为了进行测试，我们需要一个被测接口。我们准备了一个简单的 API 服务器 `api_server.py`。

在终端中运行：

```bash
python api_server.py
```

你会看到类似以下的输出，说明服务器已启动：

```
 * Running on http://127.0.0.1:5000
```

**注意**：请保持这个终端窗口开启，不要关闭它。

## 3. 接口基础知识

接口（API）就像是餐厅的服务员。你（客户端）看菜单（文档）点菜（发送请求），服务员（API）把单子给厨房（服务器），厨房做好菜后，服务员再端给你（返回响应）。

### 常见的请求方法：

- **GET**: 获取资源（比如：查看用户列表）
- **POST**: 创建资源（比如：注册新用户）
- **PUT**: 更新资源（比如：修改用户信息）
- **DELETE**: 删除资源（比如：注销账号）

## 4. 编写测试脚本

打开 `test_api.py`，你会看到我们已经写好了一些测试用例。

### 示例 1: 获取用户列表 (GET)

```python
def test_get_users():
    """Test getting the list of users."""
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2
```

- `requests.get(...)`: 发送 GET 请求。
- `response.status_code`: 获取响应状态码。`200` 表示成功。
- `response.json()`: 获取响应的 JSON 数据。
- `assert`: 断言，用于判断结果是否符合预期。如果不符合，测试就会失败。

### 示例 2: 创建用户 (POST)

```python
def test_create_user():
    """Test creating a new user."""
    new_user = {
        "name": "Charlie",
        "email": "charlie@example.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=new_user)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Charlie"
```

- `json=new_user`: 发送 JSON 格式的数据。
- `201`: 表示资源创建成功。

## 5. 运行测试

打开一个新的终端窗口（记得保持服务器那个窗口开着），运行以下命令：

```bash
pytest test_api.py
```

你会看到测试运行的结果。如果一切顺利，你会看到绿色的点点，表示测试通过！

## 6. 进阶练习

尝试修改 `test_api.py`，添加一个新的测试用例，比如：

- 尝试获取一个不存在的用户 ID，断言状态码为 404。
- 尝试创建一个没有 email 的用户，断言状态码为 400。

## 7. 生成测试报告 (Allure)

我们集成了 Allure 框架，可以生成非常漂亮的测试报告。

### 7.1 安装 Allure 命令行工具

你需要先安装 Allure 的命令行工具。

- **MacOS**:
  ```bash
  brew install allure
  ```
- **Windows**:
  可以使用 Scoop 安装 `scoop install allure`，或者下载解压包配置环境变量。

### 7.2 运行测试并生成数据

运行以下命令，将测试结果保存到 `allure-results` 目录：

```bash
pytest --alluredir=./allure-results
```

### 7.3 查看报告

运行以下命令，Allure 会自动启动一个服务并在浏览器中打开报告：

```bash
allure serve ./allure-results
```

你将看到包含测试概览、步骤详情、耗时分析等丰富信息的报告。

祝你学习愉快！
