# Java 8 新特性：Stream 流与函数式接口

## 1. 函数式接口 (Functional Interface)

### 1.1 定义

有且仅有一个抽象方法的接口，可以包含多个默认方法或静态方法。

```java
@FunctionalInterface  // 可选，编译器会检查是否符合函数式接口定义
public interface MyFunction<T, R> {
     R apply(T t);      // 唯一的抽象方法

     // 默认方法 — 不限数量
     default String describe() { return "MyFunction"; }
}
```

使用 Lambda 表达式实例化：

```java
MyFunction<String, Integer> lengthFn = s -> s.length();
int len = lengthFn.apply("hello");  // 5
```

### 1.2 Java 内置四大函数式接口

| 接口 | 方法签名 | 用途 | 示例 |
|------|----------|------|------|
| `Predicate<T>` | `boolean test(T t)` | 判断/过滤 | `s -> s.isEmpty()` |
| `Consumer<T>` | `void accept(T t)` | 消费/执行操作 | `x -> System.out.println(x)` |
| `Function<T,R>` | `R apply(T t)` | 转换/映射 | `s -> s.length()` |
| `Supplier<T>` | `T get()` | 提供/生成数据 | `() -> new User()` |

### 1.3 扩展函数式接口

| 接口 | 说明 |
|------|------|
| `BiPredicate<T,U>` | 双参数判断: `(a, b) -> a > b` |
| `BiConsumer<T,U>` | 双参数消费: `(k, v) -> map.put(k, v)` |
| `BiFunction<T,U,R>` | 双参数转换: `(x, y) -> x + y` |
| `UnaryOperator<T>` | `Function<T,T>` 特化，输入输出同类型 |
| `BinaryOperator<T>` | `BiFunction<T,T,T>` 特化，双参数同类型 |
| `IntPredicate / LongConsumer / ...` | 原始类型特化，避免装箱开销 |

### 1.4 方法引用 (Method Reference) — Lambda 的简写

| 类型 | 语法 | 等价 Lambda |
|------|------|-------------|
| 静态方法 | `Math::abs` | `x -> Math.abs(x)` |
| 实例方法（对象）| `System.out::println` | `x -> System.out.println(x)` |
| 实例方法（类）| `String::length` | `s -> s.length()` |
| 构造方法 | `ArrayList::new` | `() -> new ArrayList<>()` |

```java
// 实战对比
List<String> names = Arrays.asList("Alice", "Bob", "Charlie");

// Lambda 写法
names.forEach(name -> System.out.println(name));

// 方法引用（更简洁）
names.forEach(System.out::println);

// 构造方法引用
Supplier<List<String>> listSupplier = ArrayList::new;
List<String> newList = listSupplier.get();
```

## 2. Stream API 核心

### 2.1 什么是 Stream

Stream 不是数据结构，而是一个**数据流水线**：

```
数据源 → [中间操作1] → [中间操作2] → ... → [终端操作] → 结果
  (惰性)      (惰性)                     (触发执行)
```

- **惰性求值**：中间操作不立即执行，只在终端操作触发时才一次性完成
- **不可复用**：一个 Stream 只能被消费一次，再次使用抛 `IllegalStateException`
- **不修改源**：Stream 操作不会改变原始数据源

### 2.2 Stream 的创建

```java
// 1. 从集合
Stream<String> s1 = list.stream();           // 串行流
Stream<String> s2 = list.parallelStream();   // 并行流

// 2. 从数组
Stream<Integer> s3 = Arrays.stream(new Integer[]{1, 2, 3});
Stream<Integer> s4 = Stream.of(1, 2, 3);

// 3. 生成无限流
Stream<Integer> s5 = Stream.iterate(0, n -> n + 2);    // 0, 2, 4, 6, ...
Stream<Double> s6 = Stream.generate(Math::random);      // 随机数无限流
// 配合 limit() 截断，否则无限执行
s5.limit(10).forEach(System.out::println);  // 0 2 4 6 8 10 12 14 16 18

// 4. 从文件行
Stream<String> lines = Files.lines(Path.of("data.txt"));

// 5. 构建器
Stream<String> s7 = Stream.<String>builder().add("a").add("b").build();

// 6. IntStream / LongStream / DoubleStream (原始类型流)
IntStream range = IntStream.range(1, 100);         // 1..99
IntStream rangeClosed = IntStream.rangeClosed(1, 100); // 1..100
```

