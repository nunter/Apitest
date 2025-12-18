import requests
import pytest
import allure

BASE_URL = "http://localhost:5001"

# ==================== 用户管理测试 ====================

@allure.feature("用户管理")
@allure.story("获取用户列表")
@allure.severity(allure.severity_level.NORMAL)
def test_get_users_pagination():
    """测试用户列表分页功能"""
    with allure.step("请求第1页，每页2条"):
        response = requests.get(f"{BASE_URL}/users", params={"page": 1, "limit": 2})
    
    with allure.step("验证响应"):
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2
        assert data["page"] == 1
        assert data["limit"] == 2
        assert "total" in data

@allure.feature("用户管理")
@allure.story("获取用户列表")
def test_get_users_filtering():
    """测试按姓名过滤用户"""
    with allure.step("按姓名过滤 'Alice'"):
        response = requests.get(f"{BASE_URL}/users", params={"name": "Alice"})
    
    with allure.step("验证找到 Alice"):
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1
        assert data["data"][0]["name"] == "Alice"

@allure.feature("用户管理")
@allure.story("获取用户列表")
def test_get_users_filtering_chinese():
    """测试按中文姓名过滤用户"""
    with allure.step("按姓名过滤 '张三'"):
        response = requests.get(f"{BASE_URL}/users", params={"name": "张三"})
    
    with allure.step("验证找到张三"):
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1
        assert data["data"][0]["name"] == "张三"

@allure.feature("用户管理")
@allure.story("创建用户")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user():
    """测试创建新用户"""
    new_user = {
        "name": "新测试用户",
        "email": "newuser@example.com"
    }
    with allure.step("发送 POST 请求创建用户"):
        response = requests.post(f"{BASE_URL}/users", json=new_user)
    
    with allure.step("验证创建成功"):
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "新测试用户"
        assert "id" in data

@allure.feature("用户管理")
@allure.story("获取用户")
def test_get_single_user():
    """测试获取单个用户"""
    user_id = 1
    with allure.step(f"获取用户 ID {user_id}"):
        response = requests.get(f"{BASE_URL}/users/{user_id}")
    
    with allure.step("验证用户信息"):
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == "张三"  # 更新为新的测试数据
        assert data["email"] == "zhangsan@example.com"

@allure.feature("用户管理")
@allure.story("更新用户")
def test_update_user():
    """测试更新用户"""
    user_id = 2
    update_data = {"name": "李四(已更新)"}
    with allure.step(f"更新用户 {user_id}"):
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
    
    with allure.step("验证更新成功"):
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "李四(已更新)"

@allure.feature("用户管理")
@allure.story("删除用户")
def test_delete_user():
    """测试删除用户"""
    with allure.step("创建临时用户"):
        new_user = {"name": "待删除用户", "email": "delete@example.com"}
        create_resp = requests.post(f"{BASE_URL}/users", json=new_user)
        user_id = create_resp.json()["id"]
    
    with allure.step(f"删除用户 {user_id}"):
        delete_resp = requests.delete(f"{BASE_URL}/users/{user_id}")
        assert delete_resp.status_code == 200
    
    with allure.step("验证用户已删除"):
        get_resp = requests.get(f"{BASE_URL}/users/{user_id}")
        assert get_resp.status_code == 404

@allure.feature("用户管理")
@allure.story("创建用户")
def test_create_user_invalid_data():
    """测试缺少必填字段创建用户"""
    invalid_data = {"name": "缺少邮箱"}
    with allure.step("发送不完整数据"):
        response = requests.post(f"{BASE_URL}/users", json=invalid_data)
    assert response.status_code == 400

# ==================== 认证测试 ====================

@allure.feature("认证")
@allure.story("登录")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_admin_success():
    """测试管理员账号登录成功"""
    credentials = {"username": "admin", "password": "admin123"}
    with allure.step("使用 admin/admin123 登录"):
        response = requests.post(f"{BASE_URL}/login", json=credentials)
    
    with allure.step("验证登录成功"):
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "token" in data
        assert data["user"]["username"] == "admin"
        assert data["user"]["role"] == "admin"

@allure.feature("认证")
@allure.story("登录")
def test_login_test_user_success():
    """测试普通用户账号登录成功"""
    credentials = {"username": "test", "password": "test123"}
    with allure.step("使用 test/test123 登录"):
        response = requests.post(f"{BASE_URL}/login", json=credentials)
    
    with allure.step("验证登录成功"):
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["user"]["role"] == "user"

@allure.feature("认证")
@allure.story("登录")
def test_login_vip_user_success():
    """测试VIP用户账号登录成功"""
    credentials = {"username": "vip", "password": "vip888"}
    with allure.step("使用 vip/vip888 登录"):
        response = requests.post(f"{BASE_URL}/login", json=credentials)
    
    with allure.step("验证登录成功"):
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["user"]["role"] == "vip"

