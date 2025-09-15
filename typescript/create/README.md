# create-smithery

The official CLI to get started with [Smithery](https://www.smithery.ai/).

This package helps you set up a new Smithery project for building MCPs.

## Usage

To create a new Smithery project, run the following command in your terminal:

```bash
npm create smithery
```

You will be prompted to enter a name for your project. A new directory will be created with that name, containing a basic Smithery project structure.

Alternatively, you can specify the project name directly:

```bash
npm create smithery <your-project-name>
```

### Package Manager

You can specify a package manager to use for installing dependencies. By default, it uses `npm`.

To use a different package manager, use the `--package-manager` flag:

```bash
npm create smithery -- --package-manager <yarn|pnpm|bun>
```
Note the extra `--` which is needed to pass flags to the underlying script.

## Development

To work on this package locally:

1. Clone the repository.
2. Run `npm install` to install dependencies.
3. Run `npm run build` to build the project.
4. To test your local changes, you can run `node dist/index.js <test-project-name>`.
