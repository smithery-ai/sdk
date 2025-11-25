# Profiles
(*profiles*)

## Overview

Endpoints for listing profiles and their servers

### Available Operations

* [list](#list) - List user profiles
* [listServers](#listservers) - List MCP servers for a profile
* [addServer](#addserver) - Save a server to a profile
* [getServer](#getserver) - Get a profile server
* [deleteServer](#deleteserver) - Delete a profile server

## list

List user profiles

### Example Usage

<!-- UsageSnippet language="typescript" operationID="getProfiles" method="get" path="/profiles" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.profiles.list({
    page: 1,
    pageSize: 10,
  });

  console.log(result);
}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { profilesList } from "@smithery/registry/funcs/profilesList.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await profilesList(smitheryRegistry, {
    page: 1,
    pageSize: 10,
  });
  if (res.ok) {
    const { value: result } = res;
    console.log(result);
  } else {
    console.log("profilesList failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.GetProfilesRequest](../../models/operations/getprofilesrequest.md)                                                                                                 | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[components.ProfilesResponse](../../models/components/profilesresponse.md)\>**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.APIError | 4XX, 5XX        | \*/\*           |

## listServers

List MCP servers for a profile

### Example Usage

<!-- UsageSnippet language="typescript" operationID="getProfilesBySlugServers" method="get" path="/profiles/{slug}/servers" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.profiles.listServers({
    page: 1,
    pageSize: 10,
    slug: "<value>",
  });

  console.log(result);
}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { profilesListServers } from "@smithery/registry/funcs/profilesListServers.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await profilesListServers(smitheryRegistry, {
    page: 1,
    pageSize: 10,
    slug: "<value>",
  });
  if (res.ok) {
    const { value: result } = res;
    console.log(result);
  } else {
    console.log("profilesListServers failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.GetProfilesBySlugServersRequest](../../models/operations/getprofilesbyslugserversrequest.md)                                                                       | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[components.ProfileServersResponse](../../models/components/profileserversresponse.md)\>**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.APIError | 4XX, 5XX        | \*/\*           |

## addServer

Save a server to a profile

### Example Usage

<!-- UsageSnippet language="typescript" operationID="postProfilesBySlugServers" method="post" path="/profiles/{slug}/servers" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.profiles.addServer({
    slug: "<value>",
  });

  console.log(result);
}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { profilesAddServer } from "@smithery/registry/funcs/profilesAddServer.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await profilesAddServer(smitheryRegistry, {
    slug: "<value>",
  });
  if (res.ok) {
    const { value: result } = res;
    console.log(result);
  } else {
    console.log("profilesAddServer failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.PostProfilesBySlugServersRequest](../../models/operations/postprofilesbyslugserversrequest.md)                                                                     | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[operations.PostProfilesBySlugServersResponse](../../models/operations/postprofilesbyslugserversresponse.md)\>**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.APIError | 4XX, 5XX        | \*/\*           |

## getServer

Get a profile server

### Example Usage

<!-- UsageSnippet language="typescript" operationID="getProfilesBySlugServersByConfigSlug" method="get" path="/profiles/{slug}/servers/{configSlug}" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.profiles.getServer({
    slug: "<value>",
    configSlug: "<value>",
  });

  console.log(result);
}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { profilesGetServer } from "@smithery/registry/funcs/profilesGetServer.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await profilesGetServer(smitheryRegistry, {
    slug: "<value>",
    configSlug: "<value>",
  });
  if (res.ok) {
    const { value: result } = res;
    console.log(result);
  } else {
    console.log("profilesGetServer failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.GetProfilesBySlugServersByConfigSlugRequest](../../models/operations/getprofilesbyslugserversbyconfigslugrequest.md)                                               | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[operations.GetProfilesBySlugServersByConfigSlugResponse](../../models/operations/getprofilesbyslugserversbyconfigslugresponse.md)\>**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.APIError | 4XX, 5XX        | \*/\*           |

## deleteServer

Delete a profile server

### Example Usage

<!-- UsageSnippet language="typescript" operationID="deleteProfilesBySlugServersByConfigSlug" method="delete" path="/profiles/{slug}/servers/{configSlug}" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  await smitheryRegistry.profiles.deleteServer({
    slug: "<value>",
    configSlug: "<value>",
  });


}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { profilesDeleteServer } from "@smithery/registry/funcs/profilesDeleteServer.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const res = await profilesDeleteServer(smitheryRegistry, {
    slug: "<value>",
    configSlug: "<value>",
  });
  if (res.ok) {
    const { value: result } = res;
    
  } else {
    console.log("profilesDeleteServer failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `request`                                                                                                                                                                      | [operations.DeleteProfilesBySlugServersByConfigSlugRequest](../../models/operations/deleteprofilesbyslugserversbyconfigslugrequest.md)                                         | :heavy_check_mark:                                                                                                                                                             | The request object to use for the request.                                                                                                                                     |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<void\>**

### Errors

| Error Type      | Status Code     | Content Type    |
| --------------- | --------------- | --------------- |
| errors.APIError | 4XX, 5XX        | \*/\*           |