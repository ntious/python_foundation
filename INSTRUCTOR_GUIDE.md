# 👩‍🏫 Instructor Guide

## Overview

This guide supports instructors delivering IT1009C · Introduction to Python or adapting these Python foundations materials for beginner learners with no prior programming experience.

The course is designed to be:
- beginner-friendly  
- hands-on  
- guided  
- practical  


## Teaching Philosophy

The course follows a **utility-first approach**:

- focus on what the code does, not theory  
- emphasize real-world usefulness  
- build confidence through small wins  
- allow mistakes as part of learning  


## Instructional Approach

Each module should follow this pattern:

1. Short explanation  
2. Demonstration (run code together)  
3. Guided student activity  
4. Reflection or discussion  


## Running the Notebooks

Before starting, ensure students know how to:

- run a cell (Shift + Enter)  
- read output  
- recognize error messages  

Spend 5–10 minutes demonstrating this in the first session.


## Estimated Time Per Module

- Each module: ~45–60 minutes  
- Some modules may move faster depending on class pace  


## Adoption and Workload Planning

The 45–60 minute module estimates above are provisional guided-activity estimates, not measured completion times or a total student workload. The course's approximately 12 guided hours do not include all independent practice, setup, reflection, or project completion. A module is not necessarily a calendar week. Map selected activities to your institution's credit-hour expectations and calendar; this OER does not certify those requirements.

Before teaching:

- [ ] Choose a primary notebook environment and fallback; test the first notebook as a learner.
- [ ] Publish required activities and what students may skip. Keep Notebook 12 as the final-project specification.
- [ ] Adopt or adapt the [base rubric](docs/grading_overview.md). Publish assignment weights, partial credit, late-work rules, and whether/how re-review is offered.
- [ ] State a help channel, expected response time, and private route to request support.
- [ ] Decide whether to substitute the check-in and peer activity below. Publish the solo option.
- [ ] Budget guided and independent time separately and review actual learner experience during delivery.

### Small Substitutions, Not Added Assignments

| Resource | Placement | Replaces | Suggested active time | Assessment treatment |
| --- | --- | --- | --- | --- |
| [Mid-course check-in](templates/mid_course_reflection.md) | End of Module 6, before loops | Module 6's end reflection; its real-world question is retained | About 5 minutes | Prefer feedback only; any completion credit replaces existing reflection credit |
| [Peer exchange or solo equivalent](docs/peer_learning.md) | Module 6: Comparing AND vs OR | That example's discussion/practice segment | About 10 minutes across a flexible reply window | Optional adoption; no new grading category |
| [Stretch prompt](docs/stretch_prompts.md) | After the matching concept | At most one repeated practice attempt, if desired | About 3–5 minutes | Optional; never necessary for full credit |

These are planning estimates, not validated workload measurements. Do not append all three to a full session. Preserve essential first examples; shorten repeated practice before adding support activities. Leave the numbered sequence, learning objectives, and small final project unchanged.

## Teaching Online Without Required Videos

Use the same **explain → demonstrate → practice → reflect** sequence in a written module checklist. No video, recording, or live attendance is a prerequisite for using this OER. Keep instructions available as selectable text, not image-only screenshots.

### Reusable Module Instructions

Copy and complete this checklist in your learning-management system:

1. **Purpose:** This module helps you [one existing notebook objective].
2. **Open:** [link the original notebook and website reading page]. Use [chosen environment]; download your work before closing it.
3. **Predict and explore:** Read [named example], predict its output, run it, and change one value.
4. **Practice:** Complete [selected existing TODO/mini-lab sections]. [Name optional sections] are not needed for full credit.
5. **Explain and submit:** Answer [existing reflection, or its selected replacement]. Submit [one format] at [location] by [deadline]. Link the published rubric.
6. **Time and help:** Plan for [guided time] and [independent practice time], with flexibility. Ask at [help channel]; expect a response within [locally chosen time]. Use [fallback or extension process] if access fails.

