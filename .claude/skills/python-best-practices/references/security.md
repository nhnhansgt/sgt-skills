# Python Security Best Practices (OWASP Top 10)

## SQL Injection Prevention

### Vulnerable Code
```python
# BAD - Direct string concatenation
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# BAD - String formatting
query = "SELECT * FROM users WHERE id = %s" % user_id
cursor.execute(query)
```

### Secure Code
```python
# GOOD - Parameterized queries
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))

# GOOD - With SQLAlchemy
User.query.filter_by(id=user_id).first()
```

## Command Injection Prevention

### Vulnerable Code
```python
# BAD - Direct OS command execution
os.system(f"tar -czf {filename} archive.tar.gz")
subprocess.call(f"ls {directory}", shell=True)
```

### Secure Code
```python
# GOOD - Use subprocess without shell
subprocess.call(["tar", "-czf", filename, "archive.tar.gz"])
subprocess.call(["ls", directory])

# GOOD - Use shlex.quote if shell is required
import shlex
safe_arg = shlex.quote(user_input)
subprocess.call(f"ls {safe_arg}", shell=True)
```

## Input Validation & Sanitization

```python
from typing import Any
import re

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Sanitize user input."""
    # Strip whitespace
    text = text.strip()
    # Truncate to max length
    text = text[:max_length]
    # Remove null bytes
    text = text.replace('\x00', '')
    return text
```

## Sensitive Data Protection

### Avoid Hardcoded Credentials
```python
# BAD - Hardcoded secrets
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "password123"

# GOOD - Use environment variables
import os
API_KEY = os.getenv("API_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# GOOD - Use python-dotenv
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
```

### Secure Password Storage
```python
import bcrypt

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed.encode('utf-8')
    )
```

### Never Log Sensitive Data
```python
import logging

# BAD
logging.info(f"User login: {username}, {password}")

# GOOD - Redact sensitive data
logging.info(f"User login: {username}")
# Or use custom filter to redact
```

## Safe Deserialization

### Vulnerable Code
```python
# BAD - pickle with untrusted data
import pickle
data = pickle.loads(untrusted_data)
```

### Secure Alternative
```python
# GOOD - Use JSON for simple data
import json
data = json.loads(untrusted_data)

# GOOD - Use hmac for signature verification
import hmac
import json

def serialize(data: dict, secret: str) -> str:
    json_data = json.dumps(data)
    signature = hmac.new(
        secret.encode(),
        json_data.encode(),
        'sha256'
    ).hexdigest()
    return f"{json_data}.{signature}"

def deserialize(data: str, secret: str) -> dict:
    json_data, signature = data.rsplit('.', 1)
    expected_sig = hmac.new(
        secret.encode(),
        json_data.encode(),
        'sha256'
    ).hexdigest()
    if not hmac.compare_digest(signature, expected_sig):
        raise ValueError("Invalid signature")
    return json.loads(json_data)
```

## HTTPS Only in Production

```python
import ssl

# Configure SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

# For Flask
if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Development
    # Production: Use proper SSL certificates
```

## Dependency Management

### Regular Security Audits
```bash
# Check for vulnerabilities
pip-audit
pip check

# With poetry
poetry check
poetry show --outdated
```

### requirements.txt with pinned versions
```txt
# Good practice
requests==2.31.0
flask==3.0.0
# Not just:
# requests>=2.28.0
```

## Common Security Mistakes

| Mistake | Risk | Solution |
|---------|------|----------|
| Hardcoded secrets | Credential exposure | Environment variables |
| `eval()` on user input | Code execution | Avoid, use `ast.literal_eval()` |
| `pickle` untrusted data | RCE | Use JSON or messagepack |
| SQL string concat | SQL injection | Parameterized queries |
| Shell=True with user input | Command injection | List arguments, no shell |
| Logging passwords | Credential leakage | Redact sensitive data |

## Reference
- [Python Security Best Practices Guide](https://corgea.com/Learn/python-security-best-practices-a-comprehensive-guide-for-engineers)
- [Python and OWASP Top 10](https://qwiet.ai/appsec-resources/python-and-owasp-top-10-a-developers-guide/)
- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