## 3. 中间操作 (Intermediate Operations)

### 3.1 filter — 过滤

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6);
List<Integer> evens = numbers.stream()
         .filter(n -> n % 2 == 0)
         .collect(Collectors.toList());  // [2, 4, 6]
```

### 3.2 map — 映射/转换

```java
List<String> names = Arrays.asList("alice", "bob", "charlie");
List<String> upper = names.stream()
         .map(String::toUpperCase)
         .collect(Collectors.toList());  // ["ALICE", "BOB", "CHARLIE"]

// mapToInt / mapToLong / mapToDouble — 避免装箱
int totalLength = names.stream()
         .mapToInt(String::length)   // 返回 IntStream
         .sum();                     // IntStream 专属方法
```

### 3.3 flatMap — 扁平化

将多个 Stream 合并为一个：

```java
// 问题：获取所有订单中的所有商品名
List<Order> orders = getOrders();  // Order 包含 List<Item>

// ❌ map 返回 Stream<Stream<String>>
orders.stream().map(o -> o.getItems().stream().map(Item::getName));

// ✅ flatMap 返回 Stream<String>
List<String> allItemNames = orders.stream()
         .flatMap(o -> o.getItems().stream())
         .map(Item::getName)
         .collect(Collectors.toList());
```

经典例题 — 字符串切分去重：

```java
List<String> words = Arrays.asList("Hello World", "Hello Java");
List<String> distinct = words.stream()
         .flatMap(s -> Arrays.stream(s.split(" ")))
         .distinct()
         .collect(Collectors.toList());  // ["Hello", "World", "Java"]
```

### 3.4 distinct — 去重

```java
List<Integer> nums = Arrays.asList(1, 2, 2, 3, 3, 3);
List<Integer> unique = nums.stream()
         .distinct()
         .collect(Collectors.toList());  // [1, 2, 3]
```

`distinct()` 依赖 `equals()` 和 `hashCode()`，自定义对象需要正确重写。

### 3.5 sorted — 排序

```java
// 自然排序
List<String> sorted = list.stream().sorted().collect(Collectors.toList());

// 自定义比较器
List<User> byAge = users.stream()
         .sorted(Comparator.comparing(User::getAge).reversed())
         .collect(Collectors.toList());

// 多级排序: 先按部门，再按薪资降序
List<User> multiSort = users.stream()
         .sorted(Comparator.comparing(User::getDept)
                 .thenComparing(User::getSalary, Comparator.reverseOrder()))
         .collect(Collectors.toList());
```

### 3.6 peek — 调试/副作用

```java
// peek 常用来调试中间状态，生产代码慎用
List<String> result = list.stream()
         .filter(s -> s.startsWith("A"))
         .peek(s -> System.out.println("After filter: " + s))
         .map(String::toUpperCase)
         .peek(s -> System.out.println("After map: " + s))
         .collect(Collectors.toList());
```

### 3.7 limit / skip — 截断/跳过

```java
Stream.iterate(1, n -> n + 1)
         .skip(5)      // 跳过前 5 个
         .limit(3)     // 取 3 个
         .forEach(System.out::println);  // 6 7 8
```

## 4. 终端操作 (Terminal Operations)

### 4.1 collect — 最核心的终端操作

```java
// toList / toSet / toMap
List<String> list = stream.collect(Collectors.toList());
Set<String> set = stream.collect(Collectors.toSet());
Map<Integer, User> map = users.stream()
         .collect(Collectors.toMap(User::getId, Function.identity()));

// 处理重复 key
Map<String, User> noDup = users.stream()
         .collect(Collectors.toMap(
             User::getName,
             Function.identity(),
             (existing, replacement) -> existing  // 保留先出现的
         ));
```

### 4.2 groupingBy / partitioningBy — 分组/分区

```java
// groupingBy — 按部门分组
Map<String, List<User>> byDept = users.stream()
         .collect(Collectors.groupingBy(User::getDept));

// groupingBy + 下游收集器 — 按部门统计人数
Map<String, Long> countByDept = users.stream()
         .collect(Collectors.groupingBy(User::getDept, Collectors.counting()));

// groupingBy + downstream — 每个部门的最高工资员工
Map<String, Optional<User>> topByDept = users.stream()
         .collect(Collectors.groupingBy(
             User::getDept,
             Collectors.maxBy(Comparator.comparing(User::getSalary))
         ));

// partitioningBy — 按布尔条件二分
Map<Boolean, List<User>> adults = users.stream()
         .collect(Collectors.partitioningBy(u -> u.getAge() >= 18));
```

### 4.3 reduce — 归约

```java
// 无初始值 — 返回 Optional
Optional<Integer> sum = numbers.stream().reduce((a, b) -> a + b);

// 有初始值 — 返回具体类型
int sum2 = numbers.stream().reduce(0, Integer::sum);

// 三参数 reduce — 用于并行流(combiner)
int parallelSum = numbers.parallelStream()
         .reduce(0, Integer::sum, Integer::sum);

// 更推荐的方式：用 IntStream 的 sum()
int best = numbers.stream().mapToInt(Integer::intValue).sum();
```

### 4.4 查找与匹配

```java
// anyMatch — 任意元素满足
boolean hasAdult = users.stream().anyMatch(u -> u.getAge() >= 18);

// allMatch — 所有元素都满足
boolean allPositive = numbers.stream().allMatch(n -> n > 0);

// noneMatch — 没有元素满足
boolean noNegative = numbers.stream().noneMatch(n -> n < 0);

// findFirst — 返回第一个元素
Optional<User> first = users.stream()
         .filter(u -> u.getAge() > 30)
         .findFirst();

// findAny — 返回任意元素（并行流中更高效）
Optional<User> any = users.parallelStream()
         .filter(u -> u.getAge() > 30)
         .findAny();

// min / max
Optional<User> youngest = users.stream()
         .min(Comparator.comparing(User::getAge));
Optional<User> richest = users.stream()
         .max(Comparator.comparing(User::getSalary));
```

### 4.5 forEach / forEachOrdered

```java
// forEach — 不保证顺序（并行流中）
list.parallelStream().forEach(System.out::println);

// forEachOrdered — 保证顺序（即使并行流）
list.parallelStream().forEachOrdered(System.out::println);
```

> 注意：`forEach` 是终端操作，`peek` 是中间操作。不要在 `forEach` 中修改外部状态（破坏函数式编程原则）。

## 5. Collectors 进阶

### 5.1 常用收集器一览

| 收集器 | 用途 |
|--------|------|
| `Collectors.toList()` | 收集为 List |
| `Collectors.toSet()` | 收集为 Set |
| `Collectors.toCollection(TreeSet::new)` | 收集到指定集合 |
| `Collectors.toMap(...)` | 收集为 Map |
| `Collectors.joining(", ")` | 字符串拼接 |
| `Collectors.counting()` | 计数 |
| `Collectors.summingInt(Person::getAge)` | 求和 |
| `Collectors.averagingInt(Person::getAge)` | 平均值 |
| `Collectors.summarizingInt(Person::getAge)` | 统计摘要（count, sum, min, avg, max）|

### 5.2 collectingAndThen — 收集后转换

```java
// 收集为不可变列表
List<String> unmodifiable = stream.collect(
         Collectors.collectingAndThen(
             Collectors.toList(),
             Collections::unmodifiableList
         )
);
```

### 5.3 mapping / flatMapping (JDK 9+)

```java
// 在 groupingBy 内部做映射，减少中间操作
Map<String, List<String>> deptNames = users.stream()
         .collect(Collectors.groupingBy(
             User::getDept,
             Collectors.mapping(User::getName, Collectors.toList())
         ));
```

## 6. 并行流 (Parallel Stream)

### 6.1 使用方式

```java
// 方式1：从集合直接获取
list.parallelStream()

// 方式2：转换已有流
list.stream().parallel()

// 方式3：切换回串行
stream.parallel().sequential()
```

### 6.2 底层机制：ForkJoinPool

默认使用 `ForkJoinPool.commonPool()`，线程数 = CPU 核心数 - 1。可自定义：

```java
ForkJoinPool customPool = new ForkJoinPool(4);
customPool.submit(() ->
     list.parallelStream().forEach(heavyTask)
).get();
```

### 6.3 什么时候用并行流

| 条件 | 适合 | 不适合 |
|------|------|--------|
| 数据量 | 大（> 10,000）| 小 |
| 操作开销 | CPU 密集型 | IO 密集 / 有锁 |
| 数据结构 | ArrayList, 数组（可高效拆分）| LinkedList（拆分慢）|
| 操作顺序 | 无顺序要求 | 要求严格顺序 |

```java
// ✅ 适合并行：大数组 + 独立计算
long sum = IntStream.rangeClosed(1, 10_000_000)
         .parallel()
         .map(x -> x * x)
         .sum();

