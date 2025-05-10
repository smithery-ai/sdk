<!-- Start SDK Example Usage [usage] -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry({
  bearerAuth: process.env["SMITHERY_BEARER_AUTH"] ?? "",
});

async function run() {
  const result = await smitheryRegistry.servers.list({
    q: "owner:mem0ai is:verified memory",
  });

  for await (const page of result) {
    // Handle the page
    console.log(page);
  }
}

run();

```
<!-- End SDK Example Usage [usage] -->