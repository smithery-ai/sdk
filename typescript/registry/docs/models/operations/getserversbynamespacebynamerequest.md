# GetServersByNamespaceByNameRequest

## Example Usage

```typescript
import { GetServersByNamespaceByNameRequest } from "@smithery/registry/models/operations";

let value: GetServersByNamespaceByNameRequest = {
  name: "<value>",
};
```

## Fields

| Field                                                             | Type                                                              | Required                                                          | Description                                                       |
| ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| `namespace`                                                       | *string*                                                          | :heavy_check_mark:                                                | Server namespace (optional, leave empty for unnamespaced servers) |
| `name`                                                            | *string*                                                          | :heavy_check_mark:                                                | N/A                                                               |