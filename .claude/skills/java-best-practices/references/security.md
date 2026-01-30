# Security Best Practices

## Input Validation

```java
// Always validate and sanitize user input
public void setEmail(String email) {
    if (email == null || email.isBlank()) {
        throw new IllegalArgumentException("Email required");
    }
    if (!email.matches("^[A-Za-z0-9+_.-]+@(.+)$")) {
        throw new IllegalArgumentException("Invalid email format");
    }
    this.email = email;
}

// Use bean validation annotations
public class User {
    @NotNull
    @Email
    @Size(max = 100)
    private String email;
    
    @Pattern(regexp = "^[A-Za-z0-9]{8,30}$")
    private String password;
}
```

## Password Handling

```java
// NEVER store plain text passwords
// Bad
public void setPassword(String password) {
    this.password = password;  // NEVER!
}

// Good: Use bcrypt/Argon2/SCrypt
private final PasswordEncoder encoder = new BCryptPasswordEncoder();

public void setPassword(String plainPassword) {
    this.passwordHash = encoder.encode(plainPassword);
}

public boolean checkPassword(String plainPassword) {
    return encoder.matches(plainPassword, this.passwordHash);
}
```

## SQL Injection Prevention

```java
// Bad: String concatenation
String query = "SELECT * FROM users WHERE id = " + userId;  // DANGER!

// Bad: String.format
String query = String.format("SELECT * FROM users WHERE name = '%s'", name);

// Good: Prepared statements with parameterized queries
String sql = "SELECT * FROM users WHERE id = ?";
try (PreparedStatement ps = conn.prepareStatement(sql)) {
    ps.setLong(1, userId);
    ResultSet rs = ps.executeQuery();
}
```

## XSS Prevention

```java
// Always encode user-generated content for HTML output
String safe = StringEscapeUtils.escapeHtml4(userInput);

// In Spring, automatic with @ResponseBody and proper templates
// For JSP/JSTL: <c:out value="${userInput}" />
```

## Path Traversal Prevention

```java
// Bad: User input directly in file path
String path = "/app/files/" + filename;  // Could be "../../etc/passwd"

// Good: Normalize and validate
String safePath = Paths.get("/app/files", filename)
    .normalize()
    .toAbsolutePath();
if (!safePath.startsWith("/app/files/")) {
    throw new SecurityException("Invalid path");
}
```

## Secrets Management

```java
// NEVER hardcode secrets
// Bad
private static final String API_KEY = "sk_live_12345...";  // NEVER!

// Good: Environment variables
private static final String API_KEY = System.getenv("API_KEY");

// Better: Use secrets management (HashiCorp Vault, AWS Secrets Manager)
@Value("${api.key}")
private String apiKey;

// Or Spring Cloud Config
@Value("${spring.datasource.password}")
private String dbPassword;
```

## HTTPS & TLS

```java
// Always use HTTPS, disable HTTP
server.ssl.enabled=true
server.ssl.key-store=classpath:keystore.p12
server.ssl.key-store-password=${SSL_PASSWORD}
server.ssl.key-store-type=PKCS12

// Enable HSTS (HTTP Strict Transport Security)
server.headers.hsts.enabled=true
server.headers.hsts.max-age=31536000
```

## Authentication & Authorization

```java
// Use established frameworks (Spring Security, Apache Shiro)
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(auth -> auth
            .requestMatchers("/admin/**").hasRole("ADMIN")
            .requestMatchers("/api/**").authenticated()
            .anyRequest().permitAll()
        );
        return http.build();
    }
}

// Method-level security
@PreAuthorize("hasRole('ADMIN')")
public void deleteUser(Long id) { }
```

## Secure Random

```java
// Use SecureRandom for security-sensitive operations
SecureRandom secureRandom = SecureRandom.getInstanceStrong();
byte[] token = new byte[32];
secureRandom.nextBytes(token);

// Generate session tokens, CSRF tokens, API keys
String csrfToken = new BigInteger(130, secureRandom).toString(32);
```

## Sensitive Data Logging

```java
// Bad: Logging sensitive data
log.info("User login: username={}, password={}", username, password);

// Good: Mask sensitive data
log.info("User login: username={}, password=***", username);
```

## Dependencies

```java
// Keep dependencies updated
// Use OWASP Dependency Check
// Enable Maven/Gradle security scanning
// Use Snyk, Dependabot for vulnerability alerts
```

## References

- `references/exception-handling.md` - Error handling security
- `references/spring-best-practices.md` - Spring Security
