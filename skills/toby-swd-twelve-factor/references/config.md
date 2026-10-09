# Config

Deploy config is the set of values that change between environments. Examples are database URLs, service endpoints, credentials, log levels, pool sizes, and connections to the feature flag service. The build must not contain it. The Twelve-Factor App guidelines say to read these values from environment variables.

Do not read `process.env.THING` across the code. Each read is a hidden dependency in a module that otherwise looks pure. Every reader also repeats the same facts about `THING`: its name, that it is a string, that it holds a URL, its default. If one of those facts changes, every reader has to change.

---

## Four rules

1. **One module reads the environment.** In a new service, or a repo that has a config module, `process.env` and `import.meta.env` appear in exactly one file. Everything else imports values from it.
2. **Parse and validate at startup.** That module turns raw strings into a typed, frozen object with `zod`, `envalid`, or a hand-written parser. A missing or malformed variable stops boot with a message that includes the variable's name. Without this check, an unexplained `undefined` shows up later in code several calls away, while the service is handling traffic.
3. **Import the typed values.** Code imports the typed config object, such as Django's `settings` or the `config` object below. Build each client once, at module scope or at startup. When a client opens connections as it is built, such as psycopg_pool's `ConnectionPool`, build it in each worker after the fork, and check out one connection per request. Build it on first use or in gunicorn's `post_fork` hook. Pass a value or a client in as an argument only when a test cannot patch it, as the Composition root rule in `toby-swd-architecture` says.
4. **Keep the interface to a few typed fields.** The config module hides the variable names, parsing, coercion, defaults, validation, and the work of keeping secrets out of logs.

---

## The composition root

The composition root is the code that builds clients from config when the process starts. Examples are Django's `settings.py` with clients at module scope, and `config.ts` with `clients.ts` below. Other code imports the config object and the clients, and never reads an environment variable or picks an implementation.

```ts
// config.ts is the only file that reads the environment
import { z } from "zod";

const schema = z
  .object({
    DATABASE_URL: z.string().url(),
    LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
    PAYMENT_GATEWAY: z.enum(["stripe", "legacy"]),
    STRIPE_KEY: z.string().optional(),
  })
  // The legacy gateway needs no key, and the Stripe gateway cannot boot without one.
  .refine((env) => env.PAYMENT_GATEWAY !== "stripe" || env.STRIPE_KEY, {
    message: "STRIPE_KEY is required when PAYMENT_GATEWAY is stripe",
    path: ["STRIPE_KEY"],
  });

const parsed = schema.safeParse(process.env);
if (!parsed.success) {
  console.error(parsed.error.flatten().fieldErrors);
  process.exit(1);
}

export const config = Object.freeze({
  databaseUrl: parsed.data.DATABASE_URL,
  logLevel: parsed.data.LOG_LEVEL,
  gatewayName: parsed.data.PAYMENT_GATEWAY,
  stripeKey: parsed.data.STRIPE_KEY,
});
```

```ts
// clients.ts builds each client once, when the process starts
import { config } from "./config";

export const db = new Database(config.databaseUrl);
export const logger = new Logger(config.logLevel);
export const gateway = GATEWAYS[config.gatewayName];   // GATEWAYS maps each gateway name to its implementation.
```

A module that charges a card imports `gateway` from `clients.ts`. Its test replaces the import with the runner's module mock, such as `vi.mock("./clients")`.

---

## Choosing behavior by environment

Choosing behavior by environment, such as which gateway, storage driver, or log sink to use, is one decision made once at the composition root. Read the config value, and pick the implementation from a map, as `clients.ts` does for `gateway`. A codebase with `if (process.env.NODE_ENV === "production")` in ten modules has spread one decision across ten files. `toby-swd-extensibility` covers this problem in `replace-the-conditional.md`, where the same `if` is copied into many files. Here the environment variable is the value each `if` checks.

---

## React and React Native

- Build-time env (`EXPO_PUBLIC_*`, `VITE_*`, `app.config.ts`) follows the same rule: one typed config module, imported values, no raw `process.env` or `import.meta.env` reads in components.
- Expo and Next.js insert a value into client code only where the code names it in full. List each variable by its full name in the object you validate, such as `{ EXPO_PUBLIC_API_URL: process.env.EXPO_PUBLIC_API_URL }`. Throw an Error where the example above calls `process.exit`, because a browser and a mobile app have no `process.exit`. Run the same schema at build time, in `app.config.ts` or `vite.config.ts`, so a missing value fails the build before release.
- The build compiles every `VITE_*`, `NEXT_PUBLIC_*`, and `EXPO_PUBLIC_*` value into the bundle, and anyone can read the bundle. Put no secret there. A secret stays on a server that the client calls.
- Config that changes without a redeploy, such as remote flags and remote config, is its own module. The interface is `flags.someFeature`. The module hides a fetch, a cache of the last fetched values, and a refresh policy. `toby-swd-flags` covers a flag's default and its fallback when the flag service is down.
