# Uplink
(*uplink*)

## Overview

Endpoints for managing uplink tokens

### Available Operations

* [createToken](#createtoken) - Create uplink token

## createToken

Create or retrieve an authtoken for uplink connections

### Example Usage

<!-- UsageSnippet language="typescript" operationID="postUplinkToken" method="post" path="/uplink/token" -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry();

async function run() {
  const result = await smitheryRegistry.uplink.createToken();

  console.log(result);
}

run();
```

### Standalone function

The standalone function version of this method:

```typescript
import { SmitheryRegistryCore } from "@smithery/registry/core.js";
import { uplinkCreateToken } from "@smithery/registry/funcs/uplinkCreateToken.js";

// Use `SmitheryRegistryCore` for best tree-shaking performance.
// You can create one instance of it to use across an application.
const smitheryRegistry = new SmitheryRegistryCore();

async function run() {
  const res = await uplinkCreateToken(smitheryRegistry);
  if (res.ok) {
    const { value: result } = res;
    console.log(result);
  } else {
    console.log("uplinkCreateToken failed:", res.error);
  }
}

run();
```

### Parameters

| Parameter                                                                                                                                                                      | Type                                                                                                                                                                           | Required                                                                                                                                                                       | Description                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `options`                                                                                                                                                                      | RequestOptions                                                                                                                                                                 | :heavy_minus_sign:                                                                                                                                                             | Used to set various options for making HTTP requests.                                                                                                                          |
| `options.fetchOptions`                                                                                                                                                         | [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/Request/Request#options)                                                                                        | :heavy_minus_sign:                                                                                                                                                             | Options that are passed to the underlying HTTP request. This can be used to inject extra headers for examples. All `Request` options, except `method` and `body`, are allowed. |
| `options.retries`                                                                                                                                                              | [RetryConfig](../../lib/utils/retryconfig.md)                                                                                                                                  | :heavy_minus_sign:                                                                                                                                                             | Enables retrying HTTP requests under certain failure conditions.                                                                                                               |

### Response

**Promise\<[components.UplinkTokenResponse](../../models/components/uplinktokenresponse.md)\>**

### Errors

| Error Type         | Status Code        | Content Type       |
| ------------------ | ------------------ | ------------------ |
| errors.UplinkError | 401                | application/json   |
| errors.UplinkError | 500                | application/json   |
| errors.APIError    | 4XX, 5XX           | \*/\*              |