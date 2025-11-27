<!-- Start SDK Example Usage [usage] -->
```typescript
import { SmitheryRegistry } from "@smithery/registry";

const smitheryRegistry = new SmitheryRegistry();

async function run() {
  const result = await smitheryRegistry.system.checkHealth();

  console.log(result);
}

run();

```
<!-- End SDK Example Usage [usage] -->