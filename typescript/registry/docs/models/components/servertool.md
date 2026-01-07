# ServerTool

## Example Usage

```typescript
import { ServerTool } from "@smithery/registry/models/components";

let value: ServerTool = {
  name: "get_weather",
  description: "Get current weather",
  inputSchema: {
    type: "object",
  },
};
```

## Fields

| Field                                                                    | Type                                                                     | Required                                                                 | Description                                                              | Example                                                                  |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `name`                                                                   | *string*                                                                 | :heavy_check_mark:                                                       | N/A                                                                      | get_weather                                                              |
| `description`                                                            | *string*                                                                 | :heavy_check_mark:                                                       | N/A                                                                      | Get current weather                                                      |
| `inputSchema`                                                            | [components.ToolInputSchema](../../models/components/toolinputschema.md) | :heavy_check_mark:                                                       | N/A                                                                      |                                                                          |