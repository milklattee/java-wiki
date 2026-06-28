# MyBatis

## 核心组件

| 组件 | 作用 |
|------|------|
| `SqlSessionFactory` | 创建 SqlSession（应用生命周期一个实例）|
| `SqlSession` | 执行 SQL、获取 Mapper（线程不安全）|
| `Mapper` 接口 | 定义 SQL 操作的 Java 接口 |
| `Mapper XML` | SQL 映射文件 |

## Mapper XML

```xml
<!-- UserMapper.xml -->
<mapper namespace="com.app.mapper.UserMapper">
     <resultMap id="userMap" type="User">
         <id property="id" column="id"/>
         <result property="name" column="user_name"/>
         <result property="email" column="email"/>
     </resultMap>

     <select id="findById" resultMap="userMap">
         SELECT * FROM users WHERE id = #{id}
     </select>

     <insert id="insert" useGeneratedKeys="true" keyProperty="id">
         INSERT INTO users (user_name, email) VALUES (#{name}, #{email})
     </insert>
</mapper>
```

## 注解方式 (Spring Boot)

```java
@Mapper
public interface UserMapper {
     @Select("SELECT * FROM users WHERE id = #{id}")
     User findById(Long id);

     @Insert("INSERT INTO users(name, email) VALUES(#{name}, #{email})")
     @Options(useGeneratedKeys = true, keyProperty = "id")
     int insert(User user);
}
```

## 动态 SQL

```xml
<select id="findByCondition" resultType="User">
     SELECT * FROM users
     <where>
         <if test="name != null">
             AND name LIKE CONCAT('%', #{name}, '%')
         </if>
         <if test="email != null">
             AND email = #{email}
         </if>
     </where>
</select>
```

## #{} vs ${}

| 占位符 | 说明 |
|--------|------|
| `#{}` | 预编译占位符（安全，防 SQL 注入）|
| `${}` | 直接字符串拼接（不安全，用于动态表名/字段名）|