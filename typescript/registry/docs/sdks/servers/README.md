# Servers

## Overview

Registry endpoints for listing and configuring servers

### Available Operations

* [deploy](#deploy) - Deploy an MCP server
* [listDeployments](#listdeployments) - List deployments for a server
* [getDeploymentStatus](#getdeploymentstatus) - Get deployment status
* [resumeDeployment](#resumedeployment) - Resume a paused deployment workflow (e.g., after OAuth authorization)
* [getLogs](#getlogs) - Get runtime logs for a server
* [getByQualifiedName](#getbyqualifiedname) - Get a server by qualified name
* [list](#list) - List all servers

## deploy

Upload and deploy an MCP server (hosted or external)

### Example Usage

<!-- UsageSnippet language="typescript" operationID="putServersByQualifiedNameDeployments" method="put" path="/servers/{qualifiedName}/deployments" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.servers.deploy({
    qualifiedName: "<value>",
  });

  console.log(result);
}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { serversDeploy } from "@smithery/registry/funcs/serversDeploy.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await serversDeploy(smitheryRegistry, {
    qualifiedName: "<value>",
  });
  if (res.ok) {
    const { value: result } = res;
    console.log(result);
  } else {
    console.log("serversDeploy failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.PutServersByQualifiedNameDeploymentsRequest](../../models/operations/putserversbyqualifiednamedeploymentsrequest.md)                                               | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[components.DeployResponse](../../models/components/deployresponse.md)\>**

### Errors

| Error Type             | Status Code            | Content Type           |
| ---------------------- | ---------------------- | ---------------------- |
| errors.DeploymentError | 400                    | application/json       |
| errors.APIError        | 4XX, 5XX               | \*/\*                  |

## listDeployments

List deployments for a server

### Example Usage

<!-- UsageSnippet language="typescript" operationID="getServersByQualifiedNameDeployments" method="get" path="/servers/{qualifiedName}/deployments" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.servers.listDeployments({
    qualifiedName: "<value>",
  });

  console.log(result);
}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { serversListDeployments } from "@smithery/registry/funcs/serversListDeployments.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await serversListDeployments(smitheryRegistry, {
    qualifiedName: "<value>",
  });
  if (res.ok) {
    const { value: result } = res;
    console.log(result);
  } else {
    console.log("serversListDeployments failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.GetServersByQualifiedNameDeploymentsRequest](../../models/operations/getserversbyqualifiednamedeploymentsrequest.md)                                               | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[components.DeploymentList[]](../../models/.md)\>**

### Errors

| Error Type             | Status Code            | Content Type           |
| ---------------------- | ---------------------- | ---------------------- |
| errors.DeploymentError | 403, 404               | application/json       |
| errors.APIError        | 4XX, 5XX               | \*/\*                  |

## getDeploymentStatus

Get deployment status

### Example Usage

<!-- UsageSnippet language="typescript" operationID="getServersByQualifiedNameDeploymentsById" method="get" path="/servers/{qualifiedName}/deployments/{id}" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.servers.getDeploymentStatus({
    qualifiedName: "<value>",
    id: "<id>",
  });

  console.log(result);
}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { serversGetDeploymentStatus } from "@smithery/registry/funcs/serversGetDeploymentStatus.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await serversGetDeploymentStatus(smitheryRegistry, {
    qualifiedName: "<value>",
    id: "<id>",
  });
  if (res.ok) {
    const { value: result } = res;
    console.log(result);
  } else {
    console.log("serversGetDeploymentStatus failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.GetServersByQualifiedNameDeploymentsByIdRequest](../../models/operations/getserversbyqualifiednamedeploymentsbyidrequest.md)                                       | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[components.DeploymentInfo](../../models/components/deploymentinfo.md)\>**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.APIError | 4XX, 5XX        | \*/\*           |

## resumeDeployment

Use id='latest' to resume the most recent deployment

### Example Usage

<!-- UsageSnippet language="typescript" operationID="postServersByQualifiedNameDeploymentsByIdResume" method="post" path="/servers/{qualifiedName}/deployments/{id}/resume" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  await smitheryRegistry.servers.resumeDeployment({
    qualifiedName: "<value>",
    id: "<id>",
  });


}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { serversResumeDeployment } from "@smithery/registry/funcs/serversResumeDeployment.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await serversResumeDeployment(smitheryRegistry, {
    qualifiedName: "<value>",
    id: "<id>",
  });
  if (res.ok) {
    const { value: result } = res;
    
  } else {
    console.log("serversResumeDeployment failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.PostServersByQualifiedNameDeploymentsByIdResumeRequest](../../models/operations/postserversbyqualifiednamedeploymentsbyidresumerequest.md)                         | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<void\>**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.APIError | 4XX, 5XX        | \*/\*           |

## getLogs

Fetch recent runtime logs for the server's deployed Worker, grouped by invocation (requires ownership).

### Example Usage

<!-- UsageSnippet language="typescript" operationID="getServersByQualifiedNameLogs" method="get" path="/servers/{qualifiedName}/logs" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.servers.getLogs({
    numberRootComponentsSchemasLogsQuery: {
      from: "2026-01-01T00:00:00Z",
      to: "2026-01-01T01:00:00Z",
      limit: 50,
    },
    qualifiedName: "<value>",
  });

  console.log(result);
}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { serversGetLogs } from "@smithery/registry/funcs/serversGetLogs.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await serversGetLogs(smitheryRegistry, {
    numberRootComponentsSchemasLogsQuery: {
      from: "2026-01-01T00:00:00Z",
      to: "2026-01-01T01:00:00Z",
      limit: 50,
    },
    qualifiedName: "<value>",
  });
  if (res.ok) {
    const { value: result } = res;
    console.log(result);
  } else {
    console.log("serversGetLogs failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.GetServersByQualifiedNameLogsRequest](../../models/operations/getserversbyqualifiednamelogsrequest.md)                                                             | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[components.RuntimeLogsResponse](../../models/components/runtimelogsresponse.md)\>**

### Errors

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.RuntimeLogsError | 403, 404                | application/json        |
| errors.RuntimeLogsError | 500                     | application/json        |
| errors.APIError         | 4XX, 5XX                | \*/\*                   |

## getByQualifiedName

Get a single server by its qualified name. The qualified name can be either 'name' (unnamespaced) or 'namespace/name' (namespaced).

### Example Usage

<!-- UsageSnippet language="typescript" operationID="getServersByQualifiedName" method="get" path="/servers/{qualifiedName}" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.servers.getByQualifiedName({
    qualifiedName: "<value>",
  });

  console.log(result);
}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { serversGetByQualifiedName } from "@smithery/registry/funcs/serversGetByQualifiedName.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await serversGetByQualifiedName(smitheryRegistry, {
    qualifiedName: "<value>",
  });
  if (res.ok) {
    const { value: result } = res;
    console.log(result);
  } else {
    console.log("serversGetByQualifiedName failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.GetServersByQualifiedNameRequest](../../models/operations/getserversbyqualifiednamerequest.md)                                                                     | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[components.Server](../../models/components/server.md)\>**

### Errors

| Error Type           | Status Code          | Content Type         |
| -------------------- | -------------------- | -------------------- |
| errors.RegistryError | 404                  | application/json     |
| errors.APIError      | 4XX, 5XX             | \*/\*                |

## list

Get a paginated list of all servers

### Example Usage

<!-- UsageSnippet language="typescript" operationID="getServers" method="get" path="/servers" -->
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

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { serversList } from "@smithery/registry/funcs/serversList.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await serversList(smitheryRegistry, {
    q: "search term",
  });
  if (res.ok) {
    const { value: result } = res;
    for await (const page of result) {
    console.log(page);
  }
  } else {
    console.log("serversList failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.GetServersRequest](../../models/operations/getserversrequest.md)                                                                                                   | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[operations.GetServersResponse](../../models/operations/getserversresponse.md)\>**

### Errors

| Error Type           | Status Code          | Content Type         |
| -------------------- | -------------------- | -------------------- |
| errors.RegistryError | 400, 401, 422        | application/json     |
| errors.APIError      | 4XX, 5XX             | \*/\*                |