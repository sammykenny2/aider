# Custom Models Module

This module provides support for custom LLM providers in Aider.

## Overview

The `custom_models` module extends Aider to work with custom LLM APIs while remaining loosely coupled with the core codebase. This design makes it easy to sync with upstream Aider updates.

## Supported Provider Types

This module supports three types of custom LLM providers:

1. **Custom GPT** - OpenAI-compatible APIs
2. **Custom Gemini** - Google-compatible APIs
3. **Custom Claude** - Anthropic-compatible APIs

## Architecture

### Module Structure

```
custom_models/
├── __init__.py                    # Module entry point and public API
├── README.md                      # This file
├── base_provider.py               # Abstract base class for providers
├── env_loader.py                  # .env and certificate loading
├── provider_registry.py           # Provider registration and routing
├── custom_gpt_provider.py         # OpenAI-compatible provider
├── custom_gemini_provider.py      # Google-compatible provider
└── custom_claude_provider.py      # Anthropic-compatible provider
```

### Public API

The module exports three functions used by core Aider:

1. **`load_custom_models()`** - Load and register all enabled providers
2. **`get_custom_aliases()`** - Get model aliases from all providers
3. **`route_custom_model(model_name, **kwargs)`** - Route requests to custom providers

## Configuration

Custom models are configured via `.env` file in the project root.

See `.env.example` for configuration template.

## Integration with Aider

This module integrates with Aider core in only 3 places (~50 lines total):

1. **`aider/main.py`** - Load custom models at startup
2. **`aider/models.py`** - Register model aliases
3. **`aider/llm.py`** - Route completion requests

All integration uses try-except blocks for graceful degradation.

## Design Principles

### Loose Coupling

- Custom models code isolated in this directory
- Core integration uses try-except (graceful degradation)
- Module can be deleted to restore original Aider behavior
- Easy to sync with upstream Aider updates

### Graceful Fallback

- If custom_models fails to load, Aider continues with standard models
- If a provider fails authentication, it's skipped
- If a custom model is unavailable, LiteLLM handles the error

## Dependencies

Core dependencies are managed by the module. Provider-specific dependencies are loaded on-demand.

## Maintenance

### Syncing with Upstream

When syncing with upstream Aider:

1. Fetch and merge upstream changes
2. Check the 3 integration points if conflicts occur
3. Test custom models still work

### Version Compatibility

- Python 3.10, 3.11, 3.12 (match aider compatibility)
- Provider SDKs are loaded dynamically

## License

Same as Aider (Apache 2.0)
