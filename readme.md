# Python script to generate AI response for any of three providers: anthropic, openai, or mistral 

## To set up development environment and run
1. Install Python and the required SDKs: 
     * pip install anthropic openai 
     * pip install mistralai==0.4.2
     * python -m pip install python-dotenv
2. Set your API keys as environment variables or pass them with the --api-key flag
     * set ANTHROPIC_API_KEY=your_anthropic_api_key
     * set OPENAI_API_KEY=your_openai_api_key
     * set MISTRAL_API_KEY=your_mistral_api_key
3. Run the script (any of the following will work): 
     * python python_llm.py
     * python python_llm.py --provider anthropic
     * python python_llm.py --provider openai
     * python python_llm.py --provider mistral
     * python python_llm.py --provider openai --model gpt-4
     * python python_llm.py --provider mistral --model mistral-large-latest

## Example Anthropic Execution -- As an aside, Alan MacMasters is fictional, so this response is a point against Anthropic
```
PS C:\Users\austi\rep\PythonLLM>  python python_llm.py --provider anthropic
Welcome to the Anthropic CLI Interface!
Using model: claude-3-7-sonnet-20250219
Type 'exit', 'quit', or Ctrl+C to exit.
Type 'save <filename>' to save the conversation.
Type 'clear' to clear the conversation history.
------------------------------------------------

You: Who invented the electric toaster?

Assistant: The first electric toaster for home use was invented by Frank Shailor of the General Electric Company, who filed for a patent in 1909 for the "D-12" model, which was released commercially in 1910. However, Alan MacMasters had created an earlier electric bread toaster in 1893 in Scotland, though it wasn't as practical or commercially successful as later designs. The pop-up toaster mechanism we're familiar with today was invented by Charles Strite in 1921.

[Response time: 3.58s]
```

# Example OpenAI Execution
```
PS C:\Users\austi\rep\PythonLLM> python python_llm.py --provider openai --model gpt-4
Welcome to the Openai CLI Interface!
Using model: gpt-4
Type 'exit', 'quit', or Ctrl+C to exit.
Type 'save <filename>' to save the conversation.
Type 'clear' to clear the conversation history.
------------------------------------------------

You: Who invented the electric toaster?

Assistant: The electric toaster was invented by Frank Shailor of General Electric in 1909.
[Response time: 1.57s]
```
## Example Mistral Execution
```
PS C:\Users\austi\rep\PythonLLM> python python_llm.py --provider mistral
Welcome to the Mistral CLI Interface!
Using model: mistral-large-latest
Type 'exit', 'quit', or Ctrl+C to exit.
Type 'save <filename>' to save the conversation.
Type 'clear' to clear the conversation history.
------------------------------------------------

You: Who invented the electric toaster?

Assistant: The electric toaster was not invented by a single individual but rather evolved through a series of innovations by various inventors. The process of toasting bread using electricity began in the late 19th century.

One of the earliest patents for an electric toaster was filed by Crompton & Co. of the United Kingdom in 1893. However, the design was quite rudimentary and not very efficient.

A more significant development came in 1909 when General Electric introduced the D-12 toaster. This toaster was designed by Frank Shailor and was one of the first commercially successful electric toasters. It featured a design that allowed for even toasting and was more user-friendly than previous models.

Another notable figure in the development of the electric toaster was Charles Strite. In 1919, Strite invented the first automatic pop-up toaster. His design included a timer and a mechanism that would automatically eject the toast when it was done, a feature that became standard in modern toasters.

Thus, the electric toaster as we know it today is the result of contributions from multiple inventors and companies over several decades.

[Response time: 4.80s]
```
