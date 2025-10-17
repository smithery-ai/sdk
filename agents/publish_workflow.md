# Publishing Workflow - TypeScript SDK

This guide explains how the Smithery TypeScript SDK publishing workflow works and how to manage releases.

## Overview

The publishing workflow automatically publishes new versions to npm when version tags are pushed. It uses a tag-based approach with namespaced tags to avoid conflicts in the monorepo.

## Workflow Structure

### Triggers
- **Push namespaced tags (`typescript/sdk/v*`)** - Runs build, checks, and publishes to npm

### Jobs

#### 1. Build Job
```yaml
build:
  runs-on: ubuntu-latest
  steps:
    - Checkout code
    - Setup Node.js 22
    - Install dependencies (npm ci)
    - Build project (npm run build)
    - Run checks (npm run check - linting/formatting)
```

#### 2. Publish Job (After Build Passes)
```yaml
publish:
  runs-on: ubuntu-latest
  needs: build
  steps:
    - Checkout code
    - Setup Node.js with npm registry
    - Install dependencies
    - Publish to npm with provenance
```

## How to Publish

### Step-by-Step Process

```bash
# 1. Navigate to the SDK directory
cd typescript/sdk

# 2. Update version in package.json manually, or use npm version
npm version patch  # 1.6.8 → 1.6.9
# or
npm version minor  # 1.6.8 → 1.7.0
# or
npm version major  # 1.6.8 → 2.0.0

# 3. Get the new version
VERSION=$(node -p "require('./package.json').version")

# 4. Create and push namespaced tag (from repo root or sdk directory)
git tag typescript/sdk/v$VERSION && git push origin typescript/sdk/v$VERSION
```

### One-liner (from SDK directory)

```bash
npm version patch && git tag typescript/sdk/v$(node -p "require('./package.json').version") && git push origin typescript/sdk/v$(node -p "require('./package.json').version")
```

### Manual Tag Creation

If you've already updated `package.json` manually:

```bash
# Create and push the tag
git tag typescript/sdk/v1.7.0 && git push origin typescript/sdk/v1.7.0
```

### What happens automatically:
1. Tag push triggers GitHub workflow
2. Build job runs (install, build, checks)
3. If build passes, publish job runs and publishes to npm
4. Package appears on npm with provenance attestation

## Workflow Features

### Security
- **Provenance**: Uses `--provenance` flag for supply chain security
- **Access control**: Uses `--access public` for public packages
- **Token authentication**: Uses `NODE_AUTH_TOKEN` secret
- **Permissions**: Minimal required permissions (contents: read, id-token: write)

### Reliability
- **Dependency separation**: Build job must pass before publish
- **Concurrency control**: Prevents conflicting runs
- **Clean installs**: Uses `npm ci` for reproducible builds
- **Namespace isolation**: Uses `typescript/sdk/` prefix to avoid tag conflicts

## Environment Setup

### Required Secrets
- `NPM_TOKEN`: npm authentication token with publish permissions

### Node.js Version
- Uses Node.js 22
- Ensure your local environment matches for testing

## Troubleshooting

### Common Issues

1. **Publish fails with authentication error**
   - Check that `NPM_TOKEN` secret is set correctly
   - Verify token has publish permissions for @smithery/sdk

2. **Build fails before publish**
   - Check that all tests pass locally: `npm run build`
   - Ensure linting passes: `npm run check`

3. **Tag not triggering publish**
   - Ensure tag matches pattern: `typescript/sdk/v*`
   - Example: `typescript/sdk/v1.7.0` (NOT just `v1.7.0`)
   - Check that tag was pushed: `git push origin <tag>`

4. **Version conflicts**
   - Ensure the version doesn't already exist on npm
   - Check existing versions: `npm view @smithery/sdk versions --json`

5. **Wrong working directory**
   - Tags should be created from repo root or sdk directory
   - The workflow automatically sets working-directory to `typescript/sdk`

### Debugging Steps

1. **Check workflow runs**: Go to GitHub Actions tab
2. **Review build logs**: Look at both build and publish job logs
3. **Verify tag format**: Tags must match `typescript/sdk/v*` pattern
4. **Test locally**: 
   ```bash
   cd typescript/sdk
   npm ci
   npm run build
   npm run check
   ```

## Best Practices

1. **Always test locally** before creating tags
2. **Use semantic versioning** (patch/minor/major)
3. **Commit package.json changes** before creating tags
4. **Use namespaced tags** to avoid conflicts with other packages (Python SDK, CLI, etc.)
5. **Monitor npm** for successful publication after workflow completes
6. **Document breaking changes** in commit messages for major versions

## Integration with Development Workflow

1. **Feature development**: Work on feature branches
2. **Pull requests**: Create PRs to main
3. **Merge to main**: Merge PR after review
4. **Version bump**: Update version in `typescript/sdk/package.json`
5. **Create tag**: Use namespaced tag pattern `typescript/sdk/v*`
6. **Push tag**: Workflow triggers automatically

## Monorepo Considerations

Since the SDK lives in a monorepo with multiple packages:

- **Use namespaced tags**: `typescript/sdk/v*` prevents conflicts with:
  - Python SDK tags
  - CLI tags  
  - Registry client tags

- **Working directory**: Workflow automatically uses `typescript/sdk` as working directory

- **Independent versioning**: Each package can have its own version number

This workflow ensures reliable, automated publishing while maintaining quality through automated testing and builds.