@allure.feature("认证")
@allure.story("登录")
def test_login_failure_wrong_password():
    """测试密码错误登录失败"""
    credentials = {"username": "admin", "password": "wrongpassword"}
    with allure.step("使用错误密码登录"):
        response = requests.post(f"{BASE_URL}/login", json=credentials)
    
    with allure.step("验证登录失败"):
        assert response.status_code == 401
        assert response.json()["success"] == False

@allure.feature("认证")
@allure.story("登录")
def test_login_failure_user_not_exist():
    """测试用户不存在登录失败"""
    credentials = {"username": "nonexistent", "password": "123456"}
    with allure.step("使用不存在的用户登录"):
        response = requests.post(f"{BASE_URL}/login", json=credentials)
    
    with allure.step("验证登录失败"):
        assert response.status_code == 401

@allure.feature("认证")
@allure.story("受保护资源")
def test_protected_endpoint_success():
    """测试使用有效 token 访问受保护资源"""
    with allure.step("登录获取 token"):
        login_resp = requests.post(f"{BASE_URL}/login", json={"username": "admin", "password": "admin123"})
        token = login_resp.json()["token"]
    
    with allure.step("使用 token 访问受保护资源"):
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/protected", headers=headers)
    
    with allure.step("验证访问成功"):
        assert response.status_code == 200
        assert "secret_data" in response.json()

@allure.feature("认证")
@allure.story("受保护资源")
def test_protected_endpoint_unauthorized():
    """测试无 token 访问受保护资源"""
    with allure.step("不带 token 访问受保护资源"):
        response = requests.get(f"{BASE_URL}/protected")
    assert response.status_code == 401

@allure.feature("认证")
@allure.story("受保护资源")
def test_protected_endpoint_invalid_token():
    """测试使用无效 token 访问受保护资源"""
    with allure.step("使用无效 token 访问"):
        headers = {"Authorization": "Bearer invalid_token_123"}
        response = requests.get(f"{BASE_URL}/protected", headers=headers)
    assert response.status_code == 401

# ==================== 商品管理测试 ====================

@allure.feature("商品管理")
@allure.story("获取商品列表")
def test_get_products():
    """测试获取商品列表"""
    with allure.step("请求商品列表"):
        response = requests.get(f"{BASE_URL}/products")
    
    with allure.step("验证响应"):
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0
        assert "total" in data

@allure.feature("商品管理")
@allure.story("获取商品列表")
def test_get_products_by_category():
    """测试按分类过滤商品"""
    with allure.step("获取手机分类商品"):
        response = requests.get(f"{BASE_URL}/products", params={"category": "手机"})
    
    with allure.step("验证结果"):
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) >= 1
        for product in data["data"]:
            assert product["category"] == "手机"

@allure.feature("商品管理")
@allure.story("获取商品列表")
def test_get_products_by_status():
    """测试按状态过滤商品"""
    with allure.step("获取在售商品"):
        response = requests.get(f"{BASE_URL}/products", params={"status": "on_sale"})
    
    with allure.step("验证结果"):
        assert response.status_code == 200
        data = response.json()
        for product in data["data"]:
            assert product["status"] == "on_sale"

@allure.feature("商品管理")
@allure.story("获取商品")
def test_get_single_product():
    """测试获取单个商品"""
    product_id = 1
    with allure.step(f"获取商品 ID {product_id}"):
        response = requests.get(f"{BASE_URL}/products/{product_id}")
    
    with allure.step("验证商品信息"):
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == "iPhone 15 Pro"
        assert data["price"] == 8999.00

@allure.feature("商品管理")
@allure.story("获取商品")
def test_get_product_not_found():
    """测试获取不存在的商品"""
    with allure.step("获取不存在的商品"):
        response = requests.get(f"{BASE_URL}/products/9999")
    assert response.status_code == 404

# ==================== 订单管理测试 ====================

@allure.feature("订单管理")
@allure.story("获取订单列表")
def test_get_orders():
    """测试获取订单列表"""
    with allure.step("请求订单列表"):
        response = requests.get(f"{BASE_URL}/orders")
    
    with allure.step("验证响应"):
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) > 0

@allure.feature("订单管理")
@allure.story("获取订单列表")
def test_get_orders_by_user():
    """测试按用户ID过滤订单"""
    with allure.step("获取用户1的订单"):
        response = requests.get(f"{BASE_URL}/orders", params={"user_id": 1})
    
    with allure.step("验证结果"):
        assert response.status_code == 200
        data = response.json()
        for order in data["data"]:
            assert order["user_id"] == 1

@allure.feature("订单管理")
@allure.story("获取订单列表")
def test_get_orders_by_status():
    """测试按状态过滤订单"""
    with allure.step("获取已完成订单"):
        response = requests.get(f"{BASE_URL}/orders", params={"status": "completed"})
    
    with allure.step("验证结果"):
        assert response.status_code == 200
        data = response.json()
        for order in data["data"]:
            assert order["status"] == "completed"

