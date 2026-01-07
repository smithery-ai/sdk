# Servers

## Overview

Registry endpoints for listing and configuring servers

### Available Operations

* [deploy](#deploy) - Deploy an MCP server
* [listDeployments](#listdeployments) - List deployments for a server
* [getDeploymentStatus](#getdeploymentstatus) - Get deployment status
* [resumeDeployment](#resumedeployment) - Resume a paused deployment workflow (e.g., after OAuth authorization)
* [getLogs](#getlogs) - Get runtime logs for a server
* [get](#get) - Get a server by qualified name
* [list](#list) - List all servers

## deploy

Upload and deploy an MCP server (hosted or external)

### Example Usage

<!-- UsageSnippet language="typescript" operationID="putServersByNamespaceByNameDeployments" method="put" path="/servers/{namespace}/{name}/deployments" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.servers.deploy({
    name: "<value>",
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
    name: "<value>",
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
| `request`                                                                                                                                                                      | [operations.PutServersByNamespaceByNameDeploymentsRequest](../../models/operations/putserversbynamespacebynamedeploymentsrequest.md)                                           | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
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

<!-- UsageSnippet language="typescript" operationID="getServersByNamespaceByNameDeployments" method="get" path="/servers/{namespace}/{name}/deployments" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.servers.listDeployments({
    name: "<value>",
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
    name: "<value>",
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
| `request`                                                                                                                                                                      | [operations.GetServersByNamespaceByNameDeploymentsRequest](../../models/operations/getserversbynamespacebynamedeploymentsrequest.md)                                           | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
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

<!-- UsageSnippet language="typescript" operationID="getServersByNamespaceByNameDeploymentsById" method="get" path="/servers/{namespace}/{name}/deployments/{id}" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.servers.getDeploymentStatus({
    name: "<value>",
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
    name: "<value>",
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
| `request`                                                                                                                                                                      | [operations.GetServersByNamespaceByNameDeploymentsByIdRequest](../../models/operations/getserversbynamespacebynamedeploymentsbyidrequest.md)                                   | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[components.DeploymentInfo](../../models/components/deploymentinfo.md)\>**

### Errors

| Error Type             | Status Code            | Content Type           |
| ---------------------- | ---------------------- | ---------------------- |
| errors.DeploymentError | 403, 404               | application/json       |
| errors.APIError        | 4XX, 5XX               | \*/\*                  |

## resumeDeployment

Use id='latest' to resume the most recent deployment

### Example Usage

<!-- UsageSnippet language="typescript" operationID="postServersByNamespaceByNameDeploymentsByIdResume" method="post" path="/servers/{namespace}/{name}/deployments/{id}/resume" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.servers.resumeDeployment({
    name: "<value>",
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
import { serversResumeDeployment } from "@smithery/registry/funcs/serversResumeDeployment.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await serversResumeDeployment(smitheryRegistry, {
    name: "<value>",
    id: "<id>",
  });
  if (res.ok) {
    const { value: result } = res;
    console.log(result);
  } else {
    console.log("serversResumeDeployment failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.PostServersByNamespaceByNameDeploymentsByIdResumeRequest](../../models/operations/postserversbynamespacebynamedeploymentsbyidresumerequest.md)                     | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[components.ResumeResponse](../../models/components/resumeresponse.md)\>**

### Errors

| Error Type             | Status Code            | Content Type           |
| ---------------------- | ---------------------- | ---------------------- |
| errors.DeploymentError | 400, 403, 404          | application/json       |
| errors.APIError        | 4XX, 5XX               | \*/\*                  |

## getLogs

Fetch recent runtime logs for the server's deployed Worker, grouped by invocation (requires ownership).

### Example Usage

<!-- UsageSnippet language="typescript" operationID="getServersByNamespaceByNameLogs" method="get" path="/servers/{namespace}/{name}/logs" -->
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
    name: "<value>",
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
    name: "<value>",
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
| `request`                                                                                                                                                                      | [operations.GetServersByNamespaceByNameLogsRequest](../../models/operations/getserversbynamespacebynamelogsrequest.md)                                                         | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
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

## get

Get a single server by its qualified name. The qualified name can be either 'name' (unnamespaced) or 'namespace/name' (namespaced).

### Example Usage

<!-- UsageSnippet language="typescript" operationID="getServersByNamespaceByName" method="get" path="/servers/{namespace}/{name}" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.servers.get({
    name: "<value>",
  });

  console.log(result);
}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { serversGet } from "@smithery/registry/funcs/serversGet.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await serversGet(smitheryRegistry, {
    name: "<value>",
  });
  if (res.ok) {
    const { value: result } = res;
    console.log(result);
  } else {
    console.log("serversGet failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.GetServersByNamespaceByNameRequest](../../models/operations/getserversbynamespacebynamerequest.md)                                                                 | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
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

| Error Type              | Status Code             | Content Type            |
| ----------------------- | ----------------------- | ----------------------- |
| errors.ServersListError | 400, 401, 422           | application/json        |
| errors.APIError         | 4XX, 5XX                | \*/\*                   |