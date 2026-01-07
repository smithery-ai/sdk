# StdioConnection

## Example Usage

```typescript
import { StdioConnection } from "@smithery/registry/models/components";

let value: StdioConnection = {
  type: "stdio",
  configSchema: {
    "key": "<value>",
  },
};
```

## Fields

| Field                 | Type                  | Required              | Description           |
| --------------------- | --------------------- | --------------------- | --------------------- |
| `type`                | *"stdio"*             | :heavy_check_mark:    | N/A                   |
| `bundleUrl`           | *string*              | :heavy_minus_sign:    | N/A                   |
| `runtime`             | *string*              | :heavy_minus_sign:    | N/A                   |
| `stdioFunction`       | *string*              | :heavy_minus_sign:    | N/A                   |
| `configSchema`        | Record<string, *any*> | :heavy_check_mark:    | N/A                   |