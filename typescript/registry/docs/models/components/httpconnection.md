# HttpConnection

## Example Usage

```typescript
import { HttpConnection } from "@smithery/registry/models/components";

let value: HttpConnection = {
  type: "http",
  deploymentUrl: "https://vivacious-divine.name/",
  configSchema: {
    "key": "<value>",
    "key1": "<value>",
    "key2": "<value>",
  },
};
```

## Fields

| Field                 | Type                  | Required              | Description           |
| --------------------- | --------------------- | --------------------- | --------------------- |
| `type`                | *"http"*              | :heavy_check_mark:    | N/A                   |
| `deploymentUrl`       | *string*              | :heavy_check_mark:    | N/A                   |
| `configSchema`        | Record<string, *any*> | :heavy_check_mark:    | N/A                   |