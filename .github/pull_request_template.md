## Summary
Explain what this PR does and why it exists.

## Type of change
- [ ] Bug fix
- [ ] New feature
- [ ] Refactor
- [ ] Performance
- [ ] Build / CI
- [ ] Documentation

## Implementation detail
Anything reviewers should pay attention to (design decisions, edge cases).

## Testing
- [ ] Tests added or updated
- [ ] Existing tests pass
- [ ] No tests (explaiun why)

Commands used:
```bash
cmake -S . -B build -SPHYSIM_TESTING=ON
cmake --build build --parallel
ctest --test-dir build --output-on-failure
