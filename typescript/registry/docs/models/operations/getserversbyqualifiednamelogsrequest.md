# GetServersByQualifiedNameLogsRequest

## Example Usage

```typescript
import { GetServersByQualifiedNameLogsRequest } from "@smithery/registry/models/operations";

let value: GetServersByQualifiedNameLogsRequest = {
  numberRootComponentsSchemasLogsQuery: {
    from: "2026-01-01T00:00:00Z",
    to: "2026-01-01T01:00:00Z",
    limit: 50,
  },
  qualifiedName: "<value>",
};
```

## Fields

| Field                                                        | Type                                                         | Required                                                     | Description                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `numberRootComponentsSchemasLogsQuery`                       | [components.LogsQuery](../../models/components/logsquery.md) | :heavy_minus_sign:                                           | N/A                                                          |
| `qualifiedName`                                              | *string*                                                     | :heavy_check_mark:                                           | N/A                                                          |