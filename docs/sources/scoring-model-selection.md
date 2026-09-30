# Scoring configuration reference

Accessed 7 September 2026 during the continuation. Purpose: qualify another scoring configuration after one Astra calibration call read its inputs but returned no score before timeout. This is an experiment, not a claim that model choice caused the timeout or that another model is generally faster.

- [Official Codex model guidance](https://learn.chatgpt.com/zh-Hans/docs/models), “选择推理强度,” original excerpt: “使用能得到所需结果的最低推理强度。” The same page lists the `gpt-5.6-sol` CLI selector and says availability depends on account/client rollout. Actual access and scoring quality require execution.
- [Official GPT-5.6 Sol model page](https://developers.openai.com/api/docs/models/gpt-5.6-sol), original feature entry: “Structured outputs” — “Supported”. This makes the existing JSON grading protocol a supported capability; it does not guarantee correct judgments or literal citations.

Run the unchanged nineteen known-output controls with Sol/medium as a potential scoring configuration. Keep worker model/effort and scoring configuration identical within each prior/candidate comparison. Accept a scorer only after complete matching calibration; retain invalid attempts. Record actual worker and grader time/usage separately. API list prices are not estimates of this ChatGPT-authenticated account's quota consumption.
