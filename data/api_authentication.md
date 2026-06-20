# API Authentication

All API requests require a valid Bearer Token.

Example:

Authorization: Bearer <token>

Common Errors:

401 Unauthorized:
- Invalid token
- Expired token
- Missing Authorization header

403 Forbidden:
- Insufficient permissions