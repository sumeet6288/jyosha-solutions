// Available AI models and providers
export const AI_PROVIDERS = {
  openai: {
    name: 'OpenAI',
    models: [
      { value: 'gpt-5', label: 'GPT-5' },
      { value: 'gpt-5-mini', label: 'GPT-5 Mini' },
      { value: 'gpt-4o', label: 'GPT-4o' },
      { value: 'gpt-4o-mini', label: 'GPT-4o Mini' },
      { value: 'gpt-4', label: 'GPT-4' },
      { value: 'o1', label: 'O1' },
      { value: 'o1-mini', label: 'O1 Mini' },
      { value: 'o3-mini', label: 'O3 Mini' },
    ]
  },
  anthropic: {
    name: 'Anthropic (Claude)',
    models: [
      { value: 'claude-4-sonnet-20250514', label: 'Claude 4 Sonnet' },
      { value: 'claude-4-opus-20250514', label: 'Claude 4 Opus' },
      { value: 'claude-3-7-sonnet-20250219', label: 'Claude 3.7 Sonnet' },
      { value: 'claude-3-5-sonnet-20241022', label: 'Claude 3.5 Sonnet' },
      { value: 'claude-3-5-haiku-20241022', label: 'Claude 3.5 Haiku' },
    ]
  },
  gemini: {
    name: 'Google (Gemini)',
    models: [
      { value: 'gemini-2.5-pro', label: 'Gemini 2.5 Pro' },
      { value: 'gemini-2.5-flash', label: 'Gemini 2.5 Flash' },
      { value: 'gemini-2.0-flash', label: 'Gemini 2.0 Flash' },
      { value: 'gemini-2.0-flash-lite', label: 'Gemini 2.0 Flash Lite' },
      { value: 'gemini-1.5-pro', label: 'Gemini 1.5 Pro' },
      { value: 'gemini-1.5-flash', label: 'Gemini 1.5 Flash' },
    ]
  }
};

export const getProviderForModel = (model) => {
  for (const [provider, data] of Object.entries(AI_PROVIDERS)) {
    if (data.models.some(m => m.value === model)) {
      return provider;
    }
  }
  return 'openai'; // Default
};

export const getAllModels = () => {
  const allModels = [];
  Object.entries(AI_PROVIDERS).forEach(([provider, data]) => {
    data.models.forEach(model => {
      allModels.push({
        ...model,
        provider,
        providerName: data.name
      });
    });
  });
  return allModels;
};
