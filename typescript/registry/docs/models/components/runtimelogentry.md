# RuntimeLogEntry

## Example Usage

```typescript
import { RuntimeLogEntry } from "@smithery/registry/models/components";

let value: RuntimeLogEntry = {
  timestamp: "2026-01-04 10:53:39",
  level: "info",
  message: "Processing request...",
};
```

## Fields

| Field                 | Type                  | Required              | Description           | Example               |
| --------------------- | --------------------- | --------------------- | --------------------- | --------------------- |
| `timestamp`           | *string*              | :heavy_check_mark:    | N/A                   | 2026-01-04 10:53:39   |
| `level`               | *string*              | :heavy_check_mark:    | N/A                   | info                  |
| `message`             | *string*              | :heavy_check_mark:    | N/A                   | Processing request... |