Replace every bracketed field before sharing. Avoid duplicate uploads of the same reflection or notebook. The website is for reading; students need a notebook environment to execute code.

### Short Written Walkthroughs

Use one existing cell at a time instead of adding a lecture. For Module 6's **AND Logic** access example: ask for a prediction, have students run it, change only `has_active_account` to `False`, and ask which requirement now fails. Refer to the original cell so examples remain in one place. Learners can do these steps asynchronously; do not make a live demonstration the only source of instructions.

### Help and Notebook Troubleshooting

Online learners may miss that a cell is waiting for `input()`, that earlier variables are missing after a restart, or that the website cannot execute code. Check cell order and input prompts, and distinguish intentional debugging examples from unexpected failures. Do not use “Run All must pass” as a blanket grading rule: some course cells are intentionally broken.

Link the existing [troubleshooting guide](setup/troubleshooting.md) and [notebook guide](docs/how_to_use_notebooks.md). Ask help requests to include the platform, notebook and section, expected/actual result, exact error text, and one attempted fix. Use small synthetic examples, never credentials or personal records. Provide private help for sensitive issues; do not require public disclosure of a student's difficulties.

Download a checkpoint before refreshing or restarting a troubled session. If Binder is unavailable, use the [documented Colab alternative](setup/colab_instructions.md) or an instructor-supported environment. While access is unavailable, a learner can record predictions from the reading page and run them later; do not call unexecuted code tested. Publish an access-related extension route so outages are not treated as lack of effort.

### When Live Attendance Is Impossible

Provide the same notebook links, named cells, written steps, and submission instructions asynchronously. Replace live discussion with a short text response or the peer activity's solo route using equivalent evidence and credit. Offer a flexible reply window rather than requiring everyone online together. Live help can supplement these materials, but essential explanations remain available in writing.

### Different Learning Paces

Use the check-in to find sticking points and plan the next short walkthrough. Offer [stretch choices](docs/stretch_prompts.md) using only already-taught concepts. Do not raise the full-credit standard for faster learners, require advanced syntax, or make them responsible for teaching classmates. A clearer explanation or another small test can provide challenge without a larger application.

### Checking Workload and Beginner Accessibility

During a pilot or first delivery, invite an optional estimate of active time and one confusing step through the existing check-in. Distinguish setup delays from practice and project time. Do not grade speed or confidence. Compare workload with local requirements and adjust repetitive tasks or pacing before adding content. Actual learner feedback is needed to validate time estimates and accessibility.

## Supporting Common Difficulties

Students may struggle with:

- understanding what variables represent  
- interpreting error messages  
- forgetting syntax (quotes, parentheses)  
- expecting computers to "guess" intent  

### Instructor Tip:
Normalize mistakes early:
> “Errors are part of programming, not failure.”


## Debugging Guidance

Encourage students to check:

- spelling  
- quotes (" ")  
- parentheses ( )  

Avoid deep debugging explanations—keep it simple and practical.


## Teaching Career Context (Important)

Python is used in many fields, including:

- data analysis  
- artificial intelligence  
- software and IT systems  

You may briefly mention these areas to motivate students.

⚠️ Do NOT:
- go into technical depth  
- introduce advanced tools or libraries  

The goal is awareness, not specialization.


## Classroom Tips

- Encourage students to predict outputs before running code  
- Ask students to explain what the code is doing in plain language  
- Allow students to work in pairs when possible  
- Keep activities short and focused  


## Final Project Guidance

The mini project should be:

- simple  
- meaningful  
- based on real-life tasks  

Focus on:
- correct logic  
- clarity  
- student understanding  

Not complexity.


## Instructor Role

Your role is not to lecture extensively, but to:

- guide  
- support  
- encourage  
- simplify  


## Final Note

Students are not expected to become programmers in this course.

They are expected to:
- understand programming basics  
- gain confidence  
- see how programming applies to their world  
