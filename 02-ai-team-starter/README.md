# The AI team starter

One chat window doing everything gets messy fast. It forgets, it mixes jobs, and you end up checking all of it.

So I run my work like a small team: **ten agents, each with one job**, one shared task board, and one rule that decides what reaches me. This is that setup, minus my business details.

You can run it with any agent tool that has a shared task list (a kanban board, Linear, Notion, even a spreadsheet). The ideas matter more than the tool.

## 1. The team

Each agent gets a nickname so you remember its job. Mine are named after people famous for that skill. Name yours whatever you like.

| Seat | My nickname | One job | Never does |
|---|---|---|---|
| Chief of staff | Kittle | Front door. Takes every request, splits it into tasks, decides what needs me. | Builds things itself |
| Reviewer | Claude | Checks every finished task before it counts as done. | Reviews its own work |
| Tech lead | Carmack | Plans and builds the bigger technical pieces. | Ships without review |
| Builder | Theo | Smaller builds and fixes. | Changes live systems without approval |
| Finance | Chamath | Books, costs, invoices, weekly money summary. | Moves money |
| Content | Gary | Drafts posts, captions and scripts in my voice. | Posts anything |
| Growth | Ogilvy | Ads, hooks and tests. | Spends money |
| Sales | Lenny | Researches leads and drafts outreach. | Sends emails |
| Research | Scout | Finds facts and sources. | Guesses |
| Customers | Tony | Keeps the customer list clean and answers support drafts. | Promises refunds |

Start with three: **chief of staff, reviewer, and the one job that eats most of your week.** Add seats only when one gets overloaded.

## 2. The board

Every task lives on one board with these columns:

`Triage → To do → Ready → Running → Review → Done`, plus **Blocked**.

- Only the chief of staff adds to Triage.
- Nothing reaches Done without passing Review by a *different* agent.

## 3. Statuses at a glance

| Status | Means |
|---|---|
| **Working** | Running, with a recent heartbeat |
| **Waiting** | Has a task, waiting its turn or on review |
| **Needs you** | Blocked on a decision only you can make |
| **Stuck** | Blocked on anything else; the team should fix it, not you |
| **Done** | Finished and reviewed |
| **Free** | No open tasks |

## 4. The rule that protects your time

> **An agent can only put something in front of you by blocking a task with a reason that starts with `Needs [your name]:`**, written as one yes/no question with the work already done.

Good: `Needs Garet: Send roster reminders to the 6 coaches missing one? Drafts are attached. Nothing sends until you say yes.`

Bad: `Needs Garet: what should we do about reminders?`

Everything else, agents solve among themselves. Agents never skip the chief of staff to reach you.

## 5. The approval rule

Agents **draft**. You **approve**. Anything that sends, posts, pays, deletes or goes live waits for a yes. This one rule is what lets you trust the team with real work.

## 6. Set it up

1. Fill in the [business brain](../01-business-brain/) first. Every agent reads it.
2. Copy `roles/ROLE-TEMPLATE.md` once per seat and fill it in. See the three examples in `roles/`.
3. Give each agent its role card plus the business brain as its instructions.
4. Make the board. Tell the chief of staff the rule in section 4.
5. Hand it one real task this week and watch where it gets stuck. Fix that, then add the next seat.

---
Want this built around your business and run for you every month? Free 20-minute audit at garetbuilds.ai.
