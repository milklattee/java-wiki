# Maven

## 核心概念

- **POM** — Project Object Model，项目描述文件 `pom.xml`
- **坐标** — `groupId:artifactId:version` 唯一定位一个构件
- **生命周期** — clean / default / site 三套生命周期
- **依赖管理** — 自动下载传递依赖

## pom.xml 结构

```xml
<project>
     <groupId>com.example</groupId>
     <artifactId>my-app</artifactId>
     <version>1.0.0</version>

     <properties>
         <java.version>17</java.version>
     </properties>

     <dependencies>
         <dependency>
             <groupId>org.springframework.boot</groupId>
             <artifactId>spring-boot-starter-web</artifactId>
         </dependency>
     </dependencies>
</project>
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `mvn clean` | 清理 target 目录 |
| `mvn compile` | 编译源代码 |
| `mvn test` | 运行测试 |
| `mvn package` | 打包 (jar/war) |
| `mvn install` | 安装到本地仓库 |
| `mvn deploy` | 部署到远程仓库 |
| `mvn spring-boot:run` | 运行 Spring Boot 应用 |

## 依赖范围

| scope | classpath | 说明 |
|-------|-----------|------|
| `compile` | 编译+运行+测试 | 默认 |
| `provided` | 编译+测试 | 运行时由环境提供（如 servlet-api）|
| `runtime` | 运行+测试 | 编译时不需（如 JDBC 驱动）|
| `test` | 测试 | 仅测试阶段（如 JUnit）|

## 多模块项目

```
parent-project/
├── pom.xml (packaging=pom)
├── module-api/
├── module-service/
└── module-web/
```