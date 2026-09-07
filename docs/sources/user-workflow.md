# Original workflow request

Source: repository owner's instructions in the working conversation, 2026-09-06. Original wording is retained; Markdown list/quote escaping is normalized. The interpreted requirements are in SPEC. This source passage is retained rather than replaced by that interpretation.

> 我通常的正经开发流程是：
>
> - 拿到feature specs
> - 自己找面试官问clarification，让LLM也看下有没有需要澄清的
> - => Design doc => review design doc
> - => stage/commit-wise implementation doc => review and fix loop
> - 然后开始实现，每次实现完显然要先跑pre-commit hook
> - review agent 和我同时review和test
> - 没问题的话前进到下一个stage
> - 全部完成后， update version/changelog, push for PR review
> - complete PR后，tag and release

Additional owner instructions (verbatim):

> 我是说skills和design/justification doc

> 你甚至可以在这个repo里用你的这些skills来test自己来self-improve

Document-audience clarification (verbatim):

> 这里面规定了比如入口readme是给人看的，然后要有devnotes，changelog这些都是干啥的么，code/之前把乱七八糟的都放在一起扔到readme里，changelog和development.md都放在docs里了

## Outcome-driven revision, 7 September 2026

Source: subsequent owner messages in the same conversation. Original wording follows; the proposal and tests are interpretations, not substitutes for these requests.

> 这肯定没有包含我提到的问题啊。我提到生成的design doc，implementation plan不能glance，长到不是给人看的，一个小改动，review 10分钟啥的都没有啊

> 这里流程方面有没有什么需要改进的，我这套流程确实一般用着用着就越来越慢，复杂。我不是很确定是应该更加精细化的调整每一个步骤的prompt（比如明确写：不要over-enginnering或者过度复杂话之类的），还是要整个调整这个流程。这个流程其实原理上是没什么问题，但是和当前LLM用下来，除了慢之外，就是可能会过度去追求几个工程化指标，把简单问题搞得很复杂。我有点怀疑是不是有一个问题分类，难度分级之类的东西会有所帮助之类的？

The owner accepted the proposed direction: select depth using uncertainty, consequences/reversibility and affected boundaries; combine the design/plan note and review for local understood changes; retain appropriate checks; define useful exit/recheck conditions. The following is the execution authorization (verbatim):

> 可以。这个方向非常promising。我现在要去睡觉了，请沿着这个方向继续，然后从goal出发给每个skill添加相应的canaries，然后根据canaries结果迭代这些skills。在迭代过程中，也请经常jump out of the box审视全局，这个也比较有帮助。明早起来我来审查最后完成的skills。

## Continued repair and small behavioral checks, 7 September 2026

Source: later owner messages in the same conversation, retained verbatim.

> 你为什么停止分析以及系统性修复这些问题了

> 修复仍要确保通用性和普世意义，不要做reward，rubric hack 和overfit

> 虽然比较真实的canary很重要，不过一些更简单的smoke test版本的llm based test可能可能帮我们快速发现一些基本的问题，消耗时间和token也更可控？

> 这样可以把每个小块/拆分细分其职责，不容易出现改prompt按下葫芦起来piao的问题

> 以及像design doc和implementation plan，和review feedback，你有明确的rules规定其职责，甚至提供一个模板或者after generation rubric么（可以不用太制式），这都可以极大的避免coding agent在做任务过程中还要carry一大串关于结果格式的context

## Delivery repair authorization — 7 September 2026

> 你有正经验收一下你的pr么，32250 file changes？
> 当前问题的根本是什么？

The owner approved the proposed correction of delivery boundaries, task-proportionate workflow, goal-based tests and whole-PR acceptance:

> Go ahead。记得经常jump out of the box从high level观察，goal-oriented。不要陷入局部泥潭。
