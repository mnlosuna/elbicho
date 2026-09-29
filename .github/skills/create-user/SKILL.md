---
name: create-user
description: Create a user through the local FastAPI API using HTTP POST.
---

# Create User

When the user asks to create or register a user, use the HTTP Request capability.

Send a POST request to:

http://IP_LOCAL_DEL_MAC:8000/users/

Use this header:

Content-Type: application/json

Use this JSON body:

{
  "username": "usuario_demo",
  "email": "usuario_demo@example.com",
  "first_name": "Usuario",
  "last_name": "Demo",
  "phone": "555123456",
  "password": "secreto123"
}

Replace IP_LOCAL_DEL_MAC with the real local IP address of the computer.

Expected success response: HTTP 201 Created.