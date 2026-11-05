# Config

This file shows how to centralize environment configuration, validate it at startup, and wire clients at startup.

## Four rules

1. **One module reads the environment.** Keep `process.env`, `os.environ`, and `import.meta.env` inside a single config module.
2. **Parse, validate, and redact at startup.** Parse raw strings into a frozen, typed config object at boot, fail immediately on missing or invalid variables, and redact secrets from errors and serialization.
3. **Build clients at startup.** Construct shared database pools, loggers, and API clients from typed config at startup (or in `post_fork` when a pool opens sockets on creation). Supply dependencies through the repo's composition mechanism according to responsibility and lifetime (`toby-swd-architecture`). Construct a scoped client when its credentials or lifetime require one. Test patching doesn't determine that boundary.
4. **Select implementations from config maps.** Pick a provider (`GATEWAYS[config.gatewayName]`) once at startup, and don't scatter `if (env === "production")` checks across modules.

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

- Validate `VITE_*`, `NEXT_PUBLIC_*`, and `EXPO_PUBLIC_*` variables in one config module. Run the same schema in `vite.config.ts`, `next.config.js`, or `app.config.ts` so missing variables fail the build.
- Next.js and Expo replace client env vars only when you write the full property name (`process.env.EXPO_PUBLIC_API_URL`), so pass each variable explicitly to the validator.
- Every `VITE_*`, `NEXT_PUBLIC_*`, and `EXPO_PUBLIC_*` value ships in the public bundle, so keep secrets on the server.
- Treat remote feature flags as a separate module (`toby-swd-flags`) that caches the last fetched values.
