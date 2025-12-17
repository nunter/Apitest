# API 接口文档

本文档详细说明了演示服务器提供的 API 接口。

**Base URL**: `http://127.0.0.1:5001`

## 1. 用户管理

### 1.1 获取用户列表 (Get Users)

获取所有用户，支持分页和名称过滤。

- **URL**: `/users`
- **Method**: `GET`
- **Parameters**:
  - `page` (int, optional): 页码，默认为 1。
  - `limit` (int, optional): 每页数量，默认为 10。
  - `name` (string, optional): 根据用户名进行模糊搜索。

**Response Example (Success 200)**:

```json
{
  "data": [
    {
      "email": "alice@example.com",
      "id": 1,
      "name": "Alice"
    },
    {
      "email": "bob@example.com",
      "id": 2,
      "name": "Bob"
    }
  ],
  "limit": 10,
  "page": 1,
  "total": 5
}
```

### 1.2 获取单个用户 (Get User)

根据 ID 获取特定用户信息。

- **URL**: `/users/<id>`
- **Method**: `GET`

**Response Example (Success 200)**:

```json
{
  "email": "alice@example.com",
  "id": 1,
  "name": "Alice"
}
```

**Response Example (Not Found 404)**:

```json
{
  "error": "User not found"
}
```

### 1.3 创建用户 (Create User)

注册一个新用户。

- **URL**: `/users`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "name": "Charlie",
    "email": "charlie@example.com"
  }
  ```

**Response Example (Created 201)**:

```json
{
  "email": "charlie@example.com",
  "id": 6,
  "name": "Charlie"
}
```

### 1.4 更新用户 (Update User)

更新现有用户的信息。

- **URL**: `/users/<id>`
- **Method**: `PUT`
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "name": "Charlie Updated"
  }
  ```

**Response Example (Success 200)**:

```json
{
  "email": "charlie@example.com",
  "id": 6,
  "name": "Charlie Updated"
}
```

### 1.5 删除用户 (Delete User)

删除一个用户。

- **URL**: `/users/<id>`
- **Method**: `DELETE`

**Response Example (Success 200)**:

```json
{
  "message": "User deleted"
}
```

## 2. 认证与授权 (Authentication)

### 2.1 登录 (Login)

获取访问令牌（Token）。

- **URL**: `/login`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "username": "admin",
    "password": "password"
  }
  ```

**Response Example (Success 200)**:

```json
{
  "token": "fake-jwt-token-123456"
}
```

**Response Example (Unauthorized 401)**:

```json
{
  "error": "Invalid credentials"
}
```

### 2.2 受保护资源 (Protected Resource)

需要携带 Token 才能访问的接口。

- **URL**: `/protected`
- **Method**: `GET`
- **Headers**:
  - `Authorization`: `Bearer <your_token>`

**Response Example (Success 200)**:

```json
{
  "message": "Access granted to protected resource",
  "secret_data": "42"
}
```

**Response Example (Unauthorized 401)**:

```json
{
  "error": "Unauthorized"
}
```
