# Documentation
# Django Backend API Documentation

This document provides a comprehensive overview of the Django backend APIs for your project. It includes details about available endpoints, request types, required parameters, responses, and authentication methods. This will assist frontend developers in understanding how to interact with the backend effectively.

## Table of Contents

- [General Information](#general-information)
- [Authentication Endpoints](#authentication-endpoints)
  - [Login User](#1-login-user)
  - [Register User](#2-register-user)
  - [Change Password](#3-change-password)
  - [Forgot Password](#4-forgot-password)
  - [Check OTP](#5-check-otp)
  - [Verify Mail](#6-verify-mail)
  - [Create New Verification Message](#7-create-new-verification-message)
- [Store Endpoints](#store-endpoints)
  - [Show Categories](#1-show-categories)
  - [Show Products](#2-show-products)
  - [Add to Cart](#3-add-to-cart)
  - [Remove from Cart](#4-remove-from-cart)
  - [Show Cart](#5-show-cart)
  - [Change Quantity](#6-change-quantity)
  - [Checkout](#7-checkout)
  - [Place Order](#8-place-order)
- [Authentication Details](#authentication-details)
- [Error Handling](#error-handling)

---

## General Information

- **Base URL:** `/` (All endpoints are relative to the base URL)
- **Authentication:** JSON Web Tokens (JWT) are used for authenticated endpoints.
- **Content Type:** All requests and responses use `application/json`.
- **CSRF Protection:** Disabled for API endpoints using `@csrf_exempt`.

---

## Authentication Endpoints

### 1. Login User

- **URL:** `/authentication/login_user`
- **Method:** `POST`
- **Description:** Authenticates a user and returns an access token.

#### Request Parameters

| Parameter | Type   | Description      | Required |
|-----------|--------|------------------|----------|
| uname     | string | Username         | Yes      |
| password  | string | User's password  | Yes      |

#### Request Example

```json
{
  "uname": "john_doe",
  "password": "securePassword123"
}
```

#### Response

- **Success (200 OK):**

  ```json
  {
    "access": "jwt_access_token_string"
  }
  ```

- **Failure (400 Bad Request):**

  ```json
  {
    "mssg": "Incorrect Credentials",
    "status": 0
  }
  ```

---

### 2. Register User

- **URL:** `/authentication/register_user`
- **Method:** `POST`
- **Description:** Registers a new user and sends an email verification link.

#### Request Parameters

| Parameter   | Type    | Description                  | Required |
|-------------|---------|------------------------------|----------|
| uname        | string  | Desired username             | Yes      |
| password1    | string  | Password                     | Yes      |
| password2    | string  | Password confirmation        | Yes      |
| name         | string  | Full name                    | Yes      |
| age          | integer | Age                          | Yes      |
| mobile       | string  | Mobile number                | Yes      |
| email        | string  | Email address                | Yes      |
| city         | string  | City                         | Yes      |
| state        | string  | State                        | Yes      |
| pin          | string  | PIN code                     | Yes      |
| address      | string  | Residential address          | Yes      |
| company      | string  | Company name (optional)      | No       |

#### Request Example

```json
{
  "uname": "john_doe",
  "password1": "securePassword123",
  "password2": "securePassword123",
  "name": "John Doe",
  "age": 30,
  "mobile": "1234567890",
  "email": "john@example.com",
  "city": "New York",
  "state": "NY",
  "pin": "10001",
  "address": "123 Main St",
  "company": "OpenAI"
}
```

#### Response

- **Success (201 Created):**

  ```json
  {
    "mssg": "Profile created Successfully...",
    "status": true,
    "access_token": "jwt_access_token_string"
  }
  ```

- **Failure (400 Bad Request):**

  - Passwords do not match:

    ```json
    {
      "mssg": "Passwords Don't Match ... Try Again",
      "status": false
    }
    ```

  - Username already taken:

    ```json
    {
      "mssg": "Try a different username... 'john_doe' is already taken",
      "status": false
    }
    ```

---

### 3. Change Password

- **URL:** `/authentication/change_password`
- **Method:** `POST`
- **Description:** Allows authenticated users to change their password.

#### Headers

| Header            | Description                     | Required |
|-------------------|---------------------------------|----------|
| Authorization     | `Bearer <access_token>`         | Yes      |

#### Request Parameters

| Parameter      | Type   | Description         | Required |
|----------------|--------|---------------------|----------|
| old_password   | string | Current password    | Yes      |
| new_password   | string | New desired password| Yes      |

#### Request Example

```json
{
  "old_password": "oldPassword123",
  "new_password": "newSecurePassword456"
}
```

#### Response

- **Success (201 Created):**

  ```json
  {
    "status": true,
    "message": "Password Changed Successfully....",
    "new_access_token": "new_jwt_access_token_string"
  }
  ```

- **Failure (406 Not Acceptable):**

  ```json
  {
    "status": false,
    "message": "Incorrect Previous Password.."
  }
  ```

---

### 4. Forgot Password

- **URL:** `/authentication/forgot_password`
- **Method:** `POST`
- **Description:** Initiates the password reset process by sending an OTP to the user's email.

#### Request Parameters

| Parameter      | Type   | Description          | Required |
|----------------|--------|----------------------|----------|
| email_of_user  | string | User's registered email | Yes      |

#### Request Example

```json
{
  "email_of_user": "john@example.com"
}
```

#### Response

- **Success (200 OK):**

  ```json
  {
    "otp": "123456",
    "token": "encrypted_token_string"
  }
  ```

- **Failure (404 Not Found):**

  ```json
  {
    "mssg": "error finding user.."
  }
  ```

---

### 5. Check OTP

- **URL:** `/authentication/check_otp`
- **Method:** `POST`
- **Description:** Verifies the OTP sent to the user's email and returns a new access token if valid.

#### Request Parameters

| Parameter | Type   | Description        | Required |
|-----------|--------|--------------------|----------|
| otp       | string | One-Time Password  | Yes      |
| token     | string | Encrypted token    | Yes      |

#### Request Example

```json
{
  "otp": "123456",
  "token": "encrypted_token_string"
}
```

#### Response

- **Success (200 OK):**

  ```json
  {
    "access_token": "jwt_access_token_string",
    "status": true
  }
  ```

- **Failure (400 Bad Request):**

  - OTP mismatch:

    ```json
    {
      "message": "OTP didn't match...."
    }
    ```

  - OTP expired:

    ```json
    {
      "message": "OTP expired...Try Again!!",
      "status": false
    }
    ```

---

### 6. Verify Mail

- **URL:** `/authentication/verify_mail`
- **Method:** `POST`
- **Description:** Verifies the user's email address using the token sent via email.

#### Request Parameters

| Parameter | Type   | Description     | Required |
|-----------|--------|-----------------|----------|
| token     | string | Encrypted token | Yes      |

#### Request Example

```json
{
  "token": "encrypted_token_string"
}
```

#### Response

- **Success (Redirect to Success Page):**

  Redirects to `https://ettarracoffee.in/`

- **Failure (Redirect to Expired Link Page):**

  Redirects to a specified URL indicating the verification link has expired.

---

### 7. Create New Verification Message

- **URL:** `/authentication/create_new_verification_message`
- **Method:** `POST`
- **Description:** Sends a new email verification link to the authenticated user.

#### Headers

| Header            | Description                     | Required |
|-------------------|---------------------------------|----------|
| Authorization     | `Bearer <access_token>`         | Yes      |

#### Request Parameters

_None_

#### Request Example

```json
{}
```

#### Response

- **Success (200 OK):**

  ```json
  {
    "status": true,
    "mssg": "Verification Link Sent to john@example.com"
  }
  ```

---

## Store Endpoints

### 1. Show Categories

- **URL:** `/store/show_categories`
- **Method:** `POST`
- **Description:** Retrieves a list of all product categories.

#### Request Parameters

_None_

#### Request Example

```json
{}
```

#### Response

- **Success (200 OK):**

  ```json
  {
    "categories": [
      {
        "id": 1,
        "name": "Beverages"
      },
      {
        "id": 2,
        "name": "Snacks"
      }
      // ... more categories
    ]
  }
  ```

---

### 2. Show Products

- **URL:** `/store/show_products`
- **Method:** `POST`
- **Description:** Retrieves a list of products. If the user is authenticated and provides activity data, it returns recommended products based on user activity.

#### Headers

| Header            | Description                     | Required |
|-------------------|---------------------------------|----------|
| Authorization     | `Bearer <access_token>`         | Optional (for recommendations) |

#### Request Parameters

- **For Recommendations:**

  | Parameter | Type   | Description               | Required |
  |-----------|--------|---------------------------|----------|
  | activity  | array  | List of user activity IDs | No       |

- **Without Recommendations:**

  _No parameters_

#### Request Example

- **With Recommendations:**

  ```json
  {
    "activity": [101, 102, 103]
  }
  ```

- **Without Recommendations:**

  ```json
  {}
  ```

#### Response

- **Success (200 OK):**

  - **With Recommendations:**

    ```json
    {
      "data": [
        {
          "id": 201,
          "name": "Espresso",
          "price": 3.99,
          "description": "Strong coffee shot."
        },
        // ... more recommended products
      ]
    }
    ```

  - **Without Recommendations:**

    ```json
    {
      "data": [
        {
          "id": 101,
          "name": "Latte",
          "price": 4.99,
          "description": "Milk-based coffee."
        },
        // ... more products
      ]
    }
    ```

---

### 3. Add to Cart

- **URL:** `/store/add_to_cart`
- **Method:** `POST`
- **Description:** Adds a product to the authenticated user's cart.

#### Headers

| Header            | Description                     | Required |
|-------------------|---------------------------------|----------|
| Authorization     | `Bearer <access_token>`         | Yes      |
| Content-Type      | `application/json`              | Yes      |

#### Request Parameters

| Parameter  | Type   | Description      | Required |
|------------|--------|------------------|----------|
| product_id | integer| ID of the product| Yes      |
| quantity   | integer| Quantity to add  | Yes      |

#### Request Example

```json
{
  "product_id": 101,
  "quantity": 2
}
```

#### Response

- **Success (200 OK):**

  - **If Product Added:**

    ```json
    {
      "mssg": "Product Latte added to cart..with quantity=2",
      "status": 1
    }
    ```

  - **If Product Already in Cart:**

    ```json
    {
      "mssg": "Product Already In Cart...",
      "status": 0
    }
    ```

---

### 4. Remove from Cart

- **URL:** `/store/remove_from_cart`
- **Method:** `POST`
- **Description:** Removes a product from the authenticated user's cart.

#### Headers

| Header            | Description                     | Required |
|-------------------|---------------------------------|----------|
| Authorization     | `Bearer <access_token>`         | Yes      |
| Content-Type      | `application/json`              | Yes      |

#### Request Parameters

| Parameter  | Type    | Description       | Required |
|------------|---------|-------------------|----------|
| product_id | integer | ID of the product | Yes      |

#### Request Example

```json
{
  "product_id": 101
}
```

#### Response

- **Success (200 OK):**

  ```json
  {
    "mssg": "Latte Removed from Cart"
  }
  ```

- **Failure (404 Not Found):**

  ```json
  {
    "mssg": "error finding product in cart.."
  }
  ```

---

### 5. Show Cart

- **URL:** `/store/show_cart`
- **Method:** `POST`
- **Description:** Retrieves the contents of the authenticated user's cart.

#### Headers

| Header            | Description                     | Required |
|-------------------|---------------------------------|----------|
| Authorization     | `Bearer <access_token>`         | Yes      |
| Content-Type      | `application/json`              | Yes      |

#### Request Parameters

_None_

#### Request Example

```json
{}
```

#### Response

- **Success (200 OK):**

  ```json
  {
    "quantity": 3,
    "data": [
      {
        "id": 1,
        "product": {
          "id": 101,
          "name": "Latte",
          "price": 4.99
        },
        "quantity": 2,
        "total_price": 9.98
      },
      {
        "id": 2,
        "product": {
          "id": 102,
          "name": "Espresso",
          "price": 3.99
        },
        "quantity": 1,
        "total_price": 3.99
      }
    ],
    "status": true
  }
  ```

- **Failure (200 OK):**

  ```json
  {
    "status": false,
    "mssg": "No items in Cart.."
  }
  ```

---

### 6. Change Quantity

- **URL:** `/store/change_quantity`
- **Method:** `POST`
- **Description:** Changes the quantity of a specific product in the authenticated user's cart.

#### Headers

| Header            | Description                     | Required |
|-------------------|---------------------------------|----------|
| Authorization     | `Bearer <access_token>`         | Yes      |
| Content-Type      | `application/json`              | Yes      |

#### Request Parameters

| Parameter        | Type    | Description                 | Required |
|------------------|---------|-----------------------------|----------|
| type             | string  | Type of change (`reduce` or `increase`) | Yes      |
| quantity         | integer | Quantity to change by      | Yes      |
| product_id       | integer | ID of the product           | Yes      |

#### Request Example

- **Increase Quantity:**

  ```json
  {
    "type": "increase",
    "quantity": 1,
    "product_id": 101
  }
  ```

- **Reduce Quantity:**

  ```json
  {
    "type": "reduce",
    "quantity": 1,
    "product_id": 101
  }
  ```

#### Response

- **Success (200 OK):**

  ```json
  {
    "mssg": "Quantity changed for Latte",
    "status": true
  }
  ```

- **Failure (200 OK):**

  ```json
  {
    "mssg": "Only 5 Latte left in stock..",
    "status": false
  }
  ```

---

### 7. Checkout

- **URL:** `/store/checkout`
- **Method:** `POST`
- **Description:** Retrieves the checkout details for the authenticated user's cart, including total price and quantity.

#### Headers

| Header            | Description                     | Required |
|-------------------|---------------------------------|----------|
| Authorization     | `Bearer <access_token>`         | Yes      |
| Content-Type      | `application/json`              | Yes      |

#### Request Parameters

_None_

#### Request Example

```json
{}
```

#### Response

- **Success (200 OK):**

  ```json
  {
    "data": [
      {
        "id": 1,
        "product": {
          "id": 101,
          "name": "Latte",
          "price": 4.99
        },
        "quantity": 2,
        "total_price": 9.98
      },
      {
        "id": 2,
        "product": {
          "id": 102,
          "name": "Espresso",
          "price": 3.99
        },
        "quantity": 1,
        "total_price": 3.99
      }
    ],
    "total_price": 13.97,
    "total_quantity": 3
  }
  ```

---

### 8. Place Order

- **URL:** `/store/place_order`
- **Method:** `POST`
- **Description:** Places an order for the authenticated user based on the current cart contents.

#### Headers

| Header            | Description                     | Required |
|-------------------|---------------------------------|----------|
| Authorization     | `Bearer <access_token>`         | Yes      |
| Content-Type      | `application/json`              | Yes      |

#### Request Parameters

| Parameter        | Type    | Description           | Required |
|------------------|---------|-----------------------|----------|
| shipping_address | string  | Shipping address      | Yes      |
| city             | string  | City                  | Yes      |
| state            | string  | State                 | Yes      |
| pincode          | string  | PIN code              | Yes      |
| phone_number     | string  | Contact phone number  | Yes      |
| email            | string  | Contact email address | Yes      |
| payment_mode     | string  | Payment method        | Yes      |

#### Request Example

```json
{
  "shipping_address": "123 Main St",
  "city": "New York",
  "state": "NY",
  "pincode": "10001",
  "phone_number": "1234567890",
  "email": "john@example.com",
  "payment_mode": "Credit Card"
}
```

#### Response

- **Success (201 Created):**

  ```json
  {
    "mssg": "Order Placed successfully!!",
    "order_id": 5001
  }
  ```

---

## Authentication Details

### JSON Web Tokens (JWT)

- **Access Token:** Used to authenticate requests to protected endpoints.
- **Token Acquisition:** Obtained via the `/authentication/login_user` or `/authentication/register_user` endpoints.
- **Token Refresh:** Automatically handled when changing passwords or upon expiration.

### Authorization Header

For authenticated endpoints, include the JWT in the `Authorization` header as follows:

```
Authorization: Bearer <access_token>
```

### Example

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJI...
```

---

## Error Handling

All error responses include appropriate HTTP status codes and descriptive messages to help identify issues.

- **400 Bad Request:** Invalid input or request parameters.
- **401 Unauthorized:** Missing or invalid authentication token.
- **403 Forbidden:** Insufficient permissions.
- **404 Not Found:** Resource not found.
- **406 Not Acceptable:** Validation errors (e.g., incorrect password).
- **500 Internal Server Error:** Unexpected server errors.

### Example Error Response

```json
{
  "mssg": "Incorrect Credentials",
  "status": 0
}
```

---

## Additional Notes

- **Email Verification:** After registration, users receive an email verification link. Clicking the link redirects them to the frontend application indicating successful verification.
- **CSRF Protection:** Disabled for all API endpoints using `@csrf_exempt`. Ensure that other security measures are in place.
- **Data Validation:** The backend performs basic validation. Frontend should also implement client-side validation for better user experience.
- **Rate Limiting:** Not implemented. Consider adding rate limiting to protect against abuse.

---

Feel free to reach out if you have any questions or need further clarification on the API endpoints.