@allure.feature("订单管理")
@allure.story("获取订单")
def test_get_single_order():
    """测试获取单个订单"""
    order_id = "ORD20231201001"
    with allure.step(f"获取订单 {order_id}"):
        response = requests.get(f"{BASE_URL}/orders/{order_id}")
    
    with allure.step("验证订单信息"):
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == order_id
        assert data["status"] == "completed"

@allure.feature("订单管理")
@allure.story("创建订单")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_order():
    """测试创建订单"""
    order_data = {
        "user_id": 1,
        "product_id": 1,
        "quantity": 2
    }
    with allure.step("创建新订单"):
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
    
    with allure.step("验证订单创建成功"):
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == 1
        assert data["product_id"] == 1
        assert data["quantity"] == 2
        assert data["total"] == 8999.00 * 2
        assert data["status"] == "pending"
        assert "id" in data

@allure.feature("订单管理")
@allure.story("创建订单")
def test_create_order_invalid_product():
    """测试创建订单 - 商品不存在"""
    order_data = {
        "user_id": 1,
        "product_id": 9999,
        "quantity": 1
    }
    with allure.step("使用不存在的商品创建订单"):
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
    
    with allure.step("验证创建失败"):
        assert response.status_code == 400

# ==================== 测试辅助接口测试 ====================

@allure.feature("测试辅助")
@allure.story("获取测试账号")
def test_get_test_accounts():
    """测试获取所有测试账号信息"""
    with allure.step("请求测试账号列表"):
        response = requests.get(f"{BASE_URL}/test/accounts")
    
    with allure.step("验证响应"):
        assert response.status_code == 200
        data = response.json()
        assert "accounts" in data
        assert len(data["accounts"]) >= 5
        
        # 验证包含预期的账号
        usernames = [acc["username"] for acc in data["accounts"]]
        assert "admin" in usernames
        assert "test" in usernames
        assert "vip" in usernames

@allure.feature("测试辅助")
@allure.story("重置数据")
def test_reset_data():
    """测试重置数据功能"""
    with allure.step("重置所有数据"):
        response = requests.post(f"{BASE_URL}/test/reset")
    
    with allure.step("验证重置成功"):
        assert response.status_code == 200
        assert "message" in response.json()

# ==================== 端到端流程测试 ====================

@allure.feature("端到端测试")
@allure.story("完整购物流程")
@allure.severity(allure.severity_level.CRITICAL)
def test_e2e_shopping_flow():
    """端到端测试：完整购物流程"""
    # 1. 登录
    with allure.step("步骤1: 用户登录"):
        login_resp = requests.post(f"{BASE_URL}/login", json={"username": "user1", "password": "123456"})
        assert login_resp.status_code == 200
        token = login_resp.json()["token"]
        allure.attach(token, "登录Token", allure.attachment_type.TEXT)
    
    # 2. 浏览商品
    with allure.step("步骤2: 浏览手机商品"):
        products_resp = requests.get(f"{BASE_URL}/products", params={"category": "手机"})
        assert products_resp.status_code == 200
        products = products_resp.json()["data"]
        assert len(products) > 0
        selected_product = products[0]
        allure.attach(str(selected_product), "选中商品", allure.attachment_type.TEXT)
    
    # 3. 查看商品详情
    with allure.step("步骤3: 查看商品详情"):
        detail_resp = requests.get(f"{BASE_URL}/products/{selected_product['id']}")
        assert detail_resp.status_code == 200
    
    # 4. 创建订单
    with allure.step("步骤4: 创建订单"):
        order_data = {
            "user_id": 1,
            "product_id": selected_product["id"],
            "quantity": 1
        }
        order_resp = requests.post(f"{BASE_URL}/orders", json=order_data)
        assert order_resp.status_code == 201
        order = order_resp.json()
        allure.attach(str(order), "创建的订单", allure.attachment_type.TEXT)
    
    # 5. 查看订单
    with allure.step("步骤5: 查看订单详情"):
        order_detail_resp = requests.get(f"{BASE_URL}/orders/{order['id']}")
        assert order_detail_resp.status_code == 200
        assert order_detail_resp.json()["status"] == "pending"

@allure.feature("端到端测试")
@allure.story("多账号登录测试")
def test_e2e_multiple_accounts():
    """端到端测试：验证所有测试账号都能正常登录"""
    test_accounts = [
        {"username": "admin", "password": "admin123", "expected_role": "admin"},
        {"username": "test", "password": "test123", "expected_role": "user"},
        {"username": "user1", "password": "123456", "expected_role": "user"},
        {"username": "user2", "password": "password", "expected_role": "user"},
        {"username": "vip", "password": "vip888", "expected_role": "vip"},
    ]
    
    for account in test_accounts:
        with allure.step(f"测试账号: {account['username']}"):
            response = requests.post(f"{BASE_URL}/login", json={
                "username": account["username"],
                "password": account["password"]
            })
            assert response.status_code == 200, f"账号 {account['username']} 登录失败"
            data = response.json()
            assert data["user"]["role"] == account["expected_role"], f"账号 {account['username']} 角色不匹配"
