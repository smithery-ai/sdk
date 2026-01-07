# GetServersByNamespaceByNameDeploymentsRequest

## Example Usage

```typescript
import { GetServersByNamespaceByNameDeploymentsRequest } from "@smithery/registry/models/operations";

let value: GetServersByNamespaceByNameDeploymentsRequest = {
  name: "<value>",
};
```

## Fields

| Field                                                             | Type                                                              | Required                                                          | Description                                                       |
| ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| `namespace`                                                       | *string*                                                          | :heavy_check_mark:                                                | Server namespace (optional, leave empty for unnamespaced servers) |
| `name`                                                            | *string*                                                          | :heavy_check_mark:                                                | N/A                                                               |