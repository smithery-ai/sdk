# ServerDetailResponse

## Example Usage

```typescript
import { ServerDetailResponse } from "@smithery/registry/models/components";

let value: ServerDetailResponse = {
  qualifiedName: "smithery-ai/fetch",
  displayName: "Fetch",
  iconUrl: "https://example.com/icon.png",
  remote: true,
  connections: [
    {
      type: "http",
      url: "https://api.smithery.ai/mcp/fetch",
      configSchema: {
        "type": "object",
        "properties": {
          "apiKey": {
            "type": "string",
            "description": "API key for authentication",
          },
        },
        "required": [
          "apiKey",
        ],
      },
      published: true,
      stdioFunction: "run_server",
    },
  ],
  security: {
    scanPassed: true,
  },
  tools: [
    {
      name: "fetch_url",
      description: "Fetches content from a URL",
      inputSchema: {
        type: "object",
        properties: {
          "url": {
            "type": "string",
            "description": "URL to fetch content from",
          },
        },
        additionalProperties: {
          "required": [
            "url",
          ],
        },
      },
    },
  ],
};
```

## Fields

| Field                                                                                              | Type                                                                                               | Required                                                                                           | Description                                                                                        | Example                                                                                            |
| -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `qualifiedName`                                                                                    | *string*                                                                                           | :heavy_check_mark:                                                                                 | Qualified name of the MCP server in the format `owner/repository`                                  | smithery-ai/fetch                                                                                  |
| `displayName`                                                                                      | *string*                                                                                           | :heavy_check_mark:                                                                                 | Human-readable name of the MCP server                                                              | Fetch                                                                                              |
| `iconUrl`                                                                                          | *string*                                                                                           | :heavy_minus_sign:                                                                                 | URL to the server's icon image                                                                     | https://example.com/icon.png                                                                       |
| `remote`                                                                                           | *boolean*                                                                                          | :heavy_minus_sign:                                                                                 | Whether this server is a remote server                                                             | true                                                                                               |
| `connections`                                                                                      | [components.ConnectionInfo](../../models/components/connectioninfo.md)[]                           | :heavy_check_mark:                                                                                 | Specifies how to connect to this server                                                            |                                                                                                    |
| `security`                                                                                         | [components.ServerDetailResponseSecurity](../../models/components/serverdetailresponsesecurity.md) | :heavy_minus_sign:                                                                                 | Information about the server's security status                                                     |                                                                                                    |
| `tools`                                                                                            | [components.Tool](../../models/components/tool.md)[]                                               | :heavy_minus_sign:                                                                                 | List of tools that this server provides                                                            |                                                                                                    |