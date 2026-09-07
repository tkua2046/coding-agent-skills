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
