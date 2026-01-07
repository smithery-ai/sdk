# DeployResponse

## Example Usage

```typescript
import { DeployResponse } from "@smithery/registry/models/components";

let value: DeployResponse = {
  deploymentId: "123e4567-e89b-12d3-a456-426614174000",
  status: "WORKING",
  mcpUrl: "https://server.smithery.ai/@org/name",
};
```

## Fields

| Field                                | Type                                 | Required                             | Description                          | Example                              |
| ------------------------------------ | ------------------------------------ | ------------------------------------ | ------------------------------------ | ------------------------------------ |
| `deploymentId`                       | *string*                             | :heavy_check_mark:                   | N/A                                  | 123e4567-e89b-12d3-a456-426614174000 |
| `status`                             | *string*                             | :heavy_check_mark:                   | N/A                                  | WORKING                              |
| `mcpUrl`                             | *string*                             | :heavy_check_mark:                   | N/A                                  | https://server.smithery.ai/@org/name |
| `warnings`                           | *string*[]                           | :heavy_minus_sign:                   | N/A                                  |                                      |