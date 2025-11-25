# ConfigResponse

## Example Usage

```typescript
import { ConfigResponse } from "@smithery/registry/models/components";

let value: ConfigResponse = {
  success: true,
  result: {
    command: "npx",
    args: [
      "@smithery/hello-world",
      "--config",
      "{}",
    ],
    env: {
      "NODE_ENV": "production",
    },
  },
};
```

## Fields

| Field                                                  | Type                                                   | Required                                               | Description                                            | Example                                                |
| ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ |
| `success`                                              | *boolean*                                              | :heavy_check_mark:                                     | N/A                                                    | true                                                   |
| `result`                                               | [components.Result](../../models/components/result.md) | :heavy_check_mark:                                     | N/A                                                    |                                                        |