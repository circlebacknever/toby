# Runtime Configuration

Deploy config is the set of values that change between environments. Examples are database URLs, service endpoints, credentials, log levels, pool sizes, and connections to the feature flag service. The build must not contain it. The Twelve-Factor App guidelines say to read these values from environment variables.

Do not read `process.env.THING` across the code. Each read is a hidden dependency in a module that otherwise looks pure. Every reader also repeats the same facts about `THING`: its name, that it is a string, that it holds a URL, its default. If one of those facts changes, every reader has to change.

---

## Four rules

1. **One module reads the environment.** `process.env` and `import.meta.env` appear in exactly one file. Everything else receives values from it.
2. **Parse and validate at startup.** That module turns raw strings into a typed, frozen object with `zod`, `envalid`, or a hand-written parser. A missing or malformed variable stops boot with a message that includes the variable's name. Without this check, an unexplained `undefined` shows up later in code several calls away, while the service is handling traffic.
3. **Inject the typed values.** A module receives `config.databaseUrl`, or a client already built from it, passed in where the app is wired together. It does not import the config module and read fields from it. That import is the kind of hidden dependency that rule 1 exists to remove. It also makes the module hard to test.
4. **The config module is deep.** A deep module hides a lot of work behind a small interface. The interface is a handful of typed fields. The module hides the variable names, the parsing, the coercion, the defaults, the validation, and the work of keeping secrets out of log lines.

---

## The composition root

The composition root is the one place that uses both the config values and the concrete classes. It is the entry point: `main`, `server.ts`, the top of `App`. It reads config, constructs the real implementations, and passes them down. Code below it does not reference an environment variable or pick an implementation.

```ts
// config.ts is the only file that reads the environment
import { z } from "zod";

const schema = z.object({
  DATABASE_URL: z.string().url(),
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
  PAYMENT_GATEWAY: z.enum(["stripe", "legacy"]),
  STRIPE_KEY: z.string().optional(),
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
// main.ts is the composition root
import { config } from "./config";

const db = new Database(config.databaseUrl);
const logger = new Logger(config.logLevel);
const gateway = GATEWAYS[config.gatewayName];   // GATEWAYS maps each gateway name to its implementation (option 4, polymorphism, in toby-swd-modules).

const app = new App({ db, logger, gateway });
app.listen();
```

Every module below `main.ts` takes `db`, `logger`, and `gateway` as constructor arguments, so a test passes fakes. Those modules do not read `process.env`.

---

## Choosing behavior by environment

Choosing behavior by environment, such as which gateway, storage driver, or log sink to use, is one decision made once at the composition root. Read the config value, pick the implementation from a map, and inject it. A codebase with `if (process.env.NODE_ENV === "production")` in ten modules has spread one decision across ten files. `toby-swd-modules` covers this problem in `replace-the-conditional.md`, where the same `if` is copied into many files. Here the environment variable is the value each `if` checks.

---

## React and React Native

- Build-time env (`EXPO_PUBLIC_*`, `VITE_*`, `app.config.ts`) follows the same rule: one typed config module, imported values, no raw `process.env` or `import.meta.env` reads in components.
- Config that changes without a redeploy, such as remote flags and remote config, is its own deep module. The interface is `flags.someFeature`. The module hides a fetch, a cache, a default for the offline case, and a refresh policy.
- In React, a context provider at the top of the component tree passes config down to components. `ConfigProvider` holds the typed object. Components read it through a `useConfig` hook. The provider is how a frontend passes `config` down from the composition root.
