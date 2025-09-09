---
name: APK Build Issue
about: Report issues with Android APK building
title: '[BUILD] APK Build Issue: '
labels: build, android
assignees: ''

---

## Build Issue Description
A clear and concise description of the build problem.

## Build Method
- [ ] GitHub Actions workflow
- [ ] Local build (Linux/macOS)
- [ ] Local build (Windows)
- [ ] Docker build

## Workflow/Script Used
Which workflow or script failed?
- [ ] build-apk.yml (main)
- [ ] build-apk-docker.yml
- [ ] build-apk-specialized.yml  
- [ ] build-apk-comprehensive.yml
- [ ] build-apk-reliable.yml
- [ ] Local script (build_apk.sh/build_apk.ps1)

## Error Message
```
Paste the error message or build log here
```

## System Information
**For local builds:**
- OS: [e.g. Windows 11, Ubuntu 20.04]
- Python version: [e.g. 3.11.0]
- Java version: [e.g. OpenJDK 17]
- Buildozer version: [e.g. 1.5.0]

**For GitHub Actions:**
- Link to failed workflow run
- Workflow file that failed

## Build Configuration
- [ ] Using default buildozer.spec
- [ ] Using buildozer-flet.spec
- [ ] Custom configuration (please describe)

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
A clear and concise description of what you expected to happen.

## Additional Context
Add any other context about the problem here, such as:
- Recent changes made
- Whether this worked before
- Any modifications to configuration files
