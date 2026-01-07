# RuntimeLogsResponse

## Example Usage

```typescript
import { RuntimeLogsResponse } from "@smithery/registry/models/components";

let value: RuntimeLogsResponse = {
  invocations: [],
  total: 6452.1,
};
```

## Fields

| Field                                                            | Type                                                             | Required                                                         | Description                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| `invocations`                                                    | [components.Invocation](../../models/components/invocation.md)[] | :heavy_check_mark:                                               | N/A                                                              |
| `total`                                                          | *number*                                                         | :heavy_check_mark:                                               | Total invocations matching query                                 |