# GetServersByNamespaceByNameLogsRequest

## Example Usage

```typescript
import { GetServersByNamespaceByNameLogsRequest } from "@smithery/registry/models/operations";

let value: GetServersByNamespaceByNameLogsRequest = {
  numberRootComponentsSchemasLogsQuery: {
    from: "2026-01-01T00:00:00Z",
    to: "2026-01-01T01:00:00Z",
    limit: 50,
  },
  name: "<value>",
};
```

## Fields

| Field                                                             | Type                                                              | Required                                                          | Description                                                       |
| ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| `numberRootComponentsSchemasLogsQuery`                            | [components.LogsQuery](../../models/components/logsquery.md)      | :heavy_minus_sign:                                                | N/A                                                               |
| `namespace`                                                       | *string*                                                          | :heavy_check_mark:                                                | Server namespace (optional, leave empty for unnamespaced servers) |
| `name`                                                            | *string*                                                          | :heavy_check_mark:                                                | N/A                                                               |