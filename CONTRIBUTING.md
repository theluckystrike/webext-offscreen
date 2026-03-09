# Contributing to webext-offscreen

Thank you for your interest in contributing! This guide will help you get started.

## Getting Started

### Fork the Repository

Click the "Fork" button on the GitHub repository page to create your own copy.

### Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/webext-offscreen.git
cd webext-offscreen
```

### Install Dependencies

This project uses pnpm:

```bash
npm install -g pnpm  # if you don't have pnpm
pnpm install
```

### Create a Branch

Create a new branch for your feature or bugfix:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Development

### Build the Project

```bash
pnpm build
```

### Run Tests

```bash
pnpm test
```

### Type Checking

```bash
pnpm typecheck
```

## Making Changes

1. Make your changes in your feature branch
2. Ensure tests pass: `pnpm test`
3. Build the project: `pnpm build`
4. Commit your changes with a clear message
5. Push to your fork

## Pull Request Process

1. Update documentation if needed
2. Ensure all tests pass
3. Update the CHANGELOG.md if applicable
4. Submit a pull request to the `main` branch
5. Describe your changes clearly in the PR description

## Code Style

- Use TypeScript
- Follow existing code patterns
- Add types for new functions
- Write tests for new features

## Questions?

Feel free to open an issue for questions about contributing.
