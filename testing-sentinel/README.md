# Testing Sentinel — Claude Code Plugin

> Enforce world-class testing practices inspired by SQLite (590:1 test-to-code ratio), Linux Kernel (8,400+ bugs caught by fuzzing), Chromium (30,000-VM fuzzing infrastructure), NASA/JPL ("Power of 10" rules), curl, PostgreSQL, and Redis.

## What It Does

Testing Sentinel brings automated testing discipline into your Claude Code workflow through:

- **Slash Commands** — Audit test quality, scaffold test suites, generate fuzz targets, check coverage gaps
- **Specialized Agents** — Test architect, test reviewer, and fuzz engineer agents for deep analysis
- **Skills** — Comprehensive testing best practices knowledge base activated contextually
- **Hooks** — Automatic validation that new/edited code has corresponding tests

## Installation

### Via Claude Code CLI

```bash
/plugin install testing-sentinel
```

### Local Installation

```bash
git clone https://github.com/igorlnunes/testing-sentinel.git
cd your-project
claude --plugin-dir /path/to/testing-sentinel
```

Or add to `.claude/settings.json`:

```json
{
  "plugins": [
    { "type": "local", "path": "/path/to/testing-sentinel" }
  ]
}
```

## Commands

| Command | Description |
|---------|-------------|
| `/test-audit` | Analyze the project's testing maturity level (1-4) with actionable recommendations |
| `/test-scaffold` | Generate test files for specified modules with proper structure and patterns |
| `/test-fuzz` | Create fuzz testing targets for parsers, serializers, and protocol handlers |
| `/test-coverage` | Identify untested code paths and suggest targeted tests |
| `/test-regression` | Generate regression test from a bug description or issue |
| `/test-failure` | Create failure injection tests (OOM, I/O errors, crash recovery) |

## Agents

| Agent | Purpose |
|-------|---------|
| **test-architect** | Designs comprehensive testing strategies for projects, recommends tools, and creates CI pipeline configurations |
| **test-reviewer** | Reviews PRs and code changes for test quality, coverage gaps, and adherence to best practices |
| **fuzz-engineer** | Specializes in creating structure-aware fuzz targets, property-based tests, and failure injection scenarios |

## Hooks

| Event | Trigger | Action |
|-------|---------|--------|
| `PostToolUse` | `Write\|Edit` on source files | Warns if corresponding test file is missing or unchanged |
| `Stop` | Session end | Summarizes test-related actions and flags untested changes |

## Skills

The **testing-best-practices** skill activates automatically when Claude detects testing-related tasks. It provides contextual guidance drawn from real-world practices of SQLite, Linux Kernel, Chromium, NASA/JPL, curl, PostgreSQL, and Redis.

## Configuration

Create `.claude/testing-sentinel.json` in your project root to customize behavior:

```json
{
  "language": "python",
  "testFramework": "pytest",
  "testDir": "tests",
  "sourceDir": "src",
  "coverageTarget": 80,
  "enforceRegressionTests": true,
  "hooksEnabled": true
}
```

### Supported Languages & Frameworks

| Language | Frameworks |
|----------|-----------|
| Python | pytest, unittest |
| JavaScript/TypeScript | Jest, Vitest, Mocha |
| Go | go test |
| Rust | cargo test |
| C/C++ | Google Test, Catch2 |
| Java | JUnit, TestNG |
| PHP | PHPUnit, Pest |

## License

MIT