// ❌ 不适合：有状态操作（结果不可预测）
List<Integer> shared = new ArrayList<>();
IntStream.range(0, 1000).parallel()
         .forEach(shared::add);  // 线程不安全！结果不确定
```

> 并行流 `forEach` 中修改共享变量是**绝对禁止**的。如需线程安全收集，用 `collect()`。

## 7. Optional 与 Stream

Optional 的流式操作使 null 处理更为优雅：

```java
// 传统写法
String result;
User user = findUser(id);
if (user != null) {
     Address addr = user.getAddress();
     if (addr != null) {
         result = addr.getCity();
     } else { result = "Unknown"; }
} else { result = "Unknown"; }

// Optional + map 链式调用
String result = findUser(id)
         .map(User::getAddress)
         .map(Address::getCity)
         .orElse("Unknown");

// Optional::stream (JDK 9+) — 将 Optional 转为 Stream
List<User> users = ids.stream()
         .map(UserRepo::findById)      // Stream<Optional<User>>
         .flatMap(Optional::stream)    // Stream<User> — 自动过滤 empty
         .collect(Collectors.toList());
```

## 8. 常见陷阱与最佳实践

### 8.1 Stream 不可复用

```java
Stream<String> s = list.stream();
s.forEach(System.out::println);  // ✅
s.forEach(System.out::println);  // ❌ IllegalStateException: stream already operated upon
// 解决：每次重新获取 stream()
```

### 8.2 原始类型流优先

```java
// ❌ 装箱开销大
list.stream().map(x -> x + 1).reduce(0, Integer::sum);

// ✅ IntStream 无装箱
list.stream().mapToInt(Integer::intValue).map(x -> x + 1).sum();
```

### 8.3 短路操作放前面

```java
// ✅ limit 在前，后续操作只处理 10 个元素
stream.filter(expensive)
       .limit(10)
       .collect(Collectors.toList());

// ❌ 对所有元素都执行 expensive filter
stream.limit(10)
       .filter(expensive)   // limit 截断的是 filter 之后的流
       .collect(Collectors.toList());
```

### 8.4 调试：peek 而非修改代码

怀疑某步操作有问题时，插入 `peek()` 观察中间数据，无需改动业务逻辑。

### 8.5 空集合也安全

```java
// 即使 orders 为空也不会 NPE
int total = orders.stream()
         .mapToInt(Order::getAmount)
         .sum();  // 空流返回 0
```

### 8.6 checked exception 在 Lambda 中的处理

```java
// 问题：Files.lines() 抛 IOException，不能直接在 Lambda 中使用

// 解法1：try-catch 包裹（不优雅）
list.stream().map(path -> {
     try { return Files.readString(path); }
     catch (IOException e) { throw new UncheckedIOException(e); }
});

// 解法2：抽取工具方法（推荐）
@FunctionalInterface
public interface CheckedFunction<T, R> {
     R apply(T t) throws Exception;
}

public static <T, R> Function<T, R> wrap(CheckedFunction<T, R> f) {
     return t -> {
         try { return f.apply(t); }
         catch (Exception e) { throw new RuntimeException(e); }
     };
}

list.stream().map(wrap(Files::readString));
```

## 9. 性能对比速查

| 场景 | 传统 for 循环 | Stream | 评价 |
|------|--------------|--------|------|
| 简单遍历 | ~快 | ~慢 20% | 数据量 < 1000 差异可忽略 |
| 复杂链路(filter+map+collect) | 手写冗长 | 声明式简洁 | Stream 可读性碾压 |
| 大数组数值计算 | for + 累加 | IntStream.parallel() | 并行流在大数据量下明显更快 |
| LinkedList 多次遍历 | 每次 O(n) | 同样 O(n) | Stream 无法规避数据结构劣势 |

**结论**：优先使用 Stream 提高可读性和可维护性，热路径用 JMH 实测再做选择。