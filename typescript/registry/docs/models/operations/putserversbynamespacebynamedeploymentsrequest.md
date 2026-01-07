# PutServersByNamespaceByNameDeploymentsRequest

## Example Usage

```typescript
import { PutServersByNamespaceByNameDeploymentsRequest } from "@smithery/registry/models/operations";

let value: PutServersByNamespaceByNameDeploymentsRequest = {
  name: "<value>",
};
```

## Fields

| Field                                                                | Type                                                                 | Required                                                             | Description                                                          |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `namespace`                                                          | *string*                                                             | :heavy_check_mark:                                                   | Server namespace (optional, leave empty for unnamespaced servers)    |
| `name`                                                               | *string*                                                             | :heavy_check_mark:                                                   | N/A                                                                  |
| `deployRequest`                                                      | [components.DeployRequest](../../models/components/deployrequest.md) | :heavy_minus_sign:                                                   | N/A                                                                  |