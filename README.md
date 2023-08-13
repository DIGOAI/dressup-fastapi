# Supabase management CLI

The next information extracted from the [Supabase Docs Local Dev / CLI](https://supabase.com/docs/guides/cli).

## Init the Supabase project

Init the Supabase locally project

```shell
npx supabase init
```

Link the local repository with Supabase project

```shell
npx supabase login
npx supabase link --project-ref $PROJECT_ID
```

> You can get your `$PROJECT_ID` from your project's dashboard:

If you're using an existing Supabase project, you might have made schema changes through the Dashboard.

```shell
npx supabase db remote commit
```

This command creates a new migration in `supabase/migrations/<timestamp>_remote_commit.sql` which reflects the schema changes you have made previously.

Now commit your local changes to Git and run the local development setup:

```shell
git add .
git commit -m "init supabase"
npx supabase start
```

With the `supabse start` command, a docker container is up and present the Supabase UI in [`localhost:54323`](http://localhost:54323)

## Create a new migration

```shell
npx supabase migration new new_employee
```

You should see a new file created: `supabase/migrations/<timestamp>_new_employee.sql`. You can then write SQL statements in this script using a text editor:

```sql
create table public.employees (
  id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name VARCHAR(80) NOT NULL
);
```

Apply the new migration to your local database:

```shell
npx supabase db reset
```

Push the migration to remote project:

```shell
npx supabase db push
```

> **DANGER:** The migration will be applied to the database in the remote project, make sure to test the changes in a _test environment_ beforehand.

# Last docs

This docs is in deprecated status.

```shell
alembic init alembic
```
