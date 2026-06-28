# Spring Boot

## 核心特性

- **自动配置** — 根据依赖自动配置 Spring 组件
- **起步依赖** — `spring-boot-starter-*` 一站式包管理
- **内嵌服务器** — Tomcat / Jetty / Undertow 内嵌
- **Actuator** — 生产级监控端点

## 快速入门

```java
@SpringBootApplication
public class Application {
     public static void main(String[] args) {
         SpringApplication.run(Application.class, args);
     }
}
```

`@SpringBootApplication` 等价于:
- `@Configuration`
- `@EnableAutoConfiguration`
- `@ComponentScan`

## 配置文件

`application.yml`:
```yaml
server:
   port: 8080
spring:
   datasource:
     url: jdbc:mysql://localhost:3306/mydb
     username: root
     password: ${DB_PASSWORD}
   profiles:
     active: dev
```

## RESTful API

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

     @GetMapping("/{id}")
     public User getUser(@PathVariable Long id) {
         return userService.findById(id);
     }

     @PostMapping
     @ResponseStatus(HttpStatus.CREATED)
     public User create(@RequestBody @Valid UserDTO dto) {
         return userService.create(dto);
     }

     @DeleteMapping("/{id}")
     @ResponseStatus(HttpStatus.NO_CONTENT)
     public void delete(@PathVariable Long id) {
         userService.delete(id);
     }
}
```

## 常用 Starter

| Starter | 功能 |
|---------|------|
| `spring-boot-starter-web` | Web + REST (含 Tomcat) |
| `spring-boot-starter-data-jpa` | JPA + Hibernate |
| `spring-boot-starter-data-redis` | Redis 集成 |
| `spring-boot-starter-security` | Spring Security |
| `spring-boot-starter-test` | JUnit 5 + Mockito |
| `spring-boot-starter-actuator` | 健康检查、指标 |