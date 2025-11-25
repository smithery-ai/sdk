# Tool

## Example Usage

```typescript
import { Tool } from "@smithery/registry/models/components";

let value: Tool = {
  name: "get_weather",
  description: "Get current weather",
  inputSchema: {},
};
```

## Fields

| Field                                                            | Type                                                             | Required                                                         | Description                                                      | Example                                                          |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------- |
| `name`                                                           | *string*                                                         | :heavy_check_mark:                                               | N/A                                                              | get_weather                                                      |
| `description`                                                    | *string*                                                         | :heavy_check_mark:                                               | N/A                                                              | Get current weather                                              |
| `inputSchema`                                                    | [components.InputSchema](../../models/components/inputschema.md) | :heavy_check_mark:                                               | N/A                                                              |                                                                  |