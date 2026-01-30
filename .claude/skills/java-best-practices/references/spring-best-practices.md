# Dependency Injection & Spring Best Practices

## Dependency Injection

### Constructor Injection (Preferred)

```java
// Good: Mandatory dependencies via constructor
@Service
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
    
    // Spring 4.3+: @Autowired not needed for single constructor
    public UserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }
}

// Avoid field injection
@Service
public class UserService {
    @Autowired  // Bad: Hard to test, hides dependencies
    private UserRepository repository;
}
```

### Optional Dependencies

```java
// Use Optional for nullable dependencies
@Service
public class ReportService {
    private final PdfGenerator pdfGenerator;
    
    public ReportService(Optional<PdfGenerator> pdfGenerator) {
        this.pdfGenerator = pdfGenerator.orElse(null);
    }
}

// Or @Autowired(required = false)
@Autowired(required = false)
private PdfGenerator pdfGenerator;
```

## Component Scanning

```java
// Use specific annotations
@Repository  // Data access layer
@Service     // Business logic layer
@Controller  // Web layer
@RestController  // REST APIs
@Configuration   // Configuration
@Component    // Generic

// Avoid generic @Component when specific one applies
```

## Configuration Properties

```java
// Type-safe configuration
@ConfigurationProperties(prefix = "app")
public class AppProperties {
    private String name;
    private int maxConnections;
    private Security security = new Security();
    
    public static class Security {
        private String jwtSecret;
        private long tokenExpiration;
        // getters/setters
    }
    // getters/setters
}

// application.yml
app:
  name: MyApp
  max-connections: 100
  security:
    jwt-secret: ${JWT_SECRET:default-secret}
    token-expiration: 86400000

// Enable
@EnableConfigurationProperties(AppProperties.class)
```

## Bean Definitions

```java
// Use @Bean methods for complex objects
@Configuration
public class DatabaseConfig {
    
    @Bean
    public DataSource dataSource(
        @Value("${db.url}") String url,
        @Value("${db.user}") String user
    ) {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(url);
        config.setUsername(user);
        return new HikariDataSource(config);
    }
    
    // Conditional beans
    @Bean
    @Profile("production")
    public EmailSender productionEmailSender() { }
    
    @Bean
    @Profile("development")
    public EmailSender mockEmailSender() { }
}
```

## Profiles

```java
// Activate profiles
@ActiveProfiles("test")
@SpringBootTest
class MyTest { }

// Profile-specific beans
@Configuration
@Profile("cloud")
public class CloudConfig { }

// application-{profile}.yml
// application-dev.yml
// application-prod.yml
```

## Transaction Management

```java
// Service layer transactions
@Service
@Transactional
public class OrderService {
    
    // Read-only optimization
    @Transactional(readOnly = true)
    public Order findById(Long id) { }
    
    // Specific isolation
    @Transactional(isolation = Isolation.REPEATABLE_READ)
    public void updateInventory() { }
    
    // Rollback on specific exceptions
    @Transactional(rollbackFor = {BusinessException.class})
    public void processCriticalUpdate() { }
}

// Avoid @Transactional on controllers - keep in service layer
```

## Exception Handling

```java
// Global exception handler
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(NotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse(ex.getMessage()));
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(
        MethodArgumentNotValidException ex
    ) {
        List<String> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(FieldError::getDefaultMessage)
            .collect(Collectors.toList());
        return ResponseEntity.badRequest()
            .body(new ErrorResponse("Validation failed", errors));
    }
}
```

## REST API Design

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    // RESTful URLs
    @GetMapping("/{id}")           // GET /api/users/123
    @PostMapping                   // POST /api/users
    @PutMapping("/{id}")           // PUT /api/users/123
    @PatchMapping("/{id}")         // PATCH /api/users/123
    @DeleteMapping("/{id}")        // DELETE /api/users/123
    
    // Use proper status codes
    @PostMapping
    public ResponseEntity<User> create(@RequestBody @Valid UserDto dto) {
        User created = service.create(dto);
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(created);
    }
    
    // Pagination
    @GetMapping
    public Page<UserDto> list(
        @PageableDefault(size = 20) Pageable pageable
    ) {
        return service.findAll(pageable);
    }
}
```

## Validation

```java
// DTO validation
public class UserDto {
    @NotBlank
    @Email
    private String email;
    
    @Size(min = 8, max = 100)
    private String password;
    
    @Pattern(regexp = "^\\+?[0-9]{10,15}$")
    private String phone;
}

// Enable in controller
@PostMapping
public ResponseEntity<?> create(@RequestBody @Valid UserDto dto) { }
```

## Async Processing

```java
@EnableAsync
@Configuration
public class AsyncConfig {
    @Bean
    public TaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        return executor;
    }
}

@Service
public class EmailService {
    @Async
    public CompletableFuture<Void> sendEmail(String to, String subject) {
        // Runs in separate thread
        return CompletableFuture.completedFuture(null);
    }
}
```

## Caching

```java
@EnableCaching
@Configuration
public class CacheConfig { }

@Service
public class ProductService {
    @Cacheable("products")
    public Product findById(Long id) { }
    
    @CacheEvict("products")
    public void deleteProduct(Long id) { }
    
    @CachePut("products")
    public Product updateProduct(Product product) { }
}
```

## References

- `references/solid-principles.md` - Dependency Inversion Principle
- `references/testing.md` - Spring testing
