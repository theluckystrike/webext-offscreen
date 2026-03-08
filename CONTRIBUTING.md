# Contributing to webext-offscreen

Thank you for your interest in contributing! This document outlines the process for contributing to this project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/webext-offscreen.git
   cd webext-offscreen
   ```
3. **Install dependencies**:
   ```bash
   npm install
   ```

## Development Workflow

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and **add tests** if applicable

3. Run the test suite:
   ```bash
   npm test
   ```

4. Build the project:
   ```bash
   npm run build
   ```

5. Commit your changes with a clear message:
   ```bash
   git commit -m "Add: description of your changes"
   ```

6. Push to your fork and **submit a pull request**

## Code Style

- Use **TypeScript** for all new code
- Follow the existing code style and conventions
- Run linting before submitting (if configured)
- Keep functions small and focused

## Types

When adding new functionality:

1. Define TypeScript types first
2. Export types that users might need
3. Keep the API surface minimal

## Testing

- Add tests for new functionality
- Ensure existing tests pass
- Test both sync and async handlers

## Pull Request Guidelines

- **Branch**: Submit PRs to the `main` branch
- **Description**: Clearly describe the changes
- **Linked Issues**: Reference any related issues
- **Breaking Changes**: Document if applicable

## Reporting Issues

When reporting bugs or requesting features:

1. Check if the issue already exists
2. Provide a clear reproduction steps
3. Include relevant code samples
4. Specify your environment (Chrome version, OS, etc.)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
