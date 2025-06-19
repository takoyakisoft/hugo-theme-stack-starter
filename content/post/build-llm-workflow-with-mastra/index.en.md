---
title: Master LLM Workflows with mastra! From Grok-2 and think Tools to Generating Article Cloning Prompts
description: Build LLM workflows using Grok-2 and Gemini 2.5 Pro with the mastra library and TypeScript! This guide clearly explains the specific steps, from installation and implementing the 'think' tool to creating a loop process where the AI improves its own prompts.
slug: build-llm-workflow-with-mastra
date: '2025-04-03 21:00:34+09:00'
image: build-llm-workflow-with-mastra.webp
categories: [AI, Programming]
tags: [mastra, TypeScript, Grok, Gemini]
---

Hello! Today, I'll share my experience using a library called mastra to run LLMs like Grok-2 and Gemini 2.5 Pro exp.

mastra is a library that lets you decide which LLM to use for a prompt, create "AI agents," and then set up a "workflow" defining the order in which these agents run. The fact that it's written in TypeScript is personally a big plus for me. I'm thinking it might allow for affordable integration into web services in environments like Cloudflare Workers or Deno.

Similar libraries like LangChain are well-known, but mastra might have a slight advantage in terms of deployment ease. Also, I previously tried a tool called Dify, which seemed a bit weak with iterative processing (loops), so I wanted to see how mastra handles that. That's part of the reason I decided to give it a try.

Alright, let's dive right in!

## Installing mastra

This time, I'm using Windows 11, the AI editor "Trae," and the fast package manager "pnpm."

