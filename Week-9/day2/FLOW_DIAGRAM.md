# Multi-Agent Flow

User Query
   ↓
Planner (Task Breakdown)
   ↓
Parallel Worker Agents
   ↓
Internal Refinement (merge outputs)
   ↓
Validator
   ↓
Final Answer


## Execution Tree Example

{
  "User Query": "...",
  "Tasks": ["task1", "task2"],
  "Workers": ["output1", "output2"],
  "Final": "validated output"
}