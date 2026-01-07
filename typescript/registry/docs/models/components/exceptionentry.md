# ExceptionEntry

## Example Usage

```typescript
import { ExceptionEntry } from "@smithery/registry/models/components";

let value: ExceptionEntry = {
  timestamp: "2026-01-04 10:53:39",
  name: "TypeError",
  message: "Cannot read property 'x' of undefined",
  stack: "at handler (main.js:42:15)",
};
```

## Fields

| Field                                 | Type                                  | Required                              | Description                           | Example                               |
| ------------------------------------- | ------------------------------------- | ------------------------------------- | ------------------------------------- | ------------------------------------- |
| `timestamp`                           | *string*                              | :heavy_check_mark:                    | N/A                                   | 2026-01-04 10:53:39                   |
| `name`                                | *string*                              | :heavy_check_mark:                    | N/A                                   | TypeError                             |
| `message`                             | *string*                              | :heavy_check_mark:                    | N/A                                   | Cannot read property 'x' of undefined |
| `stack`                               | *string*                              | :heavy_minus_sign:                    | N/A                                   | at handler (main.js:42:15)            |