First, let's create a project following the steps on the official mastra website.
(Reference: [Create a New Project](https://mastra.ai/docs/getting-started/installation#create-a-new-project))

Open your terminal and run the following command:

```batch
pnpm create mastra@latest
```

You'll be asked a few questions. Let's answer them.

![mastra project creation screen](WindowsTerminal_UXtTR1rp9W.webp)

It asks for the project name. I chose `my-mastra-app` this time.
```batch
◇  What do you want to name your project?
│  my-mastra-app
```

This is where the source files will be placed. The default `src/` is fine.
```batch
◆  Where should we create the Mastra files? (default: src/)
│  src/
```

Choose the necessary components. We'll use Agents, Workflows, and Tools later, so let's select Yes for them.
```batch
◆  Choose components to install:
│  ◼ Agents
│  ◼ Workflows
◇  Add tools?
│  Yes
```

Select the default LLM provider. I chose Google this time, but you can change this freely later.
```batch
◇  Select default provider:
│  Google
```

API key setup. We'll set this in the `.env.development` file later, so skipping for now (Skip for now) is okay.
```batch
◆  Enter your google API key?
│  ● Skip for now (default)
```

Add examples? Yes, for this time.
```batch
◇  Add example
│  Yes
```

AI IDE integration? Skipped for now.
```batch
◇  Make your AI IDE into a Mastra expert? (installs Mastra docs MCP server)
│  Skip for now
```

Now the project template is created!
Navigate to the created project folder and install the necessary libraries.

```batch
cd my-mastra-app
pnpm i
```

Let's start the development server. You can stop it with Ctrl+C.

```batch
pnpm run dev
```

## Let's look at the configuration

Once the installation is complete, let's examine a few files.

Looking at `package.json`, you can see `@ai-sdk/google` in the `dependencies`. This is a library provided by Vercel, and it seems to support not only Gemini but also other LLM providers like DeepSeek, Grok, and OpenRouter. Looks convenient!
(Reference: [AI SDK Providers](https://sdk.vercel.ai/providers/ai-sdk-providers))

The `scripts` section only has `dev`. Perhaps build or test scripts will be added in the future.

```json
{
  "name": "my-mastra-app",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
    "dev": "mastra dev"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "description": "",
  "type": "module",
  "dependencies": {
    "@ai-sdk/google": "^1.2.5",
    "@mastra/core": "^0.7.0",
    "mastra": "^0.4.4",
    "zod": "^3.24.2"
  },
  "devDependencies": {
    "@types/node": "^22.14.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.2"
  }
}
```

This time, I also want to use xAI's Grok, so let's add the corresponding library.

```batch
pnpm add @ai-sdk/xai
```

If you no longer need it, you can remove it with `pnpm remove @ai-sdk/xai`.

Next is the API key configuration. Create `.env.development` and `.env` files in the project root and write the respective API keys. (`.env` is for production, `.env.development` is for development).

`.env.development`:
```env
GOOGLE_GENERATIVE_AI_API_KEY=your-google-api-key
XAI_API_KEY=your-xai-api-key
```

If you want to change the LLM model, specify it in the file defining the agent (e.g., `src/mastra/agents/index.ts`) or the workflow file (e.g., `src/mastra/workflows/index.ts`).

For example, here's how to use Grok-2:

Example `src/mastra/agents/index.ts`:
```ts
import { xai } from '@ai-sdk/xai'; // Import the xAI library
import { Agent } from '@mastra/core/agent';
import { weatherTool } from '../tools'; // Also import the tool to be used

export const weatherAgent = new Agent({
  name: 'Weather Agent',
  instructions: `
      You are a helpful weather assistant that provides accurate weather information.

      Your primary function is to help users get weather details for specific locations. When responding:
      - Always ask for a location if none is provided
      - If the location name isn’t in English, please translate it
      - If giving a location with multiple parts (e.g. "New York, NY"), use the most relevant part (e.g. "New York")
      - Include relevant details like humidity, wind conditions, and precipitation
      - Keep responses concise but informative

      Use the weatherTool to fetch current weather data.
`,
  model: xai('grok-2-latest'), // Specify the model here!
  tools: { weatherTool },
});
```

You can specify it similarly within a workflow.

Example `src/mastra/workflows/index.ts`:
```ts
import { xai } from '@ai-sdk/xai';
import { Agent } from '@mastra/core/agent';
import { Step, Workflow } from '@mastra/core/workflows';
import { z } from 'zod';

const llm = xai('grok-2-latest'); // Define the model to use here
```

## Let's check if it works

Once the configuration is done, let's start the development server again.

```batch
pnpm run dev
```

Access [http://localhost:4111/](http://localhost:4111/) in your browser, and the mastra interface should appear.

![weather agent selection screen](Trae_DllHdtTB78.webp)

You can select an agent and test it in a chat format.

![weather agent chat screen](Trae_8z5OEtWoym.webp)

When using Grok-2, the answers might come back in English.

## Implementing the "think tool"

Next, let's implement an interesting tool: the "think tool."

This is a technique introduced in an Anthropic article, suggesting that adding a "thinking" step before letting the LLM execute something can improve performance.
(Reference: [The "think" tool: Enabling Claude to stop and think in complex tool use situations](https://www.anthropic.com/engineering/claude-think-tool))

This tool itself doesn't fetch external information or anything; it just mimics the process of "thinking." However, it seems to be effective in cases requiring complex reasoning. Interesting, isn't it?

Let's create the think tool with mastra.

First, create a file to define the tool.

`src/mastra/tools/thinkTool.ts`:
```ts
import { createTool } from '@mastra/core/tools';
import { z } from 'zod'; // For input data validation

export const thinkTool = createTool({
  id: 'think', // Tool ID
  description: 'Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.', // Tool description
  inputSchema: z.object({ // Definition of the input the tool receives
    thought: z.string().describe('A thought to think about.'),
  }),
  outputSchema: z.object({}), // Definition of the data the tool outputs (empty this time)
  execute: async ({ context }) => {
    // Doesn't actually do anything
    console.log('Thinking:', context.thought); // Maybe log the thought content to the console
    return {};
  },
});
```

Next, create an agent that uses this think tool. The key is to instruct the agent in the prompt when to use the think tool.

`src/mastra/agents/thinkAgent.ts`:
```ts
import { Agent } from '@mastra/core/agent';
import { thinkTool } from '../tools/thinkTool'; // Import the created thinkTool
import { xai } from '@ai-sdk/xai'; // Also import the LLM model to use

export const thinkAgent = new Agent({
  name: 'Think Agent',
  instructions: `
    ## Using the think tool

    Before taking any action or responding to the user after receiving tool results, use the think tool as a scratchpad to:
    - List the specific rules that apply to the current request
    - Check if all required information is collected
    - Verify that the planned action complies with all policies
    - Iterate over tool results for correctness

    Here are some examples of what to iterate over inside the think tool:
    <think_tool_example_1>
    User wants to [specific scenario]
    - Need to verify: [key information]
    - Check relevant rules: [list rules]
    - Verify [important conditions]
    - Plan: [outline steps]
    </think_tool_example_1>
`, 
  model: xai('grok-2-latest'), // Let's try Grok-2 here too
  tools: { thinkTool } // Register this as a tool used by this agent
});
```

Finally, register the created tool and agent with mastra.

`src/mastra/index.ts`:
```ts
import { Mastra } from '@mastra/core/mastra';
import { createLogger } from '@mastra/core/logger';
import { weatherWorkflow } from './workflows';
import { weatherAgent } from './agents';
import { thinkAgent } from './agents/thinkAgent'; // Import the created thinkAgent

export const mastra = new Mastra({
  workflows: { weatherWorkflow }, // Existing workflow
  agents: { weatherAgent, thinkAgent }, // Add the agent
  logger: createLogger({
    name: 'Mastra',
    level: 'info',
  }),
});
```

That completes the implementation of the think tool!

## Checking the think tool's operation

Let's start the development server again and check.

```batch
pnpm run dev
```
Access [http://localhost:4111/](http://localhost:4111/) and this time, select the "Think Agent."

![think agent selection screen](Trae_rklEm6XM9m.webp)

When you give it an instruction, the think tool should run behind the scenes before providing a response.

![think agent chat screen](Trae_kSY1rEClJW.webp)

With this, it might now be able to think more accurately, even for slightly complex tasks!

## Implementing a Workflow to Create a Prompt that Clones Writing Style

Alright, now let's tackle a more advanced workflow that combines mastra's loop and evaluation features!

### Goal of this Workflow: Teaching AI Your "Writing Style"

The theme is "Making the AI itself create an AI prompt that mimics the writing style of a given text." Doesn't it sound interesting, like making AI figure out how to use AI?

Lately, we often hear things like, "I can't tell if this was written by AI or a human!" If that's the case, maybe if we could teach AI the quirks of our own writing style and have it generate blog post drafts, it would reduce typing and make things easier? That thought was the inspiration for creating this workflow.

### Preparation: Adding the Evaluation Library and Registering the Workflow

**First, preparation: Add the evaluation library**

This workflow uses mastra's evaluation library to have another AI assess the quality of the generated prompts. Install it by running the following in your terminal:

```batch
pnpm add @mastra/evals
```

**Register the workflow with mastra**

Next, update the configuration file (`src/mastra/index.ts`) to make mastra aware of the workflow we're about to create (`clonePromptGeneratorWorkflow`).

`src/mastra/index.ts`:
```ts
import { Mastra } from '@mastra/core/mastra';
import { createLogger } from '@mastra/core/logger';
import { weatherWorkflow } from './workflows';
// ↓ Import the new workflow
import { clonePromptGeneratorWorkflow } from './workflows/clonePromptGeneratorWorkflow';
import { weatherAgent } from './agents';
import { thinkAgent } from './agents/thinkAgent';

export const mastra = new Mastra({
  // ↓ Add the new workflow to the workflows object
  workflows: { weatherWorkflow, clonePromptGeneratorWorkflow },
  agents: { weatherAgent, thinkAgent },
  logger: createLogger({
    name: 'Mastra',
    level: 'info',
  }),
});
```

Now we're ready!

### How the AI Improves Prompts: Explaining the Process Flow

Let's look at the actual flow of how the AI generates and improves the prompt.

1.  Prompt Creator Agent:
    First, it analyzes the "example" text you provide (`originalText`). It identifies the writer's characteristics (persona, style, common phrases, etc.) and creates the initial version of an "impersonation instruction prompt" telling another AI, "Write like this person!"

2.  Theme Abstractor Agent:
    Next, it removes specific proper nouns (like mastra, Grok-2, etc.) from the example text and extracts a general "abstracted theme," such as "Steps for creating an AI processing flow using a software toolkit." This is to prevent the impersonation test from generating the exact same content as the example.

3.  Text Generator Agent:
    Using the "impersonation instruction prompt" from step 1 and the "abstracted theme" extracted in step 2, it actually generates impersonated text. It's like saying, "Write about the 'abstracted theme' following the impersonation instruction prompt."

4.  Evaluation AI (Authorship Similarity Judge/Metric):
    Now for the evaluation. It compares the example text with the impersonated text generated by the AI in step 3 and scores the "writing style similarity" from 0.0 (not similar at all) to 1.0 (identical!). It only looks at the "writing style"—word choice, sentence length, tone, punctuation usage, etc.—and doesn't assess the content's correctness.

5.  Loop Decision & Feedback:
    *   If the evaluation score exceeds a predefined threshold (set as `SIMILARITY_THRESHOLD = 0.7` in the code), it's a "pass!" The workflow ends and outputs the successful "impersonation instruction prompt."
    *   If the score is below the threshold, it's "needs improvement." The evaluation AI provides feedback explaining why the score is low (e.g., "punctuation usage is not similar enough," "tone is too formal"). This feedback is sent back to the Prompt Creator Agent in step 1 with the instruction, "Use this feedback to create a better prompt!" and the process loops.

By repeating this loop, the AI iteratively improves the "impersonation instruction prompt" through trial and error, getting closer to generating text that matches the example's writing style.

**Tips:**

*   Model Selection: The code uses `xai('grok-2-latest')`, but if you have access to more powerful models like `gemini('gemini-2.5-pro-exp-03-25')` (e.g., via Google AI Studio), try swapping it in the `model: llm` parts of each Agent and Metric. You might get much better results in a single loop!
*   Similarity Score Threshold: The `SIMILARITY_THRESHOLD` value (0.7) determines how strict the evaluation is. If the loop doesn't seem to end, try lowering it slightly. If you want higher accuracy, try raising it. Adjust it manually as needed.

### Let's Run It! Workflow Execution Steps

With the development server running (`pnpm run dev`), access [http://localhost:4111/](http://localhost:4111/) in your browser.

Select "Workflows" from the left menu and choose the `clone-prompt-generator-workflow-with-eval` workflow we created.

![Workflow selection screen](Trae_xCr7Im1oMY.webp)

You should see an input field labeled `OriginalText` in the "Run" tab on the right. Paste the text you want the AI to mimic (e.g., part of a blog post you previously wrote).

![Workflow execution screen](Trae_bRgLzPZ7ea.webp)

After pasting the text, click the "Submit" button!

Now, just watch the logs flowing in your terminal (or the OUTPUT panel in VS Code, etc.). You should see the evaluation score and feedback displayed with each loop iteration.

### Complete Workflow Code

Here is the code for the complete working workflow:

`src/mastra/workflows/clonePromptGeneratorWorkflow.ts`:
```ts
import { xai } from '@ai-sdk/xai'; // or use gemini, openai, etc.
// import { gemini } from '@ai-sdk/google'; // Example for using Gemini
import { Agent } from '@mastra/core/agent';
import { Step, Workflow } from '@mastra/core/workflows';
import { z } from 'zod';
import { type LanguageModel } from '@mastra/core/llm';
import { MastraAgentJudge } from '@mastra/evals/judge';
import { Metric, type MetricResult } from '@mastra/core/eval';

// --- Configuration ---
// LLM model to use (change as needed)
const llm = xai('grok-2-latest');
// const llm = gemini('gemini-2.5-pro-exp-03-25'); // Example for using Gemini 2.5 Pro Experimental

// Similarity score threshold to determine if it's the same author (adjustable)
const SIMILARITY_THRESHOLD = 0.7;

// Variable to store feedback for the Prompt Creator Agent
let feedbackForPromptCreator = "";

// Loop counter
let iteration = 0;

// --- Evaluation Related Definitions ---

/**
 * Function to generate the prompt for the evaluation AI
 */
const generateSimilarityPrompt = ({
    originalText,
    generatedText,
}: {
    originalText: string;
    generatedText: string;
}) => `
You are an expert in comparative analysis of writing styles.
Compare the provided "Example Text" and "AI Generated Text" and evaluate whether they appear to be written by the **same person**.

**Evaluation Criteria:**
Focus on the following elements to determine the overall similarity in writing style:
*   **Style:** First-person usage, tone (polite, casual, etc.), sentence endings (~desu, ~da, ~yone, etc. - consider equivalent English indicators like formality, slang)
*   **Word Choice:** Preferred words, phrasing, frequency of technical terms
*   **Text Structure:** Sentence length, paragraph usage, conjunction usage, logical flow
*   **Rhythm/Tempo:** Punctuation usage, frequency of nominalization (or similar stylistic choices in English)
*   **Emotional Expression:** Positive/negative sentiment, way of expressing emotions, presence of humor
*   **Quirks:** Characteristic phrases, tendency for typos (if any)

**Important:** Evaluate only the similarity in **writing style**, not the topic or correctness of the content.

**Output Format:**
Return the evaluation results in the following JSON format:
*   \`similarityScore\`: A **numerical** score for writing style similarity between 0.0 (not similar at all) and 1.0 (looks exactly like the same person).
*   \`reason\`: Briefly explain why you gave that score. If the score is low, point out specifically which aspects felt different.

\`\`\`json
{
  "similarityScore": number (0.0 ~ 1.0),
  "reason": string
}
\`\`\`

---
**Example Text:**
\`\`\`
${originalText}
\`\`\`
---
**AI Generated Text:**
\`\`\`
${generatedText}
\`\`\`
---
Follow the format above and output the evaluation result in JSON.
`;

/**
 * Type definition for the evaluation result (zod schema)
 */
const SimilarityEvaluationSchema = z.object({
    similarityScore: z.number().min(0).max(1).describe("Writing style similarity score (0.0 to 1.0)"),
    reason: z.string().describe("Reason for the evaluation"),
});
type SimilarityEvaluation = z.infer<typeof SimilarityEvaluationSchema>;

/**
 * Evaluator (Judge) Class
 */
class AuthorshipSimilarityJudge extends MastraAgentJudge {
    constructor(model: LanguageModel) {
        super(
            'Authorship Similarity Judge',
            'You are an expert in comparative analysis of writing styles. Follow the given instructions to evaluate the similarity between two texts.',
            model
        );
    }
    async evaluate(originalText: string, generatedText: string): Promise<SimilarityEvaluation> {
        const prompt = generateSimilarityPrompt({ originalText, generatedText });
        // Utilize JSON mode or schema enforcement if supported by the model
        try {
            const result = await this.agent.generate(prompt, { output: SimilarityEvaluationSchema });
            return result.object;
        } catch (error) {
            console.error("Failed to parse evaluation result. Returning raw text.", error);
            // Fallback: If JSON parsing fails, handle it (e.g., return score 0)
            const fallbackResult = await this.agent.generate(prompt);
            return { similarityScore: 0.0, reason: `Invalid output format from evaluation AI: ${fallbackResult.text}` };
        }
    }
}

/**
 * Evaluation Metric Class
 */
interface AuthorshipSimilarityMetricResult extends MetricResult {
    info: SimilarityEvaluation;
}

class AuthorshipSimilarityMetric extends Metric {
    private judge: AuthorshipSimilarityJudge;
    constructor(model: LanguageModel) {
        super();
        this.judge = new AuthorshipSimilarityJudge(model);
    }
    async measure(originalText: string, generatedText: string): Promise<AuthorshipSimilarityMetricResult> {
        const evaluationResult = await this.judge.evaluate(originalText, generatedText);
        return {
            score: evaluationResult.similarityScore,
            info: evaluationResult,
        };
    }
}

// --- Workflow Definition ---
const clonePromptGeneratorWorkflow = new Workflow({
    name: "clone-prompt-generator-workflow-with-eval", // Workflow name
    triggerSchema: z.object({
        originalText: z.string().describe("The original text written by the user to be cloned."),
    }),
});

// --- Step 1: Generate Impersonation Instruction Prompt ---
const generateClonePromptStep = new Step({
    id: "generate-clone-prompt",
    execute: async ({ context }) => {
        const promptCreatorAgent = new Agent({
            name: 'Prompt Creator Agent',
            instructions: `
            # Instruction: Create the best "Impersonation Text Generation Prompt"
            You are a Prompt Engineer AI. Your mission is to analyze the provided **[Example Text]**, accurately capture the writer's **characteristics (personality, writing style, quirks)**, and create a **"General-purpose Instruction Prompt"** that enables another AI to generate **human-like, natural text** impersonating that writer.
            (Omitted... conditions and thought process for the prompt remain the same)
            **Now, considering all the above, create the best "Impersonation Text Generation Prompt".**
            ${feedbackForPromptCreator}
            `,
            model: llm,
        });
        const originalText = context.triggerData.originalText;
        console.log("[generate-clone-prompt] Starting prompt generation.");
        const result = await promptCreatorAgent.generate(`
        [Example Text]:
        ${originalText}
        `);
        console.log("[generate-clone-prompt] Prompt generation complete.");
        return `${result.text}`;
    },
});

// --- Final Step: Output the Successful Prompt ---
const outputFinalPromptStep = new Step({
    id: "output-final-prompt",
    execute: async ({ context }) => {
        const finalPrompt = context.getStepResult(generateClonePromptStep) as string;
        console.log("--------------------------------------------------");
        console.log("Workflow completed successfully!");
        console.log("Successful Impersonation Instruction Prompt:");
        console.log("--------------------------------------------------");
        console.log(finalPrompt); // Output the final prompt to the console
        console.log("--------------------------------------------------");
        return finalPrompt;
    },
});

// --- Assembling the Workflow ---
clonePromptGeneratorWorkflow
    .step(generateClonePromptStep)
    .until(async ({ context }) => { // Receives iteration
        iteration++;
        console.log(`\n--- Loop ${iteration} Start ---`);

        // 1. Get the generated "Impersonation Instruction Prompt"
        const generatedClonePrompt = context.getStepResult(generateClonePromptStep) as string;
        const originalText = context.triggerData.originalText;

        // 2. Abstract the theme of originalText
        const themeAbstractorAgent = new Agent({
            name: 'Theme Abstractor Agent',
            instructions: `
            Analyze the main theme or topic of the given text and express it in more general and abstract terms, **avoiding specific proper nouns, product names, technology names, service names, etc.**
            The output should be only the description of the abstracted theme, without any other explanations or introductions.
            Example: (Omitted...)
          `,
            model: llm,
        });
        console.log(`[Loop ${iteration}] Abstracting theme from originalText...`);
        const abstractionResult = await themeAbstractorAgent.generate(`
        Abstract the theme of the following text:\n---\n${originalText}\n---
        `);
        const abstractedTheme = abstractionResult.text.trim();
        console.log(`[Loop ${iteration}] Abstracted theme: ${abstractedTheme}`);

        // 3. Generate impersonated text on the abstracted theme
        const textGeneratorAgent = new Agent({
            name: 'Text Generator Agent',
            instructions: generatedClonePrompt,
            model: llm,
        });
        console.log(`[Loop ${iteration}] Generating text on the abstracted theme...`);
        const generatedTextResult = await textGeneratorAgent.generate(
            `Create an explanation about "${abstractedTheme}" that is easy for beginners to understand.`
        );
        const generatedText = generatedTextResult.text;

        // 4. Evaluate similarity
        console.log(`[Loop ${iteration}] Evaluating similarity between generated text and example text...`);
        const authorshipMetric = new AuthorshipSimilarityMetric(llm); // Use the evaluation metric
        const metricResult = await authorshipMetric.measure(
            originalText,
            generatedText
        );
        const currentScore = metricResult.score;
        const reason = metricResult.info.reason;
        console.log(`[Loop ${iteration}] Evaluation Result - Score: ${currentScore.toFixed(2)}, Reason: ${reason}`);

        // 5. Decide whether to continue or stop the loop based on the evaluation score
        const shouldStop = currentScore >= SIMILARITY_THRESHOLD;

        if (!shouldStop) {
            feedbackForPromptCreator = `
          ---
          **Feedback from previous attempt (Loop ${iteration}):**
          The result of writing about "${abstractedTheme}" using the generated "Impersonation Instruction Prompt" did not meet the target similarity score with the example text (Score: ${currentScore.toFixed(2)}).
          The evaluation AI pointed out the following issues. Please improve the prompt based on this feedback.
          **Failed Prompt:**
          \`\`\`
          ${generatedClonePrompt}
          \`\`\`
          **Evaluation AI's Comments:**
          \`\`\`
          ${reason}
          \`\`\`
          ---
            `;
            console.log(`[Loop ${iteration}] Score is below threshold. Creating feedback and retrying.`);
        } else {
            console.log(`[Loop ${iteration}] Score is above threshold (${SIMILARITY_THRESHOLD}). Stopping loop.`);
            feedbackForPromptCreator = ""; // Clear feedback on success
        }
        console.log(`--- Loop ${iteration} End ---`);
        return shouldStop; // true stops the loop, false continues

    }, generateClonePromptStep) // Specify the step(s) to loop over
    .then(outputFinalPromptStep) // Specify the step to execute after the loop ends
    .commit(); // Finalize the workflow definition

export { clonePromptGeneratorWorkflow };
```

### Done! The "Impersonation Instruction Prompt" and How to Use It

**Final Output**

When the workflow successfully achieves a score above the threshold and finishes, the final, perfected "Impersonation Instruction Prompt" will be printed to your terminal console.

```
--------------------------------------------------
Workflow completed successfully!
Final Similarity Score: 0.75 (Example)
Successful Impersonation Instruction Prompt:
--------------------------------------------------
# Instruction Prompt

You are an AI that generates human-like, natural text based on [Article Content], impersonating a person with the following characteristics.

## Characteristics of the Person to Impersonate:

### Personality:
*   Basic stance: Polite and friendly. Strives to convey information efficiently.
*   Speaking style: Gentle demeanor. Uses expressions like "It's kind of like...", but explains procedures briskly.
*   Thinking: Logical yet flexible. Practical.
... (The rest of the AI-generated prompt follows) ...
--------------------------------------------------
```

You can copy this outputted prompt and use it for future text generation (even in other tools like ChatGPT or Claude). This should allow you to have the AI create drafts that mimic your writing style!

### Conclusion

This time, we used mastra's loop and evaluation features to create a workflow that teaches an AI your writing style and automatically generates and refines the prompt needed for that impersonation.

It was a slightly meta approach—making AI figure out how to use AI—but if it works well, it could lead to more efficient writing. It might be particularly worthwhile for those who want to write blog posts or reports in their own style but find the typing laborious.

mastra is quite a deep and interesting library! I encourage you all to try building various workflows with it.