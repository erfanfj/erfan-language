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
| `erfan runbuild <file.erfan>` | Compile the program to a standalone `.exe` (requires [PyInstaller](https://pyinstaller.org/)) |

Install PyInstaller for `runbuild`:

```bash
pip install pyinstaller
```

## Syntax Overview

- Statements are separated by newlines
- Code blocks use curly braces `{ }`
- Whitespace and blank lines inside blocks are ignored
- Single-line comments start with `//`

## Data Types

| Type | Example | Description |
|------|---------|-------------|
| Integer | `42` | Whole numbers |
| Float | `3.14` | Decimal numbers |
| String | `"hello"` | Double-quoted text |
| Boolean | `true`, `false` | Logical values |
| Null | `null` | Absence of a value |

## Variables

Variables are declared and assigned with `<-`:

```erfan
x <- 10
name <- "Erfan"
flag <- true
empty <- null
```

Variable names may contain letters, digits, and underscores. They must start with a letter or underscore.

## Operators

### Arithmetic

| Operator | Meaning |
|----------|---------|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |

### Comparison

| Operator | Meaning |
|----------|---------|
| `==` | Equal |
| `!=` | Not equal |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |

### Logical

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

## Control Flow

### If / Else

```erfan
if a < b {

    chap("less")

}
else {

    chap("greater or equal")

}
```

The condition must be an expression. Both the `if` and `else` branches use block syntax with `{ }`. The `else` branch is optional.

## Functions

Functions are defined with the `fn` keyword. Parameters are listed in parentheses, and the body is a block.

```erfan
fn add(a, b) {

    return a + b

}

chap(add(3, 4))
```

### Return

Use `return` to send a value back from a function:

```erfan
fn abs(n) {

    if n < 0 {
        return 0 - n
    }

    return n

}
```

If a function finishes without hitting a `return` statement, it returns `null`.

### Recursion

Functions can call themselves:

```erfan
fn fact(n) {

    if n <= 1 {
        return 1
    }

    return n * fact(n - 1)

}

chap(fact(5))
```

### Function Calls

User-defined functions and built-ins can be called as statements or inside expressions:

```erfan
chap(fact(5))

x <- add(1, 2)
```

## Classes and Objects

Erfan supports object-oriented programming with classes, methods, properties, and the `this` keyword.

### Defining a Class

Use the `class` keyword. A class body contains method definitions:

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

### Constructor (`init`)

The `init` method runs automatically when an object is created. Use `this` to refer to the current instance and store properties:

```erfan
this.name <- name
```

### Creating Objects

Instantiate a class by calling it like a function:

```erfan
p <- Person("Erfan", 25)
```

If a class has no `init` method, it cannot receive arguments.

### Methods

Call methods on an object with dot notation:

```erfan
p.greet()
```

Methods can return values and use `return` like regular functions:

```erfan
fn isAdult() {
    return this.age >= 18
}

if p.isAdult() {
    chap("Adult")
}
```

### Properties

Read and write object properties with dot notation:

```erfan
chap(p.name)

p.age <- 26
```

Properties are set on the instance via `this.field <- value` inside methods, or directly from outside the class.

## Built-in Functions

### `chap`

Prints one or more values to standard output, separated by spaces.

```erfan
chap("Hello")
chap(1, 2, 3)
chap("result:", x + y)
```

`chap` works like `print` in other languages.

## Comments

Single-line comments begin with `//`. Everything after `//` on that line is ignored:

```erfan
// this is a comment
x <- 10  // inline comment
```

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

    fn init(name, age) {
        this.name <- name
        this.age <- age
    }

    fn greet() {
        chap("Hello, I am", this.name)
    }

}

p <- Person("Erfan", 25)
p.greet()
```

## Project Structure

```
erfan-language/
├── erfan.py              # CLI entry point
├── lexer/                # Tokenizer and keywords
├── parser/               # Parser
├── erfan_ast/            # AST node definitions
├── interpreter/          # Runtime interpreter
├── compiler/             # Transpiler and exe builder
└── installer/            # Windows setup wizard
```

## Language Summary

| Feature | Status |
|---------|--------|
| Variables (`<-`) | Supported |
| Integers and floats | Supported |
| Strings | Supported |
| Booleans and null | Supported |
| Arithmetic operators | Supported |
| Comparison operators | Supported |
| Logical operators | Supported |
| If / else | Supported |
| Functions (`fn`) | Supported |
| Return values | Supported |
| Recursion | Supported |
| Classes (`class`) | Supported |
| Objects and methods | Supported |
| `this` keyword | Supported |
| Built-in `chap` | Supported |
| Comments (`//`) | Supported |
| Interpreted execution (`rundev`) | Supported |
| Standalone exe build (`runbuild`) | Supported |

## License

See the repository for license information.
