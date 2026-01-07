# DeploymentInfo

## Example Usage

```typescript
import { DeploymentInfo } from "@smithery/registry/models/components";

let value: DeploymentInfo = {
  id: "f4b417b2-fed7-41cb-9518-1f170bf00595",
  status: "<value>",
  createdAt: "1726332567632",
  updatedAt: "1735630963758",
};
```

## Fields

| Field                                                                            | Type                                                                             | Required                                                                         | Description                                                                      |
| -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `id`                                                                             | *string*                                                                         | :heavy_check_mark:                                                               | N/A                                                                              |
| `status`                                                                         | *string*                                                                         | :heavy_check_mark:                                                               | N/A                                                                              |
| `logs`                                                                           | [components.DeploymentLogEntry](../../models/components/deploymentlogentry.md)[] | :heavy_minus_sign:                                                               | N/A                                                                              |
| `mcpUrl`                                                                         | *string*                                                                         | :heavy_minus_sign:                                                               | N/A                                                                              |
| `createdAt`                                                                      | *string*                                                                         | :heavy_check_mark:                                                               | N/A                                                                              |
| `updatedAt`                                                                      | *string*                                                                         | :heavy_check_mark:                                                               | N/A                                                                              |