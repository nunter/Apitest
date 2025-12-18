from flask import Flask, jsonify, request, g
from flasgger import Swagger
from datetime import datetime, timedelta
import random
import json
import logging
import time

app = Flask(__name__)

# ==================== 中文支持配置 ====================
app.config['JSON_AS_ASCII'] = False  # 支持中文返回
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=utf-8'

swagger = Swagger(app)

# ==================== 日志配置 ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 日志颜色 (终端支持)
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

@app.before_request
def log_request_info():
    """记录请求日志"""
    g.start_time = time.time()
    
    # 获取请求体
    request_body = None
    if request.is_json:
        try:
            request_body = request.get_json(silent=True)
        except:
            request_body = request.data.decode('utf-8') if request.data else None
    
    # 打印请求日志
    print(f"\n{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}>>> REQUEST{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
    print(f"{Colors.YELLOW}Method:{Colors.RESET} {request.method}")
    print(f"{Colors.YELLOW}URL:{Colors.RESET} {request.url}")
    print(f"{Colors.YELLOW}Path:{Colors.RESET} {request.path}")
    
    if request.args:
        print(f"{Colors.YELLOW}Query Params:{Colors.RESET} {dict(request.args)}")
    
    if request.headers.get('Authorization'):
        print(f"{Colors.YELLOW}Authorization:{Colors.RESET} {request.headers.get('Authorization')}")
    
    if request_body:
        print(f"{Colors.YELLOW}Body:{Colors.RESET}")
        print(json.dumps(request_body, ensure_ascii=False, indent=2))
    
    logger.info(f"REQUEST: {request.method} {request.path}")

@app.after_request
def log_response_info(response):
    """记录响应日志"""
    # 计算响应时间
    duration = (time.time() - g.start_time) * 1000  # 转换为毫秒
    
    # 获取响应体
    response_body = None
    if response.content_type and 'application/json' in response.content_type:
        try:
            response_body = json.loads(response.get_data(as_text=True))
        except:
            response_body = response.get_data(as_text=True)
    
    # 状态码颜色
    status_color = Colors.GREEN if response.status_code < 400 else Colors.RED
    
    # 打印响应日志
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}<<< RESPONSE{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.YELLOW}Status:{Colors.RESET} {status_color}{response.status_code} {response.status}{Colors.RESET}")
    print(f"{Colors.YELLOW}Duration:{Colors.RESET} {duration:.2f}ms")
    print(f"{Colors.YELLOW}Content-Type:{Colors.RESET} {response.content_type}")
    
    if response_body:
        print(f"{Colors.YELLOW}Body:{Colors.RESET}")
        print(json.dumps(response_body, ensure_ascii=False, indent=2))
    
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    logger.info(f"RESPONSE: {response.status_code} - {duration:.2f}ms")
    
    return response

# ==================== 测试账号 ====================
# 可用于登录测试的账号
test_accounts = {
    "admin": {"password": "admin123", "role": "admin", "name": "管理员"},
    "test": {"password": "test123", "role": "user", "name": "测试用户"},
    "user1": {"password": "123456", "role": "user", "name": "张三"},
    "user2": {"password": "password", "role": "user", "name": "李四"},
    "vip": {"password": "vip888", "role": "vip", "name": "VIP用户"},
}

# 用于存储登录后的 token
active_tokens = {}

# ==================== 用户数据 ====================
users = [
    {"id": 1, "name": "张三", "email": "zhangsan@example.com", "phone": "13800138001", "status": "active"},
    {"id": 2, "name": "李四", "email": "lisi@example.com", "phone": "13800138002", "status": "active"},
    {"id": 3, "name": "王五", "email": "wangwu@example.com", "phone": "13800138003", "status": "inactive"},
    {"id": 4, "name": "Alice", "email": "alice@example.com", "phone": "13800138004", "status": "active"},
    {"id": 5, "name": "Bob", "email": "bob@example.com", "phone": "13800138005", "status": "active"},
    {"id": 6, "name": "测试用户A", "email": "testa@test.com", "phone": "13900139001", "status": "active"},
    {"id": 7, "name": "测试用户B", "email": "testb@test.com", "phone": "13900139002", "status": "pending"},
]

# ==================== 商品数据 ====================
products = [
    {"id": 1, "name": "iPhone 15 Pro", "price": 8999.00, "category": "手机", "stock": 100, "status": "on_sale"},
    {"id": 2, "name": "MacBook Pro 14", "price": 14999.00, "category": "电脑", "stock": 50, "status": "on_sale"},
    {"id": 3, "name": "AirPods Pro 2", "price": 1899.00, "category": "配件", "stock": 200, "status": "on_sale"},
    {"id": 4, "name": "iPad Air", "price": 4799.00, "category": "平板", "stock": 0, "status": "out_of_stock"},
    {"id": 5, "name": "Apple Watch", "price": 2999.00, "category": "手表", "stock": 80, "status": "on_sale"},
    {"id": 6, "name": "华为 Mate 60", "price": 6999.00, "category": "手机", "stock": 150, "status": "on_sale"},
    {"id": 7, "name": "小米14", "price": 3999.00, "category": "手机", "stock": 300, "status": "on_sale"},
    {"id": 8, "name": "测试商品(已下架)", "price": 99.00, "category": "测试", "stock": 10, "status": "off_sale"},
]

