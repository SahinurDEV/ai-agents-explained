import os, sys
os.environ["LLM_PROVIDER"] = "mock"          # tests never call a real API
os.environ["EMBED_PROVIDER"] = "local"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
