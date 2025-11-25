# Server

## Example Usage

```typescript
import { Server } from "@smithery/registry/models/components";

let value: Server = {
  qualifiedName: "smithery/hello-world",
  displayName: "Hello World",
  description: "A simple hello world server",
  iconUrl: "https://example.com/icon.png",
  remote: true,
  deploymentUrl: "https://api.example.com",
  connections: [],
  security: {
    scanPassed: true,
  },
  tools: [
    {
      name: "get_weather",
      description: "Get current weather",
      inputSchema: {},
    },
  ],
};
```

## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                | Example                                                    |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `qualifiedName`                                            | *string*                                                   | :heavy_check_mark:                                         | N/A                                                        | smithery/hello-world                                       |
| `displayName`                                              | *string*                                                   | :heavy_check_mark:                                         | N/A                                                        | Hello World                                                |
| `description`                                              | *string*                                                   | :heavy_check_mark:                                         | N/A                                                        | A simple hello world server                                |
| `iconUrl`                                                  | *string*                                                   | :heavy_check_mark:                                         | N/A                                                        | https://example.com/icon.png                               |
| `remote`                                                   | *boolean*                                                  | :heavy_check_mark:                                         | N/A                                                        | true                                                       |
| `deploymentUrl`                                            | *string*                                                   | :heavy_check_mark:                                         | N/A                                                        | https://api.example.com                                    |
| `connections`                                              | *components.Connection*[]                                  | :heavy_check_mark:                                         | N/A                                                        |                                                            |
| `security`                                                 | [components.Security](../../models/components/security.md) | :heavy_check_mark:                                         | N/A                                                        |                                                            |
| `tools`                                                    | [components.Tool](../../models/components/tool.md)[]       | :heavy_check_mark:                                         | N/A                                                        |                                                            |