# ServerSummary

## Example Usage

```typescript
import { ServerSummary } from "@smithery/registry/models/components";

let value: ServerSummary = {
  qualifiedName: "smithery/hello-world",
  displayName: "Hello World",
  description: "A simple hello world server",
  iconUrl: "https://example.com/icon.png",
  verified: true,
  useCount: 42,
  remote: true,
  isDeployed: true,
  createdAt: "1704751079122",
  homepage: "https://smithery.ai/server/smithery/hello-world",
};
```

## Fields

| Field                                           | Type                                            | Required                                        | Description                                     | Example                                         |
| ----------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- |
| `qualifiedName`                                 | *string*                                        | :heavy_check_mark:                              | N/A                                             | smithery/hello-world                            |
| `displayName`                                   | *string*                                        | :heavy_check_mark:                              | N/A                                             | Hello World                                     |
| `description`                                   | *string*                                        | :heavy_check_mark:                              | N/A                                             | A simple hello world server                     |
| `iconUrl`                                       | *string*                                        | :heavy_check_mark:                              | N/A                                             | https://example.com/icon.png                    |
| `verified`                                      | *boolean*                                       | :heavy_check_mark:                              | N/A                                             | true                                            |
| `useCount`                                      | *number*                                        | :heavy_check_mark:                              | N/A                                             | 42                                              |
| `remote`                                        | *boolean*                                       | :heavy_check_mark:                              | N/A                                             | true                                            |
| `isDeployed`                                    | *boolean*                                       | :heavy_check_mark:                              | N/A                                             | true                                            |
| `createdAt`                                     | *string*                                        | :heavy_check_mark:                              | N/A                                             |                                                 |
| `homepage`                                      | *string*                                        | :heavy_check_mark:                              | N/A                                             | https://smithery.ai/server/smithery/hello-world |