# @smithery/registry

Developer-friendly & type-safe Typescript SDK specifically catered to leverage *@smithery/registry* API.

<div align="left">
    <a href="https://www.speakeasy.com/?utm_source=@smithery/registry&utm_campaign=typescript"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-blue.svg" style="width: 100px; height: 28px;" />
    </a>
</div>


<br /><br />

<!-- Start Summary [summary] -->
## Summary

Smithery Platform API: Smithery API for managing servers and deployments.
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [@smithery/registry](#smitheryregistry)
  * [SDK Installation](#sdk-installation)
  * [Requirements](#requirements)
  * [SDK Example Usage](#sdk-example-usage)
  * [Authentication](#authentication)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [Standalone functions](#standalone-functions)
  * [Pagination](#pagination)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Server Selection](#server-selection)
  * [Custom HTTP Client](#custom-http-client)
  * [Debugging](#debugging)
* [Development](#development)
  * [Maturity](#maturity)
  * [Contributions](#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

The SDK can be installed with either [npm](https://www.npmjs.com/), [pnpm](https://pnpm.io/), [bun](https://bun.sh/) or [yarn](https://classic.yarnpkg.com/en/) package managers.

### NPM

```bash
npm add @smithery/registry
```

### PNPM

```bash
pnpm add @smithery/registry
```

### Bun

```bash
bun add @smithery/registry
```

### Yarn

```bash
yarn add @smithery/registry
```

> [!NOTE]
> This package is published with CommonJS and ES Modules (ESM) support.
<!-- End SDK Installation [installation] -->

<!-- Start Requirements [requirements] -->
## Requirements

For supported JavaScript runtimes, please consult [RUNTIMES.md](RUNTIMES.md).
<!-- End Requirements [requirements] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.service.healthCheck();

  console.log(result);
}

run();

```
<!-- End SDK Example Usage [usage] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name         | Type | Scheme      | Environment Variable   |
| ------------ | ---- | ----------- | ---------------------- |
| `bearerAuth` | http | HTTP Bearer | `SMITHERY_BEARER_AUTH` |

To authenticate with the API the `bearerAuth` parameter must be set when initializing the SDK client instance. For example:
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.service.healthCheck();

  console.log(result);
}

run();

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [Servers](docs/sdks/servers/README.md)

* [deploy](docs/sdks/servers/README.md#deploy) - Deploy an MCP server
* [listDeployments](docs/sdks/servers/README.md#listdeployments) - List deployments for a server
* [getDeploymentStatus](docs/sdks/servers/README.md#getdeploymentstatus) - Get deployment status
* [resumeDeployment](docs/sdks/servers/README.md#resumedeployment) - Resume a paused deployment workflow (e.g., after OAuth authorization)
* [getLogs](docs/sdks/servers/README.md#getlogs) - Get runtime logs for a server
* [get](docs/sdks/servers/README.md#get) - Get a server by qualified name
* [list](docs/sdks/servers/README.md#list) - List all servers

### [Service](docs/sdks/service/README.md)

* [healthCheck](docs/sdks/service/README.md#healthcheck) - Health check

### [Uplink](docs/sdks/uplink/README.md)

* [createToken](docs/sdks/uplink/README.md#createtoken) - Create uplink token

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Standalone functions [standalone-funcs] -->
## Standalone functions

All the methods listed above are available as standalone functions. These
functions are ideal for use in applications running in the browser, serverless
runtimes or other environments where application bundle size is a primary
concern. When using a bundler to build your application, all unused
functionality will be either excluded from the final bundle or tree-shaken away.

To read more about standalone functions, check [FUNCTIONS.md](./FUNCTIONS.md).

<details>

<summary>Available standalone functions</summary>

- [`serversDeploy`](docs/sdks/servers/README.md#deploy) - Deploy an MCP server
- [`serversGet`](docs/sdks/servers/README.md#get) - Get a server by qualified name
- [`serversGetDeploymentStatus`](docs/sdks/servers/README.md#getdeploymentstatus) - Get deployment status
- [`serversGetLogs`](docs/sdks/servers/README.md#getlogs) - Get runtime logs for a server
- [`serversList`](docs/sdks/servers/README.md#list) - List all servers
- [`serversListDeployments`](docs/sdks/servers/README.md#listdeployments) - List deployments for a server
- [`serversResumeDeployment`](docs/sdks/servers/README.md#resumedeployment) - Resume a paused deployment workflow (e.g., after OAuth authorization)
- [`serviceHealthCheck`](docs/sdks/service/README.md#healthcheck) - Health check
- [`uplinkCreateToken`](docs/sdks/uplink/README.md#createtoken) - Create uplink token

</details>
<!-- End Standalone functions [standalone-funcs] -->

<!-- Start Pagination [pagination] -->
## Pagination

Some of the endpoints in this SDK support pagination. To use pagination, you
make your SDK calls as usual, but the returned response object will also be an
async iterable that can be consumed using the [`for await...of`][for-await-of]
syntax.

[for-await-of]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for-await...of

Here's an example of one such pagination call:

```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.servers.list({
    q: "search term",
  });

  for await (const page of result) {
    console.log(page);
  }
}

run();

```
<!-- End Pagination [pagination] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries.  If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API.  However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a retryConfig object to the call:
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.service.healthCheck({
    retries: {
      strategy: "backoff",
      backoff: {
        initialInterval: 1,
        maxInterval: 50,
        exponent: 1.1,
        maxElapsedTime: 100,
      },
      retryConnectionErrors: false,
    },
  });

  console.log(result);
}

run();

```

If you'd like to override the default retry strategy for all operations that support retries, you can provide a retryConfig at SDK initialization:
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  retryConfig: {
    strategy: "backoff",
    backoff: {
      initialInterval: 1,
      maxInterval: 50,
      exponent: 1.1,
      maxElapsedTime: 100,
    },
    retryConnectionErrors: false,
  },
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.service.healthCheck();

  console.log(result);
}

run();

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

[`SmitheryRegistryError`](./src/models/errors/smitheryregistryerror.ts) is the base class for all HTTP error responses. It has the following properties:

| Property            | Type       | Description                                                                             |
| ------------------- | ---------- | --------------------------------------------------------------------------------------- |
| `error.message`     | `string`   | Error message                                                                           |
| `error.statusCode`  | `number`   | HTTP response status code eg `404`                                                      |
| `error.headers`     | `Headers`  | HTTP response headers                                                                   |
| `error.body`        | `string`   | HTTP body. Can be empty string if no body is returned.                                  |
| `error.rawResponse` | `Response` | Raw HTTP response                                                                       |
| `error.data$`       |            | Optional. Some errors may contain structured data. [See Error Classes](#error-classes). |

### Example
```typescript
import { SmitheryRegistry } from "@smithery/registry";
import * as errors from "@smithery/registry/models/errors";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  try {
    const result = await smitheryRegistry.service.healthCheck();

    console.log(result);
  } catch (error) {
    // The base class for HTTP error responses
    if (error instanceof errors.SmitheryRegistryError) {
      console.log(error.message);
      console.log(error.statusCode);
      console.log(error.body);
      console.log(error.headers);

      // Depending on the method different errors may be thrown
      if (error instanceof errors.HealthError) {
        console.log(error.data$.error); // string
      }
    }
  }
}

run();

```

### Error Classes
**Primary error:**
* [`SmitheryRegistryError`](./src/models/errors/smitheryregistryerror.ts): The base class for HTTP error responses.

<details><summary>Less common errors (12)</summary>

<br />

**Network errors:**
* [`ConnectionError`](./src/models/errors/httpclienterrors.ts): HTTP client was unable to make a request to a server.
* [`RequestTimeoutError`](./src/models/errors/httpclienterrors.ts): HTTP request timed out due to an AbortSignal signal.
* [`RequestAbortedError`](./src/models/errors/httpclienterrors.ts): HTTP request was aborted by the client.
* [`InvalidRequestError`](./src/models/errors/httpclienterrors.ts): Any input used to create a request is invalid.
* [`UnexpectedClientError`](./src/models/errors/httpclienterrors.ts): Unrecognised or unexpected error.


**Inherit from [`SmitheryRegistryError`](./src/models/errors/smitheryregistryerror.ts)**:
* [`DeploymentError`](./src/models/errors/deploymenterror.ts): Applicable to 4 of 9 methods.*
* [`ServersListError`](./src/models/errors/serverslisterror.ts): Bad request. Applicable to 1 of 9 methods.*
* [`UplinkError`](./src/models/errors/uplinkerror.ts): Unauthorized - Missing API key. Applicable to 1 of 9 methods.*
* [`RuntimeLogsError`](./src/models/errors/runtimelogserror.ts): Forbidden. Applicable to 1 of 9 methods.*
* [`RegistryError`](./src/models/errors/registryerror.ts): Server not found. Status code `404`. Applicable to 1 of 9 methods.*
* [`HealthError`](./src/models/errors/healtherror.ts): Service unhealthy. Status code `500`. Applicable to 1 of 9 methods.*
* [`ResponseValidationError`](./src/models/errors/responsevalidationerror.ts): Type mismatch between the data returned from the server and the structure expected by the SDK. See `error.rawValue` for the raw value and `error.pretty()` for a nicely formatted multi-line string.

</details>

\* Check [the method documentation](#available-resources-and-operations) to see if the error is applicable.
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `serverURL: string` optional parameter when initializing the SDK client instance. For example:
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  serverURL: "https://registry.smithery.ai",
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.service.healthCheck();

  console.log(result);
}

run();

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The TypeScript SDK makes API calls using an `HTTPClient` that wraps the native
[Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API). This
client is a thin wrapper around `fetch` and provides the ability to attach hooks
around the request lifecycle that can be used to modify the request or handle
errors and response.

The `HTTPClient` constructor takes an optional `fetcher` argument that can be
used to integrate a third-party HTTP client or when writing tests to mock out
the HTTP client and feed in fixtures.

The following example shows how to use the `"beforeRequest"` hook to to add a
custom header and a timeout to requests and how to use the `"requestError"` hook
to log errors:

```typescript
import { SmitheryRegistry } from "@smithery/registry";
import { HTTPClient } from "@smithery/registry/lib/http";

const httpClient = new HTTPClient({
  // fetcher takes a function that has the same signature as native `fetch`.
  fetcher: (request) => {
    return fetch(request);
  }
});

httpClient.addHook("beforeRequest", (request) => {
  const nextRequest = new Request(request, {
    signal: request.signal || AbortSignal.timeout(5000)
  });

  nextRequest.headers.set("x-custom-header", "custom value");

  return nextRequest;
});

httpClient.addHook("requestError", (error, request) => {
  console.group("Request Error");
  console.log("Reason:", `${error}`);
  console.log("Endpoint:", `${request.method} ${request.url}`);
  console.groupEnd();
});

const sdk = new SmitheryRegistry({ httpClient: httpClient });
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass a logger that matches `console`'s interface as an SDK option.

> [!WARNING]
> Beware that debug logging will reveal secrets, like API tokens in headers, in log messages printed to a console or files. It's recommended to use this feature only during local development and not in production.

```typescript
import { SmitheryRegistry } from "@smithery/registry";

const sdk = new SmitheryRegistry({ debugLogger: console });
```

You can also enable a default debug logger by setting an environment variable `SMITHERY_DEBUG` to true.
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=@smithery/registry&utm_campaign=typescript)
