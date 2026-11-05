# Task 2 – Understanding of AI Systems

## 1. Agentic AI

Agentic AI refers to artificial intelligence systems that can independently work toward a specific goal by understanding instructions, planning tasks, making decisions, using tools, and evaluating results. Unlike traditional AI systems that respond to individual prompts, AI agents can perform multiple connected steps to complete a task.

An agentic AI system can divide a complex problem into smaller tasks, execute them in sequence, identify errors, and attempt corrections. Multiple agents can also collaborate, with each agent having a specific responsibility.

For example, in my AutoDev AI project, I explored a multi-agent software development architecture consisting of planner, coder, fixer, reviewer, and orchestrator components. Each component handles a different stage of the software development process.

## 2. Workflow AI

Workflow AI involves integrating artificial intelligence into a sequence of connected tasks to automate processes, reduce repetitive work, and improve efficiency.

A workflow generally consists of multiple stages, such as receiving input, processing information, making decisions, executing actions, and producing an output. AI can be included in one or more stages to perform tasks that require language understanding, prediction, classification, or decision support.

For example, an AI-powered engineering workflow could receive design requirements, analyze input parameters, run thermal calculations, predict performance using an ML model, and generate a report for engineering review.

Workflow AI is useful because it connects individual AI capabilities into a practical process that can solve real-world problems.

## 3. AI Copilots and Assistants

AI copilots and assistants are systems designed to support users while they perform tasks. They can understand natural language instructions, answer questions, summarize information, generate content, provide recommendations, and assist with technical activities.

A copilot generally works alongside a human user, helping improve productivity while allowing the user to review and control important decisions.

For example, an engineering AI copilot could help engineers understand simulation results, identify possible design improvements, explain technical errors, and suggest suitable parameters.

The main difference between an AI assistant and an autonomous agent is the level of independent action. An assistant primarily helps users through responses and recommendations, whereas an agent can also plan and execute multiple actions using available tools.

## 4. Standalone AI Models vs AI Integrated into Product Workflows

A standalone AI model performs a specific task independently. Users provide input to the model and receive an output. For example, entering a question into a language model and receiving an answer is a standalone AI interaction.

AI integrated into a product workflow goes beyond generating an output. The AI model becomes part of an actual application and interacts with its frontend, backend services, APIs, databases, and business logic.

For example, a standalone ML model might predict the junction temperature of a processor using thermal parameters. When integrated into engineering software, the same model could receive design parameters directly from the application, generate predictions, display results, compare design alternatives, and help engineers make decisions.

Product integration requires additional considerations, including data validation, API reliability, security, error handling, performance, user experience, and continuous monitoring.

Therefore, integrating AI into a product makes its capabilities more useful and accessible within real-world workflows.

## 5. My Experience with GenAI, LLMs, RAG and AI Agents

I have explored Generative AI, Large Language Models, Retrieval-Augmented Generation, and AI agent architectures through personal projects and practical experimentation.

One of my major projects is AutoDev AI, an autonomous AI software engineering system. The objective is to create a system that can understand software requirements and assist with different stages of application development.

I explored a multi-agent architecture involving:

- **Planner Agent:** Understands the requirements and breaks them into smaller development tasks.
- **Coder Agent:** Generates code based on the planned tasks.
- **Fixer Agent:** Analyzes errors and attempts to correct implementation issues.
- **Reviewer Agent:** Reviews generated code and checks its quality.
- **Orchestrator Agent:** Coordinates the overall execution of the agents.

I also experimented with different LLM providers and models, including Gemini, OpenAI-compatible models, Ollama, and OpenRouter. This helped me understand model integration, prompt engineering, structured outputs, API communication, and fallback handling.

I have also explored RAG through a GenAI chatbot project. RAG combines information retrieval with language generation. It retrieves relevant information from a knowledge source and provides that information as context to an LLM before generating a response. This helps applications generate answers based on specific reference material rather than depending only on the model's general knowledge.

These projects have helped me understand how individual AI models can be combined with application logic and multi-step workflows to build useful AI-powered systems.

## 6. Workflow Automation Experience

My practical experience with workflow automation comes primarily from developing and experimenting with AI-powered applications.

In AutoDev AI, I explored connecting multiple development stages through an orchestrated workflow. Instead of treating planning, coding, fixing, and reviewing as completely separate activities, the system coordinates them as connected steps.

I also worked with Python backend services, API endpoints, model integration, and automated execution processes.

Through this work, I learned that successful workflow automation requires more than connecting different components. It also requires proper input validation, error handling, execution tracking, testing, and mechanisms to handle failures.

I am continuing to improve my understanding of production-level workflow automation, including reliability, scalability, and monitoring.

## 7. AI Integration into Applications

AI integration involves connecting AI models and services with an application's existing architecture so users can access AI capabilities through a practical interface.

My experience includes working with frontend applications, backend APIs, Python services, and LLM integrations.

For example, in my MediFlow AI project, I explored integrating an AI assistant into a healthcare operations application. The architecture uses a frontend to collect user input, a FastAPI backend to process requests, and an AI service to generate responses. The backend then returns the response to the frontend for display.

In AutoDev AI, I experimented with connecting LLM providers to backend agent components so that different agents could use AI-generated outputs during the software development workflow.

These projects helped me understand the importance of API integration, prompt management, response validation, error handling, fallback mechanisms, and user-friendly interfaces.

I believe AI integration should focus on solving a real application problem rather than adding AI functionality simply for the sake of using AI.

## 8. How I Would Learn and Implement These Concepts

When working with a new AI or engineering problem, I would follow a structured and practical approach.

First, I would understand the problem, business requirements, expected outcomes, and limitations. I would identify the required input data and determine whether the problem is better suited for traditional machine learning, Generative AI, an AI agent, or a combination of approaches.

Next, I would study relevant documentation, research existing solutions, and select suitable technologies and models. I would begin with a small prototype to validate whether the proposed approach works.

After validating the prototype, I would integrate it into the application using appropriate APIs, backend services, and frontend components.

I would then test the implementation using different inputs, edge cases, and failure scenarios. I would evaluate its accuracy, reliability, response time, and overall usefulness.

Finally, I would collect feedback, identify limitations, and continuously improve the implementation.

As an early-career engineer, I am particularly interested in learning from real engineering problems, working with experienced developers, taking ownership of tasks, and building AI solutions that provide measurable value to users.