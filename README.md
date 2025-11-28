# 🛍️ Shop Management System

Dự án này là một hệ thống quản lý cửa hàng (Shop Management System), được xây dựng để cung cấp các API cho việc quản lý sản phẩm và khách hàng.

## 🌟 Tổng quan về Công nghệ

Dự án sử dụng ngăn xếp công nghệ phổ biến cho Backend:

* **Runtime:** Node.js
* **Framework:** Express.js
* **Database ORM:** Sequelize (cho phép tương tác với database như PostgreSQL/MySQL/SQLite).
* **Authentication:** Sử dụng Middleware để xác thực.

## 🚀 Các Tính năng Chính

* **Quản lý Sản phẩm (Product Management):** CRUD (Tạo, Đọc, Cập nhật, Xóa) sản phẩm.
* **Quản lý Khách hàng (Customer Management):** CRUD (Tạo, Đọc, Cập nhật, Xóa) thông tin khách hàng.
* **Chức năng Tìm kiếm (Search):** Tìm kiếm sản phẩm và khách hàng đồng thời dựa trên tên (như đã thấy trong file `search.js`).
* **Xác thực API (Authentication):** Bảo vệ các routes bằng middleware xác thực.

## ⚙️ Cài đặt và Khởi chạy

Để chạy dự án này trên môi trường cục bộ, hãy làm theo các bước sau:

### 1. Yêu cầu

Đảm bảo bạn đã cài đặt các công cụ sau:

* Node.js (phiên bản khuyến nghị).
* npm (đi kèm với Node.js).
* Một hệ quản trị cơ sở dữ liệu (ví dụ: PostgreSQL hoặc MySQL).

### 2. Thiết lập dự án

1.  **Clone Repository:**
    ```bash
    git clone <URL_CỦA_REPO_CỦA_BẠN>
    cd ShopManagement
    ```

2.  **Cài đặt các gói phụ thuộc:**
    ```bash
    npm install
    ```

3.  **Cấu hình Môi trường (.env):**
    Tạo một file có tên `.env` trong thư mục gốc và cung cấp thông tin kết nối cơ sở dữ liệu và các biến bí mật khác (ví dụ: `JWT_SECRET`, `DB_CONNECTION_STRING`, v.v.).

    ```ini
    # VÍ DỤ CẤU HÌNH DATABASE CHO SEQUELIZE
    DB_DIALECT=mysql
    DB_HOST=localhost
    DB_USER=your_db_user
    DB_PASS=your_db_password
    DB_NAME=shopmanagement
    PORT=3000
    ```

4.  **Chạy Migrations và Seeding (Nếu có):**
    Nếu bạn sử dụng các lệnh của Sequelize CLI, hãy chạy chúng để thiết lập database.
    ```bash
    # Ví dụ:
    npx sequelize db:migrate
    ```

### 3. Khởi động Server

Chạy lệnh sau để khởi động ứng dụng:

```bash
npm start
# Hoặc node server.js/app.js tùy thuộc vào cấu hình của bạn