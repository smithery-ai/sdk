# Invocation

## Example Usage

```typescript
import { Invocation } from "@smithery/registry/models/components";

let value: Invocation = {
  id: "625f9ce6-f179-4f23-b3e3-4de28b52b39d",
  timestamp: "2026-01-04 10:53:39",
  request: {
    method: "POST",
    url: "https://gateway.smithery.ai/@smithery/unicorn",
  },
  response: {
    status: 200,
    outcome: "ok",
  },
  duration: {
    cpuMs: 5,
    wallMs: 743,
  },
  logs: [
    {
      timestamp: "2026-01-04 10:53:39",
      level: "info",
      message: "Processing request...",
    },
  ],
  exceptions: [
    {
      timestamp: "2026-01-04 10:53:39",
      name: "TypeError",
      message: "Cannot read property 'x' of undefined",
      stack: "at handler (main.js:42:15)",
    },
  ],
};
```

## Fields

| Field                                                                          | Type                                                                           | Required                                                                       | Description                                                                    | Example                                                                        |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `id`                                                                           | *string*                                                                       | :heavy_check_mark:                                                             | N/A                                                                            | 625f9ce6-f179-4f23-b3e3-4de28b52b39d                                           |
| `timestamp`                                                                    | *string*                                                                       | :heavy_check_mark:                                                             | N/A                                                                            | 2026-01-04 10:53:39                                                            |
| `request`                                                                      | [components.InvocationRequest](../../models/components/invocationrequest.md)   | :heavy_check_mark:                                                             | N/A                                                                            |                                                                                |
| `response`                                                                     | [components.InvocationResponse](../../models/components/invocationresponse.md) | :heavy_check_mark:                                                             | N/A                                                                            |                                                                                |
| `duration`                                                                     | [components.InvocationDuration](../../models/components/invocationduration.md) | :heavy_check_mark:                                                             | N/A                                                                            |                                                                                |
| `logs`                                                                         | [components.RuntimeLogEntry](../../models/components/runtimelogentry.md)[]     | :heavy_check_mark:                                                             | N/A                                                                            |                                                                                |
| `exceptions`                                                                   | [components.ExceptionEntry](../../models/components/exceptionentry.md)[]       | :heavy_check_mark:                                                             | N/A                                                                            |                                                                                |