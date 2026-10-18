# Config

This file shows how to centralize environment configuration, validate it at startup, and wire clients in the composition root.

## Four rules

1. **One module reads the environment.** Keep `process.env`, `os.environ`, and `import.meta.env` inside a single config module.
2. **Parse, validate, and redact at startup.** Parse raw strings into a frozen, typed config object at boot, fail immediately naming any missing or invalid variable, and redact secret fields from error output and `toString`/`toJSON` serialization.
3. **Build clients in the composition root.** Construct database pools, loggers, and API clients once from the typed config at startup (or in `post_fork` when a pool opens sockets on creation). Pass a client as a function argument only when tests can't module-mock it (`toby-swd-architecture`).
4. **Select implementations from config maps.** Pick a provider (`GATEWAYS[config.gatewayName]`) once in the composition root, and don't scatter `if (env === "production")` checks across modules.

```ts
// config.ts is the only file that reads process.env.
import { z } from "zod";

const schema = z
  .object({
    DATABASE_URL: z.string().url(),
    LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
    PAYMENT_GATEWAY: z.enum(["stripe", "legacy"]),
    STRIPE_SECRET: z.string().optional(),
  })
  .refine((env) => env.PAYMENT_GATEWAY !== "stripe" || env.STRIPE_SECRET, {
    message: "STRIPE_SECRET is required when PAYMENT_GATEWAY is stripe",
    path: ["STRIPE_SECRET"],
  });

const parsed = schema.safeParse(process.env);
if (!parsed.success) {
  // Log only field names and messages so secret values never print to stderr.
  console.error(parsed.error.flatten().fieldErrors);
  process.exit(1);
}

export const config = Object.freeze({
  databaseUrl: parsed.data.DATABASE_URL,
  logLevel: parsed.data.LOG_LEVEL,
  gatewayName: parsed.data.PAYMENT_GATEWAY,
  stripeSecret: parsed.data.STRIPE_SECRET,
});
```

```ts
// clients.ts builds each client once when the process starts.
import { config } from "./config";

export const db = new Database(config.databaseUrl);
export const logger = new Logger(config.logLevel);
export const gateway = GATEWAYS[config.gatewayName];
```

## Client bundles

- In React, Next.js, Vite, and Expo, validate `VITE_*`, `NEXT_PUBLIC_*`, and `EXPO_PUBLIC_*` variables in one config module and run the same schema in `vite.config.ts`, `next.config.js`, or `app.config.ts` so missing variables fail the build.
- Next.js and Expo inline client env vars by exact static property access, so pass `{ EXPO_PUBLIC_API_URL: process.env.EXPO_PUBLIC_API_URL }` explicitly to the validator and throw an `Error` on failure.
- Every `VITE_*`, `NEXT_PUBLIC_*`, and `EXPO_PUBLIC_*` value ships in the public bundle, so keep secrets on the server.
- Treat remote feature flags as a separate module (`toby-swd-flags`) that caches the last fetched values.
