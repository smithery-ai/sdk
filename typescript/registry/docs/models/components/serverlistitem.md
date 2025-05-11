# ServerListItem

## Example Usage

```typescript
import { ServerListItem } from "@smithery/registry/models/components";

let value: ServerListItem = {
  qualifiedName: "smithery-ai/fetch",
  displayName: "Fetch",
  description: "A server for fetching web content",
  homepage: "https://smithery.ai/server/smithery-ai/fetch",
  useCount: "12345",
  createdAt: new Date("2023-01-01T12:00:00Z"),
};
```

## Fields

| Field                                                                                         | Type                                                                                          | Required                                                                                      | Description                                                                                   | Example                                                                                       |
| --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `qualifiedName`                                                                               | *string*                                                                                      | :heavy_check_mark:                                                                            | Unique identifier for the server                                                              | smithery-ai/fetch                                                                             |
| `displayName`                                                                                 | *string*                                                                                      | :heavy_check_mark:                                                                            | Human-readable name of the server                                                             | Fetch                                                                                         |
| `description`                                                                                 | *string*                                                                                      | :heavy_check_mark:                                                                            | Description of the server's functionality                                                     | A server for fetching web content                                                             |
| `homepage`                                                                                    | *string*                                                                                      | :heavy_check_mark:                                                                            | Link to Smithery server page                                                                  | https://smithery.ai/server/smithery-ai/fetch                                                  |
| `useCount`                                                                                    | *string*                                                                                      | :heavy_check_mark:                                                                            | Number of times the server has been used via tool calling                                     | 12345                                                                                         |
| `createdAt`                                                                                   | [Date](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date) | :heavy_check_mark:                                                                            | Server creation timestamp                                                                     | 2023-01-01T12:00:00Z                                                                          |