# Erfan Language

Erfan is a small, interpreted programming language with an optional compiler that produces standalone Windows executables. Source files use the `.erfan` extension.

## Getting Started

Run a program directly with the interpreter:

```bash
erfan rundev program.erfan
```

Compile a program into a standalone executable:

```bash
erfan runbuild program.erfan
```

The built executable is saved to a `build/` folder next to the source file. For example, `program.erfan` becomes `build/program.exe`.

## CLI Commands

| Command | Description |
|---------|-------------|
| `erfan rundev <file.erfan>` | Parse and run the program using the built-in interpreter |
| `erfan runbuild <file.erfan>` | Compile the program to a standalone `.exe` (no extra tools required) |

`runbuild` embeds your source into a bundled Erfan runtime. End users do **not** need Python or PyInstaller installed.

## Syntax Overview

- Statements are separated by newlines
- Code blocks use curly braces `{ }`
- Whitespace and blank lines inside blocks are ignored
- Single-line comments start with `//`

---

## Language Features

### 1. Variables

Variables are declared and assigned with `<-`:

```erfan
x <- 10
name <- "Erfan"
flag <- true
empty <- null
```

Variable names may contain letters, digits, and underscores. They must start with a letter or underscore.

---

### 2. Data Types

| Type | Example | Description |
|------|---------|-------------|
| Integer | `42` | Whole numbers |
| Float | `3.14` | Decimal numbers |
| String | `"hello"` | Double-quoted text |
| Boolean | `true`, `false` | Logical values |
| Null | `null` | Absence of a value |
| Array | `[1, 2, 3]` | Ordered list of values |

---

### 3. Operators

#### Arithmetic

| Operator | Meaning |
|----------|---------|
| `+` | Addition (also string concatenation) |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `%` | Modulo (remainder) |

#### Comparison

| Operator | Meaning |
|----------|---------|
| `==` | Equal |
| `!=` | Not equal |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |

#### Logical

| Operator | Meaning |
|----------|---------|
| `&&` | Logical AND |
| `\|\|` | Logical OR |
| `!` | Logical NOT |

Unary `+` and `-` are also supported on numeric expressions.

Parentheses can be used to group expressions:

```erfan
result <- (a + b) * 2
```

---

### 4. Arrays

Create arrays with square brackets:

```erfan
numbers <- [1, 2, 3]
mixed <- [1, "hello", true]
empty <- []
```

Access and modify elements by index (zero-based):

```erfan
chap(numbers[0])
numbers[1] <- 99
```

Index access also works on strings:

```erfan
word <- "Erfan"
chap(word[0])
```

---

### 5. Control Flow

#### If / Else

```erfan
if a < b {

    chap("less")

}
else {

    chap("greater or equal")

}
```

The `else` branch is optional.

#### For-In Loop (`boro` / `roye`)

Iterate over arrays or strings:

```erfan
numbers <- [1, 2, 3]

boro n roye numbers {

    chap(n)

}
```

```erfan
boro ch roye "Erfan" {

    chap(ch)

}
```

`boro x roye y` means "for each `x` in `y`".

#### While Loop

```erfan
i <- 0

while i < 5 {

    chap(i)
    i <- i + 1

}
```

#### Break and Continue

```erfan
boro n roye [1, 2, 3, 4, 5] {

    if n == 3 {
        break
    }

    if n == 2 {
        continue
    }

    chap(n)

}
```

- `break` — exit the current loop immediately
- `continue` — skip to the next iteration

---

### 6. Functions

Functions are defined with the `fn` keyword:

```erfan
fn add(a, b) {

    return a + b

}

chap(add(3, 4))
```

#### Return

```erfan
fn abs(n) {

    if n < 0 {
        return 0 - n
    }

    return n

}
```

If a function finishes without `return`, it returns `null`.

#### Recursion

```erfan
fn fact(n) {

    if n <= 1 {
        return 1
    }

    return n * fact(n - 1)

}

chap(fact(5))
```

Functions can be called as statements or inside expressions.

---

### 7. Classes and Objects

Erfan supports object-oriented programming with classes, methods, properties, and `this`.

#### Defining a Class

```erfan
class Person {

    fn init(name, age) {
        this.name <- name
        this.age <- age
    }

    fn greet() {
        chap("Hello, I am", this.name)
    }

}
```

#### Constructor (`init`)

The `init` method runs automatically when an object is created:

```erfan
p <- Person("Erfan", 25)
```

#### Methods and Properties

```erfan
p.greet()
chap(p.name)
p.age <- 26
```

---

### 8. Built-in Functions

#### `chap`

Prints values to standard output (like `print`):

```erfan
chap("Hello")
chap(1, 2, 3)
chap("result:", x + y)
```

#### `size`

Returns the length of an array or string:

```erfan
chap(size([1, 2, 3]))
chap(size("Erfan"))
```

---

### 9. Comments

Single-line comments begin with `//`:

```erfan
// this is a comment
x <- 10
```

---

## Complete Examples

### Conditionals

```erfan
a <- 10
b <- 20

if a < b {
    chap("YES")
}
else {
    chap("NO")
}
```

### Loops and Arrays

```erfan
numbers <- [1, 2, 3, 4, 5]
sum <- 0

boro n roye numbers {
    sum <- sum + n
}

chap(sum)
```

### Factorial

```erfan
fn fact(n) {

    if n <= 1 {
        return 1
    }

    return n * fact(n - 1)

}

chap(fact(5))
```

### Classes

```erfan
class Person {

    fn init(name) {
        this.name <- name
    }

    fn greet() {
        chap("Hello,", this.name)
    }

}

p <- Person("Erfan")
p.greet()
```

---

## Project Structure

```
erfan-language/
├── erfan.py              # CLI entry point
├── lexer/                # Tokenizer and keywords
├── parser/               # Parser
├── erfan_ast/            # AST node definitions
├── interpreter/          # Runtime interpreter
├── compiler/             # Exe packer and bundled runtime
│   └── assets/           # Pre-built erfan_runtime.exe
├── scripts/              # Maintainer build scripts
└── installer/            # Windows setup wizard
```

## Building from Source (Maintainers)

End users install `setup.exe` and never need Python. Maintainers use these scripts when preparing a release:

```bash
python scripts/build_runtime.py
python scripts/build_erfan.py
```

PyInstaller is only required on the maintainer machine, not for end users.

---

## Language Summary

| Feature | Status |
|---------|--------|
| Variables (`<-`) | Supported |
| Integers and floats | Supported |
| Strings | Supported |
| Booleans and null | Supported |
| Arrays `[ ]` | Supported |
| Index access `arr[i]` | Supported |
| Arithmetic operators (`+`, `-`, `*`, `/`, `%`) | Supported |
| Comparison operators | Supported |
| Logical operators | Supported |
| If / else | Supported |
| For-in loop (`boro` / `roye`) | Supported |
| While loop | Supported |
| Break / continue | Supported |
| Functions (`fn`) | Supported |
| Return values | Supported |
| Recursion | Supported |
| Classes (`class`) | Supported |
| Objects and methods | Supported |
| `this` keyword | Supported |
| Built-in `chap` | Supported |
| Built-in `size` | Supported |
| Comments (`//`) | Supported |
| Interpreted execution (`rundev`) | Supported |
| Standalone exe build (`runbuild`) | Supported |

## License

See the repository for license information.