# ==================== 订单数据 ====================
orders = [
    {"id": "ORD20231201001", "user_id": 1, "product_id": 1, "quantity": 1, "total": 8999.00, "status": "completed", "created_at": "2023-12-01 10:30:00"},
    {"id": "ORD20231202001", "user_id": 2, "product_id": 2, "quantity": 1, "total": 14999.00, "status": "shipped", "created_at": "2023-12-02 14:20:00"},
    {"id": "ORD20231203001", "user_id": 1, "product_id": 3, "quantity": 2, "total": 3798.00, "status": "pending", "created_at": "2023-12-03 09:15:00"},
    {"id": "ORD20231204001", "user_id": 3, "product_id": 5, "quantity": 1, "total": 2999.00, "status": "cancelled", "created_at": "2023-12-04 16:45:00"},
    {"id": "ORD20231205001", "user_id": 4, "product_id": 6, "quantity": 1, "total": 6999.00, "status": "paid", "created_at": "2023-12-05 11:00:00"},
]

@app.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    tags:
      - Users
    parameters:
      - name: page
        in: query
        type: integer
        description: Page number
        default: 1
      - name: limit
        in: query
        type: integer
        description: Items per page
        default: 10
      - name: name
        in: query
        type: string
        description: Filter by name
    responses:
      200:
        description: List of users
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  email:
                    type: string
            total:
              type: integer
            page:
              type: integer
            limit:
              type: integer
    """
    # Filtering
    name_filter = request.args.get('name')
    filtered_users = users
    if name_filter:
        filtered_users = [u for u in users if name_filter.lower() in u['name'].lower()]

    # Pagination
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    start = (page - 1) * limit
    end = start + limit
    
    paginated_users = filtered_users[start:end]
    
    return jsonify({
        "data": paginated_users,
        "total": len(filtered_users),
        "page": page,
        "limit": limit
    })

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get a single user
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User found
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
      404:
        description: User not found
    """
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
          properties:
            name:
              type: string
            email:
              type: string
    responses:
      201:
        description: User created
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
      400:
        description: Invalid data
    """
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    new_user = {
        "id": users[-1]['id'] + 1 if users else 1,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update a user
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
    responses:
      200:
        description: User updated
      404:
        description: User not found
    """
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    user.update(data)
    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User deleted
    """
    global users
    users = [u for u in users if u['id'] != user_id]
    return jsonify({"message": "User deleted"}), 200

# --- New Endpoints ---

@app.route('/login', methods=['POST'])
def login():
    """
    Login to get a token
    ---
    tags:
      - Auth
    description: |
      可用的测试账号:
      - admin / admin123 (管理员)
      - test / test123 (普通用户)
      - user1 / 123456 (张三)
      - user2 / password (李四)
      - vip / vip888 (VIP用户)
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: admin123
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            token:
              type: string
            user:
              type: object
              properties:
                username:
                  type: string
                name:
                  type: string
                role:
                  type: string
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请提供用户名和密码"}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if username in test_accounts and test_accounts[username]['password'] == password:
        # 生成 token
        import hashlib
        token = f"token_{username}_{hashlib.md5(f'{username}{datetime.now().isoformat()}'.encode()).hexdigest()[:16]}"
        
        # 存储 token
        active_tokens[token] = {
            "username": username,
            "role": test_accounts[username]['role'],
            "name": test_accounts[username]['name'],
            "expires": (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
        return jsonify({
            "success": True,
            "message": "登录成功",
            "token": token,
            "user": {
                "username": username,
                "name": test_accounts[username]['name'],
                "role": test_accounts[username]['role']
            }
        }), 200
    
    return jsonify({"success": False, "error": "用户名或密码错误"}), 401

@app.route('/protected', methods=['GET'])
def protected():
    """
    Access protected resource
    ---
    tags:
      - Auth
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer <token>
    responses:
      200:
        description: Access granted
      401:
        description: Unauthorized
    """
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header[7:]
        if token in active_tokens:
            user_info = active_tokens[token]
            return jsonify({
                "message": "访问成功",
                "user": user_info,
                "secret_data": "这是受保护的数据"
            }), 200
    return jsonify({"error": "未授权访问，请先登录"}), 401

# ==================== 商品接口 ====================

@app.route('/products', methods=['GET'])
def get_products():
    """
    Get all products
    ---
    tags:
      - Products
    parameters:
      - name: page
        in: query
        type: integer
        description: Page number
        default: 1
      - name: limit
        in: query
        type: integer
        description: Items per page
        default: 10
      - name: category
        in: query
        type: string
        description: Filter by category (手机/电脑/配件/平板/手表/测试)
      - name: status
        in: query
        type: string
        description: Filter by status (on_sale/out_of_stock/off_sale)
    responses:
      200:
        description: List of products
    """
    # Filtering
    category = request.args.get('category')
    status = request.args.get('status')
    filtered = products
    
    if category:
        filtered = [p for p in filtered if p['category'] == category]
    if status:
        filtered = [p for p in filtered if p['status'] == status]
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    start = (page - 1) * limit
    end = start + limit
    
    return jsonify({
        "data": filtered[start:end],
        "total": len(filtered),
        "page": page,
        "limit": limit
    })

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get a single product
    ---
    tags:
      - Products
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Product found
      404:
        description: Product not found
    """
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "商品不存在"}), 404

# ==================== 订单接口 ====================

@app.route('/orders', methods=['GET'])
def get_orders():
    """
    Get all orders
    ---
    tags:
      - Orders
    parameters:
      - name: user_id
        in: query
        type: integer
        description: Filter by user ID
      - name: status
        in: query
        type: string
        description: Filter by status (pending/paid/shipped/completed/cancelled)
    responses:
      200:
        description: List of orders
    """
    user_id = request.args.get('user_id', type=int)
    status = request.args.get('status')
    filtered = orders
    
    if user_id:
        filtered = [o for o in filtered if o['user_id'] == user_id]
    if status:
        filtered = [o for o in filtered if o['status'] == status]
    
    return jsonify({
        "data": filtered,
        "total": len(filtered)
    })

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """
    Get a single order
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Order found
      404:
        description: Order not found
    """
    order = next((o for o in orders if o['id'] == order_id), None)
    if order:
        return jsonify(order)
    return jsonify({"error": "订单不存在"}), 404

@app.route('/orders', methods=['POST'])
def create_order():
    """
    Create a new order
    ---
    tags:
      - Orders
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_id
            - product_id
            - quantity
          properties:
            user_id:
              type: integer
              example: 1
            product_id:
              type: integer
              example: 1
            quantity:
              type: integer
              example: 1
    responses:
      201:
        description: Order created
      400:
        description: Invalid data
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请提供订单数据"}), 400
    
    product = next((p for p in products if p['id'] == data.get('product_id')), None)
    if not product:
        return jsonify({"error": "商品不存在"}), 400
    
    quantity = data.get('quantity', 1)
    total = product['price'] * quantity
    
    new_order = {
        "id": f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}",
        "user_id": data['user_id'],
        "product_id": data['product_id'],
        "quantity": quantity,
        "total": total,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    orders.append(new_order)
    
    return jsonify(new_order), 201

# ==================== 测试辅助接口 ====================

@app.route('/test/accounts', methods=['GET'])
def get_test_accounts():
    """
    Get all test accounts (for testing purpose)
    ---
    tags:
      - Test Helper
    description: 返回所有可用的测试账号信息，方便测试使用
    responses:
      200:
        description: List of test accounts
    """
    accounts_info = []
    for username, info in test_accounts.items():
        accounts_info.append({
            "username": username,
            "password": info['password'],
            "role": info['role'],
            "name": info['name']
        })
    return jsonify({
        "message": "以下是可用的测试账号",
        "accounts": accounts_info
    })

@app.route('/test/reset', methods=['POST'])
def reset_data():
    """
    Reset all data to initial state
    ---
    tags:
      - Test Helper
    description: 重置所有数据到初始状态，用于测试前清理
    responses:
      200:
        description: Data reset successfully
    """
    global users, products, orders, active_tokens
    
    users = [
        {"id": 1, "name": "张三", "email": "zhangsan@example.com", "phone": "13800138001", "status": "active"},
        {"id": 2, "name": "李四", "email": "lisi@example.com", "phone": "13800138002", "status": "active"},
        {"id": 3, "name": "王五", "email": "wangwu@example.com", "phone": "13800138003", "status": "inactive"},
        {"id": 4, "name": "Alice", "email": "alice@example.com", "phone": "13800138004", "status": "active"},
        {"id": 5, "name": "Bob", "email": "bob@example.com", "phone": "13800138005", "status": "active"},
    ]
    
    active_tokens = {}
    
    return jsonify({"message": "数据已重置"})

if __name__ == '__main__':
    print("=" * 50)
    print("API 测试服务器已启动!")
    print("=" * 50)
    print("可用的测试账号:")
    for username, info in test_accounts.items():
        print(f"  - {username} / {info['password']} ({info['name']})")
    print("=" * 50)
    print("Swagger UI: http://localhost:5001/apidocs")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5001)
