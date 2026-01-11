# Claude Code: Zero to Mediocre

<details>

<summary>Today's session</summary>

## Why have this session?

- Lots of coding agents out there. This talk is just about **Claude Code**.
- I've spent time up-skilling in CC, so hopefully this helps you too!
- **Stop me at any time** — questions are welcome!

## Plan

We will aim to cover the following lessons:

- Lesson 1: Hello Claude Code!

  -> a basic CC workflow to add a feature to this repo!

- Lesson 2: CC & memory

  -> Add **memory** via `CLAUDE.md` and Agent Skills for each CC session.

- Lesson 3: Specialized `subagents`

  -> make CC be an expert at a task.

- Lesson 4: Add external context via MCPs

  -> Add external context to CC via MCPs

- Lesson 5: Context is a budget, spend it well

- Closing remarks

## Practical points

We will go through some exercises which I've made in my repo [claude-exercises](https://github.com/jfgrea27/claude-exercises).
You can also follow the full list of exercises on my [blog post](https://jfgrea27.github.io/posts/05-claude-code-workflows/)

We will use the code in this repo to solve tasks with CC. The code looks like this:

```
books-api/
├── src/
│   └── books_api/       # Source code
│       ├── db/          # Database connection and CRUD operations
│       ├── http/        # HTTP routes and schemas
│       ├── models/      # SQLAlchemy models
│       ├── utils/       # Utilities (logging)
│       └── server.py    # FastAPI app entry point
└── test/                # Tests mirroring source structure
claude-exercises/        # the exercises on books-api.
```

We won't have time to go through all the exercises today.

Any Questions? If not let's jump in!

</details>

<details>

<summary>Lesson 1: Hello Claude Code!</summary>

Claude Code is Anthropic's official coding agent that runs in your terminal.

## Why it's good

- Orpus 4.5 et al. are becoming silly good.
- Full filesystem access (reads, writes, executes)
- Extensible with MCPs (Model Context Protocol)

## Demo time

```sh
# checkout out exercises
git checkout 00-basic-usage
# start Claude Code
claude

# Opens a CLI with a text prompt
# Prompt 1: What are Claude Code's out-of-box tools?
```

Notes:

- CC is git-aware -> open it up in the repo you want to work on.
- Lots of tools. The main ones are:
  - File/web search
  - Task/planning
  - MCPs

Let's ask it to add logs to our books-api:

```txt
Add more logging to books_api
- info for starting/ending of requests.
- debug for any db interaction
- error for any exception

Write me a plan, ask me to review it. If I agree, can you then implement this as a background task.
```

Notes:

- It uses the out-of-box tools to code
- It is generally better to plan first since it gives CC the context it needs to carry out the task.
  -> For very small tasks it's ok to no use plan.

### Basic commands

- Close CC
- `/resume`
- `/clear` - remove all context
- `/tasks` - list all tasks in session, move to foreground etc.
- `/context` - see how much context you've spent.

</details>

<details>

<summary>Lesson 2: CC & memory</summary>

If we run our linter on the changes `just check`, this fails.
This is because Claude doesn't know how we lint our codebase.

Let's add memory to CC!

> Memory allows CC to have context added to the context without us prompting CC.

There are two key ways to do this:

- A `CLAUDE.md` file in the repo which CC reads every time you start a session
  - This includes details about the project structure, dependencies, architecture decisions, quirks, best practices.
  - **Don't bload this since it takes up some of that context window**
  - This should be **actively maintained**.
- A `Skill` (defined in `.claude/skills/`).
  - These are specialised small skills that CC can decide to use when it feels it should (or you tell it to).
  - **Don't bload this since it takes up some of that context window**

Let's add these in using CC!

```
# Add the skill change-check that will lint, format and test the code
Can you create a Claude Skill called change-check that calls `just check-fmt` to format, lint, typecheck and test the code.
# Adding CLAUDE.md
Can you add a CLAUDE.md file that CC about books-api its structure etc. Make sure to say that any changes should be check-fmt!
```

Notes:

- As you can see this has created the skills and memory for CC to use in sessions.
- Skills are added to the context on-demand so are good for specific tasks you want to run

Let's ask it to implement our feature again:

```txt
Add more logging to books_api
- info for starting/ending of requests.
- debug for any db interaction
- error for any exception
```

Now if we run `just check`, we see that it doesn't cause any linting issues anymore!

</details>

<details>

<summary>Lesson 3: Specialized `subagents`</summary>

Devs do lots of tasks:

- Features - architect, plan work, build feature, add tests
- Bug fix - reproduce bug, write a test, fix the bug, see test pass
- ...

CC exposes `subagents` as a way to create specialized agents for carrying out a task.

CC already has some subagents baked in (e.g. plan-mode is one).

Let's explore this with a `bug-smasher` agent!

```txt
bug-smasher - this subagent is an expert at smashing bugs. It will try to first
reproduce the bug if it can, and then it will write a test that fails for the
given bug, fix the bug and see the test pass
```

Notes:

- This creates the subagent in `.claude/agents`.
- Each subagent has a whole new context window.

Let's explore a bug

```txt
There is a bug in the code. When I run the db, I see that we can have 2 books with the same title. Can you fix the bug please
```

(the fix: add a uniqueness constraint)

As you can see the subagent is triggered and the bug is fixed!
We also called the skill to format.

</details>

<details>

<summary>Lesson 4: Add external context via MCPs</summary>

What if we want to integrate context outside of the filesystem?

MCPs allow us to do this.

We will hook up Jira and ask CC to complete a [jira ticket](https://jfgrea27.atlassian.net/browse/DEV-4).

```txt
Can you implement the ticket DEV-4 on branch feat/dev-4
- Write a plan and get it approved by me.
- Split each item in its own commit
- Raise a PR and assign and assign it to jfgrea27
```

And there you have it, our days are limited folks!

</details>

<details>

<summary>Lesson 5: Context is a budget, spend it well</summary>

Think of working with CC as a **context budget**. Don't overspend your budget.

If CC sees that we are nearing the top of the budget, it will compact the current context.
This allows it to prevent running out of budget.
Compaction will summarise session. This may lead to misalignment.

Hence in general:

- Start a new session for a new task
- Don't bloat memory
- Use subagents for specialised tasks

</details>

<details>

<summary>Closing remarks</summary>

Hope this was useful!

There is more to learn, check the CC docs. This includes:

- Hooks - allow CC to run a hook after a tool call.
- ...

What we could do at Poly:

- Add `CLAUDE.md` files for memory in git that we maintain
- Add Skills to our repo
- Feature/Bug: Start integrating MCPs like playwright, figma, jira, so that you can have a day off.
- Refactoring: Weekly scans of our repo using claude, finding smelly code and bugs, creating tickets, fixing, etc.

If you're keen to help make our lives easier, I'm thinking of starting a `#edge-coding-agents` channel to discuss ideas.

Any questions, lmk!

</details>
