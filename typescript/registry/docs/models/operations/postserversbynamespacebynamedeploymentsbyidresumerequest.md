# PostServersByNamespaceByNameDeploymentsByIdResumeRequest

## Example Usage

```typescript
import { PostServersByNamespaceByNameDeploymentsByIdResumeRequest } from "@smithery/registry/models/operations";

let value: PostServersByNamespaceByNameDeploymentsByIdResumeRequest = {
  name: "<value>",
  id: "<id>",
};
```

## Fields

| Field                                                             | Type                                                              | Required                                                          | Description                                                       |
| ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| `namespace`                                                       | *string*                                                          | :heavy_check_mark:                                                | Server namespace (optional, leave empty for unnamespaced servers) |
| `name`                                                            | *string*                                                          | :heavy_check_mark:                                                | N/A                                                               |
| `id`                                                              | *string*                                                          | :heavy_check_mark:                                                | N/A                                                               |