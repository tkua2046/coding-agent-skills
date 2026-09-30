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

## Concrete artifact requirements recovered from the conversation

Recorded 7 September 2026. These are additional original messages from the same
conversation, not new requirements invented by the specification author. Their
interpretation is organized in [the problem inventory](../OUTPUT_REQUIREMENTS_PROPOSAL.md).

### U1 — Preparation, document usability and development tooling

> 显然你之前给我准备的doc里错过了很多我可以提前准备的关于dev workflow的
>
> - 什么是良好的design/specs doc
> - 怎么样可以将design-doc 转换成implementation doc，stage/commit-wise
> - pre commit hook
>   - test coverage report
>   - ruff lint
> - 基础dev setup，比如version advancement, 面向用户文档：readme，面向开发者文档：changelog，面向agent文档：agent.md
> - Design doc和implementation doc review prompt，生成的文档应该易懂，consequence和example清晰，你看看现在repo里那些doc，面试里怎么可能看的完。doc可以完整繁复，但是都没有清晰的outline，或者可以快速glance的可能。这不仅不利于interview，平时开发也不行。
>
> 很多这些都可以提前准备成skills或者至少是一个prompt file，我在面试中可以正当使用。给我你的proposal

### U2 — Local amendments and unresolved review history

> 1. Rover这个题里，第一问是简单的上下左右移动，然后第二问是简单的加一个obstacle。这个情况应该加一个新的design doc还是在原有的基础上改？我现在看到的是，原有的plan.md被codex疯狂重写。implementation plan也几乎重写。
> 2. 这个小feature：加obstacle的design/implementation阶段已经自己跑了估计有10min了，到现在已经出发context compacting了。我不知道这个是选gpt-6 astra的问题，还是design doc writing和review不一致的问题。还是什么
> 3. 你可以看下这些doc，本身也很冗余，比如 implementation_plan里包含“The stages below are proposed future implementation commits, in order. Each stage must pass the complete cumulative suite and installed pre-commit hooks before the next starts. Existing tests stay in place; subtests add variants without increasing named-method counts.”
> 4. design reviews doc倒是单独成为一个file了，但是也不知道里面的concern是解决了还是没解决，是否有多轮review/fix/approve

### U3 — What an implementation plan must not duplicate

> 一个重要的区别是，implementation plan不是拿自然语言把整个实现和test一个一个都说一遍，那根本不能维护。每次改一点代码，加个test难不成把整个doc都要改一遍？

### U4 — Review a proposal before changing skills

> 你先给个proposal，然后review。。。不要直接改。。。以及你的改动也应该被test

### U5 — Regression protection with proportionate cost

> 这些重要测试应该被standardize，以及结果应该记录一下么？他们也需要被用作future skill prompt modification的safe guard吧？如果没有的话，这不是violate你自己写的skills么

> 当然太过heavy的测试也不能每次小改动都跑。在最后release之前跑就行。

> 这些canary也要谨慎，不能搞个巨复杂的，也不能搞个toy

### U6 — Define the product requirements before testing

> 难道你应该至少在跑测试前先把rubrics/eval大体定下来，然后再在实际跑的过程中查缺补漏？

> 对于每个skills具体要做什么，结果满足什么有具体规定么？拟定下来了么？没定下来哪来的小规模测试？

> ”对结果的具体要求“，你这些跟具体有一分钱关系么，我还不知道这些skill的基本定义我能让你写这些skill？

### U7 — Organize requirements by skill, then derive tests

> skill A：功能是什么，期望输出大概是什么，goals, non-goals，要避免的情况是什么。这些具象化成test case和rubrics，不是就这么简单？你在BB什么？

### U8 — Efficiency is a skill requirement, not an interview schedule

> 你又开始drift，听不懂人话了。我是说你的skill垃圾要毁了我的面试。add obstacles这个agent跑了15min这个问题我没告诉你？这个跟是不是面试有关系？你rubrics有cover？

### U9 — Research, evidence and test meaning

> 在闭门造车之前，你先做足research，看看正常开发流程，正常design doc, implementation doc的focus是什么，在当前LLM-assistance已经是主流的情况下，实际flow是什么。有没有现成的skills可以参考甚至直接用。到底有哪些痛点和问题。

> 找一下面经，你知道去哪找，哪些靠谱。注意：请注重Governance，源头和原文收录！不要再丢掉原文只留下一些summarization了。

> 你有做过哪些测试？他们的grading分别是怎样的？

> 呃，所以这160个主要是关于这几个skills能不能跑，和跑的好不好一点关系没有

> 你有参考过这个么：[https://developers.openai.com/blog/eval-skills](https://developers.openai.com/blog/eval-skills)

> 为什么remote的main branch已经有commit了？

### U10 — Recover all feedback before another local correction

> 难道不是整理一下之前发给你的问题？？？这个耗时不是其中问题之一？？？

### U11 — Task attention, priority and graded quality

> 现在是在测skill还是仍然在work on eval setup？
>
> 这种skill切忌写那种和主要任务无关，细枝末节层面的hard requirement。比如格式要求，完全可以在输出之后在审查改进。one task at a time，大面上那种严格的小feature时间不能30min这种hard no当然要强调一下，但是其他的什么小细节肯定不能跟真实人物抢Attention。
>
> 当然，这个是skill prompt的写作原则，但是grading和rubrics也应该有考虑，两者毕竟要align，你应该有Priority mark/给每个rubrics，以及打分1-5/7这种，hard-pass还是hard-fail除非特别简单的，完全不模糊的可以用。

### U12 — Readability as the final step of the same task

> 另外像这种skills，很多不都是一步一步么？最后一步是保证结果的可读性，格式不行么？你现在是怎么个情况

### U13 — Global assessment and a usable local candidate

> 全局，跳出当前思维桎梏，观测评价一下这次测试和测试结果。

> 如果有什么明显需要改进的low-hanging fruits，请apply，否则对剩下三个skills进行相同操作。我需要一个我明天早上10点面试能用的版本。
