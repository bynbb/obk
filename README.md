# obk

> ⚠️ This project is in early development (pre-release/alpha).
> The current release is a “hello world” scaffold. APIs and behavior will change rapidly as features are added over the coming weeks.

Minimal CLI demonstrating dependency injection and error-handled commands.

## Installation

```bash
pip install obk
```

## Quickstart

```bash
obk hello-world
obk divide 4 2
obk trace-id
```

## Features

* `hello-world` prints a greeting
* `divide` divides two numbers with zero-checking
* `greet` greets by name with optional excitement
* `fail` triggers a fatal error for testing
* `validate-*`, `harmonize-*`, and `trace-id` handle prompt management tasks

## GSL Example

```xml
<gsl-prompt id="20250803T120000+0000" type="feat">
<gsl-header>

Example
</gsl-header>
<gsl-block>
<gsl-purpose>

p
</gsl-purpose>
<gsl-inputs>

i
</gsl-inputs>
<gsl-outputs>

o
</gsl-outputs>
<gsl-workflows/>
<gsl-tdd><gsl-test id="T1">t</gsl-test></gsl-tdd>
<gsl-document-spec>

d
</gsl-document-spec>
<gsl-surgery>
<gsl-when>
<gsl-value>

2025-08-02
</gsl-value>
</gsl-when>
</gsl-surgery>
</gsl-block>
</gsl-prompt>
```

## Usage

For help on available commands:

```bash
obk --help
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT
