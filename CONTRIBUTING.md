# Contributing to webext-offscreen

Thank you for your interest in contributing! This document outlines the process for contributing to this project.

## Getting Started

1. **Fork the repository** — Click the "Fork" button on the GitHub page
2. **Clone your fork** — `git clone https://github.com/YOUR_USERNAME/webext-offscreen.git`
3. **Navigate to the project** — `cd webext-offscreen`

## Development Setup

This project uses pnpm for package management:

```bash
# Install pnpm if you haven't already
npm install -g pnpm

# Install dependencies
pnpm install

# Build the project
pnpm build

# Run tests
pnpm test
```

## Creating a Branch

Create a new branch for your feature or fix:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

## Making Changes

1. Make your changes in the `src/` directory
2. Ensure your code follows the existing TypeScript style
3. Add or update tests as needed
4. Build the project to generate the `dist/` files

## Testing

Run the test suite:

```bash
pnpm test
```

Make sure all tests pass before submitting a PR.

## Committing

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: typed offscreen message support"
```

## Submitting a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Open a Pull Request against the `main` branch of the original repository

3. Fill out the PR template with:
   - A clear description of your changes
   - Any related issues or motivation
   - Test results from your local run

## Code Style

- Use TypeScript with strict mode
- Use functional/const patterns
- Add JSDoc comments for public APIs
- Keep dependencies minimal

## Questions?

If you have questions, feel free to open an issue for discussion before starting a PR.

---

Thank you for contributing!
