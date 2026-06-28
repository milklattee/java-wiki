# Spring 框架

## 核心概念

### IoC (控制反转) & DI (依赖注入)

对象创建和依赖关系由 Spring 容器管理，而不是由代码直接 `new`。

```java
@Component
public class UserService {
     @Autowired
     private UserRepository userRepository;  // Spring 自动注入
}
```

### Bean 作用域

| 作用域 | 说明 |
|--------|------|
| `singleton` | 默认，整个容器只有一个实例 |
| `prototype` | 每次获取创建新实例 |
| `request` | 每个 HTTP 请求一个实例 (Web) |
| `session` | 每个 HTTP 会话一个实例 (Web) |

## 注解概览

```java
@Configuration          // 标记配置类
@ComponentScan("com.app") // 扫描组件
@Component / @Service / @Repository / @Controller
@Autowired              // 按类型注入
@Qualifier("name")      // 按名称限定
@Value("${property}")   // 注入配置值
@Scope("prototype")     // 指定作用域
@Bean                   // 声明 Bean 方法
```

## AOP (面向切面编程)

将横切关注点（日志、事务、安全）从业务逻辑中分离：

```java
@Aspect
@Component
public class LoggingAspect {
     @Before("execution(* com.app.service.*.*(..))")
     public void logBefore(JoinPoint jp) {
         System.out.println("调用: " + jp.getSignature().getName());
     }
}
```

## 事务管理

```java
@Service
@Transactional  // 类级别，所有方法开启事务
public class OrderService {
     @Transactional(rollbackFor = Exception.class, propagation = Propagation.REQUIRED)
     public void placeOrder(Order order) {
         // 数据库操作
     }
}
```

| 传播行为 | 说明 |
|----------|------|
| `REQUIRED` | 默认，有则加入，无则新建 |
| `REQUIRES_NEW` | 总是新建，挂起当前 |
| `SUPPORTS` | 有则加入，无则非事务运行 |
| `MANDATORY` | 必须在事务中，无则抛异常 |