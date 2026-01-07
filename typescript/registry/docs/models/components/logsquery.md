# LogsQuery

## Example Usage

```typescript
import { LogsQuery } from "@smithery/registry/models/components";

let value: LogsQuery = {
  from: "2026-01-01T00:00:00Z",
  to: "2026-01-01T01:00:00Z",
  limit: 50,
};
```

## Fields

| Field                                      | Type                                       | Required                                   | Description                                | Example                                    |
| ------------------------------------------ | ------------------------------------------ | ------------------------------------------ | ------------------------------------------ | ------------------------------------------ |
| `from`                                     | *string*                                   | :heavy_minus_sign:                         | Start of time range (ISO 8601).            | 2026-01-01T00:00:00Z                       |
| `to`                                       | *string*                                   | :heavy_minus_sign:                         | End of time range (ISO 8601).              | 2026-01-01T01:00:00Z                       |
| `limit`                                    | *number*                                   | :heavy_minus_sign:                         | Max invocations to return. Defaults to 50. | 50                                         |