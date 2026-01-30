# Testing Best Practices

## Testing Pyramid

```
        E2E (5%)
       /       \
    Integration (15%)
   /               \
Unit Tests (80%)
```

## JUnit 5 Best Practices

```java
// Test class命名: ClassNameTest
class UserServiceTest {
    
    // @BeforeEach runs before each test
    @BeforeEach
    void setUp() {
        // Arrange - set up test data
    }
    
    // Test method命名: methodName_scenario_expectedResult
    @Test
    @DisplayName("should return user when valid id is provided")
    void findById_givenValidId_returnsUser() {
        // Arrange
        Long userId = 1L;
        User expected = new User(userId, "John");
        when(repository.findById(userId)).thenReturn(Optional.of(expected));
        
        // Act
        User actual = service.findById(userId);
        
        // Assert
        assertEquals(expected, actual);
        verify(repository).findById(userId);
    }
    
    // Test exceptions
    @Test
    void findById_whenNotFound_throwsException() {
        assertThrows(NotFoundException.class, () -> service.findById(999L));
    }
    
    // Parameterized tests
    @ParameterizedTest
    @ValueSource(strings = {"", "  ", "invalid"})
    void setEmail_whenInvalid_throwsException(String email) {
        assertThrows(IllegalArgumentException.class, 
            () -> user.setEmail(email));
    }
}
```

## Mockito Best Practices

```java
// Mock external dependencies
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private EmailService emailService;
    
    @InjectMocks
    private OrderService orderService;
    
    @Test
    void processOrder_whenSuccess_sendsEmail() {
        // Arrange
        User user = new User(1L, "test@example.com");
        Order order = new Order(1L, user);
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        
        // Act
        orderService.processOrder(order);
        
        // Assert - verify interaction
        verify(emailService).sendConfirmation(eq(user), any(Order.class));
    }
    
    // Stub return values
    @Test
    void calculateTotal_withDiscount_returnsCorrectAmount() {
        when(product.getPrice()).thenReturn(BigDecimal.valueOf(100));
        when(discountService.getDiscount(any(User.class)))
            .thenReturn(BigDecimal.valueOf(10));
        
        BigDecimal total = orderService.calculateTotal(user, product);
        
        assertEquals(BigDecimal.valueOf(90), total);
    }
}
```

## Test Coverage

- Aim for **80%+ line coverage** for critical business logic
- 100% coverage is not always necessary
- Focus on **branch coverage** for complex conditionals
- Use JaCoCo plugin:
```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
</plugin>
```

## Integration Tests

```java
@SpringBootTest
@Transactional
class UserRepositoryIntegrationTest {
    
    @Autowired
    private UserRepository userRepository;
    
    @Test
    void save_andRetrieve_success() {
        User user = new User(null, "test@example.com");
        User saved = userRepository.save(user);
        
        User found = userRepository.findById(saved.getId()).orElseThrow();
        assertEquals("test@example.com", found.getEmail());
    }
}

// For REST APIs
@AutoConfigureMockMvc
class UserControllerIntegrationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void getUsers_returnsOk() throws Exception {
        mockMvc.perform(get("/api/users"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$[0].name").value("John"));
    }
}
```

## Testing Best Practices

```java
// DO: Test one thing per test
@Test
void isValid_withValidEmail_returnsTrue() { }

// DON'T: Test multiple scenarios
@Test
void isValid_variousScenarios() { }  // Bad - multiple tests

// DO: Use descriptive test names
@Test
@DisplayName("withdraw should fail when insufficient funds")
void withdraw_whenInsufficientFunds_throwsException() { }

// DON'T: Vague names
@Test
void testWithdraw() { }

// DO: Follow AAA pattern (Arrange, Act, Assert)
@Test
void calculate_returnsCorrectSum() {
    // Arrange
    Calculator calc = new Calculator();
    
    // Act
    int result = calc.add(2, 3);
    
    // Assert
    assertEquals(5, result);
}
```

## Test Fixtures

```java
// Use test builders for complex objects
public class UserBuilder {
    private Long id = 1L;
    private String name = "Test User";
    private String email = "test@example.com";
    
    public static UserBuilder aUser() { return new UserBuilder(); }
    
    public UserBuilder withId(Long id) { this.id = id; return this; }
    public UserBuilder withEmail(String email) { this.email = email; return this; }
    
    public User build() { return new User(id, name, email); }
}

// Usage in tests
User user = UserBuilder.aUser().withEmail("custom@example.com").build();
```

## Avoid Common Mistakes

```java
// DON'T: Test implementation details
@Test
void testInternalMethod() { }  // Bad

// DO: Test behavior through public API
@Test
void processOrder_givenValidInput_returnsSuccess() { }

// DON'T: Use Thread.sleep()
Thread.sleep(1000);  // Flaky, slow

// DO: Use Awaitility or mock time
await().atMost(2, TimeUnit.SECONDS)
    .until(() -> result.isReady());

// DON'T: Hardcoded test data that changes
User user = new User(1L, "john@example.com");  // Email might change

// DO: Use test data builders or fixtures
User user = UserBuilder.aUser().build();
```

## References

- `references/clean-code.md` - Clean code principles
- `references/spring-best-practices.md` - Spring testing
