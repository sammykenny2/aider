import importlib
import os
import warnings

from aider.dump import dump  # noqa: F401

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

AIDER_SITE_URL = "https://aider.chat"
AIDER_APP_NAME = "Aider"

os.environ["OR_SITE_URL"] = AIDER_SITE_URL
os.environ["OR_APP_NAME"] = AIDER_APP_NAME
os.environ["LITELLM_MODE"] = "PRODUCTION"

# `import litellm` takes 1.5 seconds, defer it!

VERBOSE = False


class LazyLiteLLM:
    _lazy_module = None

    def __getattr__(self, name):
        if name == "_lazy_module":
            return super()
        self._load_litellm()
        return getattr(self._lazy_module, name)

    def _load_litellm(self):
        if self._lazy_module is not None:
            return

        if VERBOSE:
            print("Loading litellm...")

        self._lazy_module = importlib.import_module("litellm")

        self._lazy_module.suppress_debug_info = True
        self._lazy_module.set_verbose = False
        self._lazy_module.drop_params = True
        self._lazy_module._logging._disable_debugging()

        # Custom models integration (loosely coupled)
        # Wrap litellm.completion to route custom models
        self._setup_custom_models_routing()

    def _setup_custom_models_routing(self):
        """Setup routing for custom model providers."""
        try:
            from aider.custom_models import route_custom_model

            # Save original completion function
            original_completion = self._lazy_module.completion

            def custom_completion_wrapper(**kwargs):
                """Wrapper that routes to custom providers or falls back to litellm."""
                model_name = kwargs.get("model")
                if model_name:
                    # Try routing to custom provider
                    custom_response = route_custom_model(model_name, **kwargs)
                    if custom_response is not None:
                        return custom_response

                # Fall back to original litellm
                return original_completion(**kwargs)

            # Replace completion function
            self._lazy_module.completion = custom_completion_wrapper

        except ImportError:
            pass  # custom_models not available, use standard litellm
        except Exception as e:
            print(f"Warning: Failed to setup custom models routing: {e}")


litellm = LazyLiteLLM()

__all__ = [litellm